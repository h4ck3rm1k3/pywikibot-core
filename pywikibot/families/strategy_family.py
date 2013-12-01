# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.family import WikimediaFamily

# The Wikimedia Strategy family
class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)

        self.name = 'strategy'
        self.langs = {
            'strategy': 'strategy.wikimedia.org',
        }
        self.interwiki_forward = 'wikipedia'

    def dbName(self, code):
        return 'strategywiki_p'

    def ssl_pathprefix(self, code):
        return "/wikipedia/strategy"
