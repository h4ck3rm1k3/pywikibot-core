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


import pywikibot
import pywikibot.page

from .utils import PywikibotTestCase, unittest

site = pywikibot.Site('en', 'wikipedia')
mainpage = pywikibot.Page(pywikibot.page.Link("Main Page", site))
maintalk = pywikibot.Page(pywikibot.page.Link("Talk:Main Page", site))
badpage = pywikibot.Page(pywikibot.page.Link("There is no page with this title",
                         site))


class TestLinkObject(unittest.TestCase):
    """Test cases for Link objects"""

    enwiki = pywikibot.Site("en", "wikipedia")
    frwiki = pywikibot.Site("fr", "wikipedia")
    itwikt = pywikibot.Site("it", "wiktionary")

    namespaces = {0: [""],        # en.wikipedia.org namespaces for testing
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
    titles = {
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
    sections = ["",
                "#Phase_2",
                "#History",
                "#later life",
                ]

    def testNamespaces(self):
        """Test that Link() normalizes namespace names"""
        for num in self.namespaces:
            for prefix in self.namespaces[num]:
                l = pywikibot.page.Link(prefix + list(self.titles.keys())[0],
                                        self.enwiki)
                self.assertEqual(l.namespace, num)
                # namespace prefixes are case-insensitive
                m = pywikibot.page.Link(prefix.lower() + list(self.titles.keys())[1],
                                        self.enwiki)
                self.assertEqual(m.namespace, num)

    def testTitles(self):
        """Test that Link() normalizes titles"""
        for title in self.titles:
            for num in (0, 1):
                l = pywikibot.page.Link(self.namespaces[num][0] + title)
                self.assertEqual(l.title, self.titles[title])
                # prefixing name with ":" shouldn't change result
                m = pywikibot.page.Link(":" + self.namespaces[num][0] + title)
                self.assertEqual(m.title, self.titles[title])

    def testHashCmp(self):
        # All links point to en:wikipedia:Test
        l1 = pywikibot.page.Link('Test', source=self.enwiki)
        l2 = pywikibot.page.Link('en:Test', source=self.frwiki)
        l3 = pywikibot.page.Link('wikipedia:en:Test', source=self.itwikt)

        def assertHashCmp(link1, link2):
            self.assertEqual(link1, link2)
            self.assertEqual(hash(link1), hash(link2))

        assertHashCmp(l1, l2)
        assertHashCmp(l1, l3)
        assertHashCmp(l2, l3)

        # fr:wikipedia:Test
        other = pywikibot.page.Link('Test', source=self.frwiki)

        self.assertNotEqual(l1, other)
        self.assertNotEqual(hash(l1), hash(other))


class TestPageObject(PywikibotTestCase):
    def testGeneral(self):
        self.assertEqual(str(mainpage), "[[%s:%s]]"
                                        % (site.lang, mainpage.title()))
        self.assertTrue(mainpage < maintalk)

    def testSite(self):
        """Test site() method"""
        self.assertEqual(mainpage.site, site)

    def testNamespace(self):
        """Test namespace() method"""
        self.assertEqual(mainpage.namespace(), 0)
        self.assertEqual(maintalk.namespace(), 1)
        self.assertEqual(badpage.namespace(), 0)

    def testTitle(self):
        """Test title() method options."""
        p1 = pywikibot.Page(site, "Help:Test page#Testing")
        self.assertEqual(p1.title(),
                         "Help:Test page#Testing")
        self.assertEqual(p1.title(underscore=True),
                         "Help:Test_page#Testing")
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
        p2 = pywikibot.Page(site, "File:Jean-Léon Gérôme 003.jpg")
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
        p1 = pywikibot.Page(site, "Help:Test page#Testing")
        p2 = pywikibot.Page(site, "File:Jean-Léon Gérôme 003.jpg")
        self.assertEqual(p1.section(), "Testing")
        self.assertEqual(p2.section(), None)

    def testIsTalkPage(self):
        """Test isTalkPage() method."""
        p1 = pywikibot.Page(site, "First page")
        p2 = pywikibot.Page(site, "Talk:First page")
        p3 = pywikibot.Page(site, "User:Second page")
        p4 = pywikibot.Page(site, "User talk:Second page")
        self.assertEqual(p1.isTalkPage(), False)
        self.assertEqual(p2.isTalkPage(), True)
        self.assertEqual(p3.isTalkPage(), False)
        self.assertEqual(p4.isTalkPage(), True)

    def testIsCategory(self):
        """Test isCategory method."""
        p1 = pywikibot.Page(site, "First page")
        p2 = pywikibot.Page(site, "Category:Second page")
        p3 = pywikibot.Page(site, "Category talk:Second page")
        self.assertEqual(p1.isCategory(), False)
        self.assertEqual(p2.isCategory(), True)
        self.assertEqual(p3.isCategory(), False)

    def testIsImage(self):
        p1 = pywikibot.Page(site, "First page")
        p2 = pywikibot.Page(site, "File:Second page")
        p3 = pywikibot.Page(site, "Image talk:Second page")
        self.assertEqual(p1.isImage(), False)
        self.assertEqual(p2.isImage(), True)
        self.assertEqual(p3.isImage(), False)

    def testIsRedirect(self):
        p1 = pywikibot.Page(site, 'User:Legoktm/R1')
        p2 = pywikibot.Page(site, 'User:Legoktm/R2')
        self.assertTrue(p1.isRedirectPage())
        self.assertEqual(p1.getRedirectTarget(), p2)

    def testPageGet(self):
        p1 = pywikibot.Page(site, 'User:Legoktm/R2')
        p2 = pywikibot.Page(site, 'User:Legoktm/R1')
        p3 = pywikibot.Page(site, 'User:Legoktm/R3')

        text = 'This page is used in the [[mw:Manual:Pywikipediabot]] testing suite.'
        self.assertEqual(p1.get(), text)
        self.assertRaises(pywikibot.exceptions.IsRedirectPage, p2.get)
        self.assertRaises(pywikibot.exceptions.NoPage, p3.get)

    def testApiMethods(self):
        """Test various methods that rely on API."""
        # since there is no way to predict what data the wiki will return,
        # we only check that the returned objects are of correct type.
        self.assertType(mainpage.get(), str)
        self.assertType(maintalk.get(), str)
        self.assertRaises(pywikibot.NoPage, badpage.get)
        self.assertType(mainpage.latestRevision(), int)
        self.assertType(mainpage.userName(), str)
        self.assertType(mainpage.isIpEdit(), bool)
        self.assertType(mainpage.exists(), bool)
        self.assertType(mainpage.isRedirectPage(), bool)
        self.assertType(mainpage.isEmpty(), bool)
        self.assertEqual(mainpage.toggleTalkPage(), maintalk)
        self.assertEqual(maintalk.toggleTalkPage(), mainpage)
        self.assertType(mainpage.isDisambig(), bool)
        self.assertType(mainpage.canBeEdited(), bool)
        self.assertType(mainpage.botMayEdit(), bool)
        self.assertType(mainpage.editTime(), pywikibot.Timestamp)
        self.assertType(mainpage.previousRevision(), int)
        self.assertType(mainpage.permalink(), str)

    def testIsDisambig(self):
        """
        Test the integration with
        Extension:Disambiguator
        """
        if not site.hasExtension('Disambiguator', False):
            raise unittest.SkipTest('Disambiguator extension not loaded on test site')
        pg = pywikibot.Page(site, 'Random')
        pg._pageprops = set(['disambiguation', ''])
        self.assertTrue(pg.isDisambig())
        pg._pageprops = set()
        self.assertFalse(pg.isDisambig())

    def testReferences(self):
        count = 0
        #Ignore redirects for time considerations
        for p in mainpage.getReferences(follow_redirects=False):
            count += 1
            self.assertType(p, pywikibot.Page)
            if count >= 10:
                break
        count = 0
        for p in mainpage.backlinks(followRedirects=False):
            count += 1
            self.assertType(p, pywikibot.Page)
            if count >= 10:
                break
        count = 0
        for p in mainpage.embeddedin():
            count += 1
            self.assertType(p, pywikibot.Page)
            if count >= 10:
                break

    def testLinks(self):
        for p in mainpage.linkedPages():
            self.assertType(p, pywikibot.Page)
        iw = list(mainpage.interwiki(expand=True))
        for p in iw:
            self.assertType(p, pywikibot.Link)
        for p2 in mainpage.interwiki(expand=False):
            self.assertType(p2, pywikibot.Link)
            self.assertTrue(p2 in iw)
        for p in mainpage.langlinks():
            self.assertType(p, pywikibot.Link)
        for p in mainpage.imagelinks():
            self.assertType(p, pywikibot.ImagePage)
        for p in mainpage.templates():
            self.assertType(p, pywikibot.Page)
        for t, params in mainpage.templatesWithParams():
            self.assertType(t, pywikibot.Page)
            self.assertType(params, list)
        for p in mainpage.categories():
            self.assertType(p, pywikibot.Category)
        for p in mainpage.extlinks():
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
        pywikibot.stopme()
