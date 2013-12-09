# -*- coding: utf-8  -*-
"""
Tests for the Wikidata parts of the page module.
"""
#
# (C) Pywikipedia bot team, 2008-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

import os
import pywikibot
import json

from tests.utils import PywikibotTestCase, unittest

from pywikibot.site.base import BaseSite as Site
from pywikibot.page.wikilink import Link
#from pywikibot.page import Link
from tests.utils import PywikibotTestCase, unittest
from pywikibot.families.wikipedia_family import Family as WikipediaFamily
from pywikibot.families.wiktionary_family import Family as WiktionaryFamily
from pywikibot.page import Page


class TestGeneral(PywikibotTestCase):
    def setUp(self):
        self.site = Site('en', 'wikipedia')
        self.mainpage = Page(Link("Main Page", self.site))
        self.wikidata = self.site.data_repository()

class TestGeneral(TestGeneral):
    def testWikibase(self):
        if not self.site.has_transcluded_data:
            return
        repo = self.site.data_repository()
        item = ItemPage.fromPage(self.mainpage)
        self.assertType(item, ItemPage)
        self.assertEqual(item.getID(), 'Q5296')
        self.assertEqual(item.title(), 'Q5296')
        self.assertTrue('en' in item.labels)
        self.assertEqual(item.labels['en'], 'Main Page')
        self.assertTrue('en' in item.aliases)
        self.assertTrue('HomePage' in item.aliases['en'])
        self.assertEqual(item.namespace(), 0)
        item2 = ItemPage(repo, 'q5296')
        self.assertEqual(item2.getID(), 'Q5296')
        self.assertEqual(item.labels['en'], 'Main Page')
        prop = pywikibot.PropertyPage(repo, 'Property:P21')
        self.assertEqual(prop.getType(), 'wikibase-item')
        self.assertEqual(prop.namespace(), 120)
        claim = pywikibot.Claim(repo, 'p21')
        self.assertRaises(ValueError, claim.setTarget, value="test")
        claim.setTarget(ItemPage(repo, 'q1'))
        self.assertEqual(claim._formatDataValue(), {'entity-type': 'item', 'numeric-id': 1})

        # test WikibasePage.__cmp__
        self.assertEqual(ItemPage.fromPage(self.mainpage), ItemPage(repo, 'q5296'))

    def testItemPageExtensionability(self):
        class MyItemPage(ItemPage):
            pass
        self.assertIsInstance(MyItemPage.fromPage(self.mainpage), MyItemPage)


class TestLinks(PywikibotTestCase):
    """Test cases to test links stored in wikidata"""
    def setUp(self):
        super(TestLinks, self).setUp()
        self.wdp = ItemPage(self.wikidata, 'Q60')
        self.wdp.id = 'Q60'
        self.wdp._content = json.load(open(os.path.join(os.path.split(__file__)[0], 'pages', 'Q60_only_sitelinks.wd')))
        self.wdp.get()

    def test_iterlinks_page_object(self):
        page = [pg for pg in self.wdp.iterlinks() if pg.site.language() == 'af'][0]
        self.assertEquals(page, pywikibot.Page(pywikibot.getSite('af', 'wikipedia'), 'New York Stad'))

    def test_iterlinks_filtering(self):
        wikilinks = list(self.wdp.iterlinks('wikipedia'))
        wvlinks = list(self.wdp.iterlinks('wikivoyage'))

        self.assertEquals(len(wikilinks), 3)
        self.assertEquals(len(wvlinks), 2)


if __name__ == '__main__':
    try:
        try:
            unittest.main()
        except SystemExit:
            pass
    finally:
        pywikibot.stopme()
