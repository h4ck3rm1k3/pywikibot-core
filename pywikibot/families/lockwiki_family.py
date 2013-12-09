# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase


# The locksmithwiki family
class Family (FamilyBase):
    def __init__(self):
        FamilyBase.__init__(self)
        self.name = 'lockwiki'
        self.langs = {
            'en': 'www.locksmithwiki.com',
        }

    def scriptpath(self, code):
        return '/lockwiki'

    def version(self, code):
        return '1.15.1'

    def nicepath(self, code):
        return "%s/" % FamilyBase.path(self, code)
