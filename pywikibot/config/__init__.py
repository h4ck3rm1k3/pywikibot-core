u'''
from pywikibot.config import loadconfig
'''
#from pywikibot.families.familybase import Family
import pywikibot.families.familybase 
import os.path
import os
class Config :

    def __init__(self):
        self._put_throttle = 0
        self._family = None
        self._user_names = {}
        self._sys_op_names = {}
        self._site_interface = None

    @property
    def put_throttle(self):
        return self._put_throttle

    @property
    def actions_to_block(self):
        return []

    @property
    def max_retries(self):
        return 4

    @property
    def maxlag(self):
        return 10

    @property
    def simulate(self):
        return True

    @property
    def retry_wait(self):
        return 1

    @property
    def use_mwparserfromhell(self):
        return True

    @property
    def use_mwparserfromhell(self):
        return True

    @property
    def mylang(self):
        return "en"

    @property
    def base_dir(self):
        return "~/experiments/wiki/pywikibot-core/pywikibot/"

    @property
    def available_ssl_project(self):
        return []

    @property
    def proxy(self):
        return None

    @property
    def API_config_expiry(self):
        return 0      

    @property
    def line_separator(self):
        return "\n"

    @property
    def console_encoding(self):
        return "utf-8"

    @property
    def base_dir(self):
        return "/tmp/"
        
    @property
    def family(self):

        if self._family is None:
            self._family = pywikibot.families.familybase.Family()

        return self._family

    @property
    def usernames(self):
        return self._user_names

    @property
    def sysopnames(self):
        return self._sys_op_names

    @property
    def site_interface(self):
        return self._site_interface

    def makepath(self,path):
        """Return a normalized absolute version of the path argument.

        - if the given path already exists in the filesystem
          the filesystem is not modified.

        - otherwise makepath creates directories along the given path
          using the dirname() of the path. You may append
          a '/' to the path if you want it to be a directory path.

        from holger@trillke.net 2002/03/18

        """

        dpath = os.path.normpath(os.path.dirname(path))
        if not os.path.exists(dpath):
            os.makedirs(dpath)
        return os.path.normpath(os.path.abspath(path))


    def datafilepath(self, *filename):
        """Return an absolute path to a data file in a standard location.

        Argument(s) are zero or more directory names, optionally followed by a
        data file name. The return path is offset to config.base_dir. Any
        directories in the path that do not already exist are created.

        """

        return self.makepath(os.path.join(self.base_dir, *filename))


    def shortpath(self, path):
        """Return a file path relative to config.base_dir."""

        if path.startswith(self.base_dir):
            return path[len(self.base_dir) + len(os.path.sep):]
        return path

globalconf = None

def loadconfig ():
    global globalconf
    if (globalconf is None ):
        globalconf = Config()
    return globalconf

