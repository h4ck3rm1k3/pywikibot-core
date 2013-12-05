# -*- coding: utf-8  -*-
"""
The initialization file for the Pywikibot framework.
"""
#
# (C) Pywikibot team, 2008-213
#
# Distributed under the terms of the MIT license.
#
__release__ = '2.0b1'
__version__ = '$Id$'

## cleaned out

from pywikibot.site.sitefun import SiteManager
def Site(code=None, fam=None, user=None, sysop=None, interface=None) :
    siteman = SiteManager()
    return siteman.Site(code, fam, user, sysop, interface)

