#!/usr/bin/python
# -*- coding: utf-8  -*-
r"""
This script transfers pages from a source wiki to a target wiki.

It also copies edit history to a subpage.

-tolang:          The target site code.

-tosite:          The target site family.

-prefix:          Page prefix on the new site.

-overwrite:       Existing pages are skipped by default. Use his option to
                  overwrite pages.

Internal links are *not* repaired!

Pages to work on can be specified using any of:

&params;

Example commands:

Transfer all pages in category "Query service" from the English Wikipedia to the
Arabic Wiktionary, adding "Wiktionary:Import enwp/" as prefix:

    python pwb.py transferbot -family:wikipedia -lang:en -cat:"Query service" \
        -tofamily:wiktionary -tolang:ar -prefix:"Wiktionary:Import enwp/"

Copy the template "Query service" from the Toolserver wiki to wikitech:

    python pwb.py transferbot -family:wikipedia -lang:en \
        -tofamily:wiktionary -tolang:ar -page:"Template:Query service"

"""
#
# (C) Merlijn van Deen, 2014
# (C) Pywikibot team, 2015
# (C) James Michael DuPont h4ck3rm1k3, 2016
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

__version__ = '$Id$'
#

import pywikibot
from pywikibot import pagegenerators

docuReplacements = {
    '&params;': pagegenerators.parameterHelp,
}


class WikiTransferException(Exception):

    """Base class for exceptions from this script.

    Makes it easier for clients to catch all expected exceptions that the script might
    throw
    """

    pass


class TargetSiteMissing(WikiTransferException):

    """Thrown when the target site is the same as the source site.

    Based on the way each are initialized, this is likely to happen when the target site
    simply hasn't been specified.
    """

    pass


class TargetPagesMissing(WikiTransferException):

    """Thrown if no page range has been specified for the script to operate on."""

    pass

import sqlitedict

def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    local_args = pywikibot.handle_args(args)

    file_store = sqlitedict.SqliteDict('transferbot.db', autocommit=True)
    file_store_error = sqlitedict.SqliteDict('error.db', autocommit=True)
    file_store_history = sqlitedict.SqliteDict('history.db', autocommit=True)

    fromsite = pywikibot.Site()
    tolang = fromsite.code
    tofamily = fromsite.family.name
    prefix = ''
    overwrite = False
    gen_args = []

    genFactory = pagegenerators.GeneratorFactory()

    for arg in local_args:
        if genFactory.handleArg(arg):
            gen_args.append(arg)
            continue
        if arg.startswith('-tofamily'):
            tofamily = arg[len('-tofamily:'):]
        elif arg.startswith('-tolang'):
            tolang = arg[len('-tolang:'):]
        elif arg.startswith('-prefix'):
            prefix = arg[len('-prefix:'):]
        elif arg == "-overwrite":
            overwrite = True

    tosite = pywikibot.Site(tolang, tofamily)
    if fromsite == tosite:
        raise TargetSiteMissing('Target site not different from source site')

    gen = genFactory.getCombinedGenerator()
    if not gen:
        raise TargetPagesMissing('Target pages not specified')

    gen_args = ' '.join(gen_args)
    pywikibot.output(u"""
    Page transfer configuration
    ---------------------------
    Source: %(fromsite)r
    Target: %(tosite)r

    Pages to transfer: %(gen_args)s

    Prefix for transferred pages: %(prefix)s
    """ % {'fromsite': fromsite, 'tosite': tosite,
           'gen_args': gen_args, 'prefix': prefix})

    for page in gen:
        summary = "Moved page from %s" % page.title(asLink=True)

        title = page.title()
        
        if title in file_store:
            continue

        if title in file_store_error:
            continue

        if title in file_store_history:
            continue

        newtitle = page.title().replace(':',' - ');
        targetpage = pywikibot.Page(tosite, prefix + newtitle)
        edithistpage = pywikibot.Page(tosite, prefix + newtitle + '/edithistory')

        t = page.title()
        if t.startswith('Wikipedia:'):
            print "Skipping" + t
            continue

        if targetpage.exists() and not overwrite:
            pywikibot.output(
                u"Skipped %s (target page %s exists)" % (
                    page.title(asLink=True),
                    targetpage.title(asLink=True)
                )
            )
            continue

        pywikibot.output(u"Moving %s to %s..."
                         % (page.title(asLink=True),
                            targetpage.title(asLink=True)))

        pywikibot.log("Getting page text.")
        try:
            text = page.get(get_redirect=True)
        except Exception as e:
            print e
            continue
            
        text += ("<noinclude>\n\n{{Wikipedia-deleted-new|%s|%s}}</noinclude>"
             % (page.title(asLink=True, insite=targetpage.site),
                edithistpage.title(asLink=True, insite=targetpage.site)))

        pywikibot.log("Getting edit history.")
        historytable = page.getVersionHistoryTable()

        pywikibot.log("Putting page text.")
        try :
            targetpage.put(text, summary=summary)
        except pywikibot.exceptions.SpamfilterError as e:
            print e
            file_store_error[title]=text
            file_store_history[title]=historytable
            continue
            #print text            

        except pywikibot.exceptions.PageSaveRelatedError as e:
            print e
            file_store_error[title]=text
            file_store_history[title]=historytable

            continue
            #print text.


        #except Exception as e:
            


        pywikibot.log("Putting edit history.")
        try :
            edithistpage.put(historytable, summary=summary)
        except pywikibot.exceptions.SpamfilterError as e:
            #print historytable
            file_store_error[title]=text
            file_store_history[title]=historytable
            print e
            continue


        file_store[title]=1
            

if __name__ == "__main__":
    try:
        main()
    except TargetSiteMissing as e:
        pywikibot.error(u'Need to specify a target site and/or language')
        pywikibot.error(u'Try running this script with -help for help/usage')
        pywikibot.exception()
    except TargetPagesMissing as e:
        pywikibot.error(u'Need to specify a page range')
        pywikibot.error(u'Try running this script with -help for help/usage')
        pywikibot.exception()
