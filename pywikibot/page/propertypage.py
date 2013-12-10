
#import pywikibot
#from pywikibot.deprecate import deprecate_arg
#from pywikibot.deprecate import deprecated
#from pywikibot import config
#import pywikibot.site
#import hashlib
#import html.entities 
#import logging
#import re
#import unicodedata
#import urllib
#import collections

from pywikibot.page.wikibasepage  import WikibasePage
class PropertyPage(WikibasePage):
    """
    Any page in the property namespace
    Should be created as:
        PropertyPage(DataSite, 'Property:P21')
    """
    def __init__(self, source, title=""):
        """
        @param source: data repository property is on
        @type source: site.DataSite
        @param title: page name of property, like "Property:P##"
        """
        WikibasePage.__init__(self, source, title, ns=120)
        self.id = self.title(withNamespace=False).upper()
        if not self.id.startswith('P'):
            raise ValueError("'%s' is not a property page!" % self.title())

    def get(self, force=False, *args):
        if force or not hasattr(self, '_content'):
            WikibasePage.get(self, force=force, *args)
        self.type = self._content['datatype']

    def getType(self):
        """
        Returns the type that this item uses
        Examples: item, commons media file, StringValue, NumericalValue
        """
        if not hasattr(self, 'type'):
            self.type = self.repo.getPropertyType(self)
        return self.type

    def newClaim(self, *args, **kwargs):
        """
        Convenicence function to create a new claim object
        for a specific property
        @return: Claim
        """
        from pywikibot.page.claimpage  import Claim
        return Claim(self.site, self.getID(), *args, **kwargs)

