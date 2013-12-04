
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

class WikibasePage(Page):
    """
    The base page for the Wikibase extension.
    There really should be no need to call this directly
    """
    def __init__(self, site, title="", **kwargs):
        if not isinstance(site, site.DataSite):
            raise TypeError("site must be a site.DataSite object")
        Page.__init__(self, site, title, **kwargs)
        self.repo = self.site
        self._isredir = False  # Wikibase pages cannot be a redirect

    def __cmp__(self, other):
        """Test for equality and inequality of WikibasePage objects.

        Page objects are "equal" if and only if they are on the same site
        and have the same normalized title, including section if any.

        Page objects are sortable by namespace first, then by title.

        This is basically the same as Page.__cmp__ but slightly different.
        """
        if not isinstance(other, Page):
            # especially, return -1 if other is None
            return -1
        if self.site != other.site:
            return self.__lt__(self.site, other.site)
        if self.namespace() != other.namespace():
            return self.__lt__(self.namespace(), other.namespace())
        return self.__lt__(self.title(), other.title())

    def title(self, **kwargs):
        if self.namespace() == 0:
            self._link._text = self.getID()
            del self._link._title
        return Page(self).title(**kwargs)

    @deprecated("_defined_by")
    def __defined_by(self, singular=False):
        return self._defined_by(singular=singular)

    def _defined_by(self, singular=False):
        """
        returns the parameters needed by the API to identify an item.
        Once an item's "p/q##" is looked up, that will be used for all future
        requests.
        @param singular: Whether the parameter names should use the singular
                         form
        @type singular: bool
        """
        params = {}
        if singular:
            id = 'id'
            site = 'site'
            title = 'title'
        else:
            id = 'ids'
            site = 'sites'
            title = 'titles'
        #id overrides all
        if hasattr(self, 'id'):
            params[id] = self.id
            return params

        #the rest only applies to ItemPages, but is still needed here.
        if hasattr(self, '_site') and hasattr(self, '_title'):
            params[site] = self._site.dbName()
            params[title] = self._title
        else:
            quit()
            params[id] = self.getID()

        return params

    def exists(self):
        if not hasattr(self, '_content'):
            try:
                self.get()
                return True
            except NoPage:
                return False
        return 'lastrevid' in self._content

    def get(self, force=False, *args):
        """
        Fetches all page data, and caches it
        force will override caching
        args can be used to specify custom props.
        """
        if force or not hasattr(self, '_content'):
            data = self.repo.loadcontent(self._defined_by(), *args)
            self.id = list(data.keys())[0]
            self._content = data[self.id]
        if 'lastrevid' in self._content:
            self.lastrevid = self._content['lastrevid']
        else:
            raise NoPage(self)
        #aliases
        self.aliases = {}
        if 'aliases' in self._content:
            for lang in self._content['aliases']:
                self.aliases[lang] = list()
                for value in self._content['aliases'][lang]:
                    self.aliases[lang].append(value['value'])

        #labels
        self.labels = {}
        if 'labels' in self._content:
            for lang in self._content['labels']:
                if not 'removed' in self._content['labels'][lang]:  # Bug 54767
                    self.labels[lang] = self._content['labels'][lang]['value']

        #descriptions
        self.descriptions = {}
        if 'descriptions' in self._content:
            for lang in self._content['descriptions']:
                self.descriptions[lang] = self._content[
                    'descriptions'][lang]['value']

        return {'aliases': self.aliases,
                'labels': self.labels,
                'descriptions': self.descriptions,
                }

    def getID(self, numeric=False, force=False):
        """
        @param numeric Strip the first letter and return an int
        @type numeric bool
        @param force Force an update of new data
        @type force bool
        """
        if not hasattr(self, 'id') or force:
            self.get(force=force)
        if numeric:
            return int(self.id[1:])
        return self.id

    def latestRevision(self):
        if not hasattr(self, 'lastrevid'):
            self.get()
        return self.lastrevid

    def __normalizeLanguages(self, data):
        """
        Helper function to convert any site objects
        into the language they may represent.
        @param data The dict to check
        @type data dict
        """
        for key in data:
            if isinstance(key, BaseSite):
                data[key.language()] = data[key]
                del data[key]
        return data

    def getdbName(self, site):
        """
        Helper function to normalize site
        objects into dbnames
        """
        if isinstance(site, BaseSite):
            return site.dbName()
        return site

    def editEntity(self, data, **kwargs):
        """
        Enables updating of entities through wbeditentity
        This function is wrapped around by:
         *editLabels
         *editDescriptions
         *editAliases
         *ItemPage.setSitelinks
        @param data Data to be saved
        @type data dict
        """
        if hasattr(self, 'lastrevid'):
            baserevid = self.lastrevid
        else:
            baserevid = None
        updates = self.repo.editEntity(self._defined_by(singular=True), data,
                                       baserevid=baserevid, **kwargs)
        self.lastrevid = updates['entity']['lastrevid']

    def editLabels(self, labels, **kwargs):
        """
        Labels should be a dict, with the key
        as a language or a site object. The
        value should be the string to set it to.
        You can set it to '' to remove the label.
        """
        labels = self.__normalizeLanguages(labels)
        for key in labels:
            labels[key] = {'language': key, 'value': labels[key]}
        data = {'labels': labels}
        self.editEntity(data, **kwargs)

    def editDescriptions(self, descriptions, **kwargs):
        """
        Descriptions should be a dict, with the key
        as a language or a site object. The
        value should be the string to set it to.
        You can set it to '' to remove the description.
        """
        descriptions = self.__normalizeLanguages(descriptions)
        for key in descriptions:
            descriptions[key] = {'language': key, 'value': descriptions[key]}
        data = {'descriptions': descriptions}
        self.editEntity(data, **kwargs)

    def editAliases(self, aliases, **kwargs):
        """
        Aliases should be a dict, with the key
        as a language or a site object. The
        value should be a list of strings.
        """
        aliases = self.__normalizeLanguages(aliases)
        for (key, strings) in list(aliases.items()):
            aliases[key] = [{'language': key, 'value': i} for i in strings]
        data = {'aliases': aliases}
        self.editEntity(data, **kwargs)
