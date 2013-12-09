#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Library to log the robot in to a wiki account.
"""
#
# (C) Rob W.W. Hooft, 2003
# (C) Pywikibot team, 2003-2012
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

#import logging
#import pywikibot
#from 
import pywikibot.page 
from pywikibot.deprecate import deprecate_arg
#from pywikibot.deprecate import deprecate_arg
from pywikibot.exceptions import NoUsername
from pywikibot.bot import debug, log,  user_input, error
# NoSuchSite, 

#import pywikibot.config2 as config

# On some wikis you are only allowed to run a bot if there is a link to
# the bot's user page in a specific list.
# If bots are listed in a template, the templates name must be given as
# second parameter, otherwise it must be None


class LoginManager(object):
    @deprecate_arg("username", "user")
    @deprecate_arg("verbose", None)
    def __init__(self, password=None, sysop=False, site=None, user=None):
        self._logger = "wiki.login"
        self.botList = {
            'wikipedia': {
                'en': ['Wikipedia:Bots/Status/active bots', 'BotS'],
                'simple': ['Wikipedia:Bots', '/links']
            },
            'gentoo': {
                'en': ['Help:Bots', None],
            }
        }

        if site is not None:
            self._site = site
        else:
            self._site = pywikibot.Site()
        if user:
            self._username = user
        elif sysop:
            try:
                self._username = config.sysopnames[
                    self._site.family.name][self._site.code]
            except KeyError:
                raise NoUsername(
"""ERROR: Sysop username for %(fam_name)s:%(wiki_code)s is undefined.
If you have a sysop account for that site, please add a line to user-config.py:

sysopnames['%(fam_name)s']['%(wiki_code)s'] = 'myUsername'"""
                    % {'fam_name': self._site.family.name,
                       'wiki_code': self._site.code})
        else:
            try:
                self._username = config.usernames[
                    self._site.family.name][self._site.code]
            except:
                raise NoUsername(
"""ERROR: Username for %(fam_name)s:%(wiki_code)s is undefined.
If you have an account for that site, please add a line to user-config.py:

usernames['%(fam_name)s']['%(wiki_code)s'] = 'myUsername'"""
                    % {'fam_name': self._site.family.name,
                       'wiki_code': self._site.code})
        self._password = password
        if getattr(config, 'password_file', ''):
            self.readPassword()

    @property
    def site(self):
        return self._site

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username

    def get_site(self):
        return self._site

    def get_password(self):
        return self._password

    def get_username(self):
        return self._username

    def botAllowed(self):
        """
        Checks whether the bot is listed on a specific page to comply with
        the policy on the respective wiki.
        """
        if self._site.family.name in self.botList \
                and self._site.code in self.botList[self._site.family.name]:
            botListPageTitle, botTemplate = self.botList[
                self._site.family.name][self._site.code]
            botListPage = Page(self._site, botListPageTitle)
            if botTemplate:
                for template in botListPage.templatesWithParams():
                    if template[0] == botTemplate \
                       and template[1][0] == self._username:
                        return True
            else:
                for linkedPage in botListPage.linkedPages():
                    if linkedPage.title(withNamespace=False) == self._username:
                        return True
            return False
        else:
            # No bot policies on other sites
            return True

    def getCookie(self, remember=True, captcha=None):
        """
        Login to the site.

        remember    Remember login (default: True)
        captchaId   A dictionary containing the captcha id and answer, if any

        Returns cookie data if succesful, None otherwise.
        """
        # NOT IMPLEMENTED - see data/api.py for implementation

    def storecookiedata(self, data):
        """
        Store cookie data.

        The argument data is the raw data, as returned by getCookie().

        Returns nothing.
        """
        # THIS IS OVERRIDDEN IN data/api.py
        filename = config.datafilepath('pywikibot.lwp')
        debug("Storing cookies to %s" % filename,
                        _logger)
        f = open(filename, 'w')
        f.write(data)
        f.close()

    def readPassword(self):
        """
        Read passwords from a file.

        DO NOT FORGET TO REMOVE READ ACCESS FOR OTHER USERS!!!
        Use chmod 600 password-file.

        All lines below should be valid Python tuples in the form
        (code, family, username, password) or (username, password)
        to set a default password for an username. Default usernames
        should occur above specific usernames.

        If the username or password contain non-ascii characters, they
        should be stored using the utf-8 encoding.

        Example:

        (u"my_username", u"my_default_password")
        (u"my_sysop_user", u"my_sysop_password")
        (u"en", u"wikipedia", u"my_en_user", u"my_en_pass")
        """
        password_f = open(config.password_file)
        for line in password_f:
            if not line.strip():
                continue
            entry = eval(line.decode('utf-8'))
            if len(entry) == 2:    # for default userinfo
                if entry[0] == self._username:
                    self._password = entry[1]
            elif len(entry) == 4:  # for userinfo included code and family
                if entry[0] == self._site.code and \
                   entry[1] == self._site.family.name and \
                   entry[2] == self._username:
                    self._password = entry[3]
        password_f.close()

    def login(self, retry=False):
        if not self._password:
            # As we don't want the password to appear on the screen, we set
            # password = True
            self._password = user_input(
                'Password for user %(name)s on %(site)s (no characters will be shown):'
                % {'name': self._username, 'site': self._site},
                password=True)
#        self.password = self.password.encode(self._site.encoding())

        pywikibot.output("Logging in to %(site)s as %(name)s"
                         % {'name': self._username, 'site': self._site})
        try:
            cookiedata = self.getCookie()
        except pywikibot.data.api.APIError as e:
            error("Login failed (%s)." % e.code)
            if retry:
                self._password = None
                return self.login(retry=True)
            else:
                return False
        self.storecookiedata(cookiedata)
        log("Should be logged in now")
##        # Show a warning according to the local bot policy
##   FIXME: disabled due to recursion; need to move this to the Site object after
##   login
##        if not self.botAllowed():
##            logger.error(
##                u"Username '%(name)s' is not listed on [[%(page)s]]."
##                 % {'name': self.username,
##                    'page': botList[self._site.family.name][self._site.code]})
##            logger.error(
##"Please make sure you are allowed to use the robot before actually using it!")
##            return False
        return True

    def showCaptchaWindow(self, url):
        pass
