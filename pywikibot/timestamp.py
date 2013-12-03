import datetime
import difflib
#import logging
import math
import re
#import sys
import threading
from queue import Queue

# Use pywikibot. prefix for all in-package imports; this is to prevent
# confusion with similarly-named modules in version 1 framework, for users
# who want to continue using both

import pywikibot
from pywikibot import config2 as config
from pywikibot.bot import warning, output, inputChoice, debug
#from pywikibot.exceptions import *
#from pywikibot.textlib import *
#from pywikibot.i18n import translate

class Timestamp(datetime.datetime):
    """Class for handling Mediawiki timestamps.

    This inherits from datetime.datetime, so it can use all of the methods
    and operations of a datetime object.  To ensure that the results of any
    operation are also a Timestamp object, be sure to use only Timestamp
    objects (and datetime.timedeltas) in any operation.

    Use Timestamp.fromISOformat() and Timestamp.fromtimestampformat() to
    create Timestamp objects from Mediawiki string formats.

    Use Site.getcurrenttime() for the current time; this is more reliable
    than using Timestamp.utcnow().

    """
    mediawikiTSFormat = "%Y%m%d%H%M%S"
    ISO8601Format = "%Y-%m-%dT%H:%M:%SZ"

    @classmethod
    def fromISOformat(cls, ts):
        """Convert an ISO 8601 timestamp to a Timestamp object."""
        return cls.strptime(ts, cls.ISO8601Format)

    @classmethod
    def fromtimestampformat(cls, ts):
        """Convert the internal MediaWiki timestamp format to a Timestamp object."""
        return cls.strptime(ts, cls.mediawikiTSFormat)

    def toISOformat(self):
        """Converts the Timestamp object to an ISO 8601 timestamp"""
        return self.strftime(self.ISO8601Format)

    def totimestampformat(self):
        """Converts the Timestamp object to the internal MediaWiki timestamp format."""
        return self.strftime(self.mediawikiTSFormat)

    def __str__(self):
        """Return a string format recognized by the API"""
        return self.toISOformat()

    def __add__(self, other):
        newdt = datetime.datetime.__add__(self, other)
        if isinstance(newdt, datetime.datetime):
            return Timestamp(newdt.year, newdt.month, newdt.day, newdt.hour,
                             newdt.minute, newdt.second, newdt.microsecond,
                             newdt.tzinfo)
        else:
            return newdt

    def __sub__(self, other):
        newdt = datetime.datetime.__sub__(self, other)
        if isinstance(newdt, datetime.datetime):
            return Timestamp(newdt.year, newdt.month, newdt.day, newdt.hour,
                             newdt.minute, newdt.second, newdt.microsecond,
                             newdt.tzinfo)
        else:
            return newdt
