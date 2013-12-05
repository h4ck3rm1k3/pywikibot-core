# -*- coding: utf-8  -*-
"""
Objects representing MediaWiki sites (wikis) and families (groups of wikis
on the same topic in different languages).

from pywikibot.site.base import BaseSite
"""
#
# (C) Pywikibot team, 2008-2012
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

#try:
#    from hashlib import md5
#except ImportError:
#    #from md5 import md5
#import httplib2
#import datetime
#import itertools
#import os
import re
#import sys
import threading
import time
import urllib.request, urllib.parse, urllib.error
#import json

import pywikibot
#from pywikibot import deprecate_arg
#from pywikibot import config
#from pywikibot import deprecated
from pywikibot.bot import log
#from pywikibot import pagegenerators
from pywikibot.throttle import Throttle
#from pywikibot.data import api
#import pywikibot.data.api as api
from pywikibot.site.pageinuse import PageInUse

from pywikibot.exceptions import (
    NoSuchSite, 
    Error, 
#    UserBlocked,
#    EditConflict, 
)

from pywikibot.deprecate import deprecated


from pywikibot.familybase import Family
from config import loadconfig

class BaseSite(object):
    """Site methods that are independent of the communication interface."""
    # to implement a specific interface, define a Site class that inherits
    # from this

    def page_isredirect(self, page):
        return False

    def hasExtension(self, string, tf):
        pass

    def pagelinks(self, 
                  page=None, 
                  namespaces=None, 
                  step=None,
                  total=None, 
                  content=None
              ):
        pass


    def loadrevisions(self, *args, **kwargs):
#getText=True, sysop=None):
        pass

    def pagelanglinks(self, step, total):
        pass

    def pagelinks(self):
        pass

    def language (self, code='en'):
        return "en"


    def case(self, code='en'):
        return "first-letter"


    def page_isredirect(self, page):
        pass

    def pagereferences(
            self,
            followRedirects,
            filterRedirects,
            withTemplateInclusion,
            onlyTemplateInclusion,
            namespaces,
            step,
            total,
            content,
        ):
        pass

    def __init__(self, code, fam=None, user=None, sysop=None):
        """
        @param code: the site's language code
        @type code: str
        @param fam: wiki family name (optional)
        @type fam: str or Family
        @param user: bot user name (optional)
        @type user: str
        @param sysop: sysop account user name (optional)
        @type sysop: str

        """
        self._namespaces = {}
        self._logger = "wiki.site"
        self.__code = code.lower()
        if isinstance(fam, str) or fam is None:
            self.__family = Family(fam, fatal=False)
        else:
            self.__family = fam

        # if we got an outdated language code, use the new one instead.
        if self.__code in self.__family.obsolete:
            if self.__family.obsolete[self.__code] is not None:
                self.__code = self.__family.obsolete[self.__code]
            else:
                # no such language anymore
                raise NoSuchSite("Language %s in family %s is obsolete"
                                 % (self.__code, self.__family.name))
        if self.__code not in self.languages():
            if self.__family.name in list(self.__family.langs.keys()) and \
               len(self.__family.langs) == 1:
                oldcode = self.__code
                self.__code = self.__family.name
                if self.__family == pywikibot.config.family \
                        and oldcode == pywikibot.config.mylang:
                    pywikibot.config.mylang = self.__code
            else:
                #log (str(self))
                log (str(self.__family))
                log (str(self.__family.langs))
                message= "Language %s does not exist in family %s"  % (self.__code, self.__family.name)
                log(message)
                raise NoSuchSite(message)

        self.nocapitalize = self.code in self.family.nocapitalize
        if not self.nocapitalize:
            if user:
                user = user[0].upper() + user[1:]
            if sysop:
                sysop = sysop[0].upper() + sysop[1:]
        self._username = [user, sysop]
        self.use_hard_category_redirects = (
            self.code in self.family.use_hard_category_redirects)

        # following are for use with lock_page and unlock_page methods
        self._pagemutex = threading.Lock()
        self._locked_pages = []

    @property
    def throttle(self):
        """Return this Site's throttle.  Initialize a new one if needed."""

        if not hasattr(self, "_throttle"):
            self._throttle = Throttle(self, multiplydelay=True,
                                      verbosedelay=False)
        return self._throttle

    @property
    def family(self):
        """The Family object for this Site's wiki family."""

        return self.__family

    @property
    def code(self):
        """The identifying code for this Site.

        By convention, this is usually an ISO language code, but it does
        not have to be.

        """
        return self.__code

    @property
    def lang(self):
        """The ISO language code for this Site.

        Presumed to be equal to the wiki prefix, but this can be overridden.

        """
        return self.__code

    def __cmp__(self, other):
        """Perform equality and inequality tests on Site objects."""

        if not isinstance(other, BaseSite):
            return 1
        if self.family == other.family:
            return self.__lt__(self.code, other.code)
        return self.__lt__(self.family.name, other.family.name)

    def user(self):
        """Return the currently-logged in bot user, or None."""

        if self.logged_in(True):
            return self._username[True]
        elif self.logged_in(False):
            return self._username[False]

    def username(self, sysop=False):
        return self._username[sysop]

    def __getattr__(self, attr):
        """Calls to methods not defined in this object are passed to Family."""

        if hasattr(self.__class__, attr):
            return getattr(self.__class__, attr)
        try:
            method = getattr(self.family, attr)
            log("Attr %s got Method to call is %s" % (attr, method))
            f = lambda *args, **kwargs: method(self.code, *args, **kwargs)
            if hasattr(method, "__doc__"):
                f.__doc__ = method.__doc__
            return f
        except AttributeError:
            raise AttributeError("%s instance has no attribute '%s'"
                                 % (self.__class__.__name__, attr))

    def sitename(self):
        """Return string representing this Site's name and code."""
        #log(self)
        log(self.family)
        log(self.family.name)
        log(self.code)
        return self.family.name + ':' + self.code

    __str__ = sitename

    def __repr__(self):
        return 'Site("%s", "%s")' % (self.code, self.family.name)

    def __hash__(self):
        return hash(repr(self))

    def linktrail(self):
        """Return regex for trailing chars displayed as part of a link.

        Returns a string, not a compiled regular expression object.

        This reads from the family file, and ''not'' from
        [[MediaWiki:Linktrail]], because the MW software currently uses a
        built-in linktrail from its message files and ignores the wiki
        value.

        """
        return self.family.linktrail(self.code)

    def languages(self):
        """Return list of all valid language codes for this site's Family."""

        return list(self.family.langs.keys())

    def validLanguageLinks(self):
        """Return list of language codes that can be used in interwiki links."""

        nsnames = [name for name in list(self.namespaces().values())]
        return [lang for lang in self.languages()
                if lang[:1].upper() + lang[1:] not in nsnames]

    def ns_index(self, namespace):
        """Given a namespace name, return its int index, or None if invalid."""

        for ns in self.namespaces():
            if namespace.lower() in [name.lower()
                                     for name in self.namespaces()[ns]]:
                return ns

    getNamespaceIndex = ns_index  # for backwards-compatibility

    def namespaces(self):
        """Return dict of valid namespaces on this wiki."""

        return self._namespaces

    def ns_normalize(self, value):
        """Return canonical local form of namespace name.

        @param value: A namespace name
        @type value: unicode

        """
        index = self.ns_index(value)
        return self.namespace(index)

    normalizeNamespace = ns_normalize  # for backwards-compatibility

    def redirect(self, default=True):
        """Return list of localized redirect tags for the site.

        If default is True, falls back to 'REDIRECT' if the site has no
        special redirect tag.

        """
        return ["REDIRECT"]

    def pagenamecodes(self, default=True):
        """Return list of localized PAGENAME tags for the site."""

        return ["PAGENAME"]

    def pagename2codes(self, default=True):
        """Return list of localized PAGENAMEE tags for the site."""

        return ["PAGENAMEE"]

    def lock_page(self, page, block=True):
        """Lock page for writing.  Must be called before writing any page.

        We don't want different threads trying to write to the same page
        at the same time, even to different sections.

        @param page: the page to be locked
        @type page: pywikibot.Page
        @param block: if true, wait until the page is available to be locked;
            otherwise, raise an exception if page can't be locked

        """
        self._pagemutex.acquire()
        try:
            while page in self._locked_pages:
                if not block:
                    raise PageInUse
                time.sleep(.25)
            self._locked_pages.append(page.title(withSection=False))
        finally:
            self._pagemutex.release()

    def unlock_page(self, page):
        """Unlock page.  Call as soon as a write operation has completed.

        @param page: the page to be locked
        @type page: pywikibot.Page

        """
        self._pagemutex.acquire()
        try:
            self._locked_pages.remove(page.title(withSection=False))
        finally:
            self._pagemutex.release()

    def disambcategory(self):
        """Return Category in which disambig pages are listed."""

        try:
            name = '%s:%s' % (self.namespace(14),
                              self.family.disambcatname[self.code])
        except KeyError:
            raise Error("No disambiguation category name found for %(site)s"
                        % {'site': self})
        return pywikibot.Category(pywikibot.Link(name, self))

    @deprecated("pywikibot.Link")
    def linkto(self, title, othersite=None):
        """Return unicode string in the form of a wikilink to 'title'

        Use optional Site argument 'othersite' to generate an interwiki link.

        """
        return pywikibot.Link(title, self).astext(othersite)

    def isInterwikiLink(self, text):
        """Return True if text is in the form of an interwiki link.

        If a link object constructed using "text" as the link text parses as
        belonging to a different site, this method returns True.

        """
        linkfam, linkcode = pywikibot.Link(text, self).parse_site()
        return linkfam != self.family.name or linkcode != self.code

    def redirectRegex(self, pattern=None):
        """Return a compiled regular expression matching on redirect pages.

        Group 1 in the regex match object will be the target title.

        """
        if pattern is None:
            pattern = "REDIRECT"
        # A redirect starts with hash (#), followed by a keyword, then
        # arbitrary stuff, then a wikilink. The wikilink may contain
        # a label, although this is not useful.
        return re.compile(r'\s*#%(pattern)s\s*:?\s*\[\[(.+?)(?:\|.*?)?\]\]'
                          % locals(),
                          re.IGNORECASE | re.UNICODE | re.DOTALL)

    def sametitle(self, title1, title2):
        """Return True iff title1 and title2 identify the same wiki page."""
        # title1 and title2 may be unequal but still identify the same page,
        # if they use different aliases for the same namespace

        def valid_namespace(text, number):
            """Return True if text is a valid alias for namespace with given
            number.

            """
            for alias in self.namespace(number, all=True):
                if text.lower() == alias.lower():
                    return True
            return False

        if title1 == title2:
            return True
        # determine whether titles contain namespace prefixes
        if ":" in title1:
            ns1, name1 = title1.split(":", 1)
        else:
            ns1, name1 = 0, title1
        if ":" in title2:
            ns2, name2 = title2.split(":", 1)
        else:
            ns2, name2 = 0, title2
        for space in self.namespaces():  # iterate over all valid namespaces
            if type(ns1) is not int and valid_namespace(ns1, space):
                ns1 = space
            if type(ns2) is not int and valid_namespace(ns2, space):
                ns2 = space
        if type(ns1) is not int:
            # no valid namespace prefix found, so the string followed by ":"
            # must be part of the title
            name1 = ns1 + ":" + name1
            ns1 = 0
        if type(ns2) is not int:
            name2 = ns2 + ":" + name2
            ns2 = 0
        if ns1 != ns2:
            # pages in different namespaces
            return False
        if self.case() == "first-letter":
            name1 = name1[:1].upper() + name1[1:]
            name2 = name2[:1].upper() + name2[1:]
        return name1 == name2

    # namespace shortcuts for backwards-compatibility

    def special_namespace(self):
        return self.namespace(-1)

    def image_namespace(self):
        return self.namespace(6)

    def mediawiki_namespace(self):
        return self.namespace(8)

    def template_namespace(self):
        return self.namespace(10)

    def category_namespace(self):
        return self.namespace(14)

    def category_namespaces(self):
        return self.namespace(14, all=True)

    # site-specific formatting preferences

    def category_on_one_line(self):
        """Return True if this site wants all category links on one line."""

        return self.code in self.family.category_on_one_line

    def interwiki_putfirst(self):
        """Return list of language codes for ordering of interwiki links."""

        return self.family.interwiki_putfirst.get(self.code, None)

    def interwiki_putfirst_doubled(self, list_of_links):
        # TODO: is this even needed?  No family in the framework has this
        # dictionary defined!
        if self.lang in self.family.interwiki_putfirst_doubled:
            if (len(list_of_links) >=
                    self.family.interwiki_putfirst_doubled[self.lang][0]):
                links2 = [lang.language() for lang in list_of_links]
                result = []
                for lang in self.family.interwiki_putfirst_doubled[self.lang][1]:
                    try:
                        result.append(list_of_links[links2.index(lang)])
                    except ValueError:
                        pass
                return result
            else:
                return False
        else:
            return False

    def getSite(self, code):
        """Return Site object for language 'code' in this Family."""

        return pywikibot.Site(code=code, fam=self.family, user=self.user())

    def nice_get_address(self, title):
        """Return shorter URL path to retrieve page titled 'title'."""

        return self.family.nice_get_address(self.lang, title)

    # deprecated methods for backwards-compatibility

    @deprecated("family attribute")
    def fam(self):
        """Return Family object for this Site."""

        return self.family

    @deprecated("urllib.urlencode()")
    def urlEncode(self, query):
        """DEPRECATED"""
        return urllib.parse.urlencode(query)

    @deprecated("pywikibot.comms.http.request")
    def getUrl(self, path, retry=True, sysop=False, data=None,
               compress=True, no_hostname=False, cookie_only=False):
        """DEPRECATED.

        Retained for compatibility only. All arguments except path and data
        are ignored.

        """
        from pywikibot.comms import http
        if data:
            if not isinstance(data, str):
                data = urllib.parse.urlencode(data)
            return http.request(self, path, method="PUT", body=data)
        else:
            return http.request(self, path)

    @deprecated()
    def postForm(self, address, predata, sysop=False, cookies=None):
        """DEPRECATED"""
        return self.getUrl(address, data=predata)

    @deprecated()
    def postData(self, address, data, contentType=None, sysop=False,
                 compress=True, cookies=None):
        """DEPRECATED"""
        return self.getUrl(address, data=data)

    # unsupported methods from version 1

    def checkCharset(self, charset):
        raise NotImplementedError

    def getToken(self, getalways=True, getagain=False, sysop=False):
        raise NotImplementedError

    def export_address(self):
        raise NotImplementedError

    def move_address(self):
        raise NotImplementedError

    def delete_address(self, s):
        raise NotImplementedError

    def undelete_view_address(self, s, ts=''):
        raise NotImplementedError

    def undelete_address(self):
        raise NotImplementedError

    def protect_address(self, s):
        raise NotImplementedError

    def unprotect_address(self, s):
        raise NotImplementedError

    def put_address(self, s):
        raise NotImplementedError

    def get_address(self, s):
        raise NotImplementedError

    def edit_address(self, s):
        raise NotImplementedError

    def purge_address(self, s):
        raise NotImplementedError

    def block_address(self):
        raise NotImplementedError

    def unblock_address(self):
        raise NotImplementedError

    def blocksearch_address(self, s):
        raise NotImplementedError

    def linksearch_address(self, s, limit=500, offset=0):
        raise NotImplementedError

    def search_address(self, q, n=50, ns=0):
        raise NotImplementedError

    def allpages_address(self, s, ns=0):
        raise NotImplementedError

    def log_address(self, n=50, mode='', user=''):
        raise NotImplementedError

    def newpages_address(self, n=50, namespace=0):
        raise NotImplementedError

    def longpages_address(self, n=500):
        raise NotImplementedError

    def shortpages_address(self, n=500):
        raise NotImplementedError

    def unusedfiles_address(self, n=500):
        raise NotImplementedError

    def categories_address(self, n=500):
        raise NotImplementedError

    def deadendpages_address(self, n=500):
        raise NotImplementedError

    def ancientpages_address(self, n=500):
        raise NotImplementedError

    def lonelypages_address(self, n=500):
        raise NotImplementedError

    def protectedpages_address(self, n=500):
        raise NotImplementedError

    def unwatchedpages_address(self, n=500):
        raise NotImplementedError

    def uncategorizedcategories_address(self, n=500):
        raise NotImplementedError

    def uncategorizedimages_address(self, n=500):
        raise NotImplementedError

    def uncategorizedpages_address(self, n=500):
        raise NotImplementedError

    def uncategorizedtemplates_address(self, n=500):
        raise NotImplementedError

    def unusedcategories_address(self, n=500):
        raise NotImplementedError

    def wantedcategories_address(self, n=500):
        raise NotImplementedError

    def withoutinterwiki_address(self, n=500):
        raise NotImplementedError

    def references_address(self, s):
        raise NotImplementedError

    def allmessages_address(self):
        raise NotImplementedError

    def upload_address(self):
        raise NotImplementedError

    def double_redirects_address(self, default_limit=True):
        raise NotImplementedError

    def broken_redirects_address(self, default_limit=True):
        raise NotImplementedError

    def random_address(self):
        raise NotImplementedError

    def randomredirect_address(self):
        raise NotImplementedError

    def login_address(self):
        raise NotImplementedError

    def captcha_image_address(self, id):
        raise NotImplementedError

    def watchlist_address(self):
        raise NotImplementedError

    def contribs_address(self, target, limit=500, offset=''):
        raise NotImplementedError

    def globalusers_address(self, target='', limit=500, offset='', group=''):
        raise NotImplementedError




