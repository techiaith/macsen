# -*- coding: utf-8-*-
import re
import datetime
import struct
import urllib
import feedparser
import requests
from client.app_utils import getTimezone
from semantic.dates import DateService
import datetime

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
       
    mic.say("Mae hi'n %s:%s" % (datetime.datetime.now().time().hour, datetime.datetime.now().time().minute))


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    print("Cloc isValid......")
    return bool(re.search(r'\bgloch\b', text, re.IGNORECASE))
