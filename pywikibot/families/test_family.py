# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import WikimediaFamily

# The test wikipedia family
class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)

        self.name = 'test'
        self.langs = {
            'test': 'test.wikipedia.org',
        }

    def ssl_pathprefix(self, code):
        return "/wikipedia/test"
