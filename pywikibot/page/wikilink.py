from pywikibot.exceptions  import Error
from pywikibot.exceptions  import InvalidTitle
#import pywikibot
#from pywikibot.deprecate import deprecate_arg
#rom pywikibot.deprecate import deprecated
#from pywikibot.config import loadconfig
from pywikibot.site.base import BaseSite

#import hashlib
#import html.entities 
#import logging
import re
import unicodedata
#import urllib
#import collections
#import traceback
from pywikibot.page.htmlunicode import html2unicode

from pywikibot.debug import tryencode
from pywikibot.debug import debugprint

class Link(object):
    """A Mediawiki link (local or interwiki)

    Has the following attributes:

      - site:  The Site object for the wiki linked to
      - namespace: The namespace of the page linked to (int)
      - title: The title of the page linked to (unicode); does not include
        namespace or section
      - section: The section of the page linked to (unicode or None); this
        contains any text following a '#' character in the title
      - anchor: The anchor text (unicode or None); this contains any text
        following a '|' character inside the link

    """
    illegal_titles_pattern = re.compile(
        # Matching titles will be held as illegal.
        r'''[\x00-\x1f\x23\x3c\x3e\x5b\x5d\x7b\x7c\x7d\x7f]'''
        # URL percent encoding sequences interfere with the ability
        # to round-trip titles -- you can't link to them consistently.
        '|%[0-9A-Fa-f]{2}'
        # XML/HTML character references produce similar issues.
        '|&[A-Za-z0-9\x80-\xff]+;'
        '|&#[0-9]+;'
        '|&#x[0-9A-Fa-f]+;'
    )

    def __init__(self, text, source, defaultNamespace=0):
        """Constructor

        @param text: the link text (everything appearing between [[ and ]]
            on a wiki page)
        @type text: unicode
        @param source: the Site on which the link was found (not necessarily
            the site to which the link refers)
        @type source: Site
        @param defaultNamespace: a namespace to use if the link does not
            contain one (defaults to 0)
        @type defaultNamespace: int

        """
        assert source is None or isinstance(source, BaseSite), \
            "source parameter should be a Site object"

        self._text = text
        if (source):
            self._source = source 
        else:
            raise Exception()
            
        self._defaultns = defaultNamespace

        # preprocess text (these changes aren't site-dependent)
        # First remove anchor, which is stored unchanged, if there is one
        if "|" in self._text:
            self._text, self._anchor = text.split("|", 1)
        else:
            self._anchor = None

        # Clean up the name, it can come from anywhere.
        # Convert HTML entities to unicode
        t = html2unicode(self._text)

        #t = str( t, encoding='utf8' )

        # Convert URL-encoded characters to unicode
        #t = url2unicode(t, site=self._source)

        # Normalize unicode string to a NFC (composed) format to allow
        # proper string comparisons. According to
        # http://svn.wikimedia.org/viewvc/mediawiki/branches/REL1_6/phase3/includes/normal/UtfNormal.php?view=markup
        # the mediawiki code normalizes everything to NFC, not NFKC
        # (which might result in information loss).
        t = unicodedata.normalize('NFC', t)

        # This code was adapted from Title.php : secureAndSplit()
        #
        if '\ufffd' in t:
            raise Error(
                "Title contains illegal char (\\uFFFD 'REPLACEMENT CHARACTER')")

        # Replace underscores by spaces
        t = t.replace("_", " ")
        # replace multiple spaces with a single space
        while "  " in t:
            t = t.replace("  ", " ")
        # Strip spaces at both ends
        t = t.strip()
        # Remove left-to-right and right-to-left markers.
        t = t.replace("\u200e", "").replace("\u200f", "")
        self._text = t

    def __repr__(self):
        return "page.Link(%r, %r)" % (self.title, self.site)

    def parse_site(self):
        """Parse only enough text to determine which site the link points to.

        This method does not parse anything after the first ":"; links
        with multiple interwiki prefixes (such as "wikt:fr:Parlais") need
        to be re-parsed on the first linked wiki to get the actual site.

        @return: tuple of (familyname, languagecode) for the linked site.

        """
        t = str(self._text)
        fam = self._source.family
        code = self._source.code
        while ":" in t:
            # Initial colon
            if t.startswith(":"):
                # remove the colon but continue processing
                # remove any subsequent whitespace
                t = t.lstrip(":").lstrip(" ")
                continue
            prefix = t[:t.index(":")].lower()  # part of text before :
            ns = self._source.ns_index(prefix)
            if ns:
                # The prefix is a namespace in the source wiki
                return (fam.name, code)
            if prefix in fam.langs:
                # prefix is a language code within the source wiki family
                return (fam.name, prefix)
            known = fam.get_known_families(site=self._source)
            if prefix in known:
                if known[prefix] == fam.name:
                    # interwiki prefix links back to source family
                    t = t[t.index(":") + 1:].lstrip(" ")
                    # strip off the prefix and retry
                    continue
                # prefix is a different wiki family
                return (known[prefix], code)
            break
        return (fam.name, code)  # text before : doesn't match any known prefix

    def parse(self):
        """Parse text; called internally when accessing attributes"""

        self._site = self._source
        self._namespace = self._defaultns
        t = str(self._text)

        # This code was adapted from Title.php : secureAndSplit()
        #
        firstPass = True
        while ":" in t:
            # Initial colon indicates main namespace rather than default
            if t.startswith(":"):
                self._namespace = 0
                # remove the colon but continue processing
                # remove any subsequent whitespace
                t = t.lstrip(":").lstrip(" ")
                continue

            fam = self._site.family
            prefix = t[:t.index(":")].lower()

            encprefix = tryencode(prefix)

            debugprint("parse T"  + tryencode(t))
            debugprint("parse Fam"  + tryencode(fam))
            debugprint("parse prefix"  + tryencode(prefix))

            debugprint("parse|"  + "|".join([
                tryencode(t),
                tryencode(fam.__repr__()),
                #str(prefix,"utf-8")
                tryencode(encprefix )
            ]
            )
            )
            debugprint ("parse site: %s " % self._site)
            debugprint ("parse site: %s " % type(self._site))
            ns = self._site.ns_index(prefix)
            if ns:
                # Ordinary namespace
                t = t[t.index(":"):].lstrip(":").lstrip(" ")
                self._namespace = ns

                debugprint("parse T"  + tryencode(t))
                debugprint("parse Fam"  + tryencode(fam))
                debugprint("parse prefix"  + tryencode(prefix))
                debugprint("parse ns"  + tryencode(ns))

                break
            if prefix in list(fam.langs.keys())\
                    or prefix in fam.get_known_families(site=self._site):
                # looks like an interwiki link
                if not firstPass:
                    # Can't make a local interwiki link to an interwiki link.
                    raise Error(
                        "Improperly formatted interwiki link '%s'"
                        % self._text)
                t = t[t.index(":"):].lstrip(":").lstrip(" ")
                if prefix in list(fam.langs.keys()):
                    newsite = BaseSite(prefix, fam)
                else:
                    otherlang = self._site.code
                    familyName = fam.get_known_families(site=self._site)[prefix]

                    debugprint("LANG T:" +  t)
                    debugprint("LANG FAM:" +fam.__repr__())
                    debugprint("LANG PREFIX:" +tryencode(prefix))
                    debugprint("LANG NS" +tryencode(ns))
                    debugprint("LANG FAM" +tryencode(familyName))
                    debugprint("LANG LANG Keys" +            str(list(fam.langs.keys())))
                    debugprint("LANG SITE" +tryencode(self._site.code))

                    if familyName in ['commons', 'meta']:
                        otherlang = familyName
                    try:
                        newsite = BaseSite(otherlang, familyName)
                    except ValueError:
                        raise Error(
                            """\
%s is not a local page on %s, and the %s family is
not supported by PyWikiBot!"""
                            % (self._text, self._site, familyName))

                # Redundant interwiki prefix to the local wiki
                if newsite == self._site:
                    if not t:
                        # Can't have an empty self-link
                        raise Error(
                            "Invalid link title: '%s'" % self._text)
                    firstPass = False
                    continue
                self._site = newsite
            else:
                break   # text before : doesn't match any known prefix

        if "#" in t:
            t, sec = t.split('#', 1)
            t, self._section = t.rstrip(), sec.lstrip()
        else:
            self._section = None

        # Reject illegal characters.
        m = Link.illegal_titles_pattern.search(t)
        if m:
            raise InvalidTitle(
                "contains illegal char(s) '%s'" % m.group(0))

        # Pages with "/./" or "/../" appearing in the URLs will
        # often be unreachable due to the way web browsers deal
        #* with 'relative' URLs. Forbid them explicitly.

        if '.' in t and (
                t == '.' or t == '..'
                or t.startswith("./")
                or t.startswith("../")
                or "/./" in t
                or "/../" in t
                or t.endswith("/.")
                or t.endswith("/..")
        ):
            raise InvalidTitle(
                "(contains . / combinations): '%s'"
                % self._text)

        # Magic tilde sequences? Nu-uh!
        if "~~~" in t:
            raise InvalidTitle("(contains ~~~): '%s'" % self._text)

        if self._namespace != -1 and len(t) > 255:
            raise InvalidTitle("(over 255 bytes): '%s'" % t)

        if self._site.case() == 'first-letter':
            t = t[:1].upper() + t[1:]

        # Can't make a link to a namespace alone...
        # "empty" local links can only be self-links
        # with a fragment identifier.
        if not t and self._site == self._source and self._namespace != 0:
            raise Error("Invalid link (no page title): '%s'"
                                  % self._text)

        self._title = t

    # define attributes, to be evaluated lazily

    @property
    def site(self):
        if not hasattr(self, "_site"):
            self.parse()
        return self._site

    @property
    def namespace(self):
        if not hasattr(self, "_namespace"):
            self.parse()
        return self._namespace

    @property
    def title(self):
        if not hasattr(self, "_title"):
            self.parse()
        return self._title

    @property
    def section(self):
        if not hasattr(self, "_section"):
            self.parse()
        return self._section

    @property
    def anchor(self):
        if not hasattr(self, "_anchor"):
            self.parse()
        return self._anchor

    def canonical_title(self):
        """Return full page title, including localized namespace."""
        if self.namespace:
            return "%s:%s" % (self.site.namespace(self.namespace),
                              self.title)
        else:
            return self.title

    def astext(self, onsite=None):
        """Return a text representation of the link.

        @param onsite: if specified, present as a (possibly interwiki) link
            from the given site; otherwise, present as an internal link on
            the source site.

        """
        if onsite is None:
            onsite = self._source
        title = self.title
        if self.namespace:
            title = onsite.namespace(self.namespace) + ":" + title
        if self.section:
            title = title + "#" + self.section
        if onsite == self.site:
            return '[[%s]]' % title
        if onsite.family == self.site.family:
            return '[[%s:%s]]' % (self.site.code, title)
        if self.site.family.name == self.site.code:
            # use this form for sites like commons, where the
            # code is the same as the family name
            return '[[%s:%s]]' % (self.site.code,
                                   title)
        return '[[%s:%s:%s]]' % (self.site.family.name,
                                  self.site.code,
                                  title)

    def __str__(self):
#        return self.astext().encode("ascii", "backslashreplace")
        val= self.astext()
#        debugprint(val)
#        debugprint("%s" % val)
        return val

    def __cmp__(self, other):
        """Test for equality and inequality of Link objects.

        Link objects are "equal" if and only if they are on the same site
        and have the same normalized title, including section if any.

        Link objects are sortable by site, then namespace, then title.

        """
        if not isinstance(other, Link):
            # especially, return -1 if other is None
            return -1
        if not self.site == other.site:
            return self.__lt__(self.site, other.site)
        if self.namespace != other.namespace:
            return self.__lt__(self.namespace, other.namespace)
        return self.__lt__(self.title, other.title)

    def __unicode__(self):
        return self.astext()

    def __hash__(self):
        return hash('%s:%s:%s' % (self.site.family.name,
                                   self.site.code,
                                   self.title))

    @staticmethod
    def fromPage(page, source=None):
        """
        Create a Link to a Page.
        @param source: Link from site source
        """

        link = Link.__new__(Link)
        link._site = page.site
        link._section = page.section()
        link._namespace = page.namespace()
        link._title = page.title(withNamespace=False,
                                 allowInterwiki=False,
                                 withSection=False)
        link._anchor = None
        link._source = source or BaseSite()

        return link

    @staticmethod
    def langlinkUnsafe(lang, title, source):
        """
        Create a "lang:title" Link linked from source.
        Assumes that the lang & title come clean, no checks are made.
        """
        link = Link.__new__(Link)
        link._site = BaseSite(lang, source.family.name)
        link._section = None
        link._source = source

        link._namespace = 0

        if ':' in title:
            ns, t = title.split(':', 1)
            ns = link._site.ns_index(ns.lower())
            if ns:
                link._namespace = ns
                title = t
        if "#" in title:
            t, sec = title.split('#', 1)
            title, link._section = t.rstrip(), sec.lstrip()
        else:
            link._section = None
        link._title = title
        return link
