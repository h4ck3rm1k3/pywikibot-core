
import pywikibot
from pywikibot import deprecate_arg
from pywikibot import deprecated
from pywikibot import config
import pywikibot.site

import hashlib
import htmlentitydefs
import logging
import re
import unicodedata
import urllib
import collections

class Category(Page):
    """A page in the Category: namespace"""

    @deprecate_arg("insite", None)
    def __init__(self, source, title="", sortKey=None):
        """All parameters are the same as for Page() constructor.

        """
        Page.__init__(self, source, title, ns=14)
        if self.namespace() != 14:
            raise ValueError("'%s' is not in the category namespace!"
                             % title)
        self.sortKey = sortKey

    @deprecate_arg("forceInterwiki", None)
    @deprecate_arg("textlink", None)
    @deprecate_arg("noInterwiki", None)
    def aslink(self, sortKey=None):
        """Return a link to place a page in this Category.

        Use this only to generate a "true" category link, not for interwikis
        or text links to category pages.

        @param sortKey: The sort key for the article to be placed in this
            Category; if omitted, default sort key is used.
        @type sortKey: (optional) unicode

        """
        key = sortKey or self.sortKey
        if key:
            titleWithSortKey = '%s|%s' % (self.title(withSection=False),
                                          key)
        else:
            titleWithSortKey = self.title(withSection=False)
        return '[[%s]]' % titleWithSortKey

    @deprecate_arg("startFrom", None)
    @deprecate_arg("cacheResults", None)
    def subcategories(self, recurse=False, step=None, total=None,
                      content=False):
        """Iterate all subcategories of the current category.

        @param recurse: if not False or 0, also iterate subcategories of
            subcategories. If an int, limit recursion to this number of
            levels. (Example: recurse=1 will iterate direct subcats and
            first-level sub-sub-cats, but no deeper.)
        @type recurse: int or bool
        @param step: limit each API call to this number of categories
        @param total: iterate no more than this number of
            subcategories in total (at all levels)
        @param content: if True, retrieve the content of the current version
            of each category description page (default False)

        """
        if not isinstance(recurse, bool) and recurse:
            recurse = recurse - 1
        if not hasattr(self, "_subcats"):
            self._subcats = []
            for member in self.site.categorymembers(
                    self, namespaces=[14], step=step,
                    total=total, content=content):
                subcat = Category(self.site, member.title())
                self._subcats.append(subcat)
                yield subcat
                if total is not None:
                    total -= 1
                    if not total:
                        return
                if recurse:
                    for item in subcat.subcategories(
                            recurse, step=step, total=total, content=content):
                        yield item
                        if total is not None:
                            total -= 1
                            if not total:
                                return
        else:
            for subcat in self._subcats:
                yield subcat
                if total is not None:
                    total -= 1
                    if not total:
                        return
                if recurse:
                    for item in subcat.subcategories(
                            recurse, step=step, total=total, content=content):
                        yield item
                        if total is not None:
                            total -= 1
                            if not total:
                                return

    @deprecate_arg("startFrom", None)
    def articles(self, recurse=False, step=None, total=None,
                 content=False, namespaces=None, sortby="",
                 starttime=None, endtime=None, startsort=None,
                 endsort=None):
        """
        Yields all articles in the current category.

        By default, yields all *pages* in the category that are not
        subcategories!

        @param recurse: if not False or 0, also iterate articles in
            subcategories. If an int, limit recursion to this number of
            levels. (Example: recurse=1 will iterate articles in first-level
            subcats, but no deeper.)
        @type recurse: int or bool
        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in
            total (at all levels)
        @param namespaces: only yield pages in the specified namespaces
        @type namespace: int or list of ints
        @param content: if True, retrieve the content of the current version
            of each page (default False)
        @param sortby: determines the order in which results are generated,
            valid values are "sortkey" (default, results ordered by category
            sort key) or "timestamp" (results ordered by time page was
            added to the category). This applies recursively.
        @type sortby: str
        @param starttime: if provided, only generate pages added after this
            time; not valid unless sortby="timestamp"
        @type starttime: Timestamp
        @param endtime: if provided, only generate pages added before this
            time; not valid unless sortby="timestamp"
        @type endtime: Timestamp
        @param startsort: if provided, only generate pages >= this title
            lexically; not valid if sortby="timestamp"
        @type startsort: str
        @param endsort: if provided, only generate pages <= this title
            lexically; not valid if sortby="timestamp"
        @type endsort: str

        """
        if namespaces is None:
            namespaces = [x for x in self.site.namespaces()
                          if x >= 0 and x != 14]
        for member in self.site.categorymembers(self,
                                                namespaces=namespaces,
                                                step=step, total=total,
                                                content=content, sortby=sortby,
                                                starttime=starttime,
                                                endtime=endtime,
                                                startsort=startsort,
                                                endsort=endsort
                                                ):
            yield member
            if total is not None:
                total -= 1
                if not total:
                    return
        if recurse:
            if not isinstance(recurse, bool) and recurse:
                recurse = recurse - 1
            for subcat in self.subcategories(step=step):
                for article in subcat.articles(recurse, step=step, total=total,
                                               content=content,
                                               namespaces=namespaces,
                                               sortby=sortby,
                                               starttime=starttime,
                                               endtime=endtime,
                                               startsort=startsort,
                                               endsort=endsort
                                               ):
                    yield article
                    if total is not None:
                        total -= 1
                        if not total:
                            return

    def members(self, recurse=False, namespaces=None, step=None, total=None,
                content=False):
        """Yield all category contents (subcats, pages, and files)."""

        for member in self.site.categorymembers(
                self, namespaces, step=step, total=total, content=content):
            yield member
            if total is not None:
                total -= 1
                if not total:
                    return
        if recurse:
            if not isinstance(recurse, bool) and recurse:
                recurse = recurse - 1
            for subcat in self.subcategories(step=step):
                for article in subcat.members(
                        recurse, namespaces, step=step,
                        total=total, content=content):
                    yield article
                    if total is not None:
                        total -= 1
                        if not total:
                            return

    def isEmptyCategory(self):
        """Return True if category has no members (including subcategories)."""
        for member in self.site.categorymembers(self, total=1):
            return False
        return True

    def isHiddenCategory(self):
        """Return True if the category is hidden."""
        # FIXME
        # This should use action=query&list=allcategories
        # setting acfrom and acto to the category title and adding
        # acprop=hidden but currently fails  in some cases
        # (see bug 48824)
        return '__HIDDENCAT__' in self.expand_text()

    def copyTo(self, cat, message):
        """
        Copy text of category page to a new page.  Does not move contents.

        @param cat: New category title (without namespace) or Category object
        @type cat: unicode or Category
        @param message: message to use for category creation message
        If two %s are provided in message, will be replaced
        by (self.title, authorsList)
        @type message: unicode
        @return: True if copying was successful, False if target page
            already existed.

        """
        # This seems far too specialized to be in the top-level framework
        # move to category.py? (Although it doesn't seem to be used there,
        # either)
        if not isinstance(cat, Category):
            cat = self.site.category_namespace() + ':' + cat
            targetCat = Category(self.site, cat)
        else:
            targetCat = cat
        if targetCat.exists():
            output('Target page %s already exists!'
                             % targetCat.title(),
                             level=WARNING)
            return False
        else:
            output('Moving text from %s to %s.'
                             % (self.title(), targetCat.title()))
            authors = ', '.join(self.contributingUsers())
            try:
                creationSummary = message % (self.title(), authors)
            except TypeError:
                creationSummary = message
            targetCat.put(self.get(), creationSummary)
            return True

    def copyAndKeep(self, catname, cfdTemplates, message):
        """Copy partial category page text (not contents) to a new title.

        Like copyTo above, except this removes a list of templates (like
        deletion templates) that appear in the old category text.  It also
        removes all text between the two HTML comments BEGIN CFD TEMPLATE
        and END CFD TEMPLATE. (This is to deal with CFD templates that are
        substituted.)

        Returns true if copying was successful, false if target page already
        existed.

        @param catname: New category title (without namespace)
        @param cfdTemplates: A list (or iterator) of templates to be removed
            from the page text
        @return: True if copying was successful, False if target page
            already existed.

        """
        # I don't see why we need this as part of the framework either
        # move to scripts/category.py?
        catname = self.site.category_namespace() + ':' + catname
        targetCat = Category(self.site, catname)
        if targetCat.exists():
            warning('Target page %s already exists!'
                              % targetCat.title())
            return False
        else:
            output(
                'Moving text from %s to %s.'
                % (self.title(), targetCat.title()))
            authors = ', '.join(self.contributingUsers())
            creationSummary = message % (self.title(), authors)
            newtext = self.get()
        for regexName in cfdTemplates:
            matchcfd = re.compile(r"{{%s.*?}}" % regexName, re.IGNORECASE)
            newtext = matchcfd.sub('', newtext)
            matchcomment = re.compile(
                r"<!--BEGIN CFD TEMPLATE-->.*?<!--END CFD TEMPLATE-->",
                re.IGNORECASE | re.MULTILINE | re.DOTALL)
            newtext = matchcomment.sub('', newtext)
            pos = 0
            while (newtext[pos:pos + 1] == "\n"):
                pos = pos + 1
            newtext = newtext[pos:]
            targetCat.put(newtext, creationSummary)
            return True

#### DEPRECATED METHODS ####
    @deprecated("list(Category.subcategories(...))")
    def subcategoriesList(self, recurse=False):
        """DEPRECATED: Equivalent to list(self.subcategories(...))"""
        return sorted(list(set(self.subcategories(recurse))))

    @deprecated("list(Category.articles(...))")
    def articlesList(self, recurse=False):
        """DEPRECATED: equivalent to list(self.articles(...))"""
        return sorted(list(set(self.articles(recurse))))

    @deprecated("Category.categories()")
    def supercategories(self):
        """DEPRECATED: equivalent to self.categories()"""
        return self.categories()

    @deprecated("list(Category.categories(...))")
    def supercategoriesList(self):
        """DEPRECATED: equivalent to list(self.categories(...))"""
        return sorted(list(set(self.categories())))
