# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import WikimediaFamily

# The MediaWiki family
# user-config.py: usernames['mediawiki']['mediawiki'] = 'User name'
class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)
        self.name = 'mediawiki'

        self.langs = {
            'mediawiki': 'www.mediawiki.org',
        }

    def ssl_pathprefix(self, code):
        return "/wikipedia/mediawiki"
