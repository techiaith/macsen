#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import locale
import gettext

locale.setlocale(locale.LC_ALL,'')
macsen_language = locale.getlocale()[0][0:2]

def init_internationalization():
    ''' prepare l10n '''
    filename = "res/Macsen_%s.mo" % macsen_language

    try:
        trans = gettext.GNUTranslations(open( filename, "rb"))
    except IOError:
        print ("Locale %s not found. Will use default locale strings" % macsen_language)
        trans = gettext.NullTranslations()

    trans.install()
''' end of preparing l10n '''

