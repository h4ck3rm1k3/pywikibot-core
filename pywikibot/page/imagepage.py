
import pywikibot
from pywikibot import deprecate_arg
from pywikibot import deprecated
from pywikibot import config
import pywikibot.site

import hashlib
import html.entities 
import logging
import re
import unicodedata
import urllib
import collections

class ImagePage(Page):
    """A subclass of Page representing an image descriptor wiki page.

    Supports the same interface as Page, with the following added methods:

    getImagePageHtml          : Download image page and return raw HTML text.
    fileURL                   : Return the URL for the image described on this
                                page.
    fileIsShared              : Return True if image stored on a shared
                                repository like Wikimedia Commons or Wikitravel.
    getFileMd5Sum             : Return image file's MD5 checksum.
    getFileVersionHistory     : Return the image file's version history.
    getFileVersionHistoryTable: Return the version history in the form of a
                                wiki table.
    usingPages                : Iterate Pages on which the image is displayed.

    """
    def __init__(self, source, title="", insite=None):
        Page.__init__(self, source, title, 6)
        if self.namespace() != 6:
            raise ValueError("'%s' is not in the image namespace!" % title)

    def getImagePageHtml(self):
        """
        Download the image page, and return the HTML, as a unicode string.

        Caches the HTML code, so that if you run this method twice on the
        same ImagePage object, the page will only be downloaded once.
        """
        if not hasattr(self, '_imagePageHtml'):
            path = "%s/index.php?title=%s" \
                   % (self.site.scriptpath(), self.title(asUrl=True))
            self._imagePageHtml = pywikibot.comms.pybothttp.request(self.site, path)
        return self._imagePageHtml

    def fileUrl(self):
        """Return the URL for the image described on this page."""
        # TODO add scaling option?
        if not hasattr(self, '_imageinfo'):
            self._imageinfo = self.site.loadimageinfo(self)
        return self._imageinfo['url']

    @deprecated("fileIsShared")
    def fileIsOnCommons(self):
        """Return True if the image is stored on Wikimedia Commons"""
        return self.fileIsShared()

    def fileIsShared(self):
        """Return True if image is stored on any known shared repository."""
        # as of now, the only known repositories are commons and wikitravel
        # TODO: put the URLs to family file
        if not self.site.has_image_repository:
            return False
        elif 'wikitravel_shared' in self.site.shared_image_repository():
            return self.fileUrl().startswith(
                'http://wikitravel.org/upload/shared/')
        else:
            return self.fileUrl().startswith(
                'http://upload.wikimedia.org/wikipedia/commons/')

    @deprecated("ImagePage.getFileSHA1Sum()")
    def getFileMd5Sum(self):
        """Return image file's MD5 checksum."""
# FIXME: MD5 might be performed on incomplete file due to server disconnection
# (see bug #1795683).
        f = urllib.request.urlopen(self.fileUrl())
        # TODO: check whether this needs a User-Agent header added
        h = hashlib.md5()
        h.update(f.read())
        md5Checksum = h.hexdigest()
        f.close()
        return md5Checksum

    def getFileSHA1Sum(self):
        """Return image file's SHA1 checksum."""
        if not hasattr(self, '_imageinfo'):
            self._imageinfo = self.site.loadimageinfo(self)
        return self._imageinfo['sha1']

    def getFileVersionHistory(self):
        """Return the image file's version history.

        @return: An iterator yielding tuples containing (timestamp,
            username, resolution, filesize, comment).

        """
        #TODO; return value may need to change
        return self.site.loadimageinfo(self, history=True)

    def getFileVersionHistoryTable(self):
        """Return the version history in the form of a wiki table."""
        lines = []
        #TODO: if getFileVersionHistory changes, make sure this follows it
        for (datetime, username, resolution, size, comment) \
                in self.getFileVersionHistory():
            lines.append('| %s || %s || %s || %s || <nowiki>%s</nowiki>'
                         % (datetime, username, resolution, size, comment))
        return '{| border="1"\n! date/time || username || resolution || size || edit summary\n|----\n' + \
               '\n|----\n'.join(lines) + '\n|}'

    def usingPages(self, step=None, total=None, content=False):
        """Yield Pages on which the image is displayed.

        @param step: limit each API call to this number of pages
        @param total: iterate no more than this number of pages in total
        @param content: if True, load the current content of each iterated page
            (default False)

        """
        return self.site.imageusage(
            self, step=step, total=total, content=content)
