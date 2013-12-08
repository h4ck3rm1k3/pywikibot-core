# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import Family


# The Wikia Search family
# user-config.py: usernames['wikia']['wikia'] = 'User name'
class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
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
