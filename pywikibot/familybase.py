u"""
from pywikibot.familybase import Family as FamilyBase
"""
#import sys
#import datetime
#import difflib
#import logging
#import math
#import re
#import sys
#import threading
#from queue import Queue

# Use pywikibot. prefix for all in-package imports; this is to prevent
# confusion with similarly-named modules in version 1 framework, for users
# who want to continue using both

#import pywikibot
#from pywikibot.config import loadconfig
#from pywikibot.bot import warning, output, inputChoice, debug
#from pywikibot.exceptions import Error
#from pywikibot.textlib import *
#from pywikibot.i18n import translate

# def Family(fam=None, fatal=True):
#     """Import the named family.

#     @param fam: family name (if omitted, uses the configured default)
#     @type fam: str
#     @param fatal: if True, the bot will stop running if the given family is
#         unknown. If False, it will only raise a ValueError exception.
#     @param fatal: bool
#     @return: a Family instance configured for the named family.

#     """
#     #config = loadconfig()

#     #if fam is None:
#     #    fam = config.family
# #    try:
# #        # first try the built-in families
# #        name = "pywikibot.families.%s_family" % fam
# #        __import__(name)
# #        myfamily = sys.modules[name]
# #    except ImportError:
# #        # next see if user has defined a local family module
# #        try:
# #            print(config.datafilepath('families'))
# #            sys.path.append(config.datafilepath('families'))
# #            print("%s_family" % fam)
# ##            myfamily = __import__("%s_family" % fam)
# #        except ImportError:
# #            if fatal:
#     pywikibot.error("""\
# Error importing the %s family. This probably means the family
# does not exist. Also check your configuration file."""
#                                 % fam, exc_info=True)
#                 sys.exit(1)
#             else:
#                 raise Error("Family %s does not exist" % fam)
#     return myFamily()
