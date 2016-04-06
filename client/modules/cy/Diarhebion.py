# -*- coding: utf-8-*-
import re
import datetime
import struct
import urllib
import feedparser
import requests
from client.app_utils import getTimezone

WORDS = ["DIHAREB"]

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
    feed=feedparser.parse("http://aberth.com/diarhebion/feed/")
    dihareb_html=feed.entries[0].summary_detail.value
    dihareb_txt_start=len('<p>')
    dihareb_txt_end=dihareb_html.index('&#8211;')
    dihareb_txt=dihareb_html[dihareb_txt_start:dihareb_txt_end]
    mic.say(dihareb_txt)


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bdihareb\b', text, re.IGNORECASE))
