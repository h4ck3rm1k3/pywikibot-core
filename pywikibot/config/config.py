
# Use pywikibot. prefix for all in-package imports; this is to prevent
# confusion with similarly-named modules in version 1 framework, for users
# who want to continue using both


from pywikibot import config2 as config
from pywikibot.bot import warning, output, inputChoice, debug
#from pywikibot.exceptions import *
#from pywikibot.textlib import *
#from pywikibot.i18n import translate

def setAction(s):
    """Set a summary to use for changed page submissions"""
    config.default_edit_summary = s

