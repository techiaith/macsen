# -*- coding: utf-8 -*-
import os
import sys
import re
from getpass import getpass
import yaml
from pytz import timezone
import feedparser
import jasperpath
import l10n

def run(macsen_language):

    profile = {}

    print(_("Welcome to the profile populator for language %s" % macsen_language))
    print(_("If, at any step, you'd prefer not to enter the requested information, just hit 'Enter' with a blank field to continue."))

    def simple_request(var, cleanVar, cleanInput=None):
        input = raw_input(cleanVar + ": ")
        if input:
            if cleanInput:
                input = cleanInput(input)
            profile[var] = input

    # name
    simple_request('first_name', 'First name')
    simple_request('last_name', 'Last name')

    # timezone
    print("\n")
    print(_("Please enter a timezone from the list located in the TZ* column at http://en.wikipedia.org/wiki/List_of_tz_database_time_zones, or none at all. E.g. 'Europe/London' for Wales"))
    tz = raw_input(_("Timezone: "))
    while tz:
        try:
            timezone(tz)
            profile['timezone'] = tz
            break
        except:
            print(_("Not a valid timezone. Try again."))
            tz = raw_input(_("Timezone: "))


    # microphone hardware
    print("\n")
    print _("Microphone Configuration")
    print(_("Please state the microphone location. (Press Enter to default to 'plughw:1,0' for Raspberry Pi)"))
    response=raw_input(_("Microphone: "))
    if response:
        profile["mic"] = response
    else:
        profile["mic"] = 'plughw:1,0'

   
    # speech to text configuration
    if macsen_language == 'cy':
	stt_engines = {
		"bangor": None
	}
    else:
    	stt_engines = {
        	"sphinx": None,
        	"google": "GOOGLE_SPEECH"
    	}

    print("\n")
    print _("Speech Recognition Configuration")
    print _("Available implementations: %s. (Press Enter to default to PocketSphinx): ") 
    response = raw_input(_("If you would like to choose a specific STT engine, please specify which.") +
			"\n" +
			 _("Available implementations: %s. (Press Enter to default to PocketSphinx): ") % stt_engines.keys())

    if (response in stt_engines):
        profile["stt_engine"] = response
	if response == 'bangor':
                profile["stt_passive_engine"] = profile["stt_engine"]
		profile["bangor"]=dict(
                        # julius-cy is installed at $HOME/src/julius-cy, which contains a jconf
                        jconf=os.path.join(os.getenv('HOME'),'src/julius-cy/julius.jconf'),
			hmmdefs='/usr/share/julius/acoustic/%s/hmmdefs' % macsen_language,
		        tiedlist='/usr/share/julius/acoustic/%s/tiedlist' % macsen_language,
			lexicon='/usr/share/julius/lexicon/%s/lexicon.tgz' % macsen_language,
			lexicon_archive_member='lexicon'
		)
        api_key_name = stt_engines[response]
        if api_key_name:
	    print ("\n")
            key = raw_input(_("Please enter your API key: "))
            profile["keys"] = {api_key_name: key}

    else:
        print(_("Unrecognized STT engine. Available implementations: %s") % stt_engines.keys())
        profile["stt_engine"] = "sphinx"


    # Text to Speech Configuration
    if macsen_language == 'cy':
        tts_engines = {
                "festival-tts": "voice_cb_cy_llg_diphone",
		"ivona-tts":None
        }
    else:
        tts_engines = {
                "festival-tts": "voice_kal_diphone" 
        }

    print("\n")
    print _("Text-to-Speech Configuration")
    print _("Available implementations: %s. (Press Enter to default to E-speak):")
    response = raw_input(_("If you would like to choose a specific TTS engine, please specify which.") +
			 "\n" +
			 _("Available implementations: %s. (Press Enter to default to E-speak): ") % tts_engines.keys())
    if (response in tts_engines):
	profile["tts_engine"] = response
	if response == "festival-tts":
		profile["tts_default_voice"] = tts_engines[response]
	if response == "ivona-tts":
		pyvona_accesskey = raw_input(_("Enter your Ivona access key : "))
		pyvona_secretkey = raw_input(_("Enter your Ivona secret key : "))		
		profile["ivona-tts"] = dict(
                        access_key = pyvona_accesskey,
                        secret_key = pyvona_secretkey,
                        voice = "Geraint",
                        language = "cy-GB"
                )
    else:
	print(_("Unrecognized TTS engine. Available implementations: %s") % tts_engines.keys())
	profile["tts_engine"]="espeak-tts"		


    # write to profile
    print(_("Writing to profile..."))
    if not os.path.exists(jasperpath.CONFIG_PATH):
        os.makedirs(jasperpath.CONFIG_PATH)
    outputFileName = 'profile.%s.yml' % macsen_language
    outputFile = open(jasperpath.config(outputFileName), "w")
    yaml.dump(profile, outputFile, default_flow_style=False)
    print(_("Done."))

if __name__ == "__main__":

    import argparse

    l10n.init_internationalization()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-lang', help='profile language - en / cy', dest='language', action='store')
    
    args = parser.parse_args(sys.argv[1:])

    if args.language is None:
	args.language = l10n.macsen_language

    run(args.language)

