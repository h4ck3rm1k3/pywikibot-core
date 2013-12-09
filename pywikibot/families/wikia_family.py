# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import Family as FamilyBase


# The Wikia Search family
# user-config.py: usernames['wikia']['wikia'] = 'User name'
class Family (FamilyBase):
    def __init__(self):
        Family.__init__(self)
        self.name = 'wikia'

        self.langs = {
            'wikia': None,
        }

    def hostname(self, code):
        return 'www.wikia.com'

    def version(self, code):
        return "1.19.6"

    def scriptpath(self, code):
        return ''

    def apipath(self, code):
        return '/api.php'
