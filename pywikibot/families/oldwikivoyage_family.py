# -*- coding: utf-8 -*-
from pywikibot.families.familybase import Family

__version__ = '$Id$'


#Family file for the original wikivoyage
class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'oldwikivoyage'
        self.langs = {
            'de': 'www.wikivoyage-old.org',
            'en': 'en.wikivoyage-old.org',
            'fr': 'fr.wikivoyage-old.org',
            'it': 'www.wikivoyage-old.org',
            'nl': 'nl.wikivoyage-old.org',
            'ru': 'ru.wikivoyage-old.org',
            'shared': 'www.wikivoyage-old.org',
            'sv': 'sv.wikivoyage-old.org',
            'wts': 'wts.wikivoyage-old.org',
        }

    def scriptpath(self, code):
        return {
            'de': '/w/de',
            'en': '/w',
            'fr': '/w',
            'it': '/w/it',
            'nl': '/w',
            'ru': '/w',
            'shared': '/w/shared',
            'sv': '/w',
            'wts': '/w',
        }[code]

    def version(self, code):
        return {
            'de': '1.13.1',
            'en': '1.19.1',
            'fr': '1.19.1',
            'it': '1.13.1',
            'nl': '1.19.1',
            'ru': '1.19.1',
            'sv': '1.19.1',
            'shared': '1.13.1',
            'wts': '1.19.1',
        }[code]

    def shared_image_repository(self, code):
        return ('shared', 'oldwikivoyage')
