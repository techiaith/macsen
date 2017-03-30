# -*- coding: utf-8 -*-
import logging

from notifier import Notifier
from brain import Brain


class Conversation(object):

    def __init__(self, personas, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.personas = personas
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile)

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.", self.personas)

        while True:
            # Print notifications until empty
            notifications = self.notifier.getAllNotifications()
            for notif in notifications:
                self._logger.info("Received notification: '%s'", str(notif))

            self._logger.debug("Started listening for keywords '%s'", self.personas)
            threshold, persona = self.mic.passiveListen(self.personas)
            self._logger.debug("Stopped listening for keywords '%s'", self.personas)

            if not persona or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue

            self._logger.info("Keyword '%s' has been said!", persona)
            self._logger.debug("Started to listen actively with threshold: %r", threshold)
            audioinput = self.mic.activeListen(self.personas, threshold)
            self._logger.debug("Stopped to listen actively with threshold: %r", threshold)

            if audioinput:
                self.brain.query(persona, audioinput)
            else:
                self.mic.say(self.personas[0], "Pardon?")

