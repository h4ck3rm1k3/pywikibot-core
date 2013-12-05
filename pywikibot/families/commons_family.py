# -*- coding: utf-8  -*-

__version__ = '$Id$'

from pywikibot.families.familybase import WikimediaFamily

# The Wikimedia Commons family
class Family(WikimediaFamily):
    def __init__(self):
        WikimediaFamily.__init__(self)
        self.name = 'commons'
        self.langs = {
            'commons': 'commons.wikimedia.org',
        }

        self.interwiki_forward = 'wikipedia'

        self.category_redirect_templates = {
            'commons': ('Category redirect',
                        'Categoryredirect',
                        'Synonym taxon category redirect',
                        'Invalid taxon category redirect',
                        'Monotypic taxon category redirect',
                        'See cat',
                        'Seecat',
                        'See category',
                        'Catredirect',
                        'Cat redirect',
                        'Cat-red',
                        'Catredir',
                        'Redirect category'),
        }

        self.disambcatname = {
            'commons':  'Disambiguation'
        }

    def ssl_pathprefix(self, code):
        return "/wikipedia/commons"

    def shared_data_repository(self, code, transcluded=False):
        return ('wikidata', 'wikidata')
