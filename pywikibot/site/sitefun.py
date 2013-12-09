#_sites = {}
#getSite = Site  # alias for backwards-compability
from pywikibot.config import loadconfig
#from pywikibot.bot import debug
from pywikibot.site.base import BaseSite
class SiteManager :
    def __init__(self):
        self._sites={}

    def Site(self, code=None, fam=None, user=None, sysop=None, interface=None):
        """Return the specified Site object.

        Returns a cached object if possible, otherwise instantiates a new one.

        @param code: language code
        @type code: string
        @param fam: family name or object
        @type fam: string or Family
        @param user: bot user name to use on this site
        @type user: unicode
        """
        #_logger = "wiki"

        config = loadconfig()

        if code is None:
            code = config.mylang
        if fam is None:
            fam = config.family
        if user is None:
            try:
                user = config.usernames[fam][code]
            except KeyError:
                user = None
        if user is None:
            try:
                user = config.usernames[fam]['*']
            except KeyError:
                user = None
        if sysop is None:
            try:
                sysop = config.sysopnames[fam][code]
            except KeyError:
                sysop = None
        if interface is None:
            interface = config.site_interface
        # try:
        #     tmp = __import__('pywikibot.site', fromlist=[interface])
        #     __Site = getattr(tmp, interface)
        # except ImportError:
        #     raise ValueError("Invalid interface name '%(interface)s'" % locals())

        key = '%s:%s:%s' % (fam, code, user)
        #if not key in self._sites or not isinstance(self._sites[key], __Site):
        #    self._sites[key] = interface(code=code, fam=fam, user=user, sysop=sysop)
        #    debug("Instantiating Site object '%(site)s'"
        #                    % {'site':self._sites[key]}, _logger)
        if key in self._sites:
            return self._sites[key]
        else :
            return BaseSite(code, fam, user, sysop)
            



