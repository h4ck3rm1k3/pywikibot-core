# -*- coding: utf-8  -*-
"""
Tests for the page module.
"""
from pywikibot.page.imagepage  import ImagePage
#
# (C) Pywikipedia bot team, 2008
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

import sys
print(sys.getdefaultencoding())
import pywikibot.page
#from pywikibot.site.apisite import APISite as Site
from pywikibot.site.base import BaseSite as Site
from pywikibot.site.apisite import APISite
from pywikibot.page.wikilink import Link
#from pywikibot.page import Link
from tests.utils import PywikibotTestCase, unittest
from pywikibot.families.wikipedia_family import Family as WikipediaFamily
from pywikibot.families.wiktionary_family import Family as WiktionaryFamily
from pywikibot.page import Page
from pywikibot.exceptions import NoPage
#import pprint
from pywikibot.bot import debug
from pywikibot.timestamp  import Timestamp
from pywikibot.page.category  import Category

class TestBase(PywikibotTestCase):

    def __init__(self,  tests):
        PywikibotTestCase.__init__(self, tests)

    def testHistory(self):
        """Test various methods that rely on API."""
        wikipedia =WikipediaFamily()
        enwiki = APISite("en", wikipedia)
        link = Link(u"Kosovo", enwiki)
        page = Page(link,enwiki)
        history = page.getVersionHistory(
            #reverseOrder=False, 
            #getAll=True,
            #revCount=500
            step=1,
            total=10
        )

        revs = enwiki.loadrevisions(page, getText=False, 
                                step=1, total=10)
        print ("Revs %s" % revs)
        print ("History %s" % history)
        print ("Revisions %s" % page._revisions)

        for x in range(1,10):
            print (page.previousRevision())

        for apage in page._revisions :
            print (apage)

if __name__ == '__main__':
    try:
        try:
            unittest.main()
        except SystemExit:
            pass
    finally:
        #pywikibot.stopme()
        pass
