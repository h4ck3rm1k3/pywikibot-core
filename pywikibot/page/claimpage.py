

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
from pywikibot.page import Page
from pywikibot.page.wikibasepage  import WikibasePage
from pywikibot.page.propertypage  import PropertyPage
class Claim(PropertyPage):
    """
    Claims are standard claims as well as references.
    """
    def __init__(self, site, pid, snak=None, hash=None, isReference=False,
                 isQualifier=False):
        """
        Defined by the "snak" value, supplemented by site + pid

        @param site: repository the claim is on
        @type site: site.DataSite
        @param pid: property id, with "P" prefix
        @param snak: snak identifier for claim
        @param hash: hash identifer for references
        @param isReference: whether specified claim is a reference
        @param isQualifier: whether specified claim is a qualifier
        """
        PropertyPage.__init__(self, site, 'Property:' + pid)
        self.snak = snak
        self.hash = hash
        self.isReference = isReference
        self.isQualifier = isQualifier
        if self.isQualifier and self.isReference:
            raise ValueError('Claim cannot be both a qualifier and reference.')
        self.sources = []
        self.qualifiers = collections.defaultdict(list)
        self.target = None
        self.snaktype = 'value'
        self.rank = 'normal'
        self.on_item = None  # The item it's on

    @staticmethod
    def fromJSON(site, data):
        """
        Creates the claim object from JSON returned
        in the API call.
        """
        claim = Claim(site, data['mainsnak']['property'])
        if 'id' in data:
            claim.snak = data['id']
        elif 'hash' in data:
            claim.isReference = True
            claim.hash = data['hash']
        else:
            claim.isQualifier = True
        claim.snaktype = data['mainsnak']['snaktype']
        if claim.getSnakType() == 'value':
            if claim.getType() == 'wikibase-item':
                claim.target = ItemPage(site, 'Q' +
                                        str(data['mainsnak']['datavalue']
                                            ['value']['numeric-id']))
            elif claim.getType() == 'commonsMedia':
                claim.target = ImagePage(site.image_repository(), 'File:' +
                                         data['mainsnak']['datavalue']['value'])
            elif claim.getType() == 'globecoordinate':
                claim.target = pywikibot.Coordinate.fromWikibase(
                    data['mainsnak']['datavalue']['value'], site)
            elif claim.getType() == 'time':
                claim.target = pywikibot.WbTime.fromWikibase(
                    data['mainsnak']['datavalue']['value'])
            else:
                # This covers string, url types
                claim.target = data['mainsnak']['datavalue']['value']
        if 'rank' in data:  # References/Qualifiers don't have ranks
            claim.rank = data['rank']
        if 'references' in data:
            for source in data['references']:
                claim.sources.append(Claim.referenceFromJSON(site, source))
        if 'qualifiers' in data:
            for prop in data['qualifiers']:
                for qualifier in data['qualifiers'][prop]:
                    qual = Claim.qualifierFromJSON(site, qualifier)
                    claim.qualifiers[prop].append(qual)
        return claim

    @staticmethod
    def referenceFromJSON(site, data):
        """
        Reference objects are represented a
        bit differently, and require some
        more handling.
        """
        source = collections.defaultdict(list)
        for prop in list(data['snaks'].values()):
            for claimsnak in prop:
                claim = Claim.fromJSON(site, {'mainsnak': claimsnak,
                                              'hash': data['hash']})
                source[claim.getID()].append(claim)
        return source

    @staticmethod
    def qualifierFromJSON(site, data):
        """
        Qualifier objects are represented a bit
        differently like references, but I'm not
        sure if this even requires it's own function.
        """
        wrap = {'mainsnak': data}
        return Claim.fromJSON(site, wrap)

    def setTarget(self, value):
        """
        Sets the target to the passed value.
        There should be checks to ensure type compliance
        """
        types = {'wikibase-item': ItemPage,
                 'string': str,
                 'commonsMedia': ImagePage,
                 'globecoordinate': pywikibot.Coordinate,
                 'url': str,
                 'time': pywikibot.WbTime,
                 }
        if self.getType() in types:
            if not isinstance(value, types[self.getType()]):
                raise ValueError("%s is not type %s."
                                 % (value, str(types[self.getType()])))
        self.target = value

    def changeTarget(self, value=None, snaktype='value', **kwargs):
        """
        This actually saves the new target.
        """
        if value:
            self.setTarget(value)

        data = self.repo.changeClaimTarget(self, snaktype=snaktype,
                                           **kwargs)
        #TODO: Re-create the entire item from JSON, not just id
        self.snak = data['claim']['id']

    def getTarget(self):
        """
        Returns object that the property is associated with.
        None is returned if no target is set
        """
        return self.target

    def getSnakType(self):
        """
        Returns the "snaktype"
        Can be "value", "somevalue" or "novalue"
        """
        return self.snaktype

    def setSnakType(self, value):
        if value in ['value', 'somevalue', 'novalue']:
            self.snaktype = value
        else:
            raise ValueError(
                "snaktype must be 'value', 'somevalue', or 'novalue'.")

    def getRank(self):
        return self.rank

    def setRank(self):
        """
        Has not been implemented in the Wikibase API yet
        """
        raise NotImplementedError

    def changeSnakType(self, value=None, **kwargs):
        """
        This actually saves the new snakvalue.
        TODO: Is this function really needed?
        """
        if value:
            self.setSnakType(value)
        self.changeTarget(snaktype=self.getSnakType(), **kwargs)

    def getSources(self):
        """
        Returns a list of sources. Each source is a list of Claims.
        """
        return self.sources

    def addSource(self, claim, **kwargs):
        """
        Adds the claim as a source.
        @param claim: the claim to add
        @type claim: Claim
        """
        self.addSources([claim], **kwargs)

    def addSources(self, claims, **kwargs):
        """
        Adds the claims as one source.
        @param claims: the claims to add
        @type claims: list of Claim
        """
        data = self.repo.editSource(self, claims, new=True, **kwargs)
        source = collections.defaultdict(list)
        for claim in claims:
            claim.hash = data['reference']['hash']
            self.on_item.lastrevid = data['pageinfo']['lastrevid']
            source[claim.getID()].append(claim)
        self.sources.append(source)

    def removeSource(self, source, **kwargs):
        """
        Removes the source.
        @param source: the source to remove
        @type source: Claim
        """
        self.removeSources([source], **kwargs)

    def removeSources(self, sources, **kwargs):
        """
        Removes the individual sources.
        @param sources: the sources to remove
        @type sources: list of Claim
        """
        #data = 
        self.repo.removeSources(self, sources, **kwargs)
        for source in sources:
            source_dict = collections.defaultdict(list)
            source_dict[source.getID()].append(source)
            self.sources.remove(source_dict)

    def addQualifier(self, qualifier, **kwargs):
        """Adds the given qualifier

        @param qualifier: the qualifier to add
        @type qualifier: Claim
        """
        data = self.repo.editQualifier(self, qualifier, **kwargs)
        qualifier.isQualifier = True
        self.on_item.lastrevid = data['pageinfo']['lastrevid']
        self.qualifiers[qualifier.getID()].append(qualifier)

    def _formatDataValue(self):
        """
        Format the target into the proper JSON datavalue that Wikibase wants
        """
        if self.getType() == 'wikibase-item':
            value = {'entity-type': 'item',
                     'numeric-id': self.getTarget().getID(numeric=True)}
        elif self.getType() in ['string', 'url']:
            value = self.getTarget()
        elif self.getType() == 'commonsMedia':
            value = self.getTarget().title(withNamespace=False)
        elif self.getType() == 'globecoordinate':
            value = self.getTarget().toWikibase()
        elif self.getType() == 'time':
            value = self.getTarget().toWikibase()
        else:
            raise NotImplementedError('%s datatype is not supported yet.'
                                      % self.getType())
        return value
