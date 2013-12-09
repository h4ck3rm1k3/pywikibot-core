# -*- coding: utf-8  -*-
__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase


# ZRHwiki, formerly known as SouthernApproachWiki, a wiki about Zürich Airport.
class Family (FamilyBase):
    def __init__(self):
        Family.__init__(self)
        self.name = 'southernapproach'
        self.langs = {
            'de': 'www.zrhwiki.ch',
        }

    def version(self, code):
        return "1.17alpha"
