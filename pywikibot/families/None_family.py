# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase

# The Adams family, no just kidding, for testing 

class Family(FamilyBase):


    def __init__(self):
        
        FamilyBase.__init__(self)
        self.name = 'none'
        self.langs = {
            'en': 'localhost',
            'de': 'localhost',
        }

        self.interwiki_forward = 'wikipedia'

        self.category_redirect_templates = {
            'en': ('Category redirect',),
        }

        self.disambcatname = {
            'en':  'Disambiguation'
        }

