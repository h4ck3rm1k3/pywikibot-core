# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import Family


# The Wikimedia i18n family
class Family(family.Family):

    def __init__(self):
        family.Family.__init__(self)
        self.name = 'i18n'
        self.langs = {
            'i18n': 'translatewiki.net',
        }

    def version(self, code):
        return "1.20alpha"
