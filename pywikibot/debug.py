u'''
from pywikibot.debug import debugprint
'''

import pprint
def  tryencode(x):
    return ""
    #traceback.print_stack(limit=2)
    if x is None:
        print ("NONE TYPE:%s" % type(x))
        return "None"
    elif isinstance(x,bytes):
        print ("BYTES TYPE:%s" % type(x))
        return x.decode('utf-8')
    elif isinstance(x,str):
        print ("STR TYPE:%s" % type(x))
        print ("STR:%s" % x)
        return ("STR:%s" % x)
    else:
        print ("STR TYPE:%s" % type(x))
        return ("UNKNOWN:%s" % str(x))

def  debugprint(x):
    #traceback.print_stack(limit=2)
    #print(x)
    pass

def  debugpprint(x):
    debugprint(pprint.pformat(x))
