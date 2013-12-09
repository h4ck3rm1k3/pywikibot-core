# -*- coding: utf-8  -*-
__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase


# The LyricWiki family

# user_config.py:
# usernames['lyricwiki']['en'] = 'user'
class Family (FamilyBase):
    def __init__(self):
        Family.__init__(self)
        self.name = 'lyricwiki'
        self.langs = {
            'en': 'lyrics.wikia.com',
        }

    def version(self, code):
        return "1.16.2"

    def scriptpath(self, code):
        return ''

    def apipath(self, code):
        return '/api.php'
