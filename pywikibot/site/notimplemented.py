# -*- coding: utf-8  -*-
"""
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
#import datetime
#import itertools
import os
#import re
#import sys
#import threading
#import time
#import urllib.request, urllib.parse, urllib.error
#import json

import pywikibot
#from pywikibot.deprecate import deprecate_arg
from pywikibot import config
#from pywikibot.deprecate import deprecated
#from pywikibot.bot import log
#from pywikibot import pagegenerators
#from pywikibot.throttle import Throttle
#from pywikibot.data import api
#import pywikibot.data.api as api
#from pywikibot.exceptions import NoSuchSite, Error, UserBlocked,NoPage,NoUsername,EditConflict, SpamfilterError, LockedPage
from pywikibot.exceptions import NoUsername

#from pywikibot.deprecate import deprecated
#from pywikibot.deprecate import deprecate_arg


_logger = "wiki.site"

#### METHODS NOT IMPLEMENTED YET ####
class NotImplementedYet:
    def __init__(self):
        self._cookies=None
        self._isLoggedIn=None
        #self._userIndex=None
        self.family=None
        self.code=None

    def _userIndex(self,sysop):
        pass

    #TODO: is this needed any more? can it be obtained from the http module?
    def cookies(self, sysop=False):
        """Return a string containing the user's current cookies."""
        self._loadCookies(sysop=sysop)
        index = self._userIndex(sysop)
        return self._cookies[index]

    def _loadCookies(self, sysop=False):
        """Retrieve session cookies for login"""
        index = self._userIndex(sysop)
        if self._cookies[index] is not None:
            return
        try:
            if sysop:
                try:
                    username = config.sysopnames[self.family.name][self.code]
                except KeyError:
                    raise NoUsername("""\
You tried to perform an action that requires admin privileges, but you haven't
entered your sysop name in your user-config.py. Please add
sysopnames['%s']['%s']='name' to your user-config.py"""
                                     % (self.family.name, self.code))
            else:
                username = pywikibot.config2.usernames[self.family.name
                                                       ][self.code]
        except KeyError:
            self._cookies[index] = None
            self._isLoggedIn[index] = False
        else:
            tmp = '%s-%s-%s-login.data' % (self.family.name, self.code,
                                           username)
            fn = config.datafilepath('login-data', tmp)
            if not os.path.exists(fn):
                self._cookies[index] = None
                self._isLoggedIn[index] = False
            else:
                f = open(fn)
                self._cookies[index] = '; '.join([x.strip()
                                                  for x in f.readlines()])
                f.close()
