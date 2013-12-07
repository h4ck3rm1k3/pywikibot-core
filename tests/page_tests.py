# -*- coding: utf-8  -*-
"""
Tests for the page module.
"""
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
from pywikibot.page.wikilink import Link
#from pywikibot.page import Link
from tests.utils import PywikibotTestCase, unittest
from pywikibot.families.wikipedia_family import Family as WikipediaFamily
from pywikibot.families.wiktionary_family import Family as WiktionaryFamily
from pywikibot.page import Page
import pprint
from pywikibot.debug import debugprint
class TestBase(PywikibotTestCase):

    def __init__(self,  tests):
        PywikibotTestCase.__init__(self, tests)

    def setUp(self):
        self.maxDiff=None
        # we turn this around, create a site based on the family
        self.wikipedia = WikipediaFamily()
        self.wiktionary = WiktionaryFamily()
        self.enwiki = Site("en", self.wikipedia)
        self.frwiki = Site("fr", self.wikipedia)
        self.itwikt = Site("it", self.wiktionary)
        assert(self.enwiki)
        link = Link(u"Main Page", self.enwiki)
        self.mainpage = Page(link,self.enwiki)
        self.maintalk = Page(Link(
            u"Talk:Main Page", 
            self.enwiki))
        self.badpage = Page(Link(
            u"There is no page with this title",
            self.enwiki))

        self.namespaces = {0: [""],        # en.wikipedia.org namespaces for testing
                  1: ["Talk:"],   # canonical form first, then others
                  2: ["User:"],   # must end with :
                  3: ["User talk:", "User_talk:"],
                  4: ["Wikipedia:", "Project:", "WP:"],
                  5: ["Wikipedia talk:", "Project talk:", "Wikipedia_talk:",
                      "Project_talk:", "WT:"],
                  6: ["File:"],
                  7: ["Image talk:", "Image_talk:"],
                  8: ["MediaWiki:"],
                  9: ["MediaWiki talk:", "MediaWiki_talk:"],
                  10: ["Template:"],
                  11: ["Template talk:", "Template_talk:"],
                  12: ["Help:"],
                  13: ["Help talk:", "Help_talk:"],
                  14: ["Category:"],
                  15: ["Category talk:", "Category_talk:"],
                  100: ["Portal:"],
                  101: ["Portal talk:", "Portal_talk:"],
                  }
        self.titles = {
            # just a bunch of randomly selected titles
            # input format                  : expected output format
            "Cities in Burkina Faso":        "Cities in Burkina Faso",
            "eastern Sayan":                 "Eastern Sayan",
            "The_Addams_Family_(pinball)":   "The Addams Family (pinball)",
            "Hispanic  (U.S.  Census)":      "Hispanic (U.S. Census)",
            "Stołpce":                       "Stołpce",
            "Nowy_Sącz":                     "Nowy Sącz",
            "battle of Węgierska  Górka":    "Battle of Węgierska Górka",
        }
        # random bunch of possible section titles
        self.sections = ["",
                "#Phase_2",
                "#History",
                "#later life",
                ]

class TestLinkObject(TestBase):
    """Test cases for Link objects"""

    def __init__(self,  tests):
        TestBase.__init__(self,  tests)

    def setUp(self):
        TestBase.setUp(self)
        
    def testNamespaces(self):
        """Test that Link() normalizes namespace names"""
        for num in self.namespaces:
            for prefix in self.namespaces[num]:
                debugprint ("TEST NAMESPACE first: prefix:'%s' number:'%s' " % (str(prefix), str(num)))
                l = Link(prefix + list(self.titles.keys())[0],
                                        self.enwiki)
                debugprint (("Link: %s" % l).encode("utf-8"))

                x = list(self.titles.keys())[0]
                debugprint (("First Item %s" % x).encode("utf-8"))
                #debugprint ("TEST NAMESPACE3: %s" % (("%s" % x).encode("utf-8")   ))
                #debugprint ("TEST NAMESPACE3: %s" % (
                #    ("%s" % x).encode("ascii","replace")
                #))

                debugprint ("link namespace: %s" % (l.namespace))
                debugprint ("expected namespace: %s" % (num))
                self.assertEqual(l.namespace, num)
                # namespace prefixes are case-insensitive
                m = Link(
                    prefix.lower() + list(self.titles.keys())[1]
                    ,
                    self.enwiki
                )

                self.assertEqual(m.namespace, num)

    def testTitles(self):
        """Test that Link() normalizes titles"""
        for title in self.titles:
            for num in (0, 1):
                l = Link(self.namespaces[num][0] + title, self.enwiki)
                self.assertEqual(l.title, self.titles[title])
                # prefixing name with ":" shouldn't change result
                m = Link(
                    ":" + self.namespaces[num][0] + title, 
                    self.enwiki
                     )
                self.assertEqual(m.title, self.titles[title])

    def testHashCmp(self):
        # All links point to en:wikipedia:Test
        l1 = Link('Test', source=self.enwiki)
        l2 = Link('en:Test', source=self.frwiki)
        l3 = Link('wikipedia:en:Test', source=self.itwikt)

        debugpprint(l1)
        debugpprint(l2)
        debugpprint(l3)

        def assertHashCmp(link1, link2):
            #self.assertEqual(str(link1.__dict__), str(link2.__dict__))
            self.assertEqual(
                link1.__repr__()
                ,
                link2.__repr__()
            )
            self.assertEqual(hash(link1), hash(link2))

        assertHashCmp(l1, l2)
        assertHashCmp(l1, l3)
        assertHashCmp(l2, l3)

        # fr:wikipedia:Test
        other = Link('Test', source=self.frwiki)

        self.assertNotEqual(l1, other)
        self.assertNotEqual(hash(l1), hash(other))

class TestPageObject(TestBase):

    def __init__(self,tests):
        TestBase.__init__(self, tests)

    def setUp(self):
        TestBase.setUp(self)

    def testGeneral(self):
        self.assertEqual(
            self.mainpage, 
            "[[%s:%s]]"
            % (
                self.enwiki.lang, 
                self.mainpage.title()
            ))
        self.assertTrue(mainpage < maintalk)

    def testSite(self):
        """Test site() method"""
        self.assertEqual(
            self.mainpage.site, 
            self.enwiki
        )

    def testNamespace(self):
        """Test namespace() method"""
        self.assertEqual(self.mainpage.namespace(), 0)
        self.assertEqual(self.maintalk.namespace(), 1)
        self.assertEqual(self.badpage.namespace(), 0)

    def testTitle(self):
        """Test title() method options."""
        p1 = Page(self.enwiki, "Help:Test page#Testing")
        self.assertEqual(p1.title(),
                         "Help:Test page#Testing")
        self.assertEqual(p1.title(underscore=True),
                         "Help:Test_page#Testing")

        debugprint(p1.title(withNamespace=False))
        debugprint(p1.title(withNamespace=True))

        self.assertEqual(p1.title(withNamespace=False),
                         "Test page#Testing")
        self.assertEqual(p1.title(withSection=False),
                         "Help:Test page")
        self.assertEqual(p1.title(withNamespace=False, withSection=False),
                         "Test page")
        self.assertEqual(p1.title(asUrl=True),
                         "Help%3ATest_page%23Testing")
        self.assertEqual(p1.title(asLink=True),
                         "[[Help:Test page#Testing]]")
        self.assertEqual(p1.title(asLink=True, forceInterwiki=True),
                         "[[en:Help:Test page#Testing]]")
        self.assertEqual(p1.title(asLink=True, textlink=True),
                         p1.title(asLink=True))
        # also test a page with non-ASCII chars and a different namespace
        p2 = Page(self.enwiki, "File:Jean-Léon Gérôme 003.jpg")
        self.assertEqual(p2.title(),
                         "File:Jean-Léon Gérôme 003.jpg")
        self.assertEqual(p2.title(underscore=True),
                         "File:Jean-Léon_Gérôme_003.jpg")
        self.assertEqual(p2.title(withNamespace=False),
                         "Jean-Léon Gérôme 003.jpg")
        self.assertEqual(p2.title(withSection=False),
                         "File:Jean-Léon Gérôme 003.jpg")
        self.assertEqual(p2.title(withNamespace=False, withSection=False),
                         "Jean-Léon Gérôme 003.jpg")
        self.assertEqual(p2.title(asUrl=True),
                         "File%3AJean-L%C3%A9on_G%C3%A9r%C3%B4me_003.jpg")
        self.assertEqual(p2.title(asLink=True),
                         "[[File:Jean-Léon Gérôme 003.jpg]]")
        self.assertEqual(p2.title(asLink=True, forceInterwiki=True),
                         "[[en:File:Jean-Léon Gérôme 003.jpg]]")
        self.assertEqual(p2.title(asLink=True, textlink=True),
                         "[[:File:Jean-Léon Gérôme 003.jpg]]")
        self.assertEqual(p2.title(as_filename=True),
                         "File_Jean-Léon_Gérôme_003.jpg")

    def testSection(self):
        """Test section() method."""
        # use same pages as in previous test
        p1 = Page(self.enwiki, "Help:Test page#Testing")
        p2 = Page(self.enwiki, "File:Jean-Léon Gérôme 003.jpg")
        self.assertEqual(p1.section(), "Testing")
        self.assertEqual(p2.section(), None)

    def testIsTalkPage(self):
        """Test isTalkPage() method."""
        p1 = Page(self.enwiki, "First page")
        p2 = Page(self.enwiki, "Talk:First page")
        p3 = Page(self.enwiki, "User:Second page")
        p4 = Page(self.enwiki, "User talk:Second page")
        self.assertEqual(p1.isTalkPage(), False)
        self.assertEqual(p2.isTalkPage(), True)
        self.assertEqual(p3.isTalkPage(), False)
        self.assertEqual(p4.isTalkPage(), True)

    def testIsCategory(self):
        """Test isCategory method."""
        p1 = Page(self.enwiki, "First page")
        p2 = Page(self.enwiki, "Category:Second page")
        p3 = Page(self.enwiki, "Category talk:Second page")
        self.assertEqual(p1.isCategory(), False)
        self.assertEqual(p2.isCategory(), True)
        self.assertEqual(p3.isCategory(), False)

    def testIsImage(self):
        p1 = Page(self.enwiki, "First page")
        p2 = Page(self.enwiki, "File:Second page")
        p3 = Page(self.enwiki, "Image talk:Second page")
        self.assertEqual(p1.isImage(), False)
        self.assertEqual(p2.isImage(), True)
        self.assertEqual(p3.isImage(), False)

    def testIsRedirect(self):
        p1 = Page(self.enwiki, 'User:Legoktm/R1')
        p2 = Page(self.enwiki, 'User:Legoktm/R2')
        self.assertTrue(p1.isRedirectPage())
        self.assertEqual(p1.getRedirectTarget(), p2)

    def testPageGet(self):
        p1 = Page(self.enwiki, 'User:Legoktm/R2')
        p2 = Page(self.enwiki, 'User:Legoktm/R1')
        p3 = Page(self.enwiki, 'User:Legoktm/R3')

        text = 'This page is used in the [[mw:Manual:Pywikipediabot]] testing suite.'
        self.assertEqual(p1.get(), text)
        self.assertRaises(pywikibot.exceptions.IsRedirectPage, p2.get)
        self.assertRaises(pywikibot.exceptions.NoPage, p3.get)

    def testApiMethods(self):
        """Test various methods that rely on API."""
        # since there is no way to predict what data the wiki will return,
        # we only check that the returned objects are of correct type.
        self.assertType(self.mainpage.get(), str)
        self.assertType(self.maintalk.get(), str)
        self.assertRaises(pywikibot.NoPage, self.badpage.get)
        self.assertType(self.mainpage.latestRevision(), int)
        self.assertType(self.mainpage.userName(), str)
        self.assertType(self.mainpage.isIpEdit(), bool)
        self.assertType(self.mainpage.exists(), bool)
        self.assertType(self.mainpage.isRedirectPage(), bool)
        self.assertType(self.mainpage.isEmpty(), bool)
        self.assertEqual(self.mainpage.toggleTalkPage(), maintalk)
        self.assertEqual(maintalk.toggleTalkPage(), mainpage)
        self.assertType(self.mainpage.isDisambig(), bool)
        self.assertType(self.mainpage.canBeEdited(), bool)
        self.assertType(self.mainpage.botMayEdit(), bool)
        self.assertType(self.mainpage.editTime(), pywikibot.Timestamp)
        self.assertType(self.mainpage.previousRevision(), int)
        self.assertType(self.mainpage.permalink(), str)

    def testIsDisambig(self):
        """
        Test the integration with
        Extension:Disambiguator
        """
        if not self.enwiki.hasExtension('Disambiguator', False):
            raise unittest.SkipTest('Disambiguator extension not loaded on test site')
        pg = Page(self.enwiki, 'Random')
        pg._pageprops = set(['disambiguation', ''])
        self.assertTrue(pg.isDisambig())
        pg._pageprops = set()
        self.assertFalse(pg.isDisambig())


    def testReferences2(self):
        self.assertType(self.enwiki, Site)
        #self.assertEqual(self.enwiki, 0)
        #Site("en", "wikipedia")
        x= self.enwiki.pagereferences(
            None,
            followRedirects=True,
            filterRedirects=False,
            withTemplateInclusion=False,
            onlyTemplateInclusion=False,
            namespaces=[],
            step=1,
            total=2,
            content=3
        )


    def testReferences(self):
        count = 0
        #Ignore redirects for time considerations
        self.assertType(self.mainpage, Page)
        references = self.mainpage.getReferences(follow_redirects=False)
        debugprint (references)
        debugprint (type(references))
        self.assertType(references, Page)
        for p in references:
            count += 1
            self.assertType(p, Page)
            if count >= 10:
                break
        count = 0
        for p in self.mainpage.backlinks(followRedirects=False):
            count += 1
            self.assertType(p, Page)
            if count >= 10:
                break
        count = 0
        for p in self.mainpage.embeddedin():
            count += 1
            self.assertType(p, Page)
            if count >= 10:
                break

    def testLinks2(self):
        l= Link()
        x = l.enwiki.pagelinks(None, 
                           namespaces=None, 
                           step=1,
                           total=2, 
                           content="bla")

    def testLinks2(self):
        self.assertType(self.enwiki, Page)
        x = self.mainpage._link.enwiki.pagelinks(None, 
                           namespaces=None, 
                           step=1,
                           total=2, 
                           content="bla")


    def testLinks3(self):
        self.assertType(self.mainpage, Page)

        some_site = self.mainpage._link.site
        self.assertType(some_site, Page)

        linked_pages = self.mainpage.linkedPages()
        self.assertEqual(linked_pages, None)
        if (linked_pages is not None):
            for p in linked_pages:
                self.assertEqual(p, None)
                self.assertType(p, Page)
        iw = list(self.mainpage.interwiki(expand=True))
        for p in iw:
            self.assertType(p, pywikibot.Link)
        for p2 in self.mainpage.interwiki(expand=False):
            self.assertType(p2, pywikibot.Link)
            self.assertTrue(p2 in iw)
        for p in self.mainpage.langlinks():
            self.assertType(p, pywikibot.Link)
        for p in self.mainpage.imagelinks():
            self.assertType(p, pywikibot.ImagePage)
        for p in self.mainpage.templates():
            self.assertType(p, Page)
        for t, params in self.mainpage.templatesWithParams():
            self.assertType(t, Page)
            self.assertType(params, list)
        for p in self.mainpage.categories():
            self.assertType(p, pywikibot.Category)
        for p in self.mainpage.extlinks():
            self.assertType(p, str)

# methods that still need tests implemented or expanded:

##    def autoFormat(self):
##    def isAutoTitle(self):
##    def getOldVersion(self, oldid, force=False, get_redirect=False,
##                      sysop=False):
##    text = property(_textgetter, _textsetter, _cleartext,
##                    "The edited wikitext (unicode) of this Page")
##    def getReferences(self, follow_redirects=True, withTemplateInclusion=True,
##                      onlyTemplateInclusion=False, redirectsOnly=False,
##                      namespaces=None):
##    def backlinks(self, followRedirects=True, filterRedirects=None,
##                  namespaces=None):
##    def embeddedin(self, filter_redirects=None, namespaces=None):
##    def getVersionHistory(self, reverseOrder=False, getAll=False,
##                          revCount=500):
##    def getVersionHistoryTable(self, forceReload=False, reverseOrder=False,
##                               getAll=False, revCount=500):
##    def fullVersionHistory(self):
##    def contributingUsers(self):


if __name__ == '__main__':
    try:
        try:
            unittest.main()
        except SystemExit:
            pass
    finally:
        #pywikibot.stopme()
        pass
