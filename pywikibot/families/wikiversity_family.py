# -*- coding: utf-8  -*-
from pywikibot.family import WikimediaFamily

__version__ = '$Id$'


# The Wikimedia family that is known as Wikiversity
class Family(WikimediaFamily):
    def __init__(self):
        self.alphabetic = []
        self.alphabetic_revised = []
        self.langs = {}
        self.known_families={}
        self.crossnamespace = {}

        WikimediaFamily.__init__(self)
        self.name = 'wikiversity'

        self.languages_by_size = [
            'en', 'fr', 'de', 'beta', 'cs', 'ru', 'it', 'pt', 'es', 'ar', 'fi',
            'sv', 'el', 'sl', 'ko', 'ja',
        ]

        self.langs = dict([(lang, '%s.wikiversity.org' % lang)
                           for lang in self.languages_by_size])

        # Global bot allowed languages on http://meta.wikimedia.org/wiki/Bot_policy/Implementation#Current_implementation
        self.cross_allowed = ['ja', ]
