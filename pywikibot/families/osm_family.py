# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase


# The project wiki of OpenStreetMap (OSM).
class Family(FamilyBase):

    def __init__(self):
        FamilyBase.__init__(self)
        self.name = 'osm'
        self.langs = {
            'en': 'wiki.openstreetmap.org',
        }

    def version(self, code):
        return "1.16.2"
