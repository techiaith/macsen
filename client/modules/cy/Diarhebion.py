# -*- coding: utf-8-*-
import re
import random
import feedparser

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
    feed = feedparser.parse("http://aberth.com/diarhebion/feed/")
    random_index = random.randint(0, len(feed.entries))
    dihareb_html = feed.entries[random_index].summary_detail.value

    dihareb_txt_start = len('<p>')
    dihareb_txt_end = dihareb_html.index('.') #('&#8211;')
    dihareb_txt = dihareb_html[dihareb_txt_start:dihareb_txt_end]
    mic.say(dihareb_txt)


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bdihareb\b', text, re.IGNORECASE))
