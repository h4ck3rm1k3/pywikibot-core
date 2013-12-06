# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import WikimediaFamily

# The Wikimedia Incubator family
class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)
        self.name = 'incubator'
        self.langs = {
            'incubator': 'incubator.wikimedia.org',
        }

    def ssl_pathprefix(self, code):
        return "/wikipedia/incubator"
