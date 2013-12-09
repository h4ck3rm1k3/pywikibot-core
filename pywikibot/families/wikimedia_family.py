# -*- coding: utf-8 -*-
u'''
from pywikibot.families.wikimedia_family import Family

'''
__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase


# The wikis of Chapters of the Wikimedia Foundation living at a xy.wikimedia.org url
class Family(FamilyBase):
    def __init__(self):
        Family.__init__(self)
        self.name = 'wikimediachapter'

        self.countries = [
            'ar', 'br', 'bd', 'co', 'dk', 'fi', 'mk', 'mx', 'nl', 'no',
            'nyc', 'pl', 'rs', 'ru', 'se', 'ua', 'uk', 've',
        ]

        self.countrylangs = {
            'ar': 'es', 'br': 'pt-br', 'bd': 'bn', 'co': 'es', 'dk': 'da',
            'fi': 'fi', 'mk': 'mk', 'mx': 'es', 'nl': 'nl', 'no': 'no',
            'nyc': 'en', 'pl': 'pl', 'rs': 'sr', 'ru': 'ru', 'se': 'sv',
            'ua': 'uk', 'uk': 'en-gb', 've': 'en',
        }

        self.langs = dict([(country, '%s.wikimedia.org' % country)
                           for country in self.countries])
