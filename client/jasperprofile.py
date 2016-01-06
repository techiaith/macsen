#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os, sys, shutil
import logging
import yaml

from client import jasperpath
import l10n

class JasperProfile(object):

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

		configFileName = 'profile.%s.yml' % l10n.macsen_language
        	configfile = jasperpath.config(configFileName)
        	
		# Read config
        	self._logger.debug("Trying to read config file: '%s'", configfile)
        	try:
            		with open(configfile, "r") as f:
                		self.config = yaml.safe_load(f)
        	except OSError:
            		self._logger.error("Can't open config file: '%s'", configfile)
            		raise

	def get(self, key, default):
		try:
			result=self.config[key]
			self._logger.debug('Fetching key %s from profile returned %s' % (key,result)) 
		except KeyError:
			result=default
			self._logger.warning('%s not speficied in the profile, defaulting to %s' % (key, default))
		return result			

	def get_yml(self):
		return self.config


profile = JasperProfile()
