
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

class User(Page):
    """A class that represents a Wiki user.
    """

    @deprecate_arg("site", "source")
    @deprecate_arg("name", "title")
    def __init__(self, source, title=''):
        """Initializer for a User object.
        All parameters are the same as for Page() constructor.
        """
        if len(title) > 1 and title[0] == '#':
            self._isAutoblock = True
            title = title[1:]
        else:
            self._isAutoblock = False
        Page.__init__(self, source, title, ns=2)
        if self.namespace() != 2:
            raise ValueError("'%s' is not in the user namespace!"
                             % title)
        if self._isAutoblock:
            # This user is probably being queried for purpose of lifting
            # an autoblock.
            output(
                "This is an autoblock ID, you can only use to unblock it.")

    def name(self):
        return self.username

    @property
    def username(self):
        """ Convenience method that returns the title of the page with
        namespace prefix omitted, aka the username, as a Unicode string.
        """
        if self._isAutoblock:
            return '#' + self.title(withNamespace=False)
        else:
            return self.title(withNamespace=False)

    def isRegistered(self, force=False):
        """ Return True if a user with this name is registered on this site,
        False otherwise.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        if self.isAnonymous():
            return False
        else:
            return self.getprops(force).get('missing') is None

    def isAnonymous(self):
        return ip_regexp.match(self.username) is not None

    def getprops(self, force=False):
        """ Return a Dictionary that contains user's properties. Use cached
        values if already called before, otherwise fetch data from the API.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        if force:
            del self._userprops
        if not hasattr(self, '_userprops'):
            self._userprops = list(self.site.users([self.username, ]))[0]
            if self.isAnonymous():
                r = list(self.site.blocks(users=self.username))
                if r:
                    self._userprops['blockedby'] = r[0]['by']
                    self._userprops['blockreason'] = r[0]['reason']
        return self._userprops

    @deprecated('User.registration()')
    def registrationTime(self, force=False):
        """ Return registration date for this user, as a long in
        Mediawiki's internal timestamp format, or 0 if the date is unknown.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        if self.registration():
            return int(self.registration().strftime('%Y%m%d%H%M%S'))
        else:
            return 0

    def registration(self, force=False):
        """ Return registration date for this user as a Timestamp
        object, or None if the date is unknown.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        reg = self.getprops(force).get('registration')
        if reg:
            return pywikibot.Timestamp.fromISOformat(reg)

    def editCount(self, force=False):
        """ Return edit count for this user as int. This is always 0 for
        'anonymous' users.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        if 'editcount' in self.getprops(force):
            return self.getprops()['editcount']
        else:
            return 0

    def isBlocked(self, force=False):
        """ Return True if this user is currently blocked, False otherwise.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        return 'blockedby' in self.getprops(force)

    def isEmailable(self, force=False):
        """ Return True if emails can be send to this user through mediawiki,
        False otherwise.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        return 'emailable' in self.getprops(force)

    def groups(self, force=False):
        """ Return a list of groups to wich this user belongs. The return value
        is guaranteed to be a list object, possibly empty.

        @param force: if True, forces reloading the data from API
        @type force: bool
        """
        if 'groups' in self.getprops(force):
            return self.getprops()['groups']
        else:
            return []

    def getUserPage(self, subpage=''):
        """ Return a Page object corresponding to this user's main
        page, or a subpage of it if subpage is set.

        @param subpage: subpage part to be appended to the main
                            page title (optional)
        @type subpage: unicode
        """
        if self._isAutoblock:
            #This user is probably being queried for purpose of lifting
            #an autoblock, so has no user pages per se.
            raise AutoblockUser(
                "This is an autoblock ID, you can only use to unblock it.")
        if subpage:
            subpage = '/' + subpage
        return Page(Link(self.title() + subpage, self.site))

    def getUserTalkPage(self, subpage=''):
        """ Return a Page object corresponding to this user's main
        talk page, or a subpage of it if subpage is set.

        @param subpage: subpage part to be appended to the main
                            talk page title (optional)
        @type subpage: unicode
        """
        if self._isAutoblock:
            #This user is probably being queried for purpose of lifting
            #an autoblock, so has no user talk pages per se.
            raise AutoblockUser(
                "This is an autoblock ID, you can only use to unblock it.")
        if subpage:
            subpage = '/' + subpage
        return Page(Link(self.title(withNamespace=False) + subpage,
                         self.site, defaultNamespace=3))

    def sendMail(self, subject, text, ccme=False):
        """ Send an email to this user via mediawiki's email interface.
        Return True on success, False otherwise.
        This method can raise an UserActionRefuse exception in case this user
        doesn't allow sending email to him or the currently logged in bot
        doesn't have the right to send emails.

        @param subject: the subject header of the mail
        @type subject: unicode
        @param text: mail body
        @type text: unicode
        @param ccme: if True, sends a copy of this email to the bot
        @type ccme: bool
        """
        if not self.isEmailable():
            raise UserActionRefuse('This user is not mailable')

        if not self.site.has_right('sendemail'):
            raise UserActionRefuse('You don\'t have permission to send mail')

        params = {
            'action': 'emailuser',
            'target': self.username,
            'token': self.site.token(self, 'email'),
            'subject': subject,
            'text': text,
        }
        if ccme:
            params['ccme'] = 1
        mailrequest = pywikibot.data.api.Request(**params)
        maildata = mailrequest.submit()

        if 'error' in maildata:
            code = maildata['error']['code']
            if code == 'usermaildisabled ':
                output('User mail has been disabled')
        elif 'emailuser' in maildata:
            if maildata['emailuser']['result'] == 'Success':
                output('Email sent.')
                return True
        return False

    def block(self, expiry, reason, anononly=True, nocreate=True,
              autoblock=True, noemail=False, reblock=False):
        """
        Blocks a user
        @param expiry: When the block should expire
        @type expiry: Timestamp|str
        @param reason: Block reason
        @type reason: basestring
        @param anononly: Whether block should only affect anonymous users
        @type anononly: bool
        @param nocreate: Whether to block account creation
        @type nocreate: bool
        @param autoblock: Whether to enable autoblock
        @type autoblock: bool
        @param noemail: Whether to disable email access
        @type noemail: bool
        @param reblock: Whether to reblock if a block already is set
        @type reblock: bool
        @return: None
        """
        try:
            self.site.blockuser(self, expiry, reason, anononly, nocreate,
                                autoblock, noemail, reblock)
        except pywikibot.data.api.APIError as err:
            if err.code == 'invalidrange':
                raise ValueError("%s is not a valid IP range." % self.username)
            else:
                raise err

    @deprecated("contributions")
    @deprecate_arg("limit", "total")  # To be consistent with rest of framework
    def editedPages(self, total=500):
        """ Deprecated function that wraps 'contributions' for backwards
        compatibility. Yields Page objects that this user has
        edited, with an upper bound of 'total'. Pages returned are not
        guaranteed to be unique.

        @param total: limit result to this number of pages.
        @type total: int.
        """
        for item in self.contributions(total=total):
            yield item[0]

    @deprecate_arg("limit", "total")  # To be consistent with rest of framework
    @deprecate_arg("namespace", "namespaces")
    def contributions(self, total=500, namespaces=[]):
        """ Yield tuples describing this user edits with an upper bound of
        'limit'. Each tuple is composed of a Page object,
        the revision id (int), the edit timestamp (as a Timestamp
        object), and the comment (unicode).
        Pages returned are not guaranteed to be unique.

        @param total: limit result to this number of pages
        @type total: int
        @param namespaces: only iterate links in these namespaces
        @type namespaces: list
        """
        for contrib in self.site.usercontribs(
                user=self.username, namespaces=namespaces, total=total):
            ts = pywikibot.Timestamp.fromISOformat(contrib['timestamp'])
            yield (Page(self.site, contrib['title'], contrib['ns']),
                   contrib['revid'],
                   ts,
                   contrib.get('comment', None)
                   )

    @deprecate_arg("number", "total")
    def uploadedImages(self, total=10):
        """ Yield tuples describing files uploaded by this user.
        Each tuple is composed of a Page, the timestamp (str in
        ISO8601 format), comment (unicode) and a bool for pageid > 0.
        Pages returned are not guaranteed to be unique.

        @param total: limit result to this number of pages
        @type total: int
        """
        if not self.isRegistered():
            raise StopIteration
        for item in self.site.logevents(
                logtype='upload', user=self.username, total=total):
            yield (ImagePage(self.site, item.title().title()),
                   str(item.timestamp()),
                   item.comment(),
                   item.pageid() > 0
                   )

