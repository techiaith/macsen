# -*- coding: utf-8-*-
import re

WORDS = ["PWY"]

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

    mic.say(persona, """
Macsen ydw i, prototeip o gyfaill digidol, sy'n siarad eich iaith chi. Gofynnwch gwestiwn i mi ar 
lafar yn Gymraeg, er mwyn cael gwybodaeth am y tywydd neu'r newyddion diweddaraf. Neu gallwch 
ofyn i mi faint o'r gloch yw hi, neu oofyn am ddihareb y dydd. 
""")
    mic.say(persona, """
Cefais fy nghreu gan Uned Technolegau Iaith, Prifysgol Bangor, gyda nawdd gan Lywodraeth
Cymru ac S4C
""")
    mic.say(persona, """
Rydw i'n rhedeg ar y Rasberi Pai, cyfrifiadur bach rhad iawn, a ddefnyddir mewn clybiau 
codio ac ysgolion trwy'r wlad. Mae fy meddalwedd yn good agored, ac felly ar gael i 
chi allu creu cyfaill digidol Cymraeg Macsen eich hunain hefyd.
""")
    mic.say(persona, """
Ewch at wefan techiaith dot cymru blaen-slais Macsen, ar eich cyfrifiadur arferol, am ragor o wybodaeth.
""")


def isValid(persona, text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bpwy wyt ti\b', text, re.IGNORECASE)) or bool(re.search('r\bbeth wyt ti\b', text, re.IGNORECASE)) and persona=="MACSEN"
