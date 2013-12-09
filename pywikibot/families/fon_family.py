# -*- coding: utf-8  -*-
__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase


# The official Beta Wiki.

class Family (FamilyBase):

    def __init__(self):

        Family.__init__(self)
        self.name = 'fon'

        self.langs = {
            'en': None,
        }

    def hostname(self, code):
        return 'wiki.fon.com'

    def scriptpath(self, code):
        return '/mediawiki'

    def version(self, code):
        return "1.15.1"
