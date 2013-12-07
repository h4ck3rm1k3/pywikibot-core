# -*- coding: utf-8  -*-
"""
from pywikibot.site.apisite import APISite

Objects representing MediaWiki sites (wikis) and families (groups of wikis
on the same topic in different languages).
from pywikibot.site import BaseSite
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
import datetime
import itertools
import os
import re
#import sys
import threading
#import time
#import urllib.request, urllib.parse, urllib.error
#import json
from mustbe import must_be
from pywikibot.site.base import BaseSite
from pywikibot.captcha import Captcha
import pywikibot
#from pywikibot import deprecate_arg
from pywikibot import config
#from pywikibot import deprecated
from pywikibot.bot import log
#from pywikibot import pagegenerators
#from pywikibot.throttle import Throttle
#from pywikibot.data import api
import pywikibot.data.api
from pywikibot.exceptions import  Error, UserBlocked,NoPage,NoUsername,EditConflict, SpamfilterError, LockedPage

from pywikibot.deprecate import deprecated
from pywikibot.deprecate import deprecate_arg
from pywikibot.site.loginstatus import LoginStatus

_logger = "wiki.site"

class APISite(BaseSite):
    """API interface to MediaWiki site.

    Do not use directly; use pywikibot.Site function.

    """
##    Site methods from version 1.0 (as these are implemented in this file,
##    or declared deprecated/obsolete, they will be removed from this list)
##########
##    cookies: return user's cookies as a string
##
##    urlEncode: Encode a query to be sent using an http POST request.
##    postForm: Post form data to an address at this site.
##    postData: Post encoded form data to an http address at this site.
##
##    version: Return MediaWiki version string from Family file.
##    versionnumber: Return int identifying the MediaWiki version.
##    live_version: Return version number read from Special:Version.
##    checkCharset(charset): Warn if charset doesn't match family file.
##
##    linktrail: Return regex for trailing chars displayed as part of a link.
##    disambcategory: Category in which disambiguation pages are listed.
##
##    Methods that yield Page objects derived from a wiki's Special: pages
##    (note, some methods yield other information in a tuple along with the
##    Pages; see method docs for details) --
##

    def __init__(self, code, fam=None, user=None, sysop=None):
        BaseSite.__init__(self, code, fam, user, sysop)
        if self.family.versionnumber(self.code) >= 14:
            self._namespaces[6] = ["File"]
            self._namespaces[7] = ["File talk"]
        self.sitelock = threading.Lock()
        self._msgcache = {}
        self._loginstatus = LoginStatus.NOT_ATTEMPTED
        self._userinfo = None
        

    @staticmethod
    def fromDBName(dbname):
        # TODO this only works for some WMF sites
        req = pywikibot.data.api.CachedRequest(datetime.timedelta(days=10),
                                site=pywikibot.Site('meta', 'meta'),
                                action='sitematrix')
        data = req.submit()
        for num in data['sitematrix']:
            if num in ['specials', 'count']:
                continue
            lang = data['sitematrix'][num]['code']
            for site in data['sitematrix'][num]['site']:
                if site['dbname'] == dbname:
                    if site['code'] == 'wiki':
                        site['code'] = 'wikipedia'
                    return APISite(lang, site['code'])
        raise ValueError("Cannot parse a site out of %s." % dbname)

    def _generator(self, gen_class, type_arg=None, namespaces=None,
                   step=None, total=None, **args):
        """Convenience method that returns an API generator.

        All keyword args not listed below are passed to the generator's
        constructor unchanged.

        @param gen_class: the type of generator to construct (must be
            a subclass of pywikibot.data.api.QueryGenerator)
        @param type_arg: query type argument to be passed to generator's
            constructor unchanged (not all types require this)
        @type type_arg: str
        @param namespaces: if not None, limit the query to namespaces in this
            list
        @type namespaces: int, or list of ints
        @param step: if not None, limit each API call to this many items
        @type step: int
        @param total: if not None, limit the generator to yielding this many
            items in total
        @type total: int

        """
        if type_arg is not None:
            gen = gen_class(type_arg, site=self, **args)
        else:
            gen = gen_class(site=self, **args)
        if namespaces is not None:
            gen.set_namespace(namespaces)
        if step is not None and int(step) > 0:
            gen.set_query_increment(int(step))
        if total is not None and int(total) > 0:
            gen.set_maximum_items(int(total))
        return gen

    def logged_in(self, sysop=False):
        """Return True if logged in with the user specified in user-config.py
       (or the sysop user specified if the sysop parameter is True).

        @param sysop: if True, test if user is logged in as the sysop user
                     instead of the normal user.

        """
        if not hasattr(self, "_userinfo"):
            return False

        if sysop and 'sysop' not in self.userinfo['groups']:
            return False

        if not self.userinfo['name']:
            return False

        if self.userinfo['name'] != self._username[sysop]:
            return False

        return True

    @deprecated("Site.user()")
    def loggedInAs(self, sysop=False):
        """Return the current username if logged in, otherwise return None.

        DEPRECATED (use .user() method instead)

        """
        return self.logged_in(sysop) and self.user()

    def login(self, sysop=False):
        """Log the user in if not already logged in."""
        # check whether a login cookie already exists for this user
        self._loginstatus = LoginStatus.IN_PROGRESS
        if hasattr(self, "_userinfo"):
            del self._userinfo
        self.getuserinfo()
        if self.userinfo['name'] == self._username[sysop] and \
           self.logged_in(sysop):
            return
        loginMan = pywikibot.data.api.LoginManager(site=self, sysop=sysop,
                                    user=self._username[sysop])
        if loginMan.login(retry=True):
            self._username[sysop] = loginMan.username
            if hasattr(self, "_userinfo"):
                del self._userinfo
            self.getuserinfo()
            self._loginstatus = (LoginStatus.AS_SYSOP
                                 if sysop else LoginStatus.AS_USER)
        else:
            self._loginstatus = LoginStatus.NOT_LOGGED_IN  # failure
        if not hasattr(self, "_siteinfo"):
            self._getsiteinfo()

    forceLogin = login  # alias for backward-compatibility

    def logout(self):
        uirequest = pywikibot.data.api.Request(site=self, action="logout")
        #uidata = 
        uirequest.submit()
        self._loginstatus = LoginStatus.NOT_LOGGED_IN
        if hasattr(self, "_userinfo"):
            del self._userinfo
        self.getuserinfo()

    def getuserinfo(self):
        """Retrieve userinfo from site and store in _userinfo attribute.

        self._userinfo will be a dict with the following keys and values:

          - id: user id (numeric str)
          - name: username (if user is logged in)
          - anon: present if user is not logged in
          - groups: list of groups (could be empty)
          - rights: list of rights (could be empty)
          - message: present if user has a new message on talk page
          - blockinfo: present if user is blocked (dict)

        """
        if (not hasattr(self, "_userinfo")
                or (self._userinfo and 
                    "rights" not in self._userinfo)
                or self._userinfo['name']
                   != self._username["sysop" in self._userinfo["groups"]]):
            uirequest = pywikibot.data.api.Request(
                site=self,
                action="query",
                meta="userinfo",
                uiprop="blockinfo|hasmsg|groups|rights"
            )
            uidata = uirequest.submit()
            assert 'query' in uidata, \
                   "API userinfo response lacks 'query' key"
            assert 'userinfo' in uidata['query'], \
                   "API userinfo response lacks 'userinfo' key"
            self._userinfo = uidata['query']['userinfo']
        return self._userinfo

    userinfo = property(fget=getuserinfo, doc=getuserinfo.__doc__)

    def is_blocked(self, sysop=False):
        """Return true if and only if user is blocked.

        @param sysop: If true, log in to sysop account (if available)

        """
        if not self.logged_in(sysop):
            self.login(sysop)
        return 'blockinfo' in self._userinfo

    def isBlocked(self, sysop=False):
        """Deprecated synonym for is_blocked"""
        pywikibot.debug(
            "Site method 'isBlocked' should be changed to 'is_blocked'",
            _logger)
        return self.is_blocked(sysop)

    def checkBlocks(self, sysop=False):
        """Check if the user is blocked, and raise an exception if so."""
        if self.is_blocked(sysop):
            # User blocked
            raise UserBlocked('User is blocked in site %s' % self)

    def has_right(self, right, sysop=False):
        """Return true if and only if the user has a specific right.

        Possible values of 'right' may vary depending on wiki settings,
        but will usually include:

        * Actions: edit, move, delete, protect, upload
        * User levels: autoconfirmed, sysop, bot

        """
        if not self.logged_in(sysop):
            self.login(sysop)
        return right.lower() in self._userinfo['rights']

    @deprecated("Site.has_right()")
    def isAllowed(self, right, sysop=False):
        """Deprecated; retained for backwards-compatibility"""
        return self.has_right(right, sysop)

    def has_group(self, group, sysop=False):
        """Return true if and only if the user is a member of specified group.

        Possible values of 'group' may vary depending on wiki settings,
        but will usually include bot.

        """
        if not self.logged_in(sysop):
            self.login(sysop)
        return group.lower() in self._userinfo['groups']

    def messages(self, sysop=False):
        """Returns true if the user has new messages, and false otherwise."""
        if not self.logged_in(sysop):
            self.login(sysop)
        return 'hasmsg' in self._userinfo

    def mediawiki_message(self, key):
        """Return the MediaWiki message text for key "key" """
        if not key in self._msgcache:
            msg_query = pywikibot.data.api.QueryGenerator(site=self, meta="allmessages",
                                           ammessages=key)
            for msg in msg_query:
                if msg['name'] == key and not 'missing' in msg:
                    self._msgcache[key] = msg['*']
                    break
            else:
                raise KeyError("Site %(self)s has no message '%(key)s'"
                               % locals())
        return self._msgcache[key]

    def has_mediawiki_message(self, key):
        """Return True iff this site defines a MediaWiki message for 'key'."""
        try:
            #v = 
            self.mediawiki_message(key)
            return True
        except KeyError:
            return False

    def getcurrenttimestamp(self):
        """Return server time, {{CURRENTTIMESTAMP}}, as a string.

        Format is 'yyyymmddhhmmss'

        """
        r = pywikibot.data.api.Request(site=self,
                        action="parse",
                        text="{{CURRENTTIMESTAMP}}")
        result = r.submit()
        return re.search('\d+', result['parse']['text']['*']).group()

    def getcurrenttime(self):
        """Return a Timestamp object representing the current server time."""
        ts = self.getcurrenttimestamp()
        return pywikibot.Timestamp.fromtimestampformat(ts)

    def getmagicwords(self, word):
        """Return list of localized "word" magic words for the site."""
        if not hasattr(self, "_magicwords"):
            sirequest = pywikibot.data.api.CachedRequest(
                expiry=config.API_config_expiry,
                site=self,
                action="query",
                meta="siteinfo",
                siprop="magicwords"
            )
            try:
                sidata = sirequest.submit()
                assert 'query' in sidata, \
                       "API siteinfo response lacks 'query' key"
                sidata = sidata['query']
                assert 'magicwords' in sidata, \
                       "API siteinfo response lacks 'magicwords' key"
                self._magicwords = dict((item["name"], item["aliases"])
                                        for item in sidata["magicwords"])

            except pywikibot.data.api.APIError:
                # hack for older sites that don't support 1.13 properties
                # probably should delete if we're not going to support pre-1.13
                self._magicwords = {}

        if word in self._magicwords:
            return self._magicwords[word]
        else:
            return [word]

    def redirect(self, default=True):
        """Return the preferred localized #REDIRECT keyword.

        Argument is ignored (but maintained for backwards-compatibility).

        """
        # return the magic word without the preceding '#' character
        return self.getmagicwords("redirect")[0].lstrip("#")

    def redirectRegex(self):
        """Return a compiled regular expression matching on redirect pages.

        Group 1 in the regex match object will be the target title.

        """
        #NOTE: this is needed, since the API can give false positives!
        try:
            keywords = set(s.lstrip("#")
                           for s in self.getmagicwords("redirect"))
            keywords.add("REDIRECT")  # just in case
            pattern = "(?:" + "|".join(keywords) + ")"
        except KeyError:
            # no localized keyword for redirects
            pattern = None
        return BaseSite.redirectRegex(self, pattern)

    def pagenamecodes(self, default=True):
        """Return list of localized PAGENAME tags for the site."""
        return self.getmagicwords("pagename")

    def pagename2codes(self, default=True):
        """Return list of localized PAGENAMEE tags for the site."""
        return self.getmagicwords("pagenamee")

    def _getsiteinfo(self, force=False):
        """Retrieve siteinfo and namespaces from site."""

        print("get site info called")

        sirequest = pywikibot.data.api.CachedRequest(
            expiry=(0 if force else config.API_config_expiry),
            site=self,
            action="query",
            meta="siteinfo",
            siprop="general|namespaces|namespacealiases|extensions"
        )
        print ("after create request")
        try:
            print ("going to make request")
            sidata = sirequest.submit()
        except pywikibot.data.api.APIError as e:
            print ("error")
            print(e)
            # hack for older sites that don't support 1.12 properties
            # probably should delete if we're not going to support pre-1.12
            sirequest = pywikibot.data.api.Request(
                site=self,
                action="query",
                meta="siteinfo",
                siprop="general|namespaces"
            )
            sidata = sirequest.submit()

        assert 'query' in sidata, \
               "API siteinfo response lacks 'query' key"
        sidata = sidata['query']
        assert 'general' in sidata, \
               "API siteinfo response lacks 'general' key"
        assert 'namespaces' in sidata, \
               "API siteinfo response lacks 'namespaces' key"
        print(sidata)
        self._siteinfo = sidata['general']
        nsdata = sidata['namespaces']
        for nskey in nsdata:
            ns = int(nskey)
            if ns in self._namespaces:
                if nsdata[nskey]["*"] in self._namespaces[ns]:
                    continue
                # this is the preferred form so it goes at front of list
                self._namespaces[ns].insert(0, nsdata[nskey]["*"])
            else:
                self._namespaces[ns] = [nsdata[nskey]["*"]]
        if 'namespacealiases' in sidata:
            aliasdata = sidata['namespacealiases']
            for item in aliasdata:
                if item["*"] in self._namespaces[int(item['id'])]:
                    continue
                # this is a less preferred form so it goes at the end
                self._namespaces[int(item['id'])].append(item["*"])
        if 'extensions' in sidata:
            self._extensions = sidata['extensions']
        else:
            self._extensions = None

    def hasExtension(self, name, unknown=NotImplementedError):
        """ Determine whether extension `name` is loaded.

            @param name The extension to check for
            @param unknown The value to return if the site does not list loaded
                           extensions. Valid values are an exception to raise,
                           True or False. Default: NotImplementedError
        """
        if not hasattr(self, '_extensions'):
            self._getsiteinfo()
        if self._extensions is None:
            if isinstance(unknown, type) and issubclass(unknown, Exception):
                raise unknown(
                    "Feature 'hasExtension' only available in MW 1.14+")
            else:
                return unknown
        for ext in self._extensions:
            if ext['name'].lower() == name.lower():
                return True
        return False

    @property
    def siteinfo(self):
        """Site information dict."""
        print("siteinfo called")
        if not hasattr(self, "_siteinfo"):
            print("_siteinfo missing")
            self._getsiteinfo()
        return self._siteinfo

    def case(self):
        """Return this site's capitalization rule."""

        return self.siteinfo['case']

    def dbName(self):
        """Return this site's internal id."""

        return self.siteinfo['wikiid']

    def language(self):
        """Return the code for the language of this Site."""

        return self.siteinfo['lang']

    lang = property(fget=language, doc=language.__doc__)

    @property
    def has_image_repository(self):
        """Return True if site has a shared image repository like commons"""
        code, fam = self.shared_image_repository()
        return bool(code or fam)

    @property
    def has_data_repository(self):
        """Return True if site has a shared image repository like wikidata"""
        code, fam = self.shared_data_repository()
        return bool(code or fam)

    @property
    def has_transcluded_data(self):
        """Return True if site has a shared image repository like wikidata"""
        code, fam = self.shared_data_repository(True)
        return bool(code or fam)

    def image_repository(self):
        """Return Site object for image repository e.g. commons."""

        code, fam = self.shared_image_repository()
        if bool(code or fam):
            return pywikibot.Site(code, fam, self.username())

    def data_repository(self):
        """Return Site object for data repository e.g. wikidata."""

        code, fam = self.shared_data_repository()
        if bool(code or fam):
            return pywikibot.Site(code, fam, self.username(),
                                  interface="DataSite")

    def is_image_repository(self):
        """Return True if Site object is the image repository."""
        return self is self.image_repository()

    def is_data_repository(self):
        """Return True if Site object is the data repository."""
        return self is self.data_repository()

    def nice_get_address(self, title):
        """Return shorter URL path to retrieve page titled 'title'."""
        # 'title' is expected to be URL-encoded already
        return self.siteinfo["articlepath"].replace("$1", title)

    def namespaces(self):
        """Return dict of valid namespaces on this wiki."""

        if not hasattr(self, "_siteinfo"):
            self._getsiteinfo()
        return self._namespaces

    def namespace(self, num, all=False):
        """Return string containing local name of namespace 'num'.

        If optional argument 'all' is true, return a list of all recognized
        values for this namespace.

        """
        if all:
            return self.namespaces()[num]
        return self.namespaces()[num][0]

    def live_version(self, force=False):
        """Return the 'real' version number found on [[Special:Version]]

        Return value is a tuple (int, int, str) of the major and minor
        version numbers and any other text contained in the version.

        """
        if force:
            self._getsiteinfo(force=True)    # drop/expire cache and reload
        versionstring = self.siteinfo['generator']
        m = re.match(r"^MediaWiki ([0-9]+)\.([0-9]+)(.*)$", versionstring)
        if m:
            return (int(m.group(1)), int(m.group(2)), m.group(3))

    def loadpageinfo(self, page):
        """Load page info from api and save in page attributes"""
        title = page.title(withSection=False)
        query = self._generator(pywikibot.data.api.PropertyGenerator,
                                type_arg="info",
                                titles=title.encode(self.encoding()),
                                inprop="protection")
        for pageitem in query:
            if not self.sametitle(pageitem['title'], title):
                pywikibot.warning(
                    "loadpageinfo: Query on %s returned data on '%s'"
                    % (page, pageitem['title']))
                continue
            pywikibot.data.api.update_page(page, pageitem)

    def loadcoordinfo(self, page):
        """Load [[mw:Extension:GeoData]] info"""
        # prop=coordinates&titles=Wikimedia Foundation&format=jsonfm&coprop=type|name|dim|country|region&coprimary=all
        title = page.title(withSection=False)
        query = self._generator(pywikibot.data.api.PropertyGenerator,
                                type_arg="coordinates",
                                titles=title.encode(self.encoding()),
                                coprop=['type', 'name', 'dim',
                                        'country', 'region',
                                        'globe'],
                                coprimary='all')
        for pageitem in query:
            if not self.sametitle(pageitem['title'], title):
                pywikibot.warning(
                    "loadcoordinfo: Query on %s returned data on '%s'"
                    % (page, pageitem['title']))
                continue
            pywikibot.data.api.update_page(page, pageitem)

    def loadpageprops(self, page):
        title = page.title(withSection=False)
        query = self._generator(pywikibot.data.api.PropertyGenerator,
                                type_arg="pageprops",
                                titles=title.encode(self.encoding()),
                                )
        for pageitem in query:
            if not self.sametitle(pageitem['title'], title):
                pywikibot.warning(
                    "loadpageprops: Query on %s returned data on '%s'"
                    % (page, pageitem['title']))
                continue
            pywikibot.data.api.update_page(page, pageitem)

    def loadimageinfo(self, page, history=False):
        """Load image info from api and save in page attributes

        @param history: if true, return the image's version history

        """
        title = page.title(withSection=False)
        args = {"titles": title}
        if not history:
            args["total"] = 1
        query = self._generator(pywikibot.data.api.PropertyGenerator,
                                type_arg="imageinfo",
                                iiprop=["timestamp", "user", "comment",
                                        "url", "size", "sha1", "mime",
                                        "metadata", "archivename"],
                                **args)
        for pageitem in query:
            if not self.sametitle(pageitem['title'], title):
                raise Error(
                    "loadimageinfo: Query on %s returned data on '%s'"
                    % (page, pageitem['title']))
            pywikibot.data.api.update_page(page, pageitem)
            return (pageitem['imageinfo']
                    if history else pageitem['imageinfo'][0])

    def page_exists(self, page):
        """Return True if and only if page is an existing page on site."""
        if not hasattr(page, "_pageid"):
            self.loadpageinfo(page)
        return page._pageid > 0

    def page_restrictions(self, page):
        """Returns a dictionary reflecting page protections"""
        if not self.page_exists(page):
            raise NoPage(page)
        if not hasattr(page, "_protection"):
            self.loadpageinfo(page)
        return page._protection

    def page_can_be_edited(self, page):
        """
        Returns True if and only if:
          - page is unprotected, and bot has an account for this site, or
          - page is protected, and bot has a sysop account for this site.

        """
        rest = self.page_restrictions(page)
        sysop_protected = "edit" in rest and rest['edit'][0] == 'sysop'
        try:
            pywikibot.data.api.LoginManager(site=self, sysop=sysop_protected)
        except NoUsername:
            return False
        return True

    def page_isredirect(self, page):
        """Return True if and only if page is a redirect."""
        if not hasattr(page, "_isredir"):
            self.loadpageinfo(page)
        return page._isredir

    def getredirtarget(self, page):
        """Return Page object for the redirect target of page."""
        if not self.page_isredirect(page):
            raise pywikibot.IsNotRedirectPage(page)
        if hasattr(page, '_redirtarget'):
            return page._redirtarget
        title = page.title(withSection=False)
        query = pywikibot.data.api.Request(site=self, action="query", prop="info",
                            inprop="protection|talkid|subjectid",
                            titles=title.encode(self.encoding()),
                            redirects="")
        result = query.submit()
        if "query" not in result or "redirects" not in result["query"]:
            raise RuntimeError(
                "getredirtarget: No 'redirects' found for page %s."
                % title)
        redirmap = dict((item['from'], item['to'])
                        for item in result['query']['redirects'])
        if title not in redirmap:
            raise RuntimeError(
                "getredirtarget: 'redirects' contains no key for page %s."
                % title)
        target_title = redirmap[title]
        if target_title == title or "pages" not in result['query']:
            # no "pages" element indicates a circular redirect
            raise pywikibot.CircularRedirect(redirmap[title])
        pagedata = list(result['query']['pages'].values())[0]
            # there should be only one value in 'pages', and it is the target
        if self.sametitle(pagedata['title'], target_title):
            target = pywikibot.Page(self, pagedata['title'], pagedata['ns'])
            pywikibot.data.api.update_page(target, pagedata)
            page._redirtarget = target
        else:
            # double redirect; target is an intermediate redirect
            target = pywikibot.Page(self, target_title)
            page._redirtarget = target
        return page._redirtarget

    def preloadpages(self, pagelist, groupsize=50, templates=False,
                     langlinks=False):
        """Return a generator to a list of preloaded pages.

        Note that [at least in current implementation] pages may be iterated
        in a different order than in the underlying pagelist.

        @param pagelist: an iterable that returns Page objects
        @param groupsize: how many Pages to query at a time
        @type groupsize: int
        @param templates: preload list of templates in the pages
        @param langlinks: preload list of language links found in the pages

        """
        from pywikibot.tools import itergroup
        for sublist in itergroup(pagelist, groupsize):
            pageids = [str(p._pageid) for p in sublist
                       if hasattr(p, "_pageid") and p._pageid > 0]
            cache = dict((p.title(withSection=False), p) for p in sublist)

            props = "revisions|info|categoryinfo"
            if templates:
                props += '|templates'
            if langlinks:
                props += '|langlinks'
            rvgen = pywikibot.data.api.PropertyGenerator(props, site=self)
            rvgen.set_maximum_items(-1)  # suppress use of "rvlimit" parameter
            if len(pageids) == len(sublist):
                # only use pageids if all pages have them
                rvgen.request["pageids"] = "|".join(pageids)
            else:
                rvgen.request["titles"] = "|".join(list(cache.keys()))
            rvgen.request["rvprop"] = "ids|flags|timestamp|user|comment|content"
            pywikibot.output("Retrieving %s pages from %s."
                             % (len(cache), self))
            for pagedata in rvgen:
                pywikibot.debug("Preloading %s" % pagedata, _logger)
                try:
                    if pagedata['title'] not in cache:
#                       API always returns a "normalized" title which is
#                       usually the same as the canonical form returned by
#                       page.title(), but sometimes not (e.g.,
#                       gender-specific localizations of "User" namespace).
#                       This checks to see if there is a normalized title in
#                       the response that corresponds to the canonical form
#                       used in the query.
                        for key in cache:
                            if self.sametitle(key, pagedata['title']):
                                cache[pagedata['title']] = cache[key]
                                break
                        else:
                            pywikibot.warning(
                                "preloadpages: Query returned unexpected title"
                                "'%s'" % pagedata['title'])
                            continue
                except KeyError:
                    pywikibot.debug("No 'title' in %s" % pagedata, _logger)
                    pywikibot.debug("pageids=%s" % pageids, _logger)
                    pywikibot.debug("titles=%s" % list(cache.keys()), _logger)
                    continue
                page = cache[pagedata['title']]
                pywikibot.data.api.update_page(page, pagedata)
                yield page

    def token(self, page, tokentype):
        """Return token retrieved from wiki to allow changing page content.

        @param page: the Page for which a token should be retrieved
        @param tokentype: the type of token (e.g., "edit", "move", "delete");
            see API documentation for full list of types

        """
        query = pywikibot.data.api.PropertyGenerator("info",
                                      titles=page.title(withSection=False),
                                      intoken=tokentype,
                                      site=self)
        for item in query:
            if not self.sametitle(item['title'], page.title(withSection=False)):
                raise Error(
                    "token: Query on page %s returned data on page [[%s]]"
                    % (page.title(withSection=False, asLink=True),
                        item['title']))
            pywikibot.data.api.update_page(page, item)
            pywikibot.debug(str(item), _logger)
            return item[tokentype + "token"]

    # following group of methods map more-or-less directly to API queries

    def pagebacklinks(self, page, followRedirects=False, filterRedirects=None,
                      namespaces=None, step=None, total=None, content=False):
        """Iterate all pages that link to the given page.

        @param page: The Page to get links to.
        @param followRedirects: Also return links to redirects pointing to
            the given page.
        @param filterRedirects: If True, only return redirects to the given
            page. If False, only return non-redirect links. If None, return
            both (no filtering).
        @param namespaces: If present, only return links from the namespaces
            in this list.
        @param step: Limit on number of pages to retrieve per API query.
        @param total: Maximum number of pages to retrieve in total.
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        bltitle = page.title(withSection=False).encode(self.encoding())
        blargs = {"gbltitle": bltitle}
        if filterRedirects is not None:
            blargs["gblfilterredir"] = (filterRedirects and "redirects" or
                                        "nonredirects")
        blgen = self._generator(api.PageGenerator, type_arg="backlinks",
                                namespaces=namespaces, step=step, total=total,
                                g_content=content, **blargs)
        if followRedirects:
            # bug: see http://bugzilla.wikimedia.org/show_bug.cgi?id=7304
            # links identified by MediaWiki as redirects may not really be,
            # so we have to check each "redirect" page and see if it
            # really redirects to this page
            redirgen = self._generator(api.PageGenerator,
                                       type_arg="backlinks",
                                       gbltitle=bltitle,
                                       gblfilterredir="redirects")
            genlist = {None: blgen}
            for redir in redirgen:
                if redir == page:
                    # if a wiki contains pages whose titles contain
                    # namespace aliases that existed before those aliases
                    # were defined (example: [[WP:Sandbox]] existed as a
                    # redirect to [[Wikipedia:Sandbox]] before the WP: alias
                    # was created) they can be returned as redirects to
                    # themselves; skip these
                    continue
                if redir.getRedirectTarget() == page:
                    genlist[redir.title()] = self.pagebacklinks(
                        redir, followRedirects=True,
                        filterRedirects=filterRedirects,
                        namespaces=namespaces,
                        content=content
                    )
            return itertools.chain(*list(genlist.values()))
        return blgen

    def page_embeddedin(self, page, filterRedirects=None, namespaces=None,
                        step=None, total=None, content=False):
        """Iterate all pages that embedded the given page as a template.

        @param page: The Page to get inclusions for.
        @param filterRedirects: If True, only return redirects that embed
            the given page. If False, only return non-redirect links. If
            None, return both (no filtering).
        @param namespaces: If present, only return links from the namespaces
            in this list.
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        eiargs = {"geititle":
                  page.title(withSection=False).encode(self.encoding())}
        if filterRedirects is not None:
            eiargs["geifilterredir"] = (filterRedirects and "redirects" or
                                        "nonredirects")
        eigen = self._generator(api.PageGenerator, type_arg="embeddedin",
                                namespaces=namespaces, step=step, total=total,
                                g_content=content, **eiargs)
        return eigen

    def pagereferences(self, page, followRedirects=False, filterRedirects=None,
                       withTemplateInclusion=True, onlyTemplateInclusion=False,
                       namespaces=None, step=None, total=None, content=False):
        """Convenience method combining pagebacklinks and page_embeddedin."""

        if onlyTemplateInclusion:
            return self.page_embeddedin(page, namespaces=namespaces,
                                        filterRedirects=filterRedirects,
                                        step=step, total=total, content=content)
        if not withTemplateInclusion:
            return self.pagebacklinks(page, followRedirects=followRedirects,
                                      filterRedirects=filterRedirects,
                                      namespaces=namespaces,
                                      step=step, total=total, content=content)
        return itertools.islice(
            itertools.chain(
                self.pagebacklinks(
                    page, followRedirects, filterRedirects,
                    namespaces=namespaces, step=step, content=content),
                self.page_embeddedin(
                    page, filterRedirects, namespaces=namespaces,
                    step=step, content=content)
            ), total)

    def pagelinks(self, page, namespaces=None, follow_redirects=False,
                  step=None, total=None, content=False):
        """Iterate internal wikilinks contained (or transcluded) on page.

        @param namespaces: Only iterate pages in these namespaces (default: all)
        @type namespaces: list of ints
        @param follow_redirects: if True, yields the target of any redirects,
            rather than the redirect page
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        plargs = {}
        if hasattr(page, "_pageid"):
            plargs['pageids'] = str(page._pageid)
        else:
            pltitle = page.title(withSection=False).encode(self.encoding())
            plargs['titles'] = pltitle
        if follow_redirects:
            plargs['redirects'] = ''
        plgen = self._generator(api.PageGenerator, type_arg="links",
                                namespaces=namespaces, step=step, total=total,
                                g_content=content, **plargs)
        return plgen

    @deprecate_arg("withSortKey", None)  # Sortkey doesn't work with generator
    def pagecategories(self, page, step=None, total=None, content=False):
        """Iterate categories to which page belongs.

        @param content: if True, load the current content of each iterated page
            (default False); note that this means the contents of the
            category description page, not the pages contained in the category

        """
        clargs = {}
        if hasattr(page, "_pageid"):
            clargs['pageids'] = str(page._pageid)
        else:
            clargs['titles'] = page.title(
                withSection=False).encode(self.encoding())
        clgen = self._generator(api.CategoryPageGenerator,
                                type_arg="categories", step=step, total=total,
                                g_content=content, **clargs)
        return clgen

    def pageimages(self, page, step=None, total=None, content=False):
        """Iterate images used (not just linked) on the page.

        @param content: if True, load the current content of each iterated page
            (default False); note that this means the content of the image
            description page, not the image itself

        """
        imtitle = page.title(withSection=False).encode(self.encoding())
        imgen = self._generator(api.ImagePageGenerator, type_arg="images",
                                titles=imtitle, step=step, total=total,
                                g_content=content)
        return imgen

    def pagetemplates(self, page, namespaces=None, step=None, total=None,
                      content=False):
        """Iterate templates transcluded (not just linked) on the page.

        @param content: if True, load the current content of each iterated page
            (default False)

        """
        tltitle = page.title(withSection=False).encode(self.encoding())
        tlgen = self._generator(api.PageGenerator, type_arg="templates",
                                titles=tltitle, namespaces=namespaces,
                                step=step, total=total, g_content=content)
        return tlgen

    def categorymembers(self, category, namespaces=None, sortby="",
                        reverse=False, starttime=None, endtime=None,
                        startsort=None, endsort=None, step=None, total=None,
                        content=False, recurse=False):
        """Iterate members of specified category.
        FIXME: Properly implement recursion, see:
        https://sourceforge.net/tracker/?func=detail&atid=603138&aid=3611098&group_id=93107

        @param category: The Category to iterate.
        @param namespaces: If present, only return category members from
            these namespaces. For example, use namespaces=[14] to yield
            subcategories, use namespaces=[6] to yield image files, etc. Note,
            however, that the iterated values are always Page objects, even
            if in the Category or Image namespace.
        @type namespaces: list of ints
        @param sortby: determines the order in which results are generated,
            valid values are "sortkey" (default, results ordered by category
            sort key) or "timestamp" (results ordered by time page was
            added to the category)
        @type sortby: str
        @param reverse: if True, generate results in reverse order
            (default False)
        @param starttime: if provided, only generate pages added after this
            time; not valid unless sortby="timestamp"
        @type starttime: pywikibot.Timestamp
        @param endtime: if provided, only generate pages added before this
            time; not valid unless sortby="timestamp"
        @type endtime: pywikibot.Timestamp
        @param startsort: if provided, only generate pages >= this title
            lexically; not valid if sortby="timestamp"
        @type startsort: str
        @param endsort: if provided, only generate pages <= this title
            lexically; not valid if sortby="timestamp"
        @type endsort: str
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        if category.namespace() != 14:
            raise Error(
                "categorymembers: non-Category page '%s' specified"
                % category.title())
        cmtitle = category.title(withSection=False).encode(self.encoding())
        cmargs = dict(type_arg="categorymembers",
                      gcmtitle=cmtitle,
                      gcmprop="ids|title|sortkey")
        if sortby in ["sortkey", "timestamp"]:
            cmargs["gcmsort"] = sortby
        elif sortby:
            raise ValueError(
                "categorymembers: invalid sortby value '%(sortby)s'"
                % locals())
        if starttime and endtime and starttime > endtime:
            raise ValueError(
                "categorymembers: starttime must be before endtime")
        if startsort and endsort and startsort > endsort:
            raise ValueError(
                "categorymembers: startsort must be less than endsort")
        if reverse:
            cmargs["gcmdir"] = "desc"
            # API wants start/end params in opposite order if using descending
            # sort; we take care of this reversal for the user
            (starttime, endtime) = (endtime, starttime)
            (startsort, endsort) = (endsort, startsort)
        if starttime and sortby == "timestamp":
            cmargs["gcmstart"] = str(starttime)
        elif starttime:
            raise ValueError("categorymembers: "
                             "invalid combination of 'sortby' and 'starttime'")
        if endtime and sortby == "timestamp":
            cmargs["gcmend"] = str(endtime)
        elif endtime:
            raise ValueError("categorymembers: "
                             "invalid combination of 'sortby' and 'endtime'")
        if startsort and sortby != "timestamp":
            cmargs["gcmstartsortkey"] = startsort
        elif startsort:
            raise ValueError("categorymembers: "
                             "invalid combination of 'sortby' and 'startsort'")
        if endsort and sortby != "timestamp":
            cmargs["gcmendsortkey"] = endsort
        elif endsort:
            raise ValueError("categorymembers: "
                             "invalid combination of 'sortby' and 'endsort'")

        cmgen = self._generator(api.PageGenerator, namespaces=namespaces,
                                step=step, total=total, g_content=content,
                                **cmargs)
        return cmgen

    def loadrevisions(self, page=None, getText=False, revids=None,
                      startid=None, endid=None, starttime=None,
                      endtime=None, rvdir=None, user=None, excludeuser=None,
                      section=None, sysop=False, step=None, total=None):
        """Retrieve and store revision information.

        By default, retrieves the last (current) revision of the page,
        I{unless} any of the optional parameters revids, startid, endid,
        starttime, endtime, rvdir, user, excludeuser, or limit are
        specified. Unless noted below, all parameters not specified
        default to False.

        If rvdir is False or not specified, startid must be greater than
        endid if both are specified; likewise, starttime must be greater
        than endtime. If rvdir is True, these relationships are reversed.

        @param page: retrieve revisions of this Page (required unless ids
            is specified)
        @param getText: if True, retrieve the wiki-text of each revision;
            otherwise, only retrieve the revision metadata (default)
        @param section: if specified, retrieve only this section of the text
            (getText must be True); section must be given by number (top of
            the article is section 0), not name
        @type section: int
        @param revids: retrieve only the specified revision ids (required
            unless page is specified)
        @type revids: list of ints
        @param startid: retrieve revisions starting with this revid
        @param endid: stop upon retrieving this revid
        @param starttime: retrieve revisions starting at this Timestamp
        @param endtime: stop upon reaching this Timestamp
        @param rvdir: if false, retrieve newest revisions first (default);
            if true, retrieve earliest first
        @param user: retrieve only revisions authored by this user
        @param excludeuser: retrieve all revisions not authored by this user
        @param sysop: if True, switch to sysop account (if available) to
            retrieve this page

        """
        latest = (revids is None and
                  startid is None and
                  endid is None and
                  starttime is None and
                  endtime is None and
                  rvdir is None and
                  user is None and
                  excludeuser is None and
                  step is None and
                  total is None)  # if True, retrieving current revision

        # check for invalid argument combinations
        if page is None and revids is None:
            raise ValueError(
                "loadrevisions:  either page or revids argument required")
        if (startid is not None or endid is not None) and \
                (starttime is not None or endtime is not None):
            raise ValueError(
                "loadrevisions: startid/endid combined with starttime/endtime")
        if starttime is not None and endtime is not None:
            if rvdir and starttime >= endtime:
                raise ValueError(
                    "loadrevisions: starttime > endtime with rvdir=True")
            if (not rvdir) and endtime >= starttime:
                raise ValueError(
                    "loadrevisions: endtime > starttime with rvdir=False")
        if startid is not None and endid is not None:
            if rvdir and startid >= endid:
                raise ValueError(
                    "loadrevisions: startid > endid with rvdir=True")
            if (not rvdir) and endid >= startid:
                raise ValueError(
                    "loadrevisions: endid > startid with rvdir=False")

        # assemble API request
        if revids is None:
            rvtitle = page.title(withSection=False).encode(self.encoding())
            rvgen = self._generator(api.PropertyGenerator,
                                    type_arg="info|revisions",
                                    titles=rvtitle, step=step, total=total)
        else:
            if isinstance(revids, (int, str)):
                ids = str(revids)
            else:
                ids = "|".join(str(r) for r in revids)
            rvgen = self._generator(api.PropertyGenerator,
                                    type_arg="info|revisions", revids=ids,
                                    step=step, total=total)
        if getText:
            rvgen.request["rvprop"] = "ids|flags|timestamp|user|comment|content"
            if section is not None:
                rvgen.request["rvsection"] = str(section)
        if latest or "revids" in rvgen.request:
            rvgen.set_maximum_items(-1)  # suppress use of rvlimit parameter
        if rvdir:
            rvgen.request["rvdir"] = "newer"
        elif rvdir is not None:
            rvgen.request["rvdir"] = "older"
        if startid:
            rvgen.request["rvstartid"] = startid
        if endid:
            rvgen.request["rvendid"] = endid
        if starttime:
            rvgen.request["rvstart"] = str(starttime)
        if endtime:
            rvgen.request["rvend"] = str(endtime)
        if user:
            rvgen.request["rvuser"] = user
        elif excludeuser:
            rvgen.request["rvexcludeuser"] = excludeuser
        # TODO if sysop: something
        rvgen.continuekey = "revisions"
        for pagedata in rvgen:
            if page is not None:
                if not self.sametitle(pagedata['title'],
                                      page.title(withSection=False)):
                    raise Error(
                        "loadrevisions: Query on %s returned data on '%s'"
                        % (page, pagedata['title']))
                if "missing" in pagedata:
                    raise NoPage(page)
            else:
                page = pywikibot.Page(self, pagedata['title'])
            pywikibot.data.api.update_page(page, pagedata)
            break

    def pageinterwiki(self, page):
        # No such function in the API (this method isn't called anywhere)
        raise NotImplementedError

    def pagelanglinks(self, page, step=None, total=None):
        """Iterate all interlanguage links on page, yielding Link objects."""
        lltitle = page.title(withSection=False)
        llquery = self._generator(api.PropertyGenerator,
                                  type_arg="langlinks",
                                  titles=lltitle.encode(self.encoding()),
                                  step=step, total=total)
        for pageitem in llquery:
            if not self.sametitle(pageitem['title'], lltitle):
                raise Error(
                    "getlanglinks: Query on %s returned data on '%s'"
                    % (page, pageitem['title']))
            if 'langlinks' not in pageitem:
                continue
            for linkdata in pageitem['langlinks']:
                yield pywikibot.Link.langlinkUnsafe(linkdata['lang'],
                                                    linkdata['*'],
                                                    source=self)

    def page_extlinks(self, page, step=None, total=None):
        """Iterate all external links on page, yielding URL strings."""
        eltitle = page.title(withSection=False)
        elquery = self._generator(api.PropertyGenerator, type_arg="extlinks",
                                  titles=eltitle.encode(self.encoding()),
                                  step=step, total=total)
        for pageitem in elquery:
            if not self.sametitle(pageitem['title'], eltitle):
                raise RuntimeError(
                    "getlanglinks: Query on %s returned data on '%s'"
                    % (page, pageitem['title']))
            if 'extlinks' not in pageitem:
                continue
            for linkdata in pageitem['extlinks']:
                yield linkdata['*']

    def getcategoryinfo(self, category):
        """Retrieve data on contents of category."""
        cititle = category.title(withSection=False)
        ciquery = self._generator(api.PropertyGenerator,
                                  type_arg="categoryinfo",
                                  titles=cititle.encode(self.encoding()))
        for pageitem in ciquery:
            if not self.sametitle(pageitem['title'], cititle):
                raise Error(
                    "categoryinfo: Query on %s returned data on '%s'"
                    % (category, pageitem['title']))
            pywikibot.data.api.update_page(category, pageitem)

    def categoryinfo(self, category):
        if not hasattr(category, "_catinfo"):
            self.getcategoryinfo(category)
        if not hasattr(category, "_catinfo"):
            # a category that exists but has no contents returns no API result
            category._catinfo = {'size': 0, 'pages': 0, 'files': 0,
                                 'subcats': 0}
        return category._catinfo

    @deprecate_arg("throttle", None)
    @deprecate_arg("limit", "total")
    @deprecate_arg("includeredirects", "filterredir")
    def allpages(self, start="!", prefix="", namespace=0, filterredir=None,
                 filterlanglinks=None, minsize=None, maxsize=None,
                 protect_type=None, protect_level=None, reverse=False,
                 includeredirects=None, step=None, total=None, content=False):
        """Iterate pages in a single namespace.

        Note: parameters includeRedirects and throttle are deprecated and
        included only for backwards compatibility.

        @param start: Start at this title (page need not exist).
        @param prefix: Only yield pages starting with this string.
        @param namespace: Iterate pages from this (single) namespace
           (default: 0)
        @param filterredir: if True, only yield redirects; if False (and not
            None), only yield non-redirects (default: yield both)
        @param filterlanglinks: if True, only yield pages with language links;
            if False (and not None), only yield pages without language links
            (default: yield both)
        @param minsize: if present, only yield pages at least this many
            bytes in size
        @param maxsize: if present, only yield pages at most this many bytes
            in size
        @param protect_type: only yield pages that have a protection of the
            specified type
        @type protect_type: str
        @param protect_level: only yield pages that have protection at this
            level; can only be used if protect_type is specified
        @param reverse: if True, iterate in reverse Unicode lexigraphic
            order (default: iterate in forward order)
        @param includeredirects: DEPRECATED, use filterredirs instead
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        if not isinstance(namespace, int):
            raise Error("allpages: only one namespace permitted.")
        if includeredirects is not None:
            pywikibot.debug(
                "allpages: 'includeRedirects' argument is deprecated; "
                "use 'filterredirs'.",
                _logger)
            if includeredirects:
                if includeredirects == "only":
                    #filterredirs = True
                    pass
                else:
                    #filterredirs = None
                    pass
            else:
                #filterredirs = False
                pass

        apgen = self._generator(api.PageGenerator, type_arg="allpages",
                                gapnamespace=str(namespace),
                                gapfrom=start, step=step, total=total,
                                g_content=content)
        if prefix:
            apgen.request["gapprefix"] = prefix
        if filterredir is not None:
            apgen.request["gapfilterredir"] = (filterredir
                                               and "redirects"
                                               or "nonredirects")
        if filterlanglinks is not None:
            apgen.request["gapfilterlanglinks"] = (filterlanglinks
                                                   and "withlanglinks"
                                                   or "withoutlanglinks")
        if isinstance(minsize, int):
            apgen.request["gapminsize"] = str(minsize)
        if isinstance(maxsize, int):
            apgen.request["gapmaxsize"] = str(maxsize)
        if isinstance(protect_type, str):
            apgen.request["gapprtype"] = protect_type
            if isinstance(protect_level, str):
                apgen.request["gapprlevel"] = protect_level
        if reverse:
            apgen.request["gapdir"] = "descending"
        return apgen

    @deprecated("Site.allpages()")
    def prefixindex(self, prefix, namespace=0, includeredirects=True):
        """Yield all pages with a given prefix. Deprecated.

        Use allpages() with the prefix= parameter instead of this method.

        """
        return self.allpages(prefix=prefix, namespace=namespace,
                             includeredirects=includeredirects)

    def alllinks(self, start="!", prefix="", namespace=0, unique=False,
                 fromids=False, step=None, total=None):
        """Iterate all links to pages (which need not exist) in one namespace.

        Note that, in practice, links that were found on pages that have
        been deleted may not have been removed from the links table, so this
        method can return false positives.

        @param start: Start at this title (page need not exist).
        @param prefix: Only yield pages starting with this string.
        @param namespace: Iterate pages from this (single) namespace
            (default: 0)
        @param unique: If True, only iterate each link title once (default:
            iterate once for each linking page)
        @param fromids: if True, include the pageid of the page containing
            each link (default: False) as the '_fromid' attribute of the Page;
            cannot be combined with unique

        """
        if unique and fromids:
            raise Error("alllinks: unique and fromids cannot both be True.")
        if not isinstance(namespace, int):
            raise Error("alllinks: only one namespace permitted.")
        algen = self._generator(api.ListGenerator, type_arg="alllinks",
                                alnamespace=str(namespace), alfrom=start,
                                step=step, total=total)
        if prefix:
            algen.request["alprefix"] = prefix
        if unique:
            algen.request["alunique"] = ""
        if fromids:
            algen.request["alprop"] = "title|ids"
        for link in algen:
            p = pywikibot.Page(self, link['title'], link['ns'])
            if fromids:
                p._fromid = link['fromid']
            yield p

    def allcategories(self, start="!", prefix="", step=None, total=None,
                      reverse=False, content=False):
        """Iterate categories used (which need not have a Category page).

        Iterator yields Category objects. Note that, in practice, links that
        were found on pages that have been deleted may not have been removed
        from the database table, so this method can return false positives.

        @param start: Start at this category title (category need not exist).
        @param prefix: Only yield categories starting with this string.
        @param reverse: if True, iterate in reverse Unicode lexigraphic
            order (default: iterate in forward order)
        @param content: if True, load the current content of each iterated page
            (default False); note that this means the contents of the category
            description page, not the pages that are members of the category

        """
        acgen = self._generator(api.CategoryPageGenerator,
                                type_arg="allcategories", gacfrom=start,
                                step=step, total=total, g_content=content)
        if prefix:
            acgen.request["gacprefix"] = prefix
        if reverse:
            acgen.request["gacdir"] = "descending"
        return acgen

    @deprecated("Site.allcategories()")
    def categories(self, number=10, repeat=False):
        """Deprecated; retained for backwards-compatibility"""
        if repeat:
            limit = None
        else:
            limit = number
        return self.allcategories(total=limit)

    def allusers(self, start="!", prefix="", group=None, step=None,
                 total=None):
        """Iterate registered users, ordered by username.

        Iterated values are dicts containing 'name', 'editcount',
        'registration', and (sometimes) 'groups' keys. 'groups' will be
        present only if the user is a member of at least 1 group, and will
        be a list of unicodes; all the other values are unicodes and should
        always be present.

        @param start: start at this username (name need not exist)
        @param prefix: only iterate usernames starting with this substring
        @param group: only iterate users that are members of this group
        @type group: str

        """
        augen = self._generator(api.ListGenerator, type_arg="allusers",
                                auprop="editcount|groups|registration",
                                aufrom=start, step=step, total=total)
        if prefix:
            augen.request["auprefix"] = prefix
        if group:
            augen.request["augroup"] = group
        return augen

    def allimages(self, start="!", prefix="", minsize=None, maxsize=None,
                  reverse=False, sha1=None, sha1base36=None, step=None,
                  total=None, content=False):
        """Iterate all images, ordered by image title.

        Yields ImagePages, but these pages need not exist on the wiki.

        @param start: start at this title (name need not exist)
        @param prefix: only iterate titles starting with this substring
        @param minsize: only iterate images of at least this many bytes
        @param maxsize: only iterate images of no more than this many bytes
        @param reverse: if True, iterate in reverse lexigraphic order
        @param sha1: only iterate image (it is theoretically possible there
            could be more than one) with this sha1 hash
        @param sha1base36: same as sha1 but in base 36
        @param content: if True, load the current content of each iterated page
            (default False); note that this means the content of the image
            description page, not the image itself

        """
        aigen = self._generator(api.ImagePageGenerator,
                                type_arg="allimages", gaifrom=start,
                                step=step, total=total, g_content=content)
        if prefix:
            aigen.request["gaiprefix"] = prefix
        if isinstance(minsize, int):
            aigen.request["gaiminsize"] = str(minsize)
        if isinstance(maxsize, int):
            aigen.request["gaimaxsize"] = str(maxsize)
        if reverse:
            aigen.request["gaidir"] = "descending"
        if sha1:
            aigen.request["gaisha1"] = sha1
        if sha1base36:
            aigen.request["gaisha1base36"] = sha1base36
        return aigen

    def blocks(self, starttime=None, endtime=None, reverse=False,
               blockids=None, users=None, step=None, total=None):
        """Iterate all current blocks, in order of creation.

        Note that logevents only logs user blocks, while this method
        iterates all blocks including IP ranges.  The iterator yields dicts
        containing keys corresponding to the block properties (see
        http://www.mediawiki.org/wiki/API:Query_-_Lists for documentation).

        @param starttime: start iterating at this Timestamp
        @param endtime: stop iterating at this Timestamp
        @param reverse: if True, iterate oldest blocks first (default: newest)
        @param blockids: only iterate blocks with these id numbers
        @param users: only iterate blocks affecting these usernames or IPs

        """
        if starttime and endtime:
            if reverse:
                if starttime > endtime:
                    raise pywikibot.Error(
                        "blocks: "
                        "starttime must be before endtime with reverse=True")
            else:
                if endtime > starttime:
                    raise pywikibot.Error(
                        "blocks: "
                        "endtime must be before starttime with reverse=False")
        bkgen = self._generator(api.ListGenerator, type_arg="blocks",
                                step=step, total=total)
        bkgen.request["bkprop"] = "id|user|by|timestamp|expiry|reason|range|flags"
        if starttime:
            bkgen.request["bkstart"] = str(starttime)
        if endtime:
            bkgen.request["bkend"] = str(endtime)
        if reverse:
            bkgen.request["bkdir"] = "newer"
        if blockids:
            bkgen.request["bkids"] = blockids
        if users:
            bkgen.request["bkusers"] = users
        return bkgen

    def exturlusage(self, url, protocol="http", namespaces=None,
                    step=None, total=None, content=False):
        """Iterate Pages that contain links to the given URL.

        @param url: The URL to search for (without the protocol prefix);
            this many include a '*' as a wildcard, only at the start of the
            hostname
        @param protocol: The protocol prefix (default: "http")

        """
        eugen = self._generator(api.PageGenerator, type_arg="exturlusage",
                                geuquery=url, geuprotocol=protocol,
                                namespaces=namespaces, step=step,
                                total=total, g_content=content)
        return eugen

    def imageusage(self, image, namespaces=None, filterredir=None,
                   step=None, total=None, content=False):
        """Iterate Pages that contain links to the given ImagePage.

        @param image: the image to search for (ImagePage need not exist on
            the wiki)
        @type image: ImagePage
        @param filterredir: if True, only yield redirects; if False (and not
            None), only yield non-redirects (default: yield both)
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        iuargs = dict(giutitle=image.title(withSection=False))
        if filterredir is not None:
            iuargs["giufilterredir"] = (filterredir and "redirects"
                                        or "nonredirects")
        iugen = self._generator(api.PageGenerator, type_arg="imageusage",
                                namespaces=namespaces, step=step,
                                total=total, g_content=content, **iuargs)
        return iugen

    def logevents(self, logtype=None, user=None, page=None,
                  start=None, end=None, reverse=False, step=None, total=None):
        """Iterate all log entries.

        @param logtype: only iterate entries of this type (see wiki
            documentation for available types, which will include "block",
            "protect", "rights", "delete", "upload", "move", "import",
            "patrol", "merge")
        @param user: only iterate entries that match this user name
        @param page: only iterate entries affecting this page
        @param start: only iterate entries from and after this Timestamp
        @param end: only iterate entries up to and through this Timestamp
        @param reverse: if True, iterate oldest entries first (default: newest)

        """
        if start and end:
            if reverse:
                if end < start:
                    raise Error(
                        "logevents: "
                        "end must be later than start with reverse=True")
            else:
                if start < end:
                    raise Error(
                        "logevents: "
                        "start must be later than end with reverse=False")
        legen = self._generator(api.LogEntryListGenerator, type_arg=logtype,
                                step=step, total=total)
        if logtype is not None:
            legen.request["letype"] = logtype
        if user is not None:
            legen.request["leuser"] = user
        if page is not None:
            legen.request["letitle"] = page.title(withSection=False)
        if start is not None:
            legen.request["lestart"] = str(start)
        if end is not None:
            legen.request["leend"] = str(end)
        if reverse:
            legen.request["ledir"] = "newer"
        return legen

    def recentchanges(self, start=None, end=None, reverse=False,
                      namespaces=None, pagelist=None, changetype=None,
                      showMinor=None, showBot=None, showAnon=None,
                      showRedirects=None, showPatrolled=None, topOnly=False,
                      step=None, total=None, user=None, excludeuser=None):
        """Iterate recent changes.

        @param start: Timestamp to start listing from
        @type start: pywikibot.Timestamp
        @param end: Timestamp to end listing at
        @type end: pywikibot.Timestamp
        @param reverse: if True, start with oldest changes (default: newest)
        @type reverse: bool
        @param pagelist: iterate changes to pages in this list only
        @param pagelist: list of Pages
        @param changetype: only iterate changes of this type ("edit" for
            edits to existing pages, "new" for new pages, "log" for log
            entries)
        @type changetype: basestring
        @param showMinor: if True, only list minor edits; if False (and not
            None), only list non-minor edits
        @type showMinor: bool
        @param showBot: if True, only list bot edits; if False (and not
            None), only list non-bot edits
        @type showBot: bool
        @param showAnon: if True, only list anon edits; if False (and not
            None), only list non-anon edits
        @type showAnon: bool
        @param showRedirects: if True, only list edits to redirect pages; if
            False (and not None), only list edits to non-redirect pages
        @type showRedirects: bool
        @param showPatrolled: if True, only list patrolled edits; if False
            (and not None), only list non-patrolled edits
        @type showPatrolled: bool
        @param topOnly: if True, only list changes that are the latest revision
            (default False)
        @type topOnly: bool
        @param user: if not None, only list edits by this user or users
        @type user: basestring|list
        @param excludeuser: if not None, exclude edits by this user or users
        @type excludeuser: basestring|list

        """
        if start and end:
            if reverse:
                if end < start:
                    raise Error(
                        "recentchanges: "
                        "end must be later than start with reverse=True")
            else:
                if start < end:
                    raise Error(
                        "recentchanges: "
                        "start must be later than end with reverse=False")
        rcgen = self._generator(api.ListGenerator, type_arg="recentchanges",
                                rcprop="user|comment|timestamp|title|ids"
                                       "|sizes|redirect|loginfo|flags",
                                namespaces=namespaces, step=step,
                                total=total)
        if start is not None:
            rcgen.request["rcstart"] = str(start)
        if end is not None:
            rcgen.request["rcend"] = str(end)
        if reverse:
            rcgen.request["rcdir"] = "newer"
        if pagelist:
            if self.versionnumber() > 14:
                pywikibot.warning(
                    "recentchanges: pagelist option is disabled; ignoring.")
            else:
                rcgen.request["rctitles"] = "|".join(p.title(withSection=False)
                                                      for p in pagelist)
        if changetype:
            rcgen.request["rctype"] = changetype
        if topOnly:
            rcgen.request["rctoponly"] = ""
        filters = {'minor': showMinor,
                   'bot': showBot,
                   'anon': showAnon,
                   'redirect': showRedirects,
                   }
        if showPatrolled is not None and (
                self.has_right('patrol') or self.has_right('patrolmarks')):
            rcgen.request['rcprop'] += '|patrolled'
            filters['patrolled'] = showPatrolled
        rcshow = []
        for item in filters:
            if filters[item] is not None:
                rcshow.append(filters[item] and item or ("!" + item))
        if rcshow:
            rcgen.request["rcshow"] = "|".join(rcshow)

        if user:
            rcgen.request['rcuser'] = user

        if excludeuser:
            rcgen.request['rcexcludeuser'] = excludeuser

        return rcgen

    @deprecate_arg("number", "limit")
    def search(self, searchstring, namespaces=None, where="text",
               getredirects=False, step=None, total=None, content=False):
        """Iterate Pages that contain the searchstring.

        Note that this may include non-existing Pages if the wiki's database
        table contains outdated entries.

        @param searchstring: the text to search for
        @type searchstring: unicode
        @param where: Where to search; value must be "text" or "titles" (many
            wikis do not support title search)
        @param namespaces: search only in these namespaces (defaults to 0)
        @type namespaces: list of ints, or an empty list to signal all
            namespaces
        @param getredirects: if True, include redirects in results
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        if not searchstring:
            raise Error("search: searchstring cannot be empty")
        if where not in ("text", "titles"):
            raise Error("search: unrecognized 'where' value: %s" % where)
        if namespaces == []:
            namespaces = [ns for ns in list(self.namespaces().keys()) if ns >= 0]
        if not namespaces:
            pywikibot.warning("search: namespaces cannot be empty; using [0].")
            namespaces = [0]
        srgen = self._generator(api.PageGenerator, type_arg="search",
                                gsrsearch=searchstring, gsrwhat=where,
                                namespaces=namespaces, step=step,
                                total=total, g_content=content)
        if getredirects:
            srgen.request["gsrredirects"] = ""
        return srgen

    def usercontribs(self, user=None, userprefix=None, start=None, end=None,
                     reverse=False, namespaces=None, showMinor=None,
                     step=None, total=None, top_only=False):
        """Iterate contributions by a particular user.

        Iterated values are in the same format as recentchanges.

        @param user: Iterate contributions by this user (name or IP)
        @param userprefix: Iterate contributions by all users whose names
            or IPs start with this substring
        @param start: Iterate contributions starting at this Timestamp
        @param end: Iterate contributions ending at this Timestamp
        @param reverse: Iterate oldest contributions first (default: newest)
        @param showMinor: if True, iterate only minor edits; if False and
            not None, iterate only non-minor edits (default: iterate both)
        @param top_only: if True, iterate only edits which are the latest
            revision

        """
        if not (user or userprefix):
            raise Error(
                "usercontribs: either user or userprefix must be non-empty")
        if start and end:
            if reverse:
                if end < start:
                    raise Error(
                        "usercontribs: "
                        "end must be later than start with reverse=True")
            else:
                if start < end:
                    raise Error(
                        "usercontribs: "
                        "start must be later than end with reverse=False")
        ucgen = self._generator(api.ListGenerator, type_arg="usercontribs",
                                ucprop="ids|title|timestamp|comment|flags",
                                namespaces=namespaces, step=step,
                                total=total)
        if user:
            ucgen.request["ucuser"] = user
        if userprefix:
            ucgen.request["ucuserprefix"] = userprefix
        if start is not None:
            ucgen.request["ucstart"] = str(start)
        if end is not None:
            ucgen.request["ucend"] = str(end)
        if reverse:
            ucgen.request["ucdir"] = "newer"
        if showMinor is not None:
            ucgen.request["ucshow"] = showMinor and "minor" or "!minor"
        if top_only:
            ucgen.request["uctoponly"] = ""
        return ucgen

    def watchlist_revs(self, start=None, end=None, reverse=False,
                       namespaces=None, showMinor=None, showBot=None,
                       showAnon=None, step=None, total=None):
        """Iterate revisions to pages on the bot user's watchlist.

        Iterated values will be in same format as recentchanges.

        @param start: Iterate revisions starting at this Timestamp
        @param end: Iterate revisions ending at this Timestamp
        @param reverse: Iterate oldest revisions first (default: newest)
        @param showMinor: if True, only list minor edits; if False (and not
            None), only list non-minor edits
        @param showBot: if True, only list bot edits; if False (and not
            None), only list non-bot edits
        @param showAnon: if True, only list anon edits; if False (and not
            None), only list non-anon edits

        """
        if start and end:
            if reverse:
                if end < start:
                    raise Error(
                        "watchlist_revs: "
                        "end must be later than start with reverse=True")
            else:
                if start < end:
                    raise Error(
                        "watchlist_revs: "
                        "start must be later than end with reverse=False")
        wlgen = self._generator(api.ListGenerator, type_arg="watchlist",
                                wlprop="user|comment|timestamp|title|ids|flags",
                                wlallrev="", namespaces=namespaces,
                                step=step, total=total)
        #TODO: allow users to ask for "patrol" as well?
        if start is not None:
            wlgen.request["wlstart"] = str(start)
        if end is not None:
            wlgen.request["wlend"] = str(end)
        if reverse:
            wlgen.request["wldir"] = "newer"
        filters = {'minor': showMinor,
                   'bot': showBot,
                   'anon': showAnon}
        wlshow = []
        for item in filters:
            if filters[item] is not None:
                wlshow.append(filters[item] and item or ("!" + item))
        if wlshow:
            wlgen.request["wlshow"] = "|".join(wlshow)
        return wlgen

    def deletedrevs(self, page, start=None, end=None, reverse=None,
                    get_text=False, step=None, total=None):
        """Iterate deleted revisions.

        Each value returned by the iterator will be a dict containing the
        'title' and 'ns' keys for a particular Page and a 'revisions' key
        whose value is a list of revisions in the same format as
        recentchanges (plus a 'content' element if requested). If get_text
        is true, the toplevel dict will contain a 'token' key as well.

        @param page: The page to check for deleted revisions
        @param start: Iterate revisions starting at this Timestamp
        @param end: Iterate revisions ending at this Timestamp
        @param reverse: Iterate oldest revisions first (default: newest)
        @param get_text: If True, retrieve the content of each revision and
            an undelete token

        """
        if start and end:
            if reverse:
                if end < start:
                    raise Error(
                        "deletedrevs: "
                        "end must be later than start with reverse=True")
            else:
                if start < end:
                    raise Error(
                        "deletedrevs: "
                        "start must be later than end with reverse=False")
        if not self.logged_in():
            self.login()
        if "deletedhistory" not in self.userinfo['rights']:
            try:
                self.login(True)
            except NoUsername:
                pass
            if "deletedhistory" not in self.userinfo['rights']:
                raise Error(
                    "deletedrevs: "
                    "User:%s not authorized to access deleted revisions."
                    % self.user())
        if get_text:
            if "undelete" not in self.userinfo['rights']:
                try:
                    self.login(True)
                except NoUsername:
                    pass
                if "undelete" not in self.userinfo['rights']:
                    raise Error(
                        "deletedrevs: "
                        "User:%s not authorized to view deleted content."
                        % self.user())

        drgen = self._generator(api.ListGenerator, type_arg="deletedrevs",
                                titles=page.title(withSection=False),
                                drprop="revid|user|comment|minor",
                                step=step, total=total)
        if get_text:
            drgen.request['drprop'] = (drgen.request['drprop'] +
                                       "|content|token")
        if start is not None:
            drgen.request["drstart"] = str(start)
        if end is not None:
            drgen.request["drend"] = str(end)
        if reverse:
            drgen.request["drdir"] = "newer"
        return drgen

    def users(self, usernames):
        """Iterate info about a list of users by name or IP.

        @param usernames: a list of user names
        @type usernames: list, or other iterable, of unicodes

        """
        if not isinstance(usernames, str):
            usernames = "|".join(usernames)
        usgen = pywikibot.data.api.ListGenerator(
            "users", ususers=usernames, site=self,
            usprop="blockinfo|groups|editcount|registration|emailable"
        )
        return usgen

    @deprecated("Site.randompages()")
    def randompage(self, redirect=False):
        """
        @param redirect: Return a random redirect page
        @return: pywikibot.Page
        """
        return self.randompages(total=1, redirects=redirect)

    @deprecated("Site.randompages()")
    def randomredirectpage(self):
        return self.randompages(total=1, redirects=True)

    def randompages(self, step=None, total=10, namespaces=None,
                    redirects=False, content=False):
        """Iterate a number of random pages.

        Pages are listed in a fixed sequence, only the starting point is
        random.

        @param total: the maximum number of pages to iterate (default: 1)
        @param namespaces: only iterate pages in these namespaces.
        @param redirects: if True, include only redirect pages in results
            (default: include only non-redirects)
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        rngen = self._generator(api.PageGenerator, type_arg="random",
                                namespaces=namespaces, step=step, total=total,
                                g_content=content)
        if redirects:
            rngen.request["grnredirect"] = ""
        return rngen

    # catalog of editpage error codes, for use in generating messages
    _ep_errors = {
        "noapiwrite": "API editing not enabled on %(site)s wiki",
        "writeapidenied": "User %(user)s is not authorized to edit on %(site)s wiki",
        "protectedtitle": "Title %(title)s is protected against creation on %(site)s",
        "cantcreate": "User %(user)s not authorized to create new pages on %(site)s wiki",
        "cantcreate-anon": """Bot is not logged in, and anon users are not authorized to create new pages on %(site)s wiki""",
        "articleexists": "Page %(title)s already exists on %(site)s wiki",
        "noimageredirect-anon": """Bot is not logged in, and anon users are not authorized to create image redirects on %(site)s wiki""",
        "noimageredirect": "User %(user)s not authorized to create image redirects on %(site)s wiki",
        "spamdetected": "Edit to page %(title)s rejected by spam filter due to content:\n",
        "filtered": "%(info)s",
        "contenttoobig": "%(info)s",
        "noedit-anon": """Bot is not logged in, and anon users are not authorized to edit on %(site)s wiki""",
        "noedit": "User %(user)s not authorized to edit pages on %(site)s wiki",
        "pagedeleted": "Page %(title)s has been deleted since last retrieved from %(site)s wiki",
        "editconflict": "Page %(title)s not saved due to edit conflict.",
    }

    @must_be(group='user')
    def editpage(self, page, summary, minor=True, notminor=False,
                 bot=True, recreate=True, createonly=False, watch=None):
        """Submit an edited Page object to be saved to the wiki.

        @param page: The Page to be saved; its .text property will be used
            as the new text to be saved to the wiki
        @param token: the edit token retrieved using Site.token()
        @param summary: the edit summary (required!)
        @param minor: if True (default), mark edit as minor
        @param notminor: if True, override account preferences to mark edit
            as non-minor
        @param recreate: if True (default), create new page even if this
            title has previously been deleted
        @param createonly: if True, raise an error if this title already
            exists on the wiki
        @param watch: Specify how the watchlist is affected by this edit, set
            to one of "watch", "unwatch", "preferences", "nochange":
            * watch: add the page to the watchlist
            * unwatch: remove the page from the watchlist
            * preferences: use the preference settings (Default)
            * nochange: don't change the watchlist
        @param botflag: if True, mark edit with bot flag
        @return: True if edit succeeded, False if it failed

        """
        text = page.text
        if not text:
            raise Error("editpage: no text to be saved")
        try:
            lastrev = page.latestRevision()
        except NoPage:
            lastrev = None
            if not recreate:
                raise
        token = self.token(page, "edit")
        # getting token also updates the 'lastrevid' value, which allows us to
        # detect if page has been changed since last time text was retrieved.

        # note that the server can still return an 'editconflict' error
        # if the page is updated after the token is retrieved but
        # before the page is saved.
        self.lock_page(page)
        if lastrev is not None and page.latestRevision() != lastrev:
            raise EditConflict(
                "editpage: Edit conflict detected; saving aborted.")
        params = dict(action="edit",
                      title=page.title(withSection=False),
                      text=text, token=token, summary=summary)
        if bot:
            params["bot"] = ""
        if lastrev is not None:
            if lastrev not in page._revisions:
                self.loadrevisions(page)
            params["basetimestamp"] = page._revisions[lastrev].timestamp
        if minor:
            params['minor'] = ""
        elif notminor:
            params['notminor'] = ""
        if recreate:
            params['recreate'] = ""
        if createonly:
            params['createonly'] = ""
        if watch in ["watch", "unwatch", "preferences", "nochange"]:
            params['watchlist'] = watch
        elif watch:
            pywikibot.warning(
                "editpage: Invalid watch value '%(watch)s' ignored."
                % locals())
## FIXME: API gives 'badmd5' error
##        md5hash = md5()
##        md5hash.update(urllib.quote_plus(text.encode(self.encoding())))
##        params['md5'] = md5hash.digest()
        req = pywikibot.data.api.Request(site=self, **params)
        while True:
            try:
                result = req.submit()
                pywikibot.debug("editpage response: %s" % result,
                                _logger)
            except pywikibot.data.api.APIError as err:
                self.unlock_page(page)
                if err.code.endswith("anon") and self.logged_in():
                    pywikibot.debug(
                        "editpage: received '%s' even though bot is logged in"
                        % err.code,
                        _logger)
                errdata = {
                    'site': self,
                    'title': page.title(withSection=False),
                    'user': self.user(),
                    'info': err.info
                }
                if err.code == "spamdetected":
                    raise SpamfilterError(
                        self._ep_errors[err.code] % errdata
                        + err.info[err.info.index("fragment: ") + 9:])

                if err.code == "editconflict":
                    raise EditConflict(self._ep_errors[err.code] % errdata)
                if err.code in ("protectedpage", "cascadeprotected"):
                    raise LockedPage(errdata['title'])
                if err.code in self._ep_errors:
                    raise Error(self._ep_errors[err.code] % errdata)
                pywikibot.debug(
                    "editpage: Unexpected error code '%s' received."
                    % err.code,
                    _logger)
                raise
            assert ("edit" in result and "result" in result["edit"]), result
            if result["edit"]["result"] == "Success":
                self.unlock_page(page)
                if "nochange" in result["edit"]:
                    # null edit, page not changed
                    log("Page [[%s]] saved without any changes."
                                  % page.title())
                    return True
                page._revid = result["edit"]["newrevid"]
                # see http://www.mediawiki.org/wiki/API:Wikimania_2006_API_discussion#Notes
                # not safe to assume that saved text is the same as sent
                self.loadrevisions(page, getText=True)
                return True
            elif result["edit"]["result"] == "Failure":
                if "captcha" in result["edit"]:
                    captcha = result["edit"]["captcha"]
                    req['captchaid'] = captcha['id']
                    if captcha["type"] == "math":
                        req['captchaword'] = eval(input(captcha["question"]))
                        continue
                    elif "url" in captcha:
                        import webbrowser
                        webbrowser.open('%s://%s%s'
                                        % (self.family.protocol(self.code),
                                           self.family.hostname(self.code),
                                           captcha["url"]))

                        cap_answerwikipedia= Captcha()
                        req['captchaword'] = cap_answerwikipedia.user_input(
                            "Please view CAPTCHA in your browser, "
                            "then type answer here:")
                        continue
                    else:
                        self.unlock_page(page)
                        pywikibot.error(
                            "editpage: unknown CAPTCHA response %s, "
                            "page not saved"
                            % captcha)
                        return False
                else:
                    self.unlock_page(page)
                    pywikibot.error("editpage: unknown failure reason %s"
                                    % str(result))
                    return False
            else:
                self.unlock_page(page)
                pywikibot.error(
                    "editpage: Unknown result code '%s' received; "
                    "page not saved" % result["edit"]["result"])
                log(str(result))
                return False

    # catalog of move errors for use in error messages
    _mv_errors = {
        "noapiwrite": "API editing not enabled on %(site)s wiki",
        "writeapidenied":
"User %(user)s is not authorized to edit on %(site)s wiki",
        "nosuppress":
"User %(user)s is not authorized to move pages without creating redirects",
        "cantmove-anon":
"""Bot is not logged in, and anon users are not authorized to move pages on
%(site)s wiki""",
        "cantmove":
"User %(user)s is not authorized to move pages on %(site)s wiki",
        "immobilenamespace":
"Pages in %(oldnamespace)s namespace cannot be moved on %(site)s wiki",
        "articleexists":
"Cannot move because page [[%(newtitle)s]] already exists on %(site)s wiki",
        "protectedpage":
"Page [[%(oldtitle)s]] is protected against moving on %(site)s wiki",
        "protectedtitle":
"Page [[%(newtitle)s]] is protected against creation on %(site)s wiki",
        "nonfilenamespace":
"Cannot move a file to %(newnamespace)s namespace on %(site)s wiki",
        "filetypemismatch":
"[[%(newtitle)s]] file extension does not match content of [[%(oldtitle)s]]"
    }

    def movepage(self, page, newtitle, summary, movetalk=True,
                 noredirect=False):
        """Move a Page to a new title.

        @param page: the Page to be moved (must exist)
        @param newtitle: the new title for the Page
        @type newtitle: unicode
        @param summary: edit summary (required!)
        @param movetalk: if True (default), also move the talk page if possible
        @param noredirect: if True, suppress creation of a redirect from the
            old title to the new one
        @return: Page object with the new title

        """
        oldtitle = page.title(withSection=False)
        newlink = pywikibot.Link(newtitle, self)
        if newlink.namespace:
            newtitle = self.namespace(newlink.namespace) + ":" + newlink.title
        else:
            newtitle = newlink.title
        if oldtitle == newtitle:
            raise Error("Cannot move page %s to its own title."
                        % oldtitle)
        if not page.exists():
            raise Error("Cannot move page %s because it does not exist on %s."
                        % (oldtitle, self))
        token = self.token(page, "move")
        self.lock_page(page)
        req = pywikibot.data.api.Request(site=self, action="move", to=newtitle,
                          token=token, reason=summary)
        req['from'] = oldtitle  # "from" is a python keyword
        if movetalk:
            req['movetalk'] = ""
        if noredirect:
            req['noredirect'] = ""
        try:
            result = req.submit()
            pywikibot.debug("movepage response: %s" % result,
                            _logger)
        except pywikibot.data.api.APIError as err:
            if err.code.endswith("anon") and self.logged_in():
                pywikibot.debug(
                    "movepage: received '%s' even though bot is logged in"
                    % err.code,
                    _logger)
            errdata = {
                'site': self,
                'oldtitle': oldtitle,
                'oldnamespace': self.namespace(page.namespace()),
                'newtitle': newtitle,
                'newnamespace': self.namespace(newlink.namespace),
                'user': self.user(),
            }
            if err.code in self._mv_errors:
                raise Error(self._mv_errors[err.code] % errdata)
            pywikibot.debug("movepage: Unexpected error code '%s' received."
                            % err.code,
                            _logger)
            raise
        finally:
            self.unlock_page(page)
        if "move" not in result:
            pywikibot.error("movepage: %s" % result)
            raise Error("movepage: unexpected response")
        #TODO: Check for talkmove-error messages
        if "talkmove-error-code" in result["move"]:
            pywikibot.warning(
                "movepage: Talk page %s not moved"
                % (page.toggleTalkPage().title(asLink=True)))
        return pywikibot.Page(page, newtitle)

    # catalog of rollback errors for use in error messages
    _rb_errors = {
        "noapiwrite": "API editing not enabled on %(site)s wiki",
        "writeapidenied": "User %(user)s not allowed to edit through the API",
        "alreadyrolled": "Page [[%(title)s]] already rolled back; action aborted.",
    }  # other errors shouldn't arise because we check for those errors

    def rollbackpage(self, page, summary=''):
        """Roll back page to version before last user's edits.

        As a precaution against errors, this method will fail unless
        the page history contains at least two revisions, and at least
        one that is not by the same user who made the last edit.

        @param page: the Page to be rolled back (must exist)
        @param summary: edit summary (defaults to a standardized message)

        """
        if len(page._revisions) < 2:
            raise pywikibot.Error(
                "Rollback of %s aborted; load revision history first."
                % page.title(asLink=True))
        last_rev = page._revisions[page.latestRevision()]
        last_user = last_rev.user
        for rev in sorted(list(page._revisions.keys()), reverse=True):
            # start with most recent revision first
            if rev.user != last_user:
                prev_user = rev.user
                break
        else:
            raise pywikibot.Error(
                "Rollback of %s aborted; only one user in revision history."
                % page.title(asLink=True))
        summary = summary or (
            "Reverted edits by [[Special:Contributions/%(last_user)s|%(last_user)s]] "
            "([[User talk:%(last_user)s|Talk]]) to last version by %(prev_user)s"
            % locals())
        token = self.token(page, "rollback")
        self.lock_page(page)
        req = pywikibot.data.api.Request(site=self, action="rollback",
                          title=page.title(withSection=False),
                          user=last_user,
                          token=token)
        try:
            result = req.submit()
        except pywikibot.data.api.APIError as err:
            errdata = {
                'site': self,
                'title': page.title(withSection=False),
                'user': self.user(),
            }
            if err.code in self._rb_errors:
                raise Error(self._rb_errors[err.code] % errdata)
            pywikibot.debug("rollback: Unexpected error code '%s' received."
                            % err.code,
                            _logger)
            raise
        finally:
            self.unlock_page(page)

    # catalog of delete errors for use in error messages
    _dl_errors = {
        "noapiwrite": "API editing not enabled on %(site)s wiki",
        "writeapidenied": "User %(user)s not allowed to edit through the API",
        "permissiondenied": "User %(user)s not authorized to delete pages on %(site)s wiki.",
        "cantdelete": "Could not delete [[%(title)s]]. Maybe it was deleted already.",
    }  # other errors shouldn't occur because of pre-submission checks

    def deletepage(self, page, summary):
        """Delete page from the wiki. Requires appropriate privilege level.

        @param page: Page to be deleted.
        @param summary: Edit summary (required!).

        """
        try:
            self.login(sysop=True)
        except pywikibot.NoUsername as e:
            raise NoUsername("delete: Unable to login as sysop (%s)"
                             % e.__class__.__name__)
        if not self.logged_in(sysop=True):
            raise NoUsername("delete: Unable to login as sysop")
        token = self.token(page, "delete")
        self.lock_page(page)
        req = pywikibot.data.api.Request(site=self, action="delete", token=token,
                          title=page.title(withSection=False),
                          reason=summary)
        try:
            #result = 
            req.submit()
        except pywikibot.data.api.APIError as err:
            errdata = {
                'site': self,
                'title': page.title(withSection=False),
                'user': self.user(),
            }
            if err.code in self._dl_errors:
                raise Error(self._dl_errors[err.code] % errdata)
            pywikibot.debug("delete: Unexpected error code '%s' received."
                            % err.code,
                            _logger)
            raise
        finally:
            self.unlock_page(page)

    _protect_errors = {
        "noapiwrite": "API editing not enabled on %(site)s wiki",
        "writeapidenied": "User %(user)s not allowed to edit through the API",
        "permissiondenied": "User %(user)s not authorized to protect pages on %(site)s wiki.",
        "cantedit": "User %(user) can't protect this page because user %(user) can't edit it.",
        "protect-invalidlevel": "Invalid protection level"
    }

    def protect(self, page, edit, move, summary):
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
        try:
            self.login(sysop=True)
        except pywikibot.NoUsername as e:
            raise NoUsername("protect: Unable to login as sysop (%s)"
                             % e.__class__.__name__)
        if not self.logged_in(sysop=True):
            raise NoUsername("protect: Unable to login as sysop")
        token = self.token(page, "protect")
        self.lock_page(page)
        req = pywikibot.data.api.Request(site=self, action="protect", token=token,
                          title=page.title(withSection=False),
                          protections="edit=" + edit + "|" + "move=" + move,
                          reason=summary)
        try:
            #result = 
            req.submit()
        except pywikibot.data.api.APIError as err:
            errdata = {
                'site': self,
                'title': page.title(withSection=False),
                'user': self.user(),
                'level-edit': edit,
                'level-move': move
            }
            if err.code in self._protect_errors:
                raise Error(self._protect_errors[err.code] % errdata)
            pywikibot.debug("protect: Unexpected error code '%s' received."
                            % err.code,
                            _logger)
            raise
        finally:
            self.unlock_page(page)

    #TODO: implement undelete

    #TODO: implement patrol

    @must_be(group='sysop')
    def blockuser(self, user, expiry, reason, anononly=True, nocreate=True,
                  autoblock=True, noemail=False, reblock=False):

        token = self.token(user, 'block')
        if isinstance(expiry, pywikibot.Timestamp):
            expiry = expiry.toISOformat()
        req = pywikibot.data.api.Request(site=self, action='block', user=user.username,
                          expiry=expiry, reason=reason, token=token)
        if anononly:
            req['anononly'] = ''
        if nocreate:
            req['nocreate'] = ''
        if autoblock:
            req['autoblock'] = ''
        if noemail:
            req['noemail'] = ''
        if reblock:
            req['reblock'] = ''

        data = req.submit()
        return data

    def watchpage(self, page, unwatch=False):
        """Add or remove page from watchlist.

        @param unwatch: If True, remove page from watchlist; if False (default),
            add it.
        @return: True if API returned expected response; False otherwise

        """
        token = self.token(page, "watch")
        req = pywikibot.data.api.Request(action="watch", token=token,
                          title=page.title(withSection=False))
        if unwatch:
            req["unwatch"] = ""
        result = req.submit()
        if "watch" not in result:
            pywikibot.error("watchpage: Unexpected API response:\n%s" % result)
            return False
        watched = result["watch"]
        return ((unwatch and "unwatched" in watched)
                or (not unwatch and "watched" in result))

    @deprecated("Site().exturlusage")
    def linksearch(self, siteurl, limit=None):
        """Backwards-compatible interface to exturlusage()"""
        return self.exturlusage(siteurl, total=limit)


    def getFilesFromAnHash(self, hash_found=None):
        """Return all images that have the same hash.

        Useful to find duplicates or nowcommons.

        NOTE: it returns also the image itself, if you don't want it, just
        filter the list returned.

        NOTE 2: it returns the image title WITHOUT the image namespace.

        """
        if hash_found is None:
            return
        return [image.title(withNamespace=False)
                for image in self.allimages(sha1=hash_found)]

    @deprecated('Site().getFilesFromAnHash')
    def getImagesFromAnHash(self, hash_found=None):
        return self.getFilesFromAnHash(hash_found)

    def upload(self, imagepage, source_filename=None, source_url=None,
               comment=None, text=None, watch=False, ignore_warnings=False):
        """Upload a file to the wiki.

        Either source_filename or source_url, but not both, must be provided.

        @param imagepage: an ImagePage object from which the wiki-name of the
            file will be obtained.
        @param source_filename: path to the file to be uploaded
        @param source_url: URL of the file to be uploaded
        @param comment: Edit summary; if this is not provided, then
            imagepage.text will be used. An empty summary is not permitted.
            This may also serve as the initial page text (see below).
        @param text: Initial page text; if this is not set, then
            imagepage.text will be used, or comment.
        @param watch: If true, add imagepage to the bot user's watchlist
        @param ignore_warnings: if true, ignore API warnings and force
            upload (for example, to overwrite an existing file); default False

        """
        upload_warnings = {
            # map API warning codes to user error messages
            # %(msg)s will be replaced by message string from API responsse
            'duplicate-archive': "The file is a duplicate of a deleted file %(msg)s.",
            'was-deleted': "The file %(msg)s was previously deleted.",
            'emptyfile': "File %(msg)s is empty.",
            'exists': "File %(msg)s already exists.",
            'duplicate': "Uploaded file is a duplicate of %(msg)s.",
            'badfilename': "Target filename is invalid.",
            'filetype-unwanted-type': "File %(msg)s type is unwanted type.",
        }

        # check for required user right
        if "upload" not in self.userinfo["rights"]:
            raise pywikibot.Error(
                "User '%s' does not have upload rights on site %s."
                % (self.user(), self))
        # check for required parameters
        if (source_filename and source_url)\
                or (source_filename is None and source_url is None):
            raise ValueError("APISite.upload: must provide either "
                             "source_filename or source_url, not both.")
        if comment is None:
            comment = imagepage.text
        if not comment:
            raise ValueError("APISite.upload: cannot upload file without "
                             "a summary/description.")
        if text is None:
            text = imagepage.text
        if not text:
            text = comment
        token = self.token(imagepage, "edit")
        if source_filename:
            # upload local file
            # make sure file actually exists
            if not os.path.isfile(source_filename):
                raise ValueError("File '%s' does not exist."
                                 % source_filename)
            #filesize = 
            os.path.getsize(source_filename)
            # TODO: if file size exceeds some threshold (to be determined),
            #       upload by chunks
            req = pywikibot.data.api.Request(site=self, action="upload", token=token,
                              filename=imagepage.title(withNamespace=False),
                              file=source_filename, comment=comment,
                              text=text, mime=True)
        else:
            # upload by URL
            if "upload_by_url" not in self.userinfo["rights"]:
                raise pywikibot.Error(
                    "User '%s' is not authorized to upload by URL on site %s."
                    % (self.user(), self))
            req = pywikibot.data.api.Request(site=self, action="upload", token=token,
                              filename=imagepage.title(withNamespace=False),
                              url=source_url, comment=comment, text=text)
        if watch:
            req["watch"] = ""
        if ignore_warnings:
            req["ignorewarnings"] = ""
        try:
            result = req.submit()
        except pywikibot.data.api.APIError as err:
            print (err)
            # TODO: catch and process foreseeable errors
            raise
        result = result["upload"]
        pywikibot.debug(result, _logger)
        if "warnings" in result:
            warning = list(result["warnings"].keys())[0]
            message = result["warnings"][warning]
            raise pywikibot.UploadWarning(upload_warnings[warning]
                                          % {'msg': message})
        elif "result" not in result:
            pywikibot.output("Upload: unrecognized response: %s" % result)
        if result["result"] == "Success":
            pywikibot.output("Upload successful.")
            imagepage._imageinfo = result["imageinfo"]
            return

    @deprecate_arg("number", "step")
    @deprecate_arg("repeat", None)
    @deprecate_arg("namespace", "namespaces")
    @deprecate_arg("rc_show", None)
    @deprecate_arg("get_redirect", None)  # 20120822
    def newpages(self, user=None, returndict=False,
                 start=None, end=None, reverse=False, showBot=False,
                 showRedirects=False, excludeuser=None,
                 showPatrolled=None, namespaces=None, step=None, total=None):
        """Yield new articles (as Page objects) from recent changes.

        Starts with the newest article and fetches the number of articles
        specified in the first argument. If repeat is True, it fetches
        Newpages again. If there is no new page, it blocks until there is
        one, sleeping between subsequent fetches of Newpages.

        The objects yielded are dependent on paramater returndict.
        When true, it yields a tuple composed of a Page object and a dict of
        attributes.
        When false, it yields a tuple composed of the Page object,
        timestamp (unicode), length (int), an empty unicode string, username
        or IP address (str), comment (unicode).

        """
        # TODO: update docstring

        # N.B. API still provides no way to access Special:Newpages content
        # directly, so we get new pages indirectly through 'recentchanges'

        namespaces = namespaces 
        gen = self.recentchanges(
            start=start, end=end, reverse=reverse,
            namespaces=namespaces, changetype="new", user=user,
            excludeuser=excludeuser, showBot=showBot,
            showRedirects=showRedirects, showPatrolled=showPatrolled,
            step=step, total=total
        )
        for pageitem in gen:
            newpage = pywikibot.Page(self, pageitem['title'])
            if returndict:
                yield (newpage, pageitem)
            else:
                yield (newpage, pageitem['timestamp'], pageitem['newlen'],
                       '', pageitem['user'], pageitem['comment'])

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def newimages(self, user=None, start=None, end=None, reverse=False,
                  step=None, total=None):
        """Yield information about newly uploaded images.

        Yields a tuple of ImagePage, Timestamp, user(unicode), comment(unicode).

        N.B. the API does not provide direct access to Special:Newimages, so
        this is derived from the "upload" log events instead.

        """
        #TODO: update docstring
        for event in self.logevents(self, 
                                    #logtype="upload", 
                                    user=user,
                                    start=start, 
                                    end=end, 
                                    reverse=reverse,
                                    step=step, 
                                    total=total
        ):
            image = pywikibot.ImagePage(self, event['title'])
            date = pywikibot.Timestamp.fromISOformat(event['timestamp'])
            user = event['user']
            comment = event['comment'] or ''
            yield (image, date, user, comment)

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def longpages(self, step=None, total=None):
        """Yield Pages and lengths from Special:Longpages.

        Yields a tuple of Page object, length(int).

        """
        lpgen = self._generator(api.ListGenerator,
                                type_arg="querypage", qppage="Longpages",
                                step=step, total=total)
        for pageitem in lpgen:
            yield (pywikibot.Page(self, pageitem['title']),
                   int(pageitem['value']))

    @deprecate_arg("number", "total")
    @deprecate_arg("repeat", None)
    def shortpages(self, step=None, total=None):
        """Yield Pages and lengths from Special:Shortpages.

        Yields a tuple of Page object, length(int).

        """
        spgen = self._generator(api.ListGenerator,
                                type_arg="querypage", qppage="Shortpages",
                                step=step, total=total)
        for pageitem in spgen:
            yield (pywikibot.Page(self, pageitem['title']),
                   int(pageitem['value']))

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def deadendpages(self, step=None, total=None):
        """Yield Page objects retrieved from Special:Deadendpages."""
        degen = self._generator(api.PageGenerator,
                                type_arg="querypage", gqppage="Deadendpages",
                                step=step, total=total)
        return degen

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def ancientpages(self, step=None, total=None):
        """Yield Pages, datestamps from Special:Ancientpages."""
        apgen = self._generator(api.ListGenerator,
                                type_arg="querypage", qppage="Ancientpages",
                                step=step, total=total)
        for pageitem in apgen:
            yield (pywikibot.Page(self, pageitem['title']),
                   pywikibot.Timestamp.fromISOformat(pageitem['timestamp']))

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def lonelypages(self, step=None, total=None):
        """Yield Pages retrieved from Special:Lonelypages."""
        lpgen = self._generator(api.PageGenerator,
                                type_arg="querypage", gqppage="Lonelypages",
                                step=step, total=total)
        return lpgen

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def unwatchedpages(self, step=None, total=None):
        """Yield Pages from Special:Unwatchedpages (requires Admin privileges).

        """
        uwgen = self._generator(api.PageGenerator,
                                type_arg="querypage", gqppage="Unwatchedpages",
                                step=step, total=total)
        return uwgen

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def uncategorizedcategories(self, number=None, repeat=True,
                                step=None, total=None):
        """Yield Categories from Special:Uncategorizedcategories."""
        ucgen = self._generator(api.CategoryPageGenerator,
                                type_arg="querypage",
                                gqppage="Uncategorizedcategories",
                                step=step, total=total)
        return ucgen

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def uncategorizedimages(self, number=None, repeat=True,
                            step=None, total=None):
        """Yield ImagePages from Special:Uncategorizedimages."""
        uigen = self._generator(api.ImagePageGenerator,
                                type_arg="querypage",
                                gqppage="Uncategorizedimages",
                                step=step, total=total)
        return uigen

    #synonym
    uncategorizedfiles = uncategorizedimages

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def uncategorizedpages(self, number=None, repeat=True,
                           step=None, total=None):
        """Yield Pages from Special:Uncategorizedpages."""
        upgen = self._generator(api.PageGenerator,
                                type_arg="querypage",
                                gqppage="Uncategorizedpages",
                                step=step, total=total)
        return upgen

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def uncategorizedtemplates(self, number=None, repeat=True, step=None,
                               total=None):
        """Yield Pages from Special:Uncategorizedtemplates."""
        utgen = self._generator(api.PageGenerator,
                                type_arg="querypage",
                                gqppage="Uncategorizedtemplates",
                                step=step, total=total)
        return utgen

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def unusedcategories(self, step=None, total=None):
        """Yield Category objects from Special:Unusedcategories."""
        ucgen = self._generator(api.CategoryPageGenerator,
                                type_arg="querypage",
                                gqppage="Unusedcategories",
                                step=step, total=total)
        return ucgen

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def unusedfiles(self, step=None, total=None):
        """Yield ImagePage objects from Special:Unusedimages."""
        uigen = self._generator(api.ImagePageGenerator,
                                type_arg="querypage",
                                gqppage="Unusedimages",
                                step=step, total=total)
        return uigen

    #synonym
    unusedimages = unusedfiles

    @deprecate_arg("number", None)
    @deprecate_arg("repeat", None)
    def withoutinterwiki(self, step=None, total=None):
        """Yield Pages without language links from Special:Withoutinterwiki."""
        wigen = self._generator(api.PageGenerator,
                                type_arg="querypage",
                                gqppage="Withoutinterwiki",
                                step=step, total=total)
        return wigen

    def broken_redirects(self, step=None, total=None):
        """Yield Pages without language links from Special:BrokenRedirects."""
        assert self.versionnumber >= 18
        brgen = self._generator(api.PageGenerator,
                                type_arg="querypage",
                                gqppage="BrokenRedirects",
                                step=step, total=total)
        return brgen

    def double_redirects(self, step=None, total=None):
        """Yield Pages without language links from Special:BrokenRedirects."""
        assert self.versionnumber >= 18
        drgen = self._generator(api.PageGenerator,
                                type_arg="querypage",
                                gqppage="DoubleRedirects",
                                step=step, total=total)
        return drgen

    def redirectpages(self, step=None, total=None):
        """Yield redirect pages from Special:ListRedirects."""
        assert self.versionnumber >= 18
        lrgen = self._generator(api.PageGenerator,
                                type_arg="querypage",
                                gqppage="Listredirects",
                                step=step, total=total)
        return lrgen


