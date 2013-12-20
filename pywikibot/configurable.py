u'''
from pywikibot.configurable import Configurable
'''

class Configurable(object):
    '''
    a base class for all objects in pywikibot that needs a config
    '''
    pass
    def __init__(self):
        from pywikibot.config import loadconfig
        self.config=loadconfig()
