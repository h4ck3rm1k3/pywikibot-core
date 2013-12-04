

#import pywikibot.userinterfaces.terminal_interface_unix 

from pywikibot.userinterfaces.terminal_interface_unix  import UnixUI

class UI :
    def __init__(self, config):
        self.ui = UnixUI(config)

#ui = UI()

def get_ui():
    return ui.ui
    
