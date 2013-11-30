#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
This is a Bot written by Filnik to add a text at the end of the page but above
categories, interwiki and template for the stars of the interwiki (default).

Alternatively it may also add a text at the top of the page.
These command line parameters can be used to specify which pages to work on:

&params;

Furthermore, the following command line parameters are supported:

-page             Use a page as generator

-talkpage         Put the text onto the talk page instead the generated on
-talk

-text             Define which text to add. "\n" are interpreted as newlines.

-textfile         Define a texfile name which contains the text to add

-summary          Define the summary to use

-except           Use a regex to check if the text is already in the page

-excepturl        Use the html page as text where you want to see if there's
                  the text, not the wiki-page.

-newimages        Add text in the new images

-always           If used, the bot won't ask if it should add the text
                  specified

-up               If used, put the text at the top of the page

-noreorder        Avoid to reorder cats and interwiki

--- Example ---
1.
# This is a script to add a template to the top of the pages with
# category:catname
# Warning! Put it in one line, otherwise it won't work correctly.

python add_text.py -cat:catname -summary:"Bot: Adding a template"
-text:"{{Something}}" -except:"\{\{([Tt]emplate:|)[Ss]omething" -up

2.
# Command used on it.wikipedia to put the template in the page without any
# category.
# Warning! Put it in one line, otherwise it won't work correctly.

python add_text.py -excepturl:"class='catlinks'>" -uncat
-text:"{{Categorizzare}}" -except:"\{\{([Tt]emplate:|)[Cc]ategorizzare"
-summary:"Bot: Aggiungo template Categorizzare"

--- Credits and Help ---
This script has been written by Botwiki's staff, if you want to help us
or you need some help regarding this script, you can find us here:

* http://botwiki.sno.cc

"""

#
# (C) Filnik, 2007-2010
# (C) Pywikibot team, 2007-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import re
import webbrowser
import codecs

import pywikibot
from pywikibot import config
from pywikibot import i18n
from pywikibot import pagegenerators

docuReplacements = {
    '&params;': pagegenerators.parameterHelp,
}


starsList = [
    'bueno',
    'bom interwiki',
    'cyswllt[ _]erthygl[ _]ddethol', 'dolen[ _]ed',
    'destacado', 'destaca[tu]',
    'enllaç[ _]ad',
    'enllaz[ _]ad',
    'leam[ _]vdc',
    'legătură[ _]a[bcf]',
    'liamm[ _]pub',
    'lien[ _]adq',
    'lien[ _]ba',
    'liên[ _]kết[ _]bài[ _]chất[ _]lượng[ _]tốt',
    'liên[ _]kết[ _]chọn[ _]lọc',
    'ligam[ _]adq',
    'ligoelstara',
    'ligoleginda',
    'link[ _][afgu]a', 'link[ _]adq', 'link[ _]f[lm]', 'link[ _]km',
    'link[ _]sm', 'linkfa',
    'na[ _]lotura',
    'nasc[ _]ar',
    'tengill[ _][úg]g',
    'ua',
    'yüm yg',
    'רא',
    'وصلة مقالة جيدة',
    'وصلة مقالة مختارة',
]


class NoEnoughData(pywikibot.Error):
    """ Error class for when the user doesn't specified all the data needed """


def add_text(page=None, addText=None, summary=None, regexSkip=None,
             regexSkipUrl=None, always=False, up=False, putText=True,
             oldTextGiven=None, reorderEnabled=True, create=False):
    if not addText:
        raise NoEnoughData('You have to specify what text you want to add!')
    if not summary:
        summary = i18n.twtranslate(pywikibot.getSite(), 'add_text-adding',
                                   {'adding': addText[:200]})

    # When a page is tagged as "really well written" it has a star in the
    # interwiki links. This is a list of all the templates used (in regex
    # format) to make the stars appear.

    errorCount = 0
    site = pywikibot.getSite()
    pathWiki = site.family.nicepath(site.lang)

    if putText:
        pywikibot.output('Loading %s...' % page.title())
    if oldTextGiven is None:
        try:
            text = page.get()
        except pywikibot.NoPage:
            if create:
                pywikibot.output("%s doesn't exist, creating it!"
                                 % page.title())
                text = ''
            else:
                pywikibot.output("%s doesn't exist, skip!" % page.title())
                return (False, False, always)
        except pywikibot.IsRedirectPage:
            pywikibot.output("%s is a redirect, skip!" % page.title())
            return (False, False, always)
    else:
        text = oldTextGiven
    # Understand if the bot has to skip the page or not
    # In this way you can use both -except and -excepturl
    if regexSkipUrl is not None:
        url = '%s%s' % (pathWiki, page.urlname())
        result = re.findall(regexSkipUrl, site.getUrl(url))
        if result != []:
            pywikibot.output(
'''Exception! regex (or word) used with -exceptUrl is in the page. Skip!
Match was: %s''' % result)
            return (False, False, always)
    if regexSkip is not None:
        result = re.findall(regexSkip, text)
        if result != []:
            pywikibot.output(
'''Exception! regex (or word) used with -except is in the page. Skip!
Match was: %s''' % result)
            return (False, False, always)
    # If not up, text put below
    if not up:
        newtext = text
        # Translating the \\n into binary \n
        addText = addText.replace('\\n', config.line_separator)
        if (reorderEnabled):
            # Getting the categories
            categoriesInside = pywikibot.getCategoryLinks(newtext, site)
            # Deleting the categories
            newtext = pywikibot.removeCategoryLinks(newtext, site)
            # Getting the interwiki
            interwikiInside = pywikibot.getLanguageLinks(newtext, site)
            # Removing the interwiki
            newtext = pywikibot.removeLanguageLinks(newtext, site)

            # Adding the text
            newtext += "%s%s" % (config.line_separator, addText)
            # Reputting the categories
            newtext = pywikibot.replaceCategoryLinks(newtext,
                                                     categoriesInside, site,
                                                     True)
            # Dealing the stars' issue
            allstars = []
            starstext = pywikibot.removeDisabledParts(text)
            for star in starsList:
                regex = re.compile('(\{\{(?:template:|)%s\|.*?\}\}[\s]*)'
                                   % star, re.I)
                found = regex.findall(starstext)
                if found != []:
                    newtext = regex.sub('', newtext)
                    allstars += found
            if allstars != []:
                newtext = newtext.strip() + config.line_separator * 2
                allstars.sort()
                for element in allstars:
                    newtext += '%s%s' % (element.strip(), config.LS)
            # Adding the interwiki
            newtext = pywikibot.replaceLanguageLinks(newtext, interwikiInside,
                                                     site)
        else:
            newtext += "%s%s" % (config.line_separator, addText)
    else:
        newtext = addText + config.line_separator + text
    if putText and text != newtext:
        pywikibot.output("\n\n>>> \03{lightpurple}%s\03{default} <<<"
                         % page.title())
        pywikibot.showDiff(text, newtext)
    # Let's put the changes.
    while True:
        # If someone load it as module, maybe it's not so useful to put the
        # text in the page
        if putText:
            if not always:
                choice = pywikibot.inputChoice(
                    'Do you want to accept these changes?',
                    ['Yes', 'No', 'All', 'open in Browser'],
                    ['y', 'n', 'a', 'b'], 'n')
                if choice == 'a':
                    always = True
                elif choice == 'n':
                    return (False, False, always)
                elif choice == 'b':
                    webbrowser.open("http://%s%s" % (
                        page.site.hostname(),
                        page.site.nice_get_address(page.title())
                    ))
                    pywikibot.input("Press Enter when finished in browser.")
            if always or choice == 'y':
                try:
                    if always:
                        page.put(newtext, summary,
                                 minorEdit=page.namespace() != 3)
                    else:
                        page.put_async(newtext, summary,
                                       minorEdit=page.namespace() != 3)
                except pywikibot.EditConflict:
                    pywikibot.output('Edit conflict! skip!')
                    return (False, False, always)
                except pywikibot.ServerError:
                    errorCount += 1
                    if errorCount < config.max_retries:
                        pywikibot.output('Server Error! Wait..')
                        time.sleep(config.retry_wait)
                        continue
                    else:
                        raise pywikibot.ServerError('Fifth Server Error!')
                except pywikibot.SpamfilterError as e:
                    pywikibot.output(
                        'Cannot change %s because of blacklist entry %s'
                        % (page.title(), e.url))
                    return (False, False, always)
                except pywikibot.PageNotSaved as error:
                    pywikibot.output('Error putting page: %s' % error.args)
                    return (False, False, always)
                except pywikibot.LockedPage:
                    pywikibot.output('Skipping %s (locked page)'
                                     % page.title())
                    return (False, False, always)
                else:
                    # Break only if the errors are one after the other...
                    errorCount = 0
                    return (True, True, always)
        else:
            return (text, newtext, always)


def main():
    # If none, the var is setted only for check purpose.
    summary = None
    addText = None
    regexSkip = None
    regexSkipUrl = None
    generator = None
    always = False
    textfile = None
    talkPage = False
    reorderEnabled = True
    namespaces = []
    # Load a lot of default generators
    genFactory = pagegenerators.GeneratorFactory()
    # Put the text above or below the text?
    up = False
    # Loading the arguments
    for arg in pywikibot.handleArgs():
        if arg.startswith('-textfile'):
            if len(arg) == 9:
                textfile = pywikibot.input(
                    'Which textfile do you want to add?')
            else:
                textfile = arg[10:]
        elif arg.startswith('-text'):
            if len(arg) == 5:
                addText = pywikibot.input('What text do you want to add?')
            else:
                addText = arg[6:]
        elif arg.startswith('-summary'):
            if len(arg) == 8:
                summary = pywikibot.input('What summary do you want to use?')
            else:
                summary = arg[9:]
        elif arg.startswith('-page'):
            if len(arg) == 5:
                generator = [pywikibot.Page(
                    pywikibot.getSite(),
                    pywikibot.input('What page do you want to use?'))]
            else:
                generator = [pywikibot.Page(pywikibot.getSite(), arg[6:])]
        elif arg.startswith('-excepturl'):
            if len(arg) == 10:
                regexSkipUrl = pywikibot.input('What text should I skip?')
            else:
                regexSkipUrl = arg[11:]
        elif arg.startswith('-except'):
            if len(arg) == 7:
                regexSkip = pywikibot.input('What text should I skip?')
            else:
                regexSkip = arg[8:]
        elif arg == '-up':
            up = True
        elif arg == '-noreorder':
            reorderEnabled = False
        elif arg == '-always':
            always = True
        elif arg == '-talk' or arg == '-talkpage':
            talkPage = True
        else:
            genFactory.handleArg(arg)
    if textfile and not addText:
        f = codecs.open(textfile, 'r', config.textfile_encoding)
        addText = f.read()
        f.close()
    if not generator:
        generator = genFactory.getCombinedGenerator()
    if not generator:
        raise NoEnoughData(
            'You have to specify the generator you want to use for the script!')
    if talkPage:
        generator = pagegenerators.PageWithTalkPageGenerator(generator)
        site = pywikibot.getSite()
        for namespace in site.namespaces():
            index = site.getNamespaceIndex(namespace)
            if index % 2 == 1 and index > 0:
                namespaces += [index]
        generator = pagegenerators.NamespaceFilterPageGenerator(
            generator, namespaces)
    for page in generator:
        (text, newtext, always) = add_text(page, addText, summary, regexSkip,
                                           regexSkipUrl, always, up, True,
                                           reorderEnabled=reorderEnabled,
                                           create=talkPage)

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
