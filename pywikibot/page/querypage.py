
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

class QueryPage(WikibasePage):
    """
    For future usage, not implemented yet
    """
    def __init__(self, site, title):
        WikibasePage.__init__(self, site, title, ns=122)
        self.id = self.title(withNamespace=False).upper()
        if not self.id.startswith('U'):
            raise ValueError("'%s' is not a query page!" % self.title())
