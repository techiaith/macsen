#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import logging

import yaml
import argparse

from client import tts, stt, jasperpath, diagnose
from client.conversation import Conversation
import client.l10n

class Jasper(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)

        # Create config dir if it does not exist yet
        if not os.path.exists(jasperpath.CONFIG_PATH):
            try:
                os.makedirs(jasperpath.CONFIG_PATH)
            except OSError:
                self._logger.error("Could not create config dir: '%s'",
                                   jasperpath.CONFIG_PATH, exc_info=True)
                raise

        # Check if config dir is writable
        if not os.access(jasperpath.CONFIG_PATH, os.W_OK):
            self._logger.critical("Config dir %s is not writable. Jasper won't work correctly", 
                                  jasperpath.CONFIG_PATH)

        configFileName = 'profile.%s.yml' % client.l10n.macsen_language
        configfile = jasperpath.config(configFileName)
        # Read config
        self._logger.debug("Trying to read config file: '%s'", configfile)
        try:
            with open(configfile, "r") as f:
                self.config = yaml.safe_load(f)
        except OSError:
            self._logger.error("Can't open config file: '%s'", configfile)
            raise


        try:
            stt_engine_slug = self.config['stt_engine']
        except KeyError:
            stt_engine_slug = 'sphinx'
            logger.warning("stt_engine not specified in profile, defaulting " +
                           "to '%s'", stt_engine_slug)
        stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)

        try:
            slug = self.config['stt_passive_engine']
            stt_passive_engine_class = stt.get_engine_by_slug(slug)
        except KeyError:
            stt_passive_engine_class = stt_engine_class

        try:
            tts_engine_slug = self.config['tts_engine']
        except KeyError:
            tts_engine_slug = tts.get_default_engine_slug()
            logger.warning("tts_engine not specified in profile, defaulting " +
                           "to '%s'", tts_engine_slug)
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        # Initialize Mic
        self.mic = Mic(tts_engine_class.get_instance(),
                       stt_passive_engine_class.get_passive_instance(),
                       stt_engine_class.get_active_instance())

	if tts_engine_slug == 'festival-tts':	
		try:
			tts_engine_default_voice = self.config['tts_default_voice']
			self.mic.set_tts_default_voice(tts_engine_default_voice)
		except KeyError:
			logger.warning("Festival tts_engine default voice not specified in profile. " +
				       "Will use default provided by Festival installation")



    def run(self):
        if 'first_name' in self.config:
            salutation = (_("How can I be of service, %s?")
                          % self.config["first_name"])
        else:
            salutation = _("How can I be of service?")
        self.mic.say(salutation)

        conversation = Conversation("MACSEN", self.mic, self.config)
        conversation.handleForever()

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
