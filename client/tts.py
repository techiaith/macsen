# -*- coding: utf-8 -*-
"""
A Speaker handles audio output from Jasper to the user

Speaker methods:
    say - output 'phrase' as speech
    play - play the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
import os
import time
import platform
import re
import tempfile
import signal
import subprocess
import shlex
import pipes
import logging
import pexpect
import wave
import urllib
import urlparse
import requests
from abc import ABCMeta, abstractmethod

import argparse
import yaml

import jasperprofile
import time
import subprocess 

try:
    import mad
except ImportError:
    pass

try:
    import gtts
except ImportError:
    pass

try:
    import pyvona
except ImportError:
    pass

try:
    import festival
except ImportError:
    pass


import diagnose
import jasperpath

from pygame import mixer

class AbstractTTSEngine(object):
    """
    Generic parent class for all speakers
    """
    __metaclass__ = ABCMeta

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        config = cls.get_config()
        instance = cls(**config)
        
        mixer.init(16000)

        return instance

    @classmethod
    @abstractmethod
    def is_available(cls):
        return diagnose.check_executable('aplay')

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)

    @abstractmethod
    def say(self, persona, phrase, *args):
        pass

    @abstractmethod
    def default_voice(self, voice):
        pass

    def play(self, filename):
        # FIXME: Use platform-independent audio-output here
        # See issue jasperproject/jasper-client#188
        
	#cmd = ['aplay', str(filename)]
        #self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
        #                                             for arg in cmd]))
        #with tempfile.TemporaryFile() as f:
        #    subprocess.call(cmd, stdout=f, stderr=f)
        #    f.seek(0)
        #    output = f.read()
        #    if output:
        #        self._logger.debug("Output was: '%s'", output)
        sound = mixer.Sound(filename)
        sound.play()
        playingsound=True
        while playingsound:
            playingsound = mixer.get_busy() 
            time.sleep(0.1)

class AbstractMp3TTSEngine(AbstractTTSEngine):
    """
    Generic class that implements the 'play' method for mp3 files
    """
    @classmethod
    def is_available(cls):
        return (super(AbstractMp3TTSEngine, cls).is_available() and
                diagnose.check_python_import('mad'))


    def play_mp3(self, filename):
        DEVNULL = open(os.devnull, 'w')
        p = subprocess.call(["mpg123", filename], \
                            stdin=subprocess.PIPE, \
                            stdout=DEVNULL, \
                            stderr=subprocess.STDOUT)


class DummyTTS(AbstractTTSEngine):
    """
    Dummy TTS engine that logs phrases with INFO level instead of synthesizing
    speech.
    """

    SLUG = "dummy-tts"

    @classmethod
    def is_available(cls):
        return True

    def say(self, phrase):
        self._logger.info(phrase)

    def play(self, filename):
        self._logger.debug("Playback of file '%s' requested")
        pass


class EspeakTTS(AbstractTTSEngine):
    """
    Uses the eSpeak speech synthesizer included in the Jasper disk image
    Requires espeak to be available
    """

    SLUG = "espeak-tts"

    def __init__(self, voice='default+m3', pitch_adjustment=40,
                 words_per_minute=160):
        super(self.__class__, self).__init__()
        self.voice = voice
        self.pitch_adjustment = pitch_adjustment
        self.words_per_minute = words_per_minute

    @classmethod
    def get_config(cls, language):
        # FIXME: Replace this as soon as we have a config module
        config = {}
        # HMM dir
        # Try to get hmm_dir from config
        profile_path = jasperpath.config('profile.%s.yml' % language)
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'espeak-tts' in profile:
                    if 'voice' in profile['espeak-tts']:
                        config['voice'] = profile['espeak-tts']['voice']
                    if 'pitch_adjustment' in profile['espeak-tts']:
                        config['pitch_adjustment'] = \
                            profile['espeak-tts']['pitch_adjustment']
                    if 'words_per_minute' in profile['espeak-tts']:
                        config['words_per_minute'] = \
                            profile['espeak-tts']['words_per_minute']
        return config

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_executable('espeak'))

    def say(self, persona, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name
        cmd = ['espeak', '-v', self.voice,
               '-p', self.pitch_adjustment,
               '-s', self.words_per_minute,
               '-w', fname,
               phrase]
        cmd = [str(x) for x in cmd]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)
        self.play(fname)
        os.remove(fname)


class FestivalTTS(AbstractTTSEngine):
    """
    Uses the festival speech synthesizer
    Requires festival (text2wave) to be available
    """

    SLUG = 'festival-tts'

    @classmethod
    def is_available(cls):
        if (super(cls, cls).is_available() and
                diagnose.check_executable('festival')):
            logger = logging.getLogger(__name__)

        return True

    def default_voice(self, voice):
        self.voice = voice
        festival.execCommand('(' + voice + ')')

    def say(self, persona, phrase):
        self._logger.debug("Saying '%s' with '%s' and voice '%s'", phrase, self.SLUG, self.voice)
        wavFileName = festival.textToWavFile(phrase)
        self._logger.info("Wav file created: %s" % wavFileName)
        self.play(wavFileName)


class FliteTTS(AbstractTTSEngine):
    """
    Uses the flite speech synthesizer
    Requires flite to be available
    """

    SLUG = 'flite-tts'

    def __init__(self, voice=''):
        super(self.__class__, self).__init__()
        self.voice = voice if voice and voice in self.get_voices() else ''

    @classmethod
    def get_voices(cls):
        cmd = ['flite', '-lv']
        voices = []
        with tempfile.SpooledTemporaryFile() as out_f:
            subprocess.call(cmd, stdout=out_f)
            out_f.seek(0)
            for line in out_f:
                if line.startswith('Voices available: '):
                    voices.extend([x.strip() for x in line[18:].split()
                                   if x.strip()])
        return voices

    @classmethod
    def get_config(cls, language):
        # FIXME: Replace this as soon as we have a config module
        config = {}
        # HMM dir
        # Try to get hmm_dir from config
        profile_path = jasperpath.config('profile.%s.yml' % language)
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'flite-tts' in profile:
                    if 'voice' in profile['flite-tts']:
                        config['voice'] = profile['flite-tts']['voice']
        return config

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_executable('flite') and
                len(cls.get_voices()) > 0)

    def say(self, persona, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        cmd = ['flite']
        if self.voice:
            cmd.extend(['-voice', self.voice])
        cmd.extend(['-t', phrase])
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name
        cmd.append(fname)
        with tempfile.SpooledTemporaryFile() as out_f:
            self._logger.debug('Executing %s',
                               ' '.join([pipes.quote(arg)
                                         for arg in cmd]))
            subprocess.call(cmd, stdout=out_f, stderr=out_f)
            out_f.seek(0)
            output = out_f.read().strip()
        if output:
            self._logger.debug("Output was: '%s'", output)
        self.play(fname)
        os.remove(fname)


class MacOSXTTS(AbstractTTSEngine):
    """
    Uses the OS X built-in 'say' command
    """

    SLUG = "osx-tts"

    @classmethod
    def is_available(cls):
        return (platform.system().lower() == 'darwin' and
                diagnose.check_executable('say') and
                diagnose.check_executable('afplay'))

    def say(self, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        cmd = ['say', str(phrase)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)

    def play(self, filename):
        cmd = ['afplay', str(filename)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)


class PicoTTS(AbstractTTSEngine):
    """
    Uses the svox-pico-tts speech synthesizer
    Requires pico2wave to be available
    """

    SLUG = "pico-tts"

    def __init__(self, language="en-US"):
        super(self.__class__, self).__init__()
        self.language = language

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_executable('pico2wave'))

    @classmethod
    def get_config(cls, language):
        # FIXME: Replace this as soon as we have a config module
        config = {}
        # HMM dir
        # Try to get hmm_dir from config
        profile_path = jasperpath.config('profile.%s.yml' % language)
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'pico-tts' in profile and 'language' in profile['pico-tts']:
                    config['language'] = profile['pico-tts']['language']

        return config

    @property
    def languages(self):
        cmd = ['pico2wave', '-l', 'NULL',
               '-w', os.devnull,
               'NULL']
        with tempfile.SpooledTemporaryFile() as f:
            subprocess.call(cmd, stderr=f)
            f.seek(0)
            output = f.read()
        pattern = re.compile(r'Unknown language: NULL\nValid languages:\n' +
                             r'((?:[a-z]{2}-[A-Z]{2}\n)+)')
        matchobj = pattern.match(output)
        if not matchobj:
            raise RuntimeError("pico2wave: valid languages not detected")
        langs = matchobj.group(1).split()
        return langs

    def say(self, persona, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name
        cmd = ['pico2wave', '--wave', fname]
        if self.language not in self.languages:
                raise ValueError("Language '%s' not supported by '%s'",
                                 self.language, self.SLUG)
        cmd.extend(['-l', self.language])
        cmd.append(phrase)
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)
        self.play(fname)
        os.remove(fname)


class GoogleTTS(AbstractMp3TTSEngine):
    """
    Uses the Google TTS online translator
    Requires pymad and gTTS to be available
    """

    SLUG = "google-tts"

    def __init__(self, language='en'):
        super(self.__class__, self).__init__()
        self.language = language

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_python_import('gtts') and
                diagnose.check_network_connection())

    @classmethod
    def get_config(cls, language):
        # FIXME: Replace this as soon as we have a config module
        config = {}
        # HMM dir
        # Try to get hmm_dir from config
        profile_path = jasperpath.config('profile.%s.yml' % language)
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if ('google-tts' in profile and
                   'language' in profile['google-tts']):
                    config['language'] = profile['google-tts']['language']

        return config

    @property
    def languages(self):
        langs = ['af', 'sq', 'ar', 'hy', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs',
                 'da', 'nl', 'en', 'eo', 'fi', 'fr', 'de', 'el', 'ht', 'hi',
                 'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no',
                 'pl', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'sw', 'sv', 'ta',
                 'th', 'tr', 'vi', 'cy']
        return langs

    def say(self, persona, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        if self.language not in self.languages:
            raise ValueError("Language '%s' not supported by '%s'",
                             self.language, self.SLUG)
        tts = gtts.gTTS(text=phrase, lang=self.language)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tmpfile = f.name
        tts.save(tmpfile)
        self.play_mp3(tmpfile)
        os.remove(tmpfile)


class MaryTTS(AbstractTTSEngine):
    """
    Uses the MARY Text-to-Speech System (MaryTTS)
    MaryTTS is an open-source, multilingual Text-to-Speech Synthesis platform
    written in Java.
    Please specify your own server instead of using the demonstration server
    (http://mary.dfki.de:59125/) to save bandwidth and to protect your privacy.
    """

    SLUG = "mary-tts"

    def __init__(self, server="localhost", port="59125", language="cy",
                 voice="wispr"):
        super(self.__class__, self).__init__()

        marytts_home = '/home/pi/src/marytts'
        marytts_version = '5.2'
        
        marytts_base = os.path.join(marytts_home, 'target', "marytts-" + marytts_version)

        maryttsps = os.popen("ps auxw | grep marytts-server | grep -v grep").read()
        maryttspscount = maryttsps.count('marytts-server')
        if maryttspscount==0:         
            self._logger.info("Starting MaryTTS Server...")
            cmd = 'java -showversion -Xms40m -Xmx1g -cp "%s/lib/*" -Dmary.base="%s" marytts.server.Mary' % (marytts_base, marytts_base,)
            popen_cmd = shlex.split(cmd)
            self.marytts_pid = subprocess.Popen(popen_cmd).pid
            self._logger.info("Started MaryTTS server successfully pid:%s" % (self.marytts_pid))
        
        self.server = server
        self.port = port
        self.netloc = '{server}:{port}'.format(server=self.server,
                                               port=self.port)
        self.language = language
        self.voice = voice
        self.session = requests.Session()


    @property
    def languages(self):
        try:
            r = self.session.get(self._makeurl('/locales'))
            r.raise_for_status()
        except requests.exceptions.RequestException:
            self._logger.critical("Communication with MaryTTS server at %s " +
                                  "failed.", self.netloc)
            raise
        return r.text.splitlines()


    @property
    def voices(self):
        r = self.session.get(self._makeurl('/voices'))
        r.raise_for_status()
        return [line.split()[0] for line in r.text.splitlines()]


    @classmethod
    def get_config(cls):
        config = {}
        profile = jasperprofile.profile.get_yml()
        if 'mary-tts' in profile:
            if 'server' in profile['mary-tts']:
                config['server'] = profile['mary-tts']['server']
            if 'port' in profile['mary-tts']:
                config['port'] = profile['mary-tts']['port']
            if 'language' in profile['mary-tts']:
                config['language'] = profile['mary-tts']['language']
            if 'voice' in profile['mary-tts']:
                config['voice'] = profile['mary-tts']['voice']

        return config

    def default_voice(self, voice):
        pass

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_network_connection())

    def _makeurl(self, path, query={}):
        query_s = urllib.urlencode(query)        
        urlparts = ('http', self.netloc, path, query_s, '')
        return urlparse.urlunsplit(urlparts)

    def say(self, persona, phrase):
        print ("Saying '%s' with '%s'", phrase, self.SLUG)
        if self.language not in self.languages:
            raise ValueError("Language '%s' not supported by '%s'"
                             % (self.language, self.SLUG))

        if self.voice not in self.voices:
            raise ValueError("Voice '%s' not supported by '%s'"
                             % (self.voice, self.SLUG))

        phraseutf8 = phrase.encode('utf-8')
        self._logger.debug("SAYING: %s" % phraseutf8)

 
        query = {'OUTPUT_TYPE': 'AUDIO',
                 'AUDIO': 'WAVE_FILE',
                 'INPUT_TYPE': 'TEXT',
                 'INPUT_TEXT': phraseutf8,
                 'LOCALE': self.language,
                 'VOICE': self.voice}

        r = self.session.get(self._makeurl('/process', query=query))
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(r.content)
            tmpfile = f.name
        self.play(tmpfile)
        os.remove(tmpfile)


class IvonaTTS(AbstractMp3TTSEngine):
    """
    Uses the Ivona Speech Cloud Services.
    Ivona is a multilingual Text-to-Speech synthesis platform developed by
    Amazon.
    """

    SLUG = "ivona-tts"

    def __init__(self, access_key='', secret_key='', language=None, region=None,
                 voice=None, speech_rate=None, sentence_break=None):
        super(self.__class__, self).__init__()
        self._pyvonavoice = pyvona.Voice(access_key, secret_key)
        self._pyvonavoice.codec = "mp3"
        if language:
            self._pyvonavoice.language = language 
	if region:
            self._pyvonavoice.region = region
        if voice:
            self._pyvonavoice.voice_name = voice
        if speech_rate:
            self._pyvonavoice.speech_rate = speech_rate
        if sentence_break:
            self._pyvonavoice.sentence_break = sentence_break

    @classmethod
    def get_config(cls):
        config = {}
        profile = jasperprofile.profile.get_yml()
        if 'ivona-tts' in profile:
                if 'access_key' in profile['ivona-tts']:
                    config['access_key'] = profile['ivona-tts']['access_key']
                if 'secret_key' in profile['ivona-tts']:
                    config['secret_key'] = profile['ivona-tts']['secret_key']                    
                if 'language' in profile['ivona-tts']:
                    config['language']=profile['ivona-tts']['language']
                if 'region' in profile['ivona-tts']:
                    config['region'] = profile['ivona-tts']['region']
                if 'voice' in profile['ivona-tts']:
                    config['voice'] = profile['ivona-tts']['voice']
                if 'speech_rate' in profile['ivona-tts']:
                    config['speech_rate'] = profile['ivona-tts']['speech_rate']
                if 'sentence_break' in profile['ivona-tts']:
                    config['sentence_break'] = profile['ivona-tts']['sentence_break']

        print ("Ivona TTS Config %s" % config)

        return config

    def default_voice(self, voice):
        pass

    @classmethod
    def is_available(cls):
        return True
        #return (super(cls, cls).is_available() and
        #        diagnose.check_python_import('pyvona') and
        #        diagnose.check_network_connection())

    def say(self, persona, phrase):

        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tmpfile = f.name
        self._pyvonavoice.fetch_voice(phrase, tmpfile)
        self._logger.debug("Play mp3 %s" % tmpfile)
        self.play_mp3(tmpfile)
        #os.remove(tmpfile)

        #self._pyvonavoice.speak(phrase)



def get_default_engine_slug():
    return 'osx-tts' if platform.system().lower() == 'darwin' else 'espeak-tts'


def get_engine_by_slug(slug=None):
    """
    Returns:
        A speaker implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or type(slug) is not str:
        raise TypeError("Invalid slug '%s'", slug)

    selected_engines = filter(lambda engine: hasattr(engine, "SLUG") and
                              engine.SLUG == slug, get_engines())
    if len(selected_engines) == 0:
        raise ValueError("No TTS engine found for slug '%s'" % slug)
    else:
        if len(selected_engines) > 1:
            print("WARNING: Multiple TTS engines found for slug '%s'. " +
                  "This is most certainly a bug." % slug)
        engine = selected_engines[0]
        if not engine.is_available():
            raise ValueError(("TTS engine '%s' is not available (due to " +
                              "missing dependencies, etc.)") % slug)
        return engine


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [tts_engine for tts_engine in
            list(get_subclasses(AbstractTTSEngine))
            if hasattr(tts_engine, 'SLUG') and tts_engine.SLUG]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Jasper TTS module')
    parser.add_argument('--debug', action='store_true',
                        help='Show debug messages')
    args = parser.parse_args()

    logging.basicConfig()
    if args.debug:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    engines = get_engines()
    available_engines = []
    for engine in get_engines():
        if engine.is_available():
            available_engines.append(engine)
    disabled_engines = list(set(engines).difference(set(available_engines)))
    print("Available TTS engines:")
    for i, engine in enumerate(available_engines, start=1):
        print("%d. %s" % (i, engine.SLUG))

    print("")
    print("Disabled TTS engines:")

    for i, engine in enumerate(disabled_engines, start=1):
        print("%d. %s" % (i, engine.SLUG))

    print("")
    for i, engine in enumerate(available_engines, start=1):
        print("%d. Testing engine '%s'..." % (i, engine.SLUG))
        engine.get_instance().say("This is a test.")
    print("Done.")
