#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import logging
import argparse

from client import tts, stt, jasperpath, diagnose
from client.conversation import Conversation
import client.l10n
import client.jasperprofile

class Jasper(object):

    def __init__(self):

        self._logger = logging.getLogger(__name__)

        stt_engine_slug = client.jasperprofile.profile.get('stt_engine', 'sphinx')
        stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)

        stt_passive_engine_slug = client.jasperprofile.profile.get('stt_passive_engine', stt_engine_slug)
        stt_passive_engine_class = stt.get_engine_by_slug(stt_passive_engine_slug)

        tts_engine_slug = client.jasperprofile.profile.get('tts_engine', tts.get_default_engine_slug())
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        active_stt_engine_instance = stt_engine_class.get_active_instance()
        if active_stt_engine_instance.has_mic() is True:
            self._logger.info("Active and Passive the same")
            passive_stt_engine_instance = active_stt_engine_instance
        else:
            passive_stt_engine_instance = stt_passive_engine_class.get_passive_instance()

        # Initialize Mic
        self.mic = Mic(tts_engine_class.get_instance(),
                       passive_stt_engine_instance,
                       active_stt_engine_instance)
                       #stt_passive_engine_class.get_passive_instance(),
                       #stt_engine_class.get_active_instance())

        if tts_engine_slug == 'festival-tts':
            tts_engine_default_voice = client.jasperprofile.profile.get('tts_default_voice', '')
            if tts_engine_default_voice:
                self.mic.set_tts_default_voice(tts_engine_default_voice)
            else:
                self._logger.warning("Profile does not contain a default voice for Festival." +
					                            " Will use the Festival installation default")

    def run(self):

        #self.introduction()

        first_name = client.jasperprofile.profile.get('first_name', '')
        if first_name:
            salutation = (_("How can I be of service, %s?") % first_name)
        else:
            salutation = _("How can I be of service?")

        self.mic.say(salutation)

        conversation = Conversation("LLYWYDD", self.mic, client.jasperprofile.profile.get_yml())
        conversation.handleForever()    

    def introduction(self):

        self.mic.say("""
Macsen ydw i, prototeip o gyfaill digidol, sy'n siarad eich iaith chi. Gofynnwch gwestiwn i mi ar 
lafar yn Gymraeg, er mwyn cael gwybodaeth am y tywydd neu'r newyddion diweddaraf. Neu gallwch 
ofyn i mi faint o'r gloch yw hi, neu oofyn am ddihareb y dydd. 
""")
        self.mic.say("""
Cefais fy nghreu gan Uned Technolegau Iaith, Prifysgol Bangor, gyda nawdd gan Lywodraeth
Cymru ac S4C
""")
        self.mic.say("""Datblygwyd fy llais i gan gwmni Ivona ar y cyd a RNIB Cymru""")
        self.mic.say("""
Rydw i'n rhedeg ar y Rasberi Pai, cyfrifiadur bach rhad iawn, a ddefnyddir mewn clybiau 
codio ac ysgolion trwy'r wlad. Mae fy meddalwedd yn good agored, ac felly ar gael i 
chi allu creu cyfaill digidol Cymraeg Macsen eich hunain hefyd.
""")
        self.mic.say("""
Ewch at wefan techiaith dot cymru blaen-slais Macsen, ar eich cyfrifiadur arferol, am ragor o wybodaeth.
""")

if __name__ == "__main__":

    client.l10n.init_internationalization()

    # Add jasperpath.LIB_PATH to sys.path
    sys.path.append(jasperpath.LIB_PATH)

    parser = argparse.ArgumentParser(description=_('Macsen Voice Control Center'))
    parser.add_argument('--local', action='store_true', help=_('Use text input instead of a real microphone'))
    parser.add_argument('--no-network-check', action='store_true', help=_('Disable the network connection check'))
    parser.add_argument('--diagnose', action='store_true', help=_('Run diagnose and exit'))
    parser.add_argument('--debug', action='store_true', help=_('Show debug messages'))
    args = parser.parse_args()

    if args.local:
        from client.local_mic import Mic
    else:
        from client.mic import Mic

    print("*******************************************************")
    print(_("      MACSEN - THE MULTILINGUAL TALKING COMPUTER      *"))
    print(" (c) 2016 Prifysgol BANGOR University                 *")
    print(_(" Initial Developers:                                  *"))
    print(" Dewi Bryn Jones (techiaith@Bangor)                   *")
    print(" Stefano Ghazzali (techiaith@Bangor)                  *")
    print("                                                      *")
    print(_("MACSEN is based on :                                            *")) 
    print("*                                                     *") 
    print("*******************************************************")
    print("*             JASPER - THE TALKING COMPUTER           *")
    print("* (c) 2015 Shubhro Saha, Charlie Marsh & Jan Holthuis *")
    print("*******************************************************")

    logging.basicConfig()
    logger = logging.getLogger()
    logger.getChild("client.stt").setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if not args.no_network_check and not diagnose.check_network_connection():
        logger.warning("Network not connected. This may prevent Jasper from " +
                       "running properly.")

    if args.diagnose:
        failed_checks = diagnose.run()
        sys.exit(0 if not failed_checks else 1)

    try:
        app = Jasper()
    except Exception:
        logger.error("Error occured!", exc_info=True)
        sys.exit(1)

    app.run()
