# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.family import WikimediaFamily


# The meta wikimedia family
class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)
        self.name = 'meta'
        self.langs = {
            'meta': 'meta.wikimedia.org',
        }
        self.interwiki_forward = 'wikipedia'
        self.cross_allowed = ['meta', ]

    def ssl_pathprefix(self, code):
        return "/wikipedia/meta"
