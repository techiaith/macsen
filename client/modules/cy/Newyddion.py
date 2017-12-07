# -*- coding: utf-8-*-
import re
import datetime
import struct
import urllib
import feedparser
import requests
from bs4 import BeautifulSoup
from client.app_utils import getTimezone
import unidecode

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

    rq = requests.get("https://golwg360.cymru/ffrwd")
    data=rq.text
    soup=BeautifulSoup(data)

    mic.say(persona, "Dyma penawdau gwefan newyddion golwg tri chwech dim")

    for headline in soup.find_all('title'):
        testun_pennawd = unidecode.unidecode(headline.text)
        if testun_pennawd != 'Golwg360':
           print testun_pennawd
           mic.say(persona, testun_pennawd)
  

def isValid(persona, text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    print persona, text
    return bool(re.search(r'\bnewyddion\b', text, re.IGNORECASE)) and persona=="MACSEN"

