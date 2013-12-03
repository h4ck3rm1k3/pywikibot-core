# Utility functions for parsing page titles

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


def html2unicode(text, ignore=None):
    """Return text, replacing HTML entities by equivalent unicode characters."""
    if ignore is None:
        ignore = []
    # This regular expression will match any decimal and hexadecimal entity and
    # also entities that might be named entities.
    entityR = re.compile(
        r'&(?:amp;)?(#(?P<decimal>\d+)|#x(?P<hex>[0-9a-fA-F]+)|(?P<name>[A-Za-z]+));')
    # These characters are Html-illegal, but sadly you *can* find some of
    # these and converting them to unichr(decimal) is unsuitable
    convertIllegalHtmlEntities = {
        128: 8364,  # €
        130: 8218,  # ‚
        131: 402,   # ƒ
        132: 8222,  # „
        133: 8230,  # …
        134: 8224,  # †
        135: 8225,  # ‡
        136: 710,   # ˆ
        137: 8240,  # ‰
        138: 352,   # Š
        139: 8249,  # ‹
        140: 338,   # Œ
        142: 381,   # Ž
        145: 8216,  # ‘
        146: 8217,  # ’
        147: 8220,  # “
        148: 8221,  # ”
        149: 8226,  # •
        150: 8211,  # –
        151: 8212,  # —
        152: 732,   # ˜
        153: 8482,  # ™
        154: 353,   # š
        155: 8250,  # ›
        156: 339,   # œ
        158: 382,   # ž
        159: 376    # Ÿ
    }
    #ensuring that illegal &#129; &#141; and &#157, which have no known values,
    #don't get converted to unichr(129), unichr(141) or unichr(157)
    ignore = set(ignore) | set([129, 141, 157])
    result = ''
    i = 0
    found = True
    while found:
        text = text[i:]
        match = entityR.search(text)
        if match:
            unicodeCodepoint = None
            if match.group('decimal'):
                unicodeCodepoint = int(match.group('decimal'))
            elif match.group('hex'):
                unicodeCodepoint = int(match.group('hex'), 16)
            elif match.group('name'):
                name = match.group('name')
                if name in html.entities.name2codepoint:
                    # We found a known HTML entity.
                    unicodeCodepoint = html.entities.name2codepoint[name]
            result += text[:match.start()]
            try:
                unicodeCodepoint = convertIllegalHtmlEntities[unicodeCodepoint]
            except KeyError:
                pass
            if unicodeCodepoint and unicodeCodepoint not in ignore:
                result += chr(unicodeCodepoint)
            else:
                # Leave the entity unchanged
                result += text[match.start():match.end()]
            i = match.end()
        else:
            result += text
            found = False
    return result


def unicode2html(x, encoding):
    """
    Ensure unicode string is encodable, or else convert to ASCII for HTML.
    Arguments are a unicode string and an encoding. Attempt to encode the
    string into the desired format; if that doesn't work, encode the unicode
    into html &#; entities. If it does work, return it unchanged.
    """
    # try:
    x.encode(encoding)
    # except UnicodeError:
    #     x = UnicodeToAsciiHtml(x)
    return x


def url2unicode(title, site, site2=None):
    """Convert url-encoded text to unicode using site's encoding.

    If site2 is provided, try its encodings as well.  Uses the first encoding
    that doesn't cause an error.

    """
    # create a list of all possible encodings for both hint sites
    encList = [site.encoding()] + list(site.encodings())
    if site2 and site2 != site:
        encList.append(site2.encoding())
        encList += list(site2.encodings())
    firstException = UnicodeError()
    # try to handle all encodings (will probably retry utf-8)
    for enc in encList:
        try:
            t = title.encode(enc)
            t = str( t, encoding='utf8' )
            print(t)
            t = urllib.parse.unquote(t)
            return str(t, enc)
        except UnicodeError as ex:
            if not firstException:
                firstException = ex
            pass
    # Couldn't convert, raise the original exception
    raise firstException
