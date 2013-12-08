# -*- coding: utf-8 -*-
"""
Program to (re)categorize images at commons.

The program uses commonshelper for category suggestions.
It takes the suggestions and the current categories. Put the categories through
some filters and adds the result.

The following command line parameters are supported:

-onlyfilter     Don't use Commonsense to get categories, just filter the current
                categories

-onlyuncat      Only work on uncategorized images. Will prevent the bot from
                working on an image multiple times.

-hint           Give Commonsense a hint.
                For example -hint:li.wikipedia.org

-onlyhint       Give Commonsense a hint. And only work on this hint.
                Syntax is the same as -hint. Some special hints are possible:
                _20 : Work on the top 20 wikipedia's
                _80 : Work on the top 80 wikipedia's
                wps : Work on all wikipedia's

"""
#
# (C) Multichill 2008-2011
# (C) Pywikibot team, 2008-2013
#
#   Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#
from Category import Category
import sys
import re
import urllib.request, urllib.parse, urllib.error
import time
import socket
import xml.etree.ElementTree

import pywikibot
from pywikibot import pagegenerators

category_blacklist = []
countries = []

search_wikis = '_20'
hint_wiki = ''


def initLists():
    """
    Get the list of countries & the blacklist from Commons.
    """
    global category_blacklist
    global countries

    blacklistPage = pywikibot.Page(pywikibot.Site('commons', 'commons'),
                                   'User:Multichill/Category_blacklist')
    for cat in blacklistPage.linkedPages():
        category_blacklist.append(cat.title(withNamespace=False))

    countryPage = pywikibot.Page(pywikibot.Site('commons', 'commons'),
                                 'User:Multichill/Countries')
    for country in countryPage.linkedPages():
        countries.append(country.title(withNamespace=False))
    return


def categorizeImages(generator, onlyFilter, onlyUncat):
    """ Loop over all images in generator and try to categorize them. Get
    category suggestions from CommonSense.

    """
    for page in generator:
        if page.exists() and (page.namespace() == 6) and \
           (not page.isRedirectPage()):
            imagepage = pywikibot.ImagePage(page.site(), page.title())
            pywikibot.output('Working on ' + imagepage.title())

            if onlyUncat and not('Uncategorized' in imagepage.templates()):
                pywikibot.output('No Uncategorized template found')
            else:
                currentCats = getCurrentCats(imagepage)
                if onlyFilter:
                    commonshelperCats = []
                    usage = []
                    galleries = []
                else:
                    (commonshelperCats, usage, galleries) = getCommonshelperCats(imagepage)
                newcats = applyAllFilters(commonshelperCats + currentCats)

                if len(newcats) > 0 and not(set(currentCats) == set(newcats)):
                    for cat in newcats:
                        pywikibot.output(' Found new cat: ' + cat)
                    saveImagePage(imagepage, newcats, usage, galleries,
                                  onlyFilter)


def getCurrentCats(imagepage):
    """ Get the categories currently on the image """
    result = []
    for cat in imagepage.categories():
        result.append(cat.title(withNamespace=False))
    return list(set(result))


def getCommonshelperCats(imagepage):
    """ Get category suggestions from CommonSense. Parse them and return a list
    of suggestions.

    """
    commonshelperCats = []
    usage = []
    galleries = []

    global search_wikis
    global hint_wiki
    site = imagepage.site
    lang = site.language()
    family = site.family.name
    if lang == 'commons' and family == 'commons':
        parameters = urllib.parse.urlencode(
            {'i': imagepage.title(withNamespace=False).encode('utf-8'),
             'r': 'on',
             'go-clean': 'Find+Categories',
             'p': search_wikis,
             'cl': hint_wiki})
    elif family == 'wikipedia':
        parameters = urllib.parse.urlencode(
            {'i': imagepage.title(withNamespace=False).encode('utf-8'),
             'r': 'on',
             'go-move': 'Find+Categories',
             'p': search_wikis,
             'cl': hint_wiki,
             'w': lang})
    else:
        #Cant handle other sites atm
        return [], [], []

    commonsenseRe = re.compile('^#COMMONSENSE(.*)#USAGE(\s)+\((?P<usagenum>(\d)+)\)\s(?P<usage>(.*))\s#KEYWORDS(\s)+\((?P<keywords>(\d)+)\)(.*)#CATEGORIES(\s)+\((?P<catnum>(\d)+)\)\s(?P<cats>(.*))\s#GALLERIES(\s)+\((?P<galnum>(\d)+)\)\s(?P<gals>(.*))\s(.*)#EOF$', re.MULTILINE + re.DOTALL)  # noqa

    gotInfo = False
    matches = None
    maxtries = 10
    tries = 0
    while not gotInfo:
        try:
            if tries < maxtries:
                tries += 1
                commonsHelperPage = urllib.request.urlopen(
                    "http://toolserver.org/~daniel/WikiSense/CommonSense.php?%s" % parameters)
                matches = commonsenseRe.search(
                    commonsHelperPage.read().decode('utf-8'))
                gotInfo = True
            else:
                break
        except IOError:
            pywikibot.output('Got an IOError, let\'s try again')
        except socket.timeout:
            pywikibot.output('Got a timeout, let\'s try again')

    if matches and gotInfo:
        if matches.group('usagenum') > 0:
            used = matches.group('usage').splitlines()
            for use in used:
                usage = usage + getUsage(use)
                #pywikibot.output(use)
        if matches.group('catnum') > 0:
            cats = matches.group('cats').splitlines()
            for cat in cats:
                commonshelperCats.append(cat.replace('_', ' '))
                pywikibot.output('category : ' + cat)
        if matches.group('galnum') > 0:
            gals = matches.group('gals').splitlines()
            for gal in gals:
                galleries.append(gal.replace('_', ' '))
                pywikibot.output('gallery : ' + gal)
    commonshelperCats = list(set(commonshelperCats))
    galleries = list(set(galleries))
    for (lang, project, article) in usage:
        pywikibot.output(lang + project + article)
    return commonshelperCats, usage, galleries


def getOpenStreetMapCats(latitude, longitude):
    """
    Get a list of location categories based on the OSM nomatim tool
    """
    result = []
    locationList = getOpenStreetMap(latitude, longitude)
    for i in range(0, len(locationList)):
        #print 'Working on ' + locationList[i]
        if i <= len(locationList) - 3:
            category = getCategoryByName(name=locationList[i],
                                         parent=locationList[i + 1],
                                         grandparent=locationList[i + 2])
        elif i == len(locationList) - 2:
            category = getCategoryByName(name=locationList[i],
                                         parent=locationList[i + 1])
        else:
            category = getCategoryByName(name=locationList[i])
        if category and not category == '':
            result.append(category)
    #print result
    return result


def getOpenStreetMap(latitude, longitude):
    """
    Get the result from http://nominatim.openstreetmap.org/reverse
    and put it in a list of tuples to play around with
    """
    result = []
    gotInfo = False
    parameters = urllib.parse.urlencode({'lat': latitude, 'lon': longitude, 'accept-language': 'en'})
    while not gotInfo:
        try:
            page = urllib.request.urlopen("http://nominatim.openstreetmap.org/reverse?format=xml&%s" % parameters)
            et = xml.etree.ElementTree.parse(page)
            gotInfo = True
        except IOError:
            pywikibot.output('Got an IOError, let\'s try again')
            time.sleep(30)
        except socket.timeout:
            pywikibot.output('Got a timeout, let\'s try again')
            time.sleep(30)
    validParts = ['hamlet', 'village', 'city', 'county', 'country']
    invalidParts = ['path', 'road', 'suburb', 'state', 'country_code']
    addressparts = et.find('addressparts')
    #xml.etree.ElementTree.dump(et)

    for addresspart in addressparts.getchildren():
        if addresspart.tag in validParts:
            result.append(addresspart.text)
        elif addresspart.tag in invalidParts:
            pywikibot.output('Dropping %s, %s' % (addresspart.tag, addresspart.text))
        else:
            pywikibot.warning('%s, %s is not in addressparts lists' % (addresspart.tag, addresspart.text))
    #print result
    return result


def getCategoryByName(name, parent='', grandparent=''):

    if not parent == '':
        workname = name.strip() + ',_' + parent.strip()
        workcat = Category(pywikibot.Site('commons', 'commons'), workname)
        if workcat.exists():
            return workname
    if not grandparent == '':
        workname = name.strip() + ',_' + grandparent.strip()
        workcat = Category(pywikibot.Site('commons', 'commons'), workname)
        if workcat.exists():
            return workname
    workname = name.strip()
    workcat = Category(pywikibot.Site('commons', 'commons'), workname)
    if workcat.exists():
        return workname
    return ''


def getUsage(use):
    """ Parse the Commonsense output to get the usage """
    result = []
    lang = ''
    project = ''
    article = ''
    usageRe = re.compile(
        '^(?P<lang>([\w-]+))\.(?P<project>([\w]+))\.org:(?P<articles>\s(.*))')
    matches = usageRe.search(use)
    if matches:
        if matches.group('lang'):
            lang = matches.group('lang')
            #pywikibot.output(lang)
        if matches.group('project'):
            project = matches.group('project')
            #pywikibot.output(project)
        if matches.group('articles'):
            articles = matches.group('articles')
            #pywikibot.output(articles)
    for article in articles.split():
        result.append((lang, project, article))
    return result


def applyAllFilters(categories):
    """ Apply all filters on categories. """
    result = []
    result = filterDisambiguation(categories)
    result = followRedirects(result)
    result = filterBlacklist(result)
    result = filterCountries(result)
    result = filterParents(result)
    return result


def filterBlacklist(categories):
    """ Filter out categories which are on the blacklist. """
    result = []
    for cat in categories:
        cat = cat.replace('_', ' ')
        if not (cat in category_blacklist):
            result.append(cat)
    return list(set(result))


def filterDisambiguation(categories):
    """ Filter out disambiguation categories. """
    result = []
    for cat in categories:
        if (not pywikibot.Page(pywikibot.Site('commons', 'commons'),
                               cat, ns=14).isDisambig()):
            result.append(cat)
    return result


def followRedirects(categories):
    """ If a category is a redirect, replace the category with the target. """
    result = []
    for cat in categories:
        categoryPage = pywikibot.Page(pywikibot.getSite('commons', 'commons'),
                                      cat, ns=14)
        if categoryPage.isCategoryRedirect():
            result.append(
                categoryPage.getCategoryRedirectTarget().title(
                    withNamespace=False))
        else:
            result.append(cat)
    return result


def filterCountries(categories):
    """ Try to filter out ...by country categories.
    First make a list of any ...by country categories and try to find some
    countries. If a by country category has a subcategoy containing one of the
    countries found, add it. The ...by country categories remain in the set and
    should be filtered out by filterParents.

    """
    result = categories
    listByCountry = []
    listCountries = []
    for cat in categories:
        if cat.endswith('by country'):
            listByCountry.append(cat)

        #If cat contains 'by country' add it to the list
        #If cat contains the name of a country add it to the list
        else:
            for country in countries:
                if country in cat:
                    listCountries.append(country)
    if len(listByCountry) > 0:
        for bc in listByCountry:
            category = Category(
                pywikibot.Site('commons', 'commons'), 'Category:' + bc)
            for subcategory in category.subcategories():
                for country in listCountries:
                    if subcategory.title(withNamespace=False).endswith(country):
                        result.append(subcategory.title(withNamespace=False))
    return list(set(result))


def filterParents(categories):
    """ Remove all parent categories from the set to prevent overcategorization. """
    result = []
    toFilter = ''
    for cat in categories:
        cat = cat.replace('_', ' ')
        toFilter = toFilter + "[[Category:" + cat + "]]\n"
    parameters = urllib.parse.urlencode({'source': toFilter.encode('utf-8'),
                                   'bot': '1'})
    filterCategoriesRe = re.compile('\[\[Category:([^\]]*)\]\]')
    try:
        filterCategoriesPage = urllib.request.urlopen(
            "http://toolserver.org/~multichill/filtercats.php?%s" % parameters)
        result = filterCategoriesRe.findall(
            filterCategoriesPage.read().decode('utf-8'))
    except IOError:
        #Something is wrong, forget about this filter and just return the input
        return categories

    if not result:
        #Is empty, dont want to remove all categories
        return categories
    return result


def saveImagePage(imagepage, newcats, usage, galleries, onlyFilter):
    """ Remove the old categories and add the new categories to the image. """
    newtext = pywikibot.removeCategoryLinks(imagepage.get(), imagepage.site())
    if not onlyFilter:
        newtext = removeTemplates(newtext)
        newtext = newtext + getCheckCategoriesTemplate(usage, galleries,
                                                       len(newcats))
    newtext += '\n'
    for category in newcats:
        newtext = newtext + '[[Category:' + category + ']]\n'
    if onlyFilter:
        comment = 'Filtering categories'
    else:
        comment = 'Image is categorized by a bot using data from [[Commons:Tools#CommonSense|CommonSense]]'
    pywikibot.showDiff(imagepage.get(), newtext)
    imagepage.put(newtext, comment)
    return


def removeTemplates(oldtext=''):
    """
    Remove {{Uncategorized}} and {{Check categories}} templates
    """
    result = re.sub(
        '\{\{\s*([Uu]ncat(egori[sz]ed( image)?)?|[Nn]ocat|[Nn]eedscategory)[^}]*\}\}', '', oldtext)
    result = re.sub('<!-- Remove this line once you have added categories -->',
                    '', result)
    result = re.sub('\{\{\s*[Cc]heck categories[^}]*\}\}', '', result)
    return result


def getCheckCategoriesTemplate(usage, galleries, ncats):
    """
    Build the check categories template with all parameters
    """
    result = '{{Check categories|year={{subst:CURRENTYEAR}}|month={{subst:CURRENTMONTHNAME}}|day={{subst:CURRENTDAY}}\n'
    usageCounter = 1
    for (lang, project, article) in usage:
        result += '|lang%d=%s' % (usageCounter, lang)
        result += '|wiki%d=%s' % (usageCounter, project)
        result += '|article%d=%s' % (usageCounter, article)
        result += '\n'
        usageCounter += 1
    galleryCounter = 1
    for gallery in galleries:
        result += '|gallery%d=%s' % (galleryCounter, gallery.replace('_', ' ')) + '\n'
        galleryCounter += 1
    result += '|ncats=%d\n' % ncats
    result += '}}\n'
    return result


def main(args):
    """
    Main loop. Get a generator and options. Work on all images in the generator.
    """
    generator = None
    onlyFilter = False
    onlyUncat = False
    genFactory = pagegenerators.GeneratorFactory()

    global search_wikis
    global hint_wiki

    site = pywikibot.getSite('commons', 'commons')
    for arg in pywikibot.handleArgs():
        if arg == '-onlyfilter':
            onlyFilter = True
        elif arg == '-onlyuncat':
            onlyUncat = True
        elif arg.startswith('-hint:'):
            hint_wiki = arg[len('-hint:'):]
        elif arg.startswith('-onlyhint'):
            search_wikis = arg[len('-onlyhint:'):]
        else:
            genFactory.handleArg(arg)

    generator = genFactory.getCombinedGenerator()
    if not generator:
        generator = pagegenerators.CategorizedPageGenerator(
            Category(site, 'Category:Media needing categories'),
            recurse=True)
    initLists()
    categorizeImages(generator, onlyFilter, onlyUncat)
    pywikibot.output('All done')

if __name__ == "__main__":
    main(sys.argv[1:])
