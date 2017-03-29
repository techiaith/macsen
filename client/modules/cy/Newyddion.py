# -*- coding: utf-8-*-
import re
import datetime
import struct
import urllib
import feedparser
import requests
from bs4 import BeautifulSoup
from client.app_utils import getTimezone

WORDS = ["NEWYDDION"]

def handle(persona, text, mic, profile):
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
    mic.say(persona, "Gad i mi weld")

    rq = requests.get("http://golwg360.cymru/newyddion")
    data=rq.text
    soup=BeautifulSoup(data)

    mic.say(persona, "Dyma penawdau gwefan newyddion golwg 3 6 0")
    
    for entry in soup(attrs={'class':'headline'}):
        for headline in entry.find_all('a'):
            testun_pennawd = ''.join([x for x in headline.text if ord(x) < 128])
            print testun_pennawd
            mic.say(persona, testun_pennawd)


def isValid(persona, text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bnewyddion\b', text, re.IGNORECASE)) and persona=="MACSEN"
