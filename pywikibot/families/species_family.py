# -*- coding: utf-8  -*-

__version__ = '$Id$'


from pywikibot.family import WikimediaFamily

# The wikispecies family
class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)
        self.name = 'species'
        self.langs = {
            'species': 'species.wikimedia.org',
        }
        self.interwiki_forward = 'wikipedia'

    def ssl_pathprefix(self, code):
        return "/wikipedia/species"
