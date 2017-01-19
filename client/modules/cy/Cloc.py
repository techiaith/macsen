# -*- coding: utf-8-*-
import re
import datetime

import jasperprofile


WORDS = ["GLOCH"]

def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, with a summary of
    the relevant weather for the requested date (typically, weather
    information will not be available for days beyond tomorrow).

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    strhour = '{:02d}'.format(datetime.datetime.now().time().hour)
    strminute = '{:02d}'.format(datetime.datetime.now().time().minute)

    mic.say("Mae hi'n %s:%s" % (strhour, strminute))


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bgloch\b', text, re.IGNORECASE))
