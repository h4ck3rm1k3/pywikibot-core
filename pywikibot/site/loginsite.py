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
import datetime
import itertools
import os
import re
import sys
import threading
import time
import urllib.request, urllib.parse, urllib.error
import json

import pywikibot
#from pywikibot import deprecate_arg
from pywikibot import config
#from pywikibot import deprecated
from pywikibot.bot import log
#from pywikibot import pagegenerators
from pywikibot.throttle import Throttle
from pywikibot.data import api
#import pywikibot.data.api as api
from pywikibot.exceptions import NoSuchSite, Error, UserBlocked,NoPage,NoUsername,EditConflict, SpamfilterError, LockedPage

from pywikibot.deprecate import deprecated
from pywikibot.deprecate import deprecate_arg


_logger = "wiki.site"

class LoginStatus(object):
    """ Enum for Login statuses.

    >>> LoginStatus.NOT_ATTEMPTED
    -3
    >>> LoginStatus.AS_USER
    0
    >>> LoginStatus.name(-3)
    'NOT_ATTEMPTED'
    >>> LoginStatus.name(0)
    'AS_USER'
    """
    NOT_ATTEMPTED = -3
    IN_PROGRESS = -2
    NOT_LOGGED_IN = -1
    AS_USER = 0
    AS_SYSOP = 1

    @classmethod
    def name(cls, search_value):
        for key, value in list(cls.__dict__.items()):
            if key == key.upper() and value == search_value:
                return key
        raise KeyError("Value %r could not be found in this enum"
                       % search_value)



