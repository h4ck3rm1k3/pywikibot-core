# -*- coding: utf-8 -*-

__version__ = '$Id$'

# The new wikivoyage family that is hosted at wikimedia

from pywikibot.families.familybase import WikimediaFamily

class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)

        self.name = 'wikivoyage'
        self.languages_by_size = [
            'en', 'de', 'pt', 'fr', 'it', 'nl', 'pl', 'ru', 'es', 'vi', 'sv',
            'he', 'ro', 'uk', 'el',
        ]

        self.langs = dict([(lang, '%s.wikivoyage.org' % lang)
                           for lang in self.languages_by_size])
        # Global bot allowed languages on http://meta.wikimedia.org/wiki/Bot_policy/Implementation#Current_implementation
        self.cross_allowed = ['es', 'ru', ]

    def shared_data_repository(self, code, transcluded=False):
        return ('wikidata', 'wikidata')
