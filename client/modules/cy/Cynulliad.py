# -*- coding: utf-8-*-
import re
import datetime
import struct
import urllib
import feedparser
import requests
from bs4 import BeautifulSoup
from client.app_utils import getTimezone

WORDS = ["CYNULLIAD"]

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
    if ("CYNULLIAD" in text):
        mic.say(persona,"Cynulliad Cenedlaethol Cymru yw'r corff sy'n cael ei ethol yn ddemocrataidd i gynrychioli buddiannau Cymru a'i phobl, i ddeddfu ar gyfer Cymru, i gytuno ar drethi yng Nghymru, ac i ddwyn Llywodraeth Cymru i gyfrif")
    elif ("SENEDD" in text):
        mic.say(persona,"Y Senedd yw prif adeilad cyhoeddus y Cynulliad Cenedlaethol, a phrif ganolfan democratiaeth a datganoli yng Nghymru. Mae'n adeilad agored – adeilad y mae croeso i chi ddod iddo, i wylio'r Cynulliad wrth ei waith")
    elif ("LLYWODRAETH" in text):
        mic.say(persona,"Llywodraeth Cymru yw llywodraeth ddatganoledig Cymru. Mae'n gweithio i wella bywydau pobl yng Nghymru, a gwneud ein gwlad yn lle gwell i fyw a gweithio")


def isValid(persona, text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    if persona == "LLYWYDD":
        cynulliad = bool(re.search(r'\bcynulliad\b', text, re.IGNORECASE))
        senedd = bool(re.search(r'\bsenedd\b', text, re.IGNORECASE))
        llywodraeth =  bool(re.search(r'\bllywodraeth\b', text, re.IGNORECASE))

        return cynulliad or senedd or llywodraeth

    return False;
