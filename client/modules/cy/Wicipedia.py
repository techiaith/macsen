# -*- coding: utf-8-*-
import re
import wikipedia
import unidecode
from wikipedia import PageError

WORDS = ["WICIPEDIA"]

cychwyn_cwestiwn_wici = ["BETH_YW'R", "BETH_YW", "BETH_YDY'R", "BETH_YDY", "BE_'DI", "BETH_OEDD", "BETH_FYDD", "PWY_YDY", "PWY_YW", "PWY_'DI", "PWY_OEDD"]

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
    mic.say(persona, text.replace("_"," "))

    for s in cychwyn_cwestiwn_wici:
        text = text.replace(s,"").strip()
    
    wikipedia.set_lang("cy")
    try:
        mic.say(persona, unidecode.unidecode(wikipedia.summary(text, sentences=1)))
    except:
        mic.say(persona, "Mae'n ddrwg gen i. Fedra i ddim ateb y cwestiwn")
    

def isValid(persona, text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    if persona == "WICIPEDIA":
        return True
    elif persona == "MACSEN":
        for s in cychwyn_cwestiwn_wici:
            if text.startswith(s):
                return True

    return False

