# -*- coding: utf-8 -*-
"""
A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, Jasper is always active listening with local_mic.
"""


class Mic:
    prev = None

    def __init__(self, speaker, passive_stt_engine, active_stt_engine):
        self.speaker = speaker 
        return
 
    def set_tts_default_voice(self, default_voice):
        self.speaker.default_voice(default_voice)

    def passiveListen(self, PERSONA):
        input = raw_input("PERSONA: ")
        return True, input

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        return [self.activeListen(THRESHOLD=THRESHOLD, LISTEN=LISTEN, MUSIC=MUSIC)]

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        if not LISTEN:
            return self.prev

        input = []
        input.append(raw_input("YOU: "))
        self.prev = input
        return input

    def say(self, persona, phrase, OPTIONS=None):
        print("TTS: %s" % phrase)
        self.speaker.say(persona, phrase)
