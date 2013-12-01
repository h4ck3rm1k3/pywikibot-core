# -*- coding: utf-8  -*-

__version__ = '$Id$'


from pywikibot.family import Family as BaseFamily

# The Wikitech family
class Family(BaseFamily):

    def __init__(self):
        BaseFamily.__init__(self)
        self.name = 'wikitech'
        self.langs = {
            'en': 'wikitech.wikimedia.org',
        }

    def version(self, code):
        return '1.21wmf8'
