# -*- coding: utf-8  -*-
"""Family module for Wikisource."""
from __future__ import absolute_import, unicode_literals

from pywikibot import family

__version__ = '$Id$'


# The Wikimedia family that is known as Wikisource
class Family(family.SubdomainFamily, family.WikimediaFamily):

    """Family class for Wikisource."""

    name = 'wikisource'

    closed_wikis = [
        # https://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Old_English_Wikisource
        'ang',
        # https://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Haitian_Creole_Wikisource
        'ht',
    ]

    def __init__(self):
        """Constructor."""
        self.languages_by_size = [
            'en', 'de', 'ru', 'fr', 'he', 'zh', 'pl', 'es', 'it', 'ar', 'cs',
            'pt', 'fa', 'hu', 'ml', 'ko', 'sv', 'sl', 'te', 'ro', 'gu', 'fi',
            'sr', 'sa', 'vi', 'el', 'bn', 'ca', 'hy', 'th', 'hr', 'ja', 'nl',
            'is', 'br', 'az', 'no', 'la', 'uk', 'vec', 'eo', 'tr', 'ta', 'be',
            'mk', 'yi', 'id', 'da', 'et', 'li', 'as', 'bg', 'mr', 'kn', 'bs',
            'sah', 'lt', 'gl', 'or', 'cy', 'sk', 'zh-min-nan', 'fo',
        ]

        super(Family, self).__init__()

        # FIXME: '-' is invalid at the beginning of a hostname, and
        # '-' is not a valid subdomain.
        self.langs['-'] = self.domain
        self.languages_by_size.append('-')

        # Global bot allowed languages on
        # https://meta.wikimedia.org/wiki/Bot_policy/Implementation#Current_implementation
        self.cross_allowed = [
            'ca', 'el', 'fa', 'it', 'ko', 'no', 'pl', 'vi', 'zh',
        ]

        self.authornamespaces = {
            '_default': [0],
            'ar': [102],
            'be': [102],
            'bg': [100],
            'ca': [106],
            'cs': [100],
            'da': [102],
            'en': [102],
            'eo': [102],
            'et': [106],
            'fa': [102],
            'fr': [102],
            'he': [108],
            'hr': [100],
            'hu': [100],
            'hy': [100],
            'it': [102],
            'ko': [100],
            'la': [102],
            'nl': [102],
            'no': [102],
            'pl': [104],
            'pt': [102],
            'ro': [102],
            'sv': [106],
            'tr': [100],
            'vi': [102],
            'zh': [102],
        }

        # Subpages for documentation.
        # TODO: List is incomplete, to be completed for missing languages.
        # TODO: Remove comments for appropriate pages
        self.doc_subpages = {
            '_default': ((u'/doc', ),
                         ['ar', 'as', 'az', 'bn', 'en', 'es',
                          'et', 'gu', 'hu', 'it', 'ja', 'kn', 'ml',
                          'mk', 'mr', 'pt', 'ro', 'sa', 'sah', 'ta',
                          'te', 'th', 'vi']
                         ),
            'be': (u'/Дакументацыя', ),
            'bn': (u'/নথি', ),
            'br': (u'/diellerezh', ),
            'de': (u'/Doku', u'/Meta'),
            'el': (u'/τεκμηρίωση', ),
            'eo': ('u/dokumentado', ),
            # 'fa': (u'/صفحه الگو', ),
            # 'fa': (u'/فضای‌نام توضیحات', ),
            # 'fa': (u'/آغاز جعبه', ),
            # 'fa': (u'/پایان جعبه۲', ),
            # 'fa': (u'/آغاز جعبه۲', ),
            # 'fa': (u'/پایان جعبه', ),
            # 'fa': (u'/توضیحات', ),
            'fr': (u'/documentation', ),
            'id': (u'/dok', ),
            'ko': (u'/설명문서', ),
            'no': (u'/dok', ),
            'ru': (u'/Документация', ),
            'sl': (u'/dok', ),
            'sv': (u'/dok', ),
            'uk': (u'/документація', ),
        }
