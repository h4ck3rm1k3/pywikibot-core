
import pywikibot
from pywikibot.deprecate import deprecate_arg
from pywikibot.deprecate import deprecated
from pywikibot import config
import pywikibot.site
import hashlib
import html.entities 
import logging
import re
import unicodedata
import urllib
import collections
from pywikibot.site.apisite import APISite
from pywikibot.page.wikibasepage  import WikibasePage
class ItemPage(WikibasePage):
    def __init__(self, site, title=None):
        """
        defined by qid XOR site AND title
        @param site: data repository
        @type site: site.DataSite
        @param title: id number of item, "Q###"
        """
        super(ItemPage, self).__init__(site, title, ns=0)
        self.id = title.upper()  # This might cause issues if not ns0?

    @classmethod
    def fromPage(cls, page):
        """
        Get the ItemPage based on a Page that links to it
        @param page: Page
        @return: ItemPage
        """
        repo = page.site.data_repository()
        if hasattr(page,
                   '_pageprops') and page.properties().get('wikibase_item'):
            # If we have already fetched the pageprops for something else,
            # we already have the id, so use it
            return cls(repo, page.properties().get('wikibase_item'))
        i = cls(repo, 'null')
        del i.id
        i._site = page.site
        i._title = page.title()
        return i

    def __make_site(self, dbname):
        """
        Converts a Site.dbName() into a Site object.
        Rather hackish method that only works for WMF sites
        """
        lang = dbname.replace('wiki', '')
        lang = lang.replace('_', '-')
        return pywikibot.Site(lang, 'wikipedia')

    def get(self, force=False, *args):
        """
        Fetches all page data, and caches it
        force will override caching
        args are the values of props
        """
        super(ItemPage, self).get(force=force, *args)

        #claims
        self.claims = {}
        if 'claims' in self._content:
            for pid in self._content['claims']:
                self.claims[pid] = list()
                for claim in self._content['claims'][pid]:
                    c = Claim.fromJSON(self.repo, claim)
                    c.on_item = self
                    self.claims[pid].append(c)

        #sitelinks
        self.sitelinks = {}
        if 'sitelinks' in self._content:
            for dbname in self._content['sitelinks']:
                # Due to issues with locked/obsolete sites
                # this part is commented out
##                site = self.__make_site(dbname)
##                self.sitelinks[site] = Page(
##                    site, self._content['sitelinks'][dbname]['title'])
                self.sitelinks[dbname] = self._content[
                    'sitelinks'][dbname]['title']

        return {'aliases': self.aliases,
                'labels': self.labels,
                'descriptions': self.descriptions,
                'sitelinks': self.sitelinks,
                'claims': self.claims
                }

    def iterlinks(self, family=None):
        """
        Iterates through all the sitelinks
        @param family: string/Family object which represents what family of
                       links to iterate
        @type family: str|Family
        @return: iterator of Page objects
        """
        if not hasattr(self, 'sitelinks'):
            self.get()
        if family is not None and not isinstance(family,
                                                 Family):
            family = Family(family)
        for dbname in self.sitelinks:
            pg = Page(APISite.fromDBName(dbname),
                      self.sitelinks[dbname])
            if family is None or family == pg.site.family:
                yield pg

    def getSitelink(self, site, force=False):
        """
        Returns the title (unicode string) for the specific site
        site is a Site or database name
        force will override caching
        If the item doesn't have that language, raise NoPage
        """
        if force or not hasattr(self, '_content'):
            self.get(force=force)
        dbname = self.getdbName(site)
        if not dbname in self.sitelinks:
            raise NoPage(self)
        else:
            return self.sitelinks[dbname]

    def setSitelink(self, sitelink, **kwargs):
        """
        A sitelink can either be a Page object,
        or a {'site':dbname,'title':title} dictionary.
        """
        self.setSitelinks([sitelink], **kwargs)

    def removeSitelink(self, site, **kwargs):
        """
        A site can either be a Site object,
        or it can be a dbName.
        """
        self.removeSitelinks([site], **kwargs)

    def removeSitelinks(self, sites, **kwargs):
        """
        Sites should be a list, with values either
        being Site objects, or dbNames.
        """
        data = list()
        for site in sites:
            site = self.getdbName(site)
            data.append({'site': site, 'title': ''})
        self.setSitelinks(data, **kwargs)

    def setSitelinks(self, sitelinks, **kwargs):
        """
        Sitelinks should be a list. Each item in the
        list can either be a Page object, or a dict
        with a value for 'site' and 'title'.
        """

        data = {}
        for obj in sitelinks:
            if isinstance(obj, Page):
                dbName = self.getdbName(obj.site)
                data[dbName] = {'site': dbName, 'title': obj.title()}
            else:
                #TODO: Do some verification here
                dbName = obj['site']
                data[dbName] = obj
        data = {'sitelinks': data}
        self.editEntity(data, **kwargs)

    def addClaim(self, claim, bot=True, **kwargs):
        """
        Adds the claim to the item
        @param claim The claim to add
        @type claim Claim
        @param bot Whether to flag as bot (if possible)
        @type bot bool
        """
        self.repo.addClaim(self, claim, bot=bot, **kwargs)
        claim.on_item = self

    def removeClaims(self, claims, **kwargs):
        """
        Removes the claims from the item
        @type claims: list

        """
        # this check allows single claims to be remove by pushing them into a
        # list of length one.
        if isinstance(claims, Claim):
            claims = [claims]
        self.repo.removeClaims(claims, **kwargs)
