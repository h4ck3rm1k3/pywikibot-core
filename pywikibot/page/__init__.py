# -*- coding: utf-8  -*-
"""
Objects representing various types of MediaWiki pages.
"""
#
# (C) Pywikibot team, 2008-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

#import pywikibot
#from comms import pybothttp

#from pywikibot import deprecate_arg
#from pywikibot import deprecated
#from pywikibot import async_request
#import pywikibot # import link_regex, _sites
import pywikibot 


#from pywikibot.site import Site, Timestamp, Coordinate, WbTime
#from pywikibot import config,  Timestamp, Coordinate, WbTime
#import pywikibot.site
from pywikibot.site import Family, APISite
from pywikibot.textlib import removeLanguageLinks, removeCategoryLinks, removeDisabledParts, extract_templates_and_params, replaceCategoryInPlace, replaceCategoryLinks
from pywikibot.bot import output, inputChoice, log,  warning, user_input, calledModuleName, debug

from pywikibot.bot import error as print_error
from pywikibot.exceptions import Error, AutoblockUser, UserActionRefuse, NoUsername, EditConflict
#from pywikibot.i18n import translate
from pywikibot.exceptions import NoPage, SectionError, IsNotRedirectPage, IsRedirectPage, PageNotSaved, LockedPage, SpamfilterError, InvalidTitle
import hashlib
import html.entities
import logging
import re
import unicodedata
import urllib.request, urllib.parse, urllib.error
import collections
#from pywikibot.data.api import Request, APIError
import pywikibot.data.api # import Request, APIError
# pywikibot.data.api.Request
#  pywikibot.data.api.APIError

from pywikibot.site import BaseSite
from logging import  WARNING
from pywikibot.deprecate import deprecate_arg
from pywikibot.deprecate import deprecated
#from pywikibot.comms.pybothttp import request 
import pywikibot.config2 as config
#, ERROR
#, CRITICAL
# DEBUG,
# INFO, 

from pywikibot.page.wikilink import Link

logger = logging.getLogger("pywiki.wiki.page")

# Pre-compile re expressions
reNamespace = re.compile("^(.+?) *: *(.*)$")


# Note: Link objects (defined later on) represent a wiki-page's title, while
# Page objects (defined here) represent the page itself, including its contents.

from pywikibot.page.category import Category

class Page(object):
    """Page: A MediaWiki page

    This object only implements internally methods that do not require
    reading from or writing to the wiki.  All other methods are delegated
    to the Site object.

    """

    @deprecate_arg("insite", None)
    @deprecate_arg("defaultNamespace", "ns")
    def __init__(self, source, title="", ns=0):
        """Instantiate a Page object.

        Three calling formats are supported:

          - If the first argument is a Page, create a copy of that object.
            This can be used to convert an existing Page into a subclass
            object, such as Category or ImagePage.  (If the title is also
            given as the second argument, creates a copy with that title;
            this is used when pages are moved.)
          - If the first argument is a Site, create a Page on that Site
            using the second argument as the title (may include a section),
            and the third as the namespace number. The namespace number is
            mandatory, even if the title includes the namespace prefix. This
            is the preferred syntax when using an already-normalized title
            obtained from api.php or a database dump.  WARNING: may produce
            invalid objects if page title isn't in normal form!
          - If the first argument is a Link, create a Page from that link.
            This is the preferred syntax when using a title scraped from
            wikitext, URLs, or another non-normalized source.

        @param source: the source of the page
        @type source: Link, Page (or subclass), or Site
        @param title: normalized title of the page; required if source is a
            Site, ignored otherwise
        @type title: unicode
        @param ns: namespace number; required if source is a Site, ignored
            otherwise
        @type ns: int

        """
        # init fields for lint
        self._revid         = None
        self._isredir       = None
        self._expanded_text = ""
        self._site          = None
        self._title         = ""
        self._text          = ""

        if isinstance(source, BaseSite):
            self._link = Link(title, source=source, defaultNamespace=ns)
            self._revisions = {}
        elif isinstance(source, Page):
            # copy all of source's attributes to this object
            self.__dict__ = source.__dict__
            if title:
                # overwrite title
                self._link = Link(title, source=source.site,
                                  defaultNamespace=ns)
        elif isinstance(source, Link):
            self._link = source
            self._revisions = {}
        else:
            raise Error(
                "Invalid argument type '%s' in Page constructor: %s"
                % (type(source), source))

    #   toWikibase
    def toWikibase(self):
        raise Exception("not implemented")

    @property
    def site(self):
        """Return the Site object for the wiki on which this Page resides."""
        return self._link.site

    @property
    def image_repository(self):
        """Return the Site object for the image repository."""
        return self.site.image_repository()

    @property
    def data_repository(self):
        """Return the Site object for the data repository."""
        return self.site.data_repository()

    def namespace(self):
        """Return the number of the namespace of the page.

        """
        return self._link.namespace

    @deprecate_arg("decode", None)
    @deprecate_arg("savetitle", "asUrl")
    def title(self, underscore=False, savetitle=False, withNamespace=True,
              withSection=True, asUrl=False, asLink=False,
              allowInterwiki=True, forceInterwiki=False, textlink=False,
              as_filename=False):
        """Return the title of this Page, as a Unicode string.

        @param underscore: if true, replace all ' ' characters with '_'
        @param withNamespace: if false, omit the namespace prefix
        @param withSection: if false, omit the section
        @param asUrl: if true, quote title as if in an URL
        @param asLink: if true, return the title in the form of a wikilink
        @param allowInterwiki: (only used if asLink is true) if true, format
            the link as an interwiki link if necessary
        @param forceInterwiki: (only used if asLink is true) if true, always
            format the link as an interwiki link
        @param textlink: (only used if asLink is true) if true, place a ':'
            before Category: and Image: links
        @param as_filename: if true, replace any characters that are unsafe
            in filenames

        """
        title = self._link.canonical_title()
        if withSection and self._link.section:
            title = title + "#" + self._link.section
        if asLink:
            if forceInterwiki or \
               (allowInterwiki and
                (self.site.family.name != config.family
                 or self.site.code != config.mylang)):
                if self.site.family.name != config.family \
                   and self.site.family.name != self.site.code:
                    return '[[%s:%s:%s]]' % (self.site.family.name,
                                              self.site.code,
                                              title)
                else:
                    # use this form for sites like commons, where the
                    # code is the same as the family name
                    return '[[%s:%s]]' % (self.site.code,
                                           title)
            elif textlink and (self.isImage() or self.isCategory()):
                return '[[:%s]]' % title
            else:
                return '[[%s]]' % title
        if not withNamespace and self.namespace() != 0:
            title = self._link.title
            if withSection and self._link.section:
                title = title + "#" + self._link.section
        if underscore or asUrl:
            title = title.replace(' ', '_')
        if asUrl:
            encodedTitle = title.encode(self.site.encoding())
            title = urllib.parse.quote(encodedTitle)
        if as_filename:
            # Replace characters that are not possible in file names on some
            # systems.
            # Spaces are possible on most systems, but are bad for URLs.
            for forbidden in ':*?/\\ ':
                title = title.replace(forbidden, '_')
        return title

    @deprecate_arg("decode", None)
    @deprecate_arg("underscore", None)
    def section(self):
        """Return the name of the section this Page refers to.

        The section is the part of the title following a '#' character, if
        any. If no section is present, return None.

        """
        return self._link.section

    def __str__(self):
        """Return a console representation of the pagelink."""
        return self.title(asLink=True, forceInterwiki=True
                          ).encode(config.console_encoding,
                                   "xmlcharrefreplace")

    def __unicode__(self):
        return self.title(asLink=True, forceInterwiki=True)

    def __repr__(self):
        """Return a more complete string representation."""
        return "%s(%s)" % (self.__class__.__name__,
                           self.title().encode(config.console_encoding))

    def __cmp__(self, other):
        """Test for equality and inequality of Page objects.

        Page objects are "equal" if and only if they are on the same site
        and have the same normalized title, including section if any.

        Page objects are sortable by namespace first, then by title.

        """
        if not isinstance(other, Page):
            # especially, return -1 if other is None
            return -1
        if self.site != other.site:
            return self.__lt__(self.site, other.site)
        if self.namespace() != other.namespace():
            return self.__lt__(self.namespace(), other.namespace())
        return self.__lt__(self._link.title, other._link.title)

    def __hash__(self):
        # Pseudo method that makes it possible to store Page objects as keys
        # in hash-tables. This relies on the fact that the string
        # representation of an instance can not change after the construction.
        return hash(str(self))

    def autoFormat(self):
        """Return L{date.autoFormat} dictName and value, if any.

        Value can be a year, date, etc., and dictName is 'YearBC',
        'Year_December', or another dictionary name. Please note that two
        entries may have exactly the same autoFormat, but be in two
        different namespaces, as some sites have categories with the
        same names. Regular titles return (None, None).

        """
        if not hasattr(self, '_autoFormat'):
            from pywikibot import date
            self._autoFormat = date.getAutoFormat(
                self.site.code,
                self.title(withNamespace=False)
            )
        return self._autoFormat

    def isAutoTitle(self):
        """Return True if title of this Page is in the autoFormat dictionary."""
        return self.autoFormat()[0] is not None

    @deprecate_arg("throttle", None)
    @deprecate_arg("change_edit_time", None)
    def get(self, force=False, get_redirect=False, sysop=False):
        """Return the wiki-text of the page.

        This will retrieve the page from the server if it has not been
        retrieved yet, or if force is True. This can raise the following
        exceptions that should be caught by the calling code:

        @exception NoPage         The page does not exist
        @exception IsRedirectPage The page is a redirect. The argument of the
                                  exception is the title of the page it
                                  redirects to.
        @exception SectionError   The section does not exist on a page with
                                  a # link

        @param force            reload all page attributes, including errors.
        @param get_redirect     return the redirect text, do not follow the
                                redirect, do not raise an exception.
        @param sysop            if the user has a sysop account, use it to
                                retrieve this page

        """
        if force:
            # When forcing, we retry the page no matter what:
            # * Old exceptions do not apply any more
            # * Deleting _revid to force reload
            # * Deleting _redirtarget, that info is now obsolete.
            for attr in ['_redirtarget', '_getexception', '_revid']:
                if hasattr(self, attr):
                    delattr(self, attr)
        try:
            self._getInternals(sysop)
        except IsRedirectPage:
            if not get_redirect:
                raise

        return self._revisions[self._revid].text

    def _getInternals(self, sysop):
        """Helper function for get().

        Stores latest revision in self if it doesn't contain it, doesn't think.
        * Raises exceptions from previous runs.
        * Stores new exceptions in _getexception and raises them.

        """
        # Raise exceptions from previous runs
        if hasattr(self, '_getexception'):
            raise self._getexception

        # If not already stored, fetch revision
        if not hasattr(self, "_revid") \
                or not self._revid in self._revisions \
                or self._revisions[self._revid].text is None:
            try:
                self.site.loadrevisions(self, getText=True, sysop=sysop)
            except (NoPage, SectionError) as e:
                self._getexception = e
                raise

        # self._isredir is set by loadrevisions
        if self._isredir:
            self._getexception = IsRedirectPage(self)
            raise self._getexception

    @deprecate_arg("throttle", None)
    @deprecate_arg("change_edit_time", None)
    def getOldVersion(self, oldid, force=False, get_redirect=False,
                      sysop=False):
        """Return text of an old revision of this page; same options as get().

        @param oldid: The revid of the revision desired.

        """
        if force or not oldid in self._revisions \
                or self._revisions[oldid].text is None:
            self.site.loadrevisions(self,
                                    getText=True,
                                    revids=oldid,
                                    sysop=sysop)
        # TODO: what about redirects, errors?
        return self._revisions[oldid].text

    def permalink(self, oldid=None):
        """Return the permalink URL of an old revision of this page.

        @param oldid: The revid of the revision desired.

        """
        return "//%s%s/index.php?title=%s&oldid=%s" \
               % (self.site.hostname(),
                  self.site.scriptpath(),
                  self.title(asUrl=True),
                  (oldid if oldid is not None else self.latestRevision()))

    def latestRevision(self):
        """Return the current revision id for this page."""
        if not hasattr(self, '_revid'):
            self.site.loadrevisions(self)
        return self._revid

    @property
    def text(self):
        """Return the current (edited) wikitext, loading it if necessary."""
        if not hasattr(self, '_text') or self._text is None:
            try:
                self._text = self.get(get_redirect=True)
            except NoPage:
                # TODO: what other exceptions might be returned?
                self._text = ""
        return self._text

    @text.setter
    def text(self, value):
        """Update the edited wikitext"""
        self._text = None if value is None else str(value)

    @text.deleter
    def text(self):
        """Delete the edited wikitext"""
        if hasattr(self, "_text"):
            del self._text

    def properties(self, force=False):
        """
        Returns the various page properties stored for a page
        @param force: force updating from the live site
        @return: dict
        """
        if not hasattr(self, '_pageprops') or force:
            self._pageprops = {}  # page may not have pageprops (see bug 54868)
            self.site.loadpageprops(self)
        return self._pageprops

    def defaultsort(self, force=False):
        """
        Returns the value of {{DEFAULTSORT:}} magic word or None if no
        defaultsort has been defined.
        @param force: force updating from the live site
        @return: unicode or None
        """
        return self.properties(force=force).get('defaultsort')

    def expand_text(self, refresh=False):
        """Return the page text with all templates expanded."""
        if not hasattr(self, "_expanded_text") or (
                self._expanded_text is None) or refresh:
            req = pywikibot.data.api.Request(
                action="expandtemplates", text=self.text,
                title=self.title(withSection=False), site=self.site)
            self._expanded_text = req.submit()["expandtemplates"]["*"]
        return self._expanded_text

    def userName(self):
        """Return name or IP address of last user to edit page.

        """
        rev = self.latestRevision()
        if rev not in self._revisions:
            self.site.loadrevisions(self)
        return self._revisions[rev].user

    def isIpEdit(self):
        """Return True if last editor was unregistered.

        """
        rev = self.latestRevision()
        if rev not in self._revisions:
            self.site.loadrevisions(self)
        return self._revisions[rev].anon

    def editTime(self):
        """Return timestamp of last revision to page.

        """
        rev = self.latestRevision()
        if rev not in self._revisions:
            self.site.loadrevisions(self)
        return self._revisions[rev].timestamp

    def previousRevision(self):
        """Return the revision id for the previous revision of this Page."""
        #vh = 
        self.getVersionHistory(total=2)
        revkey = sorted(self._revisions, reverse=True)[1]
        return revkey

    def exists(self):
        """Return True if page exists on the wiki, even if it's a redirect.

        If the title includes a section, return False if this section isn't
        found.

        """
        return self.site.page_exists(self)

    def isRedirectPage(self):
        """Return True if this is a redirect, False if not or not existing."""
        return self.site.page_isredirect(self)

    def isStaticRedirect(self, force=False):
        """Return True if this is a redirect containing the magic word
        __STATICREDIRECT__, False if not or not existing.

        """
        found = False
        if self.isRedirectPage():
            staticKeys = self.site.getmagicwords('staticredirect')
            text = self.get(get_redirect=True, force=force)
            if staticKeys:
                for key in staticKeys:
                    if key in text:
                        found = True
                        break
        return found

    def isCategoryRedirect(self):
        """Return True if this is a category redirect page, False otherwise."""

        if not self.isCategory():
            return False
        if not hasattr(self, "_catredirect"):
            catredirs = self.site.category_redirects()
            for (template, args) in self.templatesWithParams():
                if template.title(withNamespace=False) in catredirs:
                    # Get target (first template argument)
                    try:
                        self._catredirect = "%s:%s" % (self.site.namespace(14),
                                                       args[0].strip())
                        break
                    except IndexError:
                        warning(
                            "No target for category redirect on %s"
                            % self.title(asLink=True))
                        self._catredirect = False
                        break
            else:
                self._catredirect = False
        return bool(self._catredirect)

    def getCategoryRedirectTarget(self):
        """If this is a category redirect, return the target category title."""
        if self.isCategoryRedirect():
            return Category(Link(self._catredirect, self.site))
        raise IsNotRedirectPage(self.title())

    def isEmpty(self):
        """Return True if the page text has less than 4 characters.

        Character count ignores language links and category links.
        Can raise the same exceptions as get().

        """
        txt = self.get()
        txt = removeLanguageLinks(txt, site=self.site)
        txt = removeCategoryLinks(txt, site=self.site)
        return len(txt) < 4

    def isTalkPage(self):
        """Return True if this page is in any talk namespace."""
        ns = self.namespace()
        return ns >= 0 and ns % 2 == 1

    def toggleTalkPage(self):
        """Return other member of the article-talk page pair for this Page.

        If self is a talk page, returns the associated content page;
        otherwise, returns the associated talk page.  The returned page need
        not actually exist on the wiki.

        Returns None if self is a special page.

        """
        ns = self.namespace()
        if ns < 0:  # Special page
            return
        if self.isTalkPage():
            if self.namespace() == 1:
                return Page(self.site, self.title(withNamespace=False))
            else:
                return Page(self.site,
                            "%s:%s" % (self.site.namespace(ns - 1),
                                       self.title(withNamespace=False)))
        else:
            return Page(self.site,
                        "%s:%s" % (self.site.namespace(ns + 1),
                                   self.title(withNamespace=False)))

    def isCategory(self):
        """Return True if the page is a Category, False otherwise."""
        return self.namespace() == 14

    def isImage(self):
        """Return True if this is an image description page, False otherwise."""
        return self.namespace() == 6

    def isDisambig(self, get_Index=True):
        """Return True if this is a disambiguation page, False otherwise.

        Relies on the presence of specific templates, identified in
        the Family file or on a wiki page, to identify disambiguation
        pages.

        By default, loads a list of template names from the Family file;
        if the value in the Family file is None no entry was made, looks for
        the list on [[MediaWiki:Disambiguationspage]]. If this page does not
        exist, take the mediawiki message.

        If get_Index is True then also load the templates for index articles
        which are given on en-wiki

        Template:Disambig is always assumed to be default, and will be
        appended regardless of its existence.

        """

        if self.site.hasExtension('Disambiguator', False):
            # If the Disambiguator extension is loaded, use it
            return 'disambiguation' in self.properties()

        if not hasattr(self.site, "_disambigtemplates"):
            try:
                default = set(self.site.family.disambig('_default'))
            except KeyError:
                default = set(['Disambig'])
            try:
                distl = self.site.family.disambig(self.site.code,
                                                  fallback=False)
            except KeyError:
                distl = None
            if distl is None:
                disambigpages = Page(self.site,
                                     "MediaWiki:Disambiguationspage")
                indexes = set()
                if disambigpages.exists():
                    disambigs = set(link.title(withNamespace=False)
                                    for link in disambigpages.linkedPages()
                                    if link.namespace() == 10)
                    # cache index article templates separately
                    if self.site.sitename() == 'wikipedia:en':
                        regex = re.compile('\(\((.+?)\)\)')
                        content = disambigpages.get()
                        for index in regex.findall(content):
                            indexes.add(index[:1].upper() + index[1:])
                        self.site._indextemplates = indexes
                else:
                    message = self.site.mediawiki_message(
                        'disambiguationspage').split(':', 1)[1]
                    # add the default template(s) for default mw message
                    # only
                    disambigs = set([message[:1].upper() +
                                     message[1:]]) | default
                self.site._disambigtemplates = disambigs
            else:
                # Normalize template capitalization
                self.site._disambigtemplates = set(
                    t[:1].upper() + t[1:] for t in distl
                )
        templates = set(tl.title(withNamespace=False)
                        for tl in self.templates())
        disambigs = set()
        # always use cached disambig templates
        disambigs.update(self.site._disambigtemplates)
        # if get_Index is True, also use cached index templates
        if get_Index and hasattr(self.site, '_indextemplates'):
            disambigs.update(self.site._indextemplates)
        # see if any template on this page is in the set of disambigs
        disambigInPage = disambigs.intersection(templates)
        return self.namespace() != 10 and len(disambigInPage) > 0

    def getReferences(self, follow_redirects=True, withTemplateInclusion=True,
                      onlyTemplateInclusion=False, redirectsOnly=False,
                      namespaces=None, step=None, total=None, content=False):
        """Return an iterator all pages that refer to or embed the page.

        If you need a full list of referring pages, use
        C{pages = list(s.getReferences())}

        @param follow_redirects: if True, also iterate pages that link to a
            redirect pointing to the page.
        @param withTemplateInclusion: if True, also iterate pages where self
            is used as a template.
        @param onlyTemplateInclusion: if True, only iterate pages where self
            is used as a template.
        @param redirectsOnly: if True, only iterate redirects to self.
        @param namespaces: only iterate pages in these namespaces
        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, retrieve the content of the current version
            of each referring page (default False)

        """
        # N.B.: this method intentionally overlaps with backlinks() and
        # embeddedin(). Depending on the interface, it may be more efficient
        # to implement those methods in the site interface and then combine
        # the results for this method, or to implement this method and then
        # split up the results for the others.
        return self.site.pagereferences(
            self,
            followRedirects=follow_redirects,
            filterRedirects=redirectsOnly,
            withTemplateInclusion=withTemplateInclusion,
            onlyTemplateInclusion=onlyTemplateInclusion,
            namespaces=namespaces,
            step=step,
            total=total,
            content=content
        )

    def backlinks(self, followRedirects=True, filterRedirects=None,
                  namespaces=None, step=None, total=None, content=False):
        """Return an iterator for pages that link to this page.

        @param followRedirects: if True, also iterate pages that link to a
            redirect pointing to the page.
        @param filterRedirects: if True, only iterate redirects; if False,
            omit redirects; if None, do not filter
        @param namespaces: only iterate pages in these namespaces
        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, retrieve the content of the current version
            of each referring page (default False)

        """
        return self.site.pagebacklinks(
            self,
            followRedirects=followRedirects,
            filterRedirects=filterRedirects,
            namespaces=namespaces,
            step=step,
            total=total,
            content=content
        )

    def embeddedin(self, filter_redirects=None, namespaces=None, step=None,
                   total=None, content=False):
        """Return an iterator for pages that embed this page as a template.

        @param filterRedirects: if True, only iterate redirects; if False,
            omit redirects; if None, do not filter
        @param namespaces: only iterate pages in these namespaces
        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, retrieve the content of the current version
            of each embedding page (default False)

        """
        return self.site.page_embeddedin(
            self,
            filterRedirects=filter_redirects,
            namespaces=namespaces,
            step=step,
            total=total,
            content=content
        )

    def canBeEdited(self):
        """Return bool indicating whether this page can be edited.

        This returns True if and only if:
          - page is unprotected, and bot has an account for this site, or
          - page is protected, and bot has a sysop account for this site.

        """
        return self.site.page_can_be_edited(self)

    def botMayEdit(self):
        """Return True if this page allows bots to edit it.

        This will be True if the page doesn't contain {{bots}} or
        {{nobots}}, or it contains them and the active bot is allowed to
        edit this page. (This method is only useful on those sites that
        recognize the bot-exclusion protocol; on other sites, it will always
        return True.)

        The framework enforces this restriction by default. It is possible
        to override this by setting ignore_bot_templates=True in
        user-config.py, or using page.put(force=True).

        """
        # TODO: move this to Site object?
        if config.ignore_bot_templates:  # Check the "master ignore switch"
            return True
        username = self.site.user()
        try:
            templates = self.templatesWithParams()
        except (NoPage,
                IsRedirectPage,
                SectionError):
            return True

        # go through all templates and look for any restriction
        # multiple bots/nobots templates are allowed
        for template in templates:
            title = template[0].title(withNamespace=False)
            if title == 'Nobots':
                if len(template[1]) == 0:
                    return False
                else:
                    bots = template[1][0].split(',')
                    if 'all' in bots or calledModuleName() in bots \
                       or username in bots:
                        return False
            elif title == 'Bots':
                if len(template[1]) == 0:
                    return True
                else:
                    (ttype, bots) = template[1][0].split('=', 1)
                    bots = bots.split(',')
                    if ttype == 'allow':
                        return 'all' in bots or username in bots
                    if ttype == 'deny':
                        return not ('all' in bots or username in bots)
                    if ttype == 'allowscript':
                        return 'all' in bots or calledModuleName() in bots
                    if ttype == 'denyscript':
                        return not ('all' in bots or calledModuleName() in bots)
        # no restricting template found
        return True

    def save(self, comment=None, watch=None, minor=True, botflag=None,
             force=False, async=False, callback=None, **kwargs):
        """Save the current contents of page's text to the wiki.

        @param comment: The edit summary for the modification (optional, but
            most wikis strongly encourage its use)
        @type comment: unicode
        @param watch: if True, add or if False, remove this Page to/from bot
            user's watchlist; if None (default), follow bot account's default
            settings
        @type watch: bool or None
        @param minor: if True, mark this edit as minor
        @type minor: bool
        @param botflag: if True, mark this edit as made by a bot (default:
            True if user has bot status, False if not)
        @param force: if True, ignore botMayEdit() setting
        @type force: bool
        @param async: if True, launch a separate thread to save
            asynchronously
        @param callback: a callable object that will be called after the
            page put operation. This object must take two arguments: (1) a
            Page object, and (2) an exception instance, which will be None
            if the page was saved successfully. The callback is intended for
            use by bots that need to keep track of which saves were
            successful.

        """
        if not comment:
            comment = config.default_edit_summary
        if watch is None:
            watchval = None
        elif watch:
            watchval = "watch"
        else:
            watchval = "unwatch"
        if not force and not self.botMayEdit():
            raise PageNotSaved(
                "Page %s not saved; editing restricted by {{bots}} template"
                % self.title(asLink=True))
        if botflag is None:
            botflag = ("bot" in self.site.userinfo["rights"])
        if async:
            async_request(self._save, comment=comment, minor=minor,
                                    watchval=watchval, botflag=botflag,
                                    async=async, callback=callback, **kwargs)
        else:
            self._save(comment=comment, minor=minor, watchval=watchval,
                       botflag=botflag, async=async, callback=callback,
                       **kwargs)

    def _save(self, comment, minor, watchval, botflag, async, callback,
              **kwargs):
        err = None
        link = self.title(asLink=True)
        if config.cosmetic_changes:
            comment = self._cosmetic_changes_hook(comment) or comment
        try:
            done = self.site.editpage(self, summary=comment, minor=minor,
                                      watch=watchval, bot=botflag, **kwargs)
            if not done:
                warning("Page %s not saved" % link)
                raise PageNotSaved(link)
            else:
                output("Page %s saved" % link)
        except LockedPage as err:
            # re-raise the LockedPage exception so that calling program
            # can re-try if appropriate
            if not callback and not async:
                raise
        # TODO: other "expected" error types to catch?
        except Error as err:
            log("Error saving page %s (%s)\n" % (link, err),
                          exc_info=True)
            if not callback and not async:
                raise PageNotSaved("%s: %s" % (link, err))
        if callback:
            callback(self, err)

    def _cosmetic_changes_hook(self, comment):
        if self.isTalkPage() or \
           calledModuleName() in config.cosmetic_changes_deny_script:
            return
        family = self.site.family.name
        config.cosmetic_changes_disable.update({'wikidata': ('repo', )})
        if config.cosmetic_changes_mylang_only:
            cc = ((family == config.family and
                   self.site.lang == config.mylang) or
                  family in list(config.cosmetic_changes_enable.keys()) and
                  self.site.lang in config.cosmetic_changes_enable[family])
        else:
            cc = True
        cc = (cc and not
              (family in list(config.cosmetic_changes_disable.keys()) and
               self.site.lang in config.cosmetic_changes_disable[family]))
        if not cc:
            return
        old = self.text
        log('Cosmetic changes for %s-%s enabled.'
                      % (family, self.site.lang))
        from scripts.cosmetic_changes import CosmeticChangesToolkit
        from pywikibot import i18n
        ccToolkit = CosmeticChangesToolkit(self.site,
                                           redirect=self.isRedirectPage(),
                                           namespace=self.namespace(),
                                           pageTitle=self.title())
        self.text = ccToolkit.change(old)
        if comment and \
           old.strip().replace('\r\n',
                               '\n') != self.text.strip().replace('\r\n', '\n'):
            comment += i18n.twtranslate(self.site, 'cosmetic_changes-append')
            return comment

    def put(self, newtext, comment='', watchArticle=None, minorEdit=True,
            botflag=None, force=False, async=False, callback=None, **kwargs):
        """Save the page with the contents of the first argument as the text.

        This method is maintained primarily for backwards-compatibility.
        For new code, using Page.save() is preferred.  See save() method
        docs for all parameters not listed here.

        @param newtext: The complete text of the revised page.
        @type newtext: unicode

        """
        self.text = newtext
        return self.save(comment=comment, watch=watchArticle,
                         minor=minorEdit, botflag=botflag, force=force,
                         async=async, callback=callback, **kwargs)

    def put_async(self, newtext, comment='', watchArticle=None,
                  minorEdit=True, botflag=None, force=False, callback=None,
                  **kwargs):
        """Put page on queue to be saved to wiki asynchronously.

        Asynchronous version of put (takes the same arguments), which places
        pages on a queue to be saved by a daemon thread. All arguments are
        the same as for .put().  This version is maintained solely for
        backwards-compatibility.

        """
        return self.put(newtext, comment=comment, watchArticle=watchArticle,
                        minorEdit=minorEdit, botflag=botflag, force=force,
                        async=True, callback=callback, **kwargs)

    def watch(self, unwatch=False):
        """Add or remove this page to/from bot account's watchlist.

        @param unwatch: True to unwatch, False (default) to watch.
        @return: True if successful, False otherwise.

        """
        return self.site.watchpage(self, unwatch)

    def linkedPages(self, namespaces=None, step=None, total=None,
                    content=False):
        """Iterate Pages that this Page links to.

        Only returns pages from "normal" internal links. Image and category
        links are omitted unless prefixed with ":". Embedded templates are
        omitted (but links within them are returned). All interwiki and
        external links are omitted.

        @param namespaces: only iterate links in these namespaces
        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, retrieve the content of the current version
            of each linked page (default False)
        @return: a generator that yields Page objects.

        """
        return self.site.pagelinks(self, namespaces=namespaces, step=step,
                                   total=total, content=content)

    def interwiki(self, expand=True):
        """Iterate interwiki links in the page text, excluding language links.

        @param expand: if True (default), include interwiki links found in
            templates transcluded onto this page; if False, only iterate
            interwiki links found in this page's own wikitext
        @return: a generator that yields Link objects

        """
        # This function does not exist in the API, so it has to be
        # implemented by screen-scraping
        if expand:
            text = self.expand_text()
        else:
            text = self.text
        for linkmatch in pywikibot.link_regex.finditer(
                removeDisabledParts(text)):
            linktitle = linkmatch.group("title")
            link = Link(linktitle, self.site)
            # only yield links that are to a different site and that
            # are not language links
            try:
                if link.site != self.site:
                    if linktitle.lstrip().startswith(":"):
                        # initial ":" indicates not a language link
                        yield link
                    elif link.site.family != self.site.family:
                        # link to a different family is not a language link
                        yield link
            except Error:
                # ignore any links with invalid contents
                continue

    def langlinks(self):
        """Return a list of all interlanguage Links on this page.

        """
        # Data might have been preloaded
        if not hasattr(self, '_langlinks'):
            self._langlinks = list(self.iterlanglinks())

        return self._langlinks

    def iterlanglinks(self, step=None, total=None):
        """Iterate all interlanguage links on this page.

        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @return: a generator that yields Link objects.

        """
        if hasattr(self, '_langlinks'):
            return iter(self._langlinks)
        # XXX We might want to fill _langlinks when the Site
        # method is called. If we do this, we'll have to think
        # about what will happen if the generator is not completely
        # iterated upon.
        return self.site.pagelanglinks(self, step=step, total=total)

    def data_item(self):
        """
        Convinience function to get the Wikibase item of a page
        @return: ItemPage
        """
        return ItemPage.fromPage(self)

    def templates(self, content=False):
        """Return a list of Page objects for templates used on this Page.

        Template parameters are ignored.  This method only returns embedded
        templates, not template pages that happen to be referenced through
        a normal link.

        @param content: if True, retrieve the content of the current version
            of each template (default False)

        """
        # Data might have been preloaded
        if not hasattr(self, '_templates'):
            self._templates = list(self.itertemplates(content=content))

        return self._templates

    def itertemplates(self, step=None, total=None, content=False):
        """Iterate Page objects for templates used on this Page.

        Template parameters are ignored.  This method only returns embedded
        templates, not template pages that happen to be referenced through
        a normal link.

        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, retrieve the content of the current version
            of each template (default False)

        """
        if hasattr(self, '_templates'):
            return iter(self._templates)
        return self.site.pagetemplates(self, step=step, total=total,
                                       content=content)

    @deprecate_arg("followRedirects", None)
    @deprecate_arg("loose", None)
    def imagelinks(self, step=None, total=None, content=False):
        """Iterate ImagePage objects for images displayed on this Page.

        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, retrieve the content of the current version
            of each image description page (default False)
        @return: a generator that yields ImagePage objects.

        """
        return self.site.pageimages(self, step=step, total=total,
                                    content=content)

    @deprecate_arg("get_redirect", None)
    def templatesWithParams(self):
        """Iterate templates used on this Page.

        @return: a generator that yields a tuple for each use of a template
        in the page, with the template Page as the first entry and a list of
        parameters as the second entry.

        """
        # WARNING: may not return all templates used in particularly
        # intricate cases such as template substitution
        titles = list(t.title() for t in self.templates())
        templates = extract_templates_and_params(self.text)
        # backwards-compatibility: convert the dict returned as the second
        # element into a list in the format used by old scripts
        result = []
        for template in templates:
            link = Link(template[0], self.site,
                                  defaultNamespace=10)
            try:
                if link.canonical_title() not in titles:
                    continue
            except Error:
                # this is a parser function or magic word, not template name
                continue
            args = template[1]
            intkeys = {}
            named = {}
            positional = []
            for key in sorted(args):
                try:
                    intkeys[int(key)] = args[key]
                except ValueError:
                    named[key] = args[key]
            for i in range(1, len(intkeys) + 1):
                # only those args with consecutive integer keys can be
                # treated as positional; an integer could also be used
                # (out of order) as the key for a named argument
                # example: {{tmp|one|two|5=five|three}}
                if i in intkeys:
                    positional.append(intkeys[i])
                else:
                    for k in intkeys:
                        if k < 1 or k >= i:
                            named[str(k)] = intkeys[k]
                    break
            for name in named:
                positional.append("%s=%s" % (name, named[name]))
            result.append((Page(link, self.site), positional))
        return result

    @deprecate_arg("nofollow_redirects", None)
    @deprecate_arg("get_redirect", None)
    def categories(self, withSortKey=False, step=None, total=None,
                   content=False):
        """Iterate categories that the article is in.

        @param withSortKey: if True, include the sort key in each Category.
        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, retrieve the content of the current version
            of each category description page (default False)
        @return: a generator that yields Category objects.

        """
        return self.site.pagecategories(self, withSortKey=withSortKey,
                                        step=step, total=total, content=content)

    def extlinks(self, step=None, total=None):
        """Iterate all external URLs (not interwiki links) from this page.

        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @return: a generator that yields unicode objects containing URLs.

        """
        return self.site.page_extlinks(self, step=step, total=total)

    def coordinates(self, primary_only=False):
        """Return a list of Coordinate objects for points
        on the page using [[mw:Extension:GeoData]]

        @param primary_only: Only return the coordinate indicated to be primary
        @return: A list of Coordinate objects
        """
        if not hasattr(self, '_coords'):
            self._coords = []
            self.site.loadcoordinfo(self)
        if primary_only:
            return self._coords[0] if len(self._coords) > 0 else None
        else:
            return self._coords

    def getRedirectTarget(self):
        """Return a Page object for the target this Page redirects to.

        If this page is not a redirect page, will raise an IsNotRedirectPage
        exception. This method also can raise a NoPage exception.

        """
        return self.site.getredirtarget(self)

    # BREAKING CHANGE: in old framework, default value for getVersionHistory
    #                  returned no more than 500 revisions; now, it iterates
    #                  all revisions unless 'total' argument is used
    @deprecate_arg("forceReload", None)
    @deprecate_arg("revCount", "total")
    @deprecate_arg("getAll", None)
    def getVersionHistory(self, reverseOrder=False, step=None,
                          total=None):
        """Load the version history page and return history information.

        Return value is a list of tuples, where each tuple represents one
        edit and is built of revision id, edit date/time, user name, and
        edit summary. Starts with the most current revision, unless
        reverseOrder is True.

        @param step: limit each API call to this number of revisions
        @param total: iterate no more than this number of revisions in total

        """
        self.site.loadrevisions(self, getText=False, rvdir=reverseOrder,
                                step=step, total=total)
        return [(self._revisions[rev].revid,
                 self._revisions[rev].timestamp,
                 self._revisions[rev].user,
                 self._revisions[rev].comment
                 ) for rev in sorted(self._revisions,
                                     reverse=not reverseOrder)
                ]

    def getVersionHistoryTable(self, forceReload=False, reverseOrder=False,
                               step=None, total=None):
        """Return the version history as a wiki table."""

        result = '{| class="wikitable"\n'
        result += '! oldid || date/time || username || edit summary\n'
        for oldid, time, username, summary \
                in self.getVersionHistory(
                    #forceReload=forceReload,
                                          reverseOrder=reverseOrder,
                                          step=step, total=total):
            result += '|----\n'
            result += '| %s || %s || %s || <nowiki>%s</nowiki>\n'\
                      % (oldid, time, username, summary)
        result += '|}\n'
        return result

    def fullVersionHistory(self, reverseOrder=False, step=None,
                           total=None):
        """Iterate previous versions including wikitext.

        Takes same arguments as getVersionHistory.

        @return: A generator that yields tuples consisting of revision ID,
            edit date/time, user name and content

        """
        self.site.loadrevisions(self, getText=True,
                                rvdir=reverseOrder,
                                step=step, total=total)
        return [(self._revisions[rev].revid,
                 self._revisions[rev].timestamp,
                 self._revisions[rev].user,
                 self._revisions[rev].text
                 ) for rev in sorted(self._revisions,
                                     reverse=not reverseOrder)
                ]

    def contributingUsers(self, step=None, total=None):
        """Return a set of usernames (or IPs) of users who edited this page.

        @param step: limit each API call to this number of revisions
        @param total: iterate no more than this number of revisions in total

        """
        edits = self.getVersionHistory(step=step, total=total)
        users = set([edit[2] for edit in edits])
        return users

    @deprecate_arg("throttle", None)
    def move(self, newtitle, reason=None, movetalkpage=True, sysop=False,
             deleteAndMove=False, safe=True):
        """Move this page to a new title.

        @param newtitle: The new page title.
        @param reason: The edit summary for the move.
        @param movetalkpage: If true, move this page's talk page (if it exists)
        @param sysop: Try to move using sysop account, if available
        @param deleteAndMove: if move succeeds, delete the old page
            (usually requires sysop privileges, depending on wiki settings)
        @param safe: If false, attempt to delete existing page at newtitle
            (if there is one) and then move this page to that title

        """
        if reason is None:
            output('Moving %s to [[%s]].'
                             % (self.title(asLink=True), newtitle))
            reason = input('Please enter a reason for the move:')
        # TODO: implement "safe" parameter (Is this necessary ?)
        # TODO: implement "sysop" parameter
        return self.site.movepage(self, newtitle, reason,
                                  movetalk=movetalkpage,
                                  noredirect=deleteAndMove)

    @deprecate_arg("throttle", None)
    def delete(self, reason=None, prompt=True, throttle=None, mark=False):
        """Deletes the page from the wiki. Requires administrator status.

        @param reason: The edit summary for the deletion. If None, ask for it.
        @param prompt: If true, prompt user for confirmation before deleting.
        @param mark: if true, and user does not have sysop rights, place a
            speedy-deletion request on the page instead.

        """
        # TODO: add support for mark
        if reason is None:
            output('Deleting %s.' % (self.title(asLink=True)))
            reason = user_input('Please enter a reason for the deletion:')
        answer = 'y'
        if prompt and not hasattr(self.site, '_noDeletePrompt'):
            answer = inputChoice(
                'Do you want to delete %s?' % self.title(asLink=True,
                                                          forceInterwiki=True),
                ['Yes', 'No', 'All'],
                ['Y', 'N', 'A'],
                'N')
            if answer in ['a', 'A']:
                answer = 'y'
                self.site._noDeletePrompt = True
        if answer in ['y', 'Y']:
            try:
                return self.site.deletepage(self, reason)
            except NoUsername as e:
                if mark:
                    raise NotImplementedError(
                        "Marking pages for deletion is not yet available.")
                raise e

    # all these DeletedRevisions methods need to be reviewed and harmonized
    # with the new framework; they do not appear functional
    def loadDeletedRevisions(self, step=None, total=None):
        """Retrieve all deleted revisions for this Page from Special/Undelete.

        Stores all revisions' timestamps, dates, editors and comments in
        self._deletedRevs attribute.

        @return: iterator of timestamps (which can be used to retrieve
            revisions later on).

        """
        if not hasattr(self, "_deletedRevs"):
            self._deletedRevs = {}
        for item in self.site.deletedrevs(self, step=step, total=total):
            for rev in item.get("revisions", []):
                self._deletedRevs[rev['timestamp']] = rev
                yield rev['timestamp']

    def getDeletedRevision(self, timestamp, retrieveText=False):
        """Return a particular deleted revision by timestamp.

        @return: a list of [date, editor, comment, text, restoration
            marker]. text will be None, unless retrieveText is True (or has
            been retrieved earlier). If timestamp is not found, returns
            None.

        """
        if hasattr(self, "_deletedRevs"):
            if timestamp in self._deletedRevs and (
                    (not retrieveText)
                    or "content" in self._deletedRevs[timestamp]):
                return self._deletedRevs[timestamp]
        for item in self.site.deletedrevs(self, start=timestamp,
                                          get_text=retrieveText, total=1):
            # should only be one item with one revision
            if item['title'] == self.title:
                if "revisions" in item:
                    return item["revisions"][0]

    def markDeletedRevision(self, timestamp, undelete=True):
        """Mark the revision identified by timestamp for undeletion.

        @param undelete: if False, mark the revision to remain deleted.

        """
        if not hasattr(self, "_deletedRevs"):
            self.loadDeletedRevisions()
        if timestamp not in self._deletedRevs:
            # TODO: Throw an exception?
            return
        self._deletedRevs[timestamp][4] = undelete
        self._deletedRevsModified = True

    @deprecate_arg("throttle", None)
    def undelete(self, comment=None):
        """Undelete revisions based on the markers set by previous calls.

        If no calls have been made since loadDeletedRevisions(), everything
        will be restored.

        Simplest case:
            Page(...).undelete('This will restore all revisions')

        More complex:
            pg = Page(...)
            revs = pg.loadDeletedRevsions()
            for rev in revs:
                if ... #decide whether to undelete a revision
                    pg.markDeletedRevision(rev) #mark for undeletion
            pg.undelete('This will restore only selected revisions.')

        @param comment: The undeletion edit summary.

        """
        if comment is None:
            output('Preparing to undelete %s.'
                             % (self.title(asLink=True)))
            comment = user_input(
                'Please enter a reason for the undeletion:')
        return self.site.undelete(self, comment)

    @deprecate_arg("throttle", None)
    def protect(self, edit='sysop', move='sysop', unprotect=False,
                reason=None, prompt=True):
        """(Un)protect a wiki page. Requires administrator status.

        Valid protection levels (in MediaWiki 1.12) are '' (equivalent to
        'none'), 'autoconfirmed', and 'sysop'.

        @param edit: Level of edit protection
        @param move: Level of move protection
        @param unprotect: If true, unprotect the page (equivalent to setting
            all protection levels to '')
        @param reason: Edit summary.
        @param prompt: If true, ask user for confirmation.

        """
        if reason is None:
            if unprotect:
                un = 'un'
            else:
                un = ''
            output('Preparing to %sprotect %s.'
                             % (un, self.title(asLink=True)))
            reason = user_input('Please enter a reason for the action:')
        if unprotect:
            edit = move = ""
        answer = 'y'
        if prompt and not hasattr(self.site, '_noProtectPrompt'):
            answer = inputChoice(
                'Do you want to change the protection level of %s?'
                % self.title(asLink=True, forceInterwiki=True),
                ['Yes', 'No', 'All'],
                ['Y', 'N', 'A'],
                'N')
            if answer in ['a', 'A']:
                answer = 'y'
                self.site._noProtectPrompt = True
        if answer in ['y', 'Y']:
            return self.site.protect(self, edit, move, reason)

    def change_category(self, oldCat, newCat, comment=None, sortKey=None,
                        inPlace=True):
        """
        Remove page from oldCat and add it to newCat.

        @param oldCat and newCat: should be Category objects.
            If newCat is None, the category will be removed.

        @param comment: string to use as an edit summary

        @param sortKey: sortKey to use for the added category.
            Unused if newCat is None, or if inPlace=True

        @param inPlace: if True, change categories in place rather than
                      rearranging them.

        """
        # get list of Category objects the article is in and remove possible
        # duplicates
        cats = []
        for cat in self.categories(
                #get_redirect=True
        ):
            if cat not in cats:
                cats.append(cat)

        site = self.site

        if not sortKey:
            sortKey = oldCat.sortKey

        if not self.canBeEdited():
            output("Can't edit %s, skipping it..."
                             % self.title(asLink=True))
            return

        if oldCat not in cats:
            print_error('%s is not in category %s!'
                            % (self.title(asLink=True), oldCat.title()))
            return

        if inPlace or self.namespace() == 10:
            oldtext = self.get(get_redirect=True)
            newtext = replaceCategoryInPlace(oldtext, oldCat, newCat)
        else:
            if newCat:
                cats[cats.index(oldCat)] = Category(site, newCat.title(),
                                                    sortKey=sortKey)
            else:
                cats.pop(cats.index(oldCat))
            oldtext = self.get(get_redirect=True)
            try:
                newtext = replaceCategoryLinks(oldtext, cats)
            except ValueError:
                # Make sure that the only way replaceCategoryLinks() can return
                # a ValueError is in the case of interwiki links to self.
                output('Skipping %s because of interwiki link to '
                                 'self' % self.title())

        if oldtext != newtext:
            try:
                self.put(newtext, comment)
            except EditConflict:
                output('Skipping %s because of edit conflict'
                                 % self.title())
            except SpamfilterError as e:
                output('Skipping %s because of blacklist entry %s'
                                 % (self.title(), e.url))
            except LockedPage:
                output('Skipping %s because page is locked'
                                 % self.title())
            except NoUsername:
                output('Page %s not saved; sysop privileges '
                                 'required.' % self.title(asLink=True))
            except PageNotSaved as error:
                output('Saving page %s failed: %s'
                                 % (self.title(asLink=True), str(error)))

    @property
    def categoryinfo(self):
        """If supported, return a dict containing category content values:

        Numbers of pages, subcategories, files, and total contents.

        """
        if not self.isCategory():
            return  # should this raise an exception??
        try:
            return self.site.categoryinfo(self)
        except NotImplementedError:
            return

######## DEPRECATED METHODS ########

    @deprecated("Site.encoding()")
    def encoding(self):
        """DEPRECATED: use Site.encoding() instead"""
        return self.site.encoding()

    @deprecated("Page.title(withNamespace=False)")
    def titleWithoutNamespace(self, underscore=False):
        """DEPRECATED: use self.title(withNamespace=False) instead."""
        return self.title(underscore=underscore, withNamespace=False,
                          withSection=False)

    @deprecated("Page.title(as_filename=True)")
    def titleForFilename(self):
        """DEPRECATED: use self.title(as_filename=True) instead."""
        return self.title(as_filename=True)

    @deprecated("Page.title(withSection=False)")
    def sectionFreeTitle(self, underscore=False):
        """DEPRECATED: use self.title(withSection=False) instead."""
        return self.title(underscore=underscore, withSection=False)

    @deprecated("Page.title(asLink=True)")
    def aslink(self, forceInterwiki=False, textlink=False, noInterwiki=False):
        """DEPRECATED: use self.title(asLink=True) instead."""
        return self.title(asLink=True, forceInterwiki=forceInterwiki,
                          allowInterwiki=not noInterwiki, textlink=textlink)

    @deprecated("Page.title(asUrl=True)")
    def urlname(self):
        """Return the Page title encoded for use in an URL.

        DEPRECATED: use self.title(asUrl=True) instead.

        """
        return self.title(asUrl=True)

####### DISABLED METHODS (warnings provided) ######
    # these methods are easily replaced by editing the page's text using
    # textlib methods and then using put() on the result.

    def removeImage(self, image, put=False, summary=None, safe=True):
        """Old method to remove all instances of an image from page."""
        warning("Page.removeImage() is no longer supported.")

    def replaceImage(self, image, replacement=None, put=False, summary=None,
                     safe=True):
        """Old method to replace all instances of an image with another."""
        warning("Page.replaceImage() is no longer supported.")















