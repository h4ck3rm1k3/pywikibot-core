# -*- coding: utf-8  -*-
#
# (C) Rob W.W. Hooft, 2003
# (C) Yuri Astrakhan, 2005
# (C) Pywikipedia bot team, 2003-2010
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#
import re

import pywikibot
import pywikibot.date as date


def translate(page, hints=None, auto=True, removebrackets=False, site=None, family=None):
    """
    Goes through all entries in 'hints'. Returns a list of pages.

    Entries for single page titles list those pages. Page titles for entries
    such as "all:" or "xyz:" or "20:" are first built from the page title of
    'page' and then listed. When 'removebrackets' is True, a trailing pair of
    brackets and the text between them is removed from the page title.
    If 'auto' is true, known year and date page titles are autotranslated
    to all known target languages and inserted into the list.

    """
    result = []
    if site is None and page:
        site = page.site
    if family is None and site:
        family = site.family
    #if site:
        #sitelang = site.language()
    if hints:
        for h in hints:
            if ':' not in h:
                # argument given as -hint:xy where xy is a language code
                codes = h
                newname = ''
            else:
                codes, newname = h.split(':', 1)
            if newname == '':
                # if given as -hint:xy or -hint:xy:, assume that there should
                # be a page in language xy with the same title as the page
                # we're currently working on ...
                if page is None:
                    continue
                ns = page.namespace()
                if ns:
                    newname = u'%s:%s' % (family.namespace('_default', ns),
                                          page.title(withNamespace=False))
                else:
                    # article in the main namespace
                    newname = page.title()
                # ... unless we do want brackets
                if removebrackets:
                    newname = re.sub(re.compile(ur"\W*?\(.*?\)\W*?", re.UNICODE), u" ", newname)
            try:
                number = int(codes)
                codes = site.family.languages_by_size[:number]
            except ValueError:
                if codes == 'all':
                    codes = site.family.languages_by_size
                elif codes in site.family.language_groups:
                    codes = site.family.language_groups[codes]
                else:
                    codes = codes.split(',')
            for newcode in codes:
                if newcode in site.languages():
                    if newcode != site.code:
                        x = pywikibot.Link(site.getSite(code=newcode), newname)
                        if x not in result:
                            result.append(x)
                else:
                    if pywikibot.verbose:
                        pywikibot.output(u"Ignoring unknown language code %s"
                                         % newcode)

    # Autotranslate dates into all other languages, the rest will come from
    # existing interwiki links.
    if auto and page:
        # search inside all dictionaries for this link
        dictName, value = date.getAutoFormat(page.site.code,
                                             page.title())
        if dictName:
            if not (dictName == 'yearsBC' and
                    page.site.code in date.maxyearBC and
                    value > date.maxyearBC[page.site.code]) or \
                    (dictName == 'yearsAD' and
                     page.site.code in date.maxyearAD and
                     value > date.maxyearAD[page.site.code]):
                pywikibot.output(
                    u'TitleTranslate: %s was recognized as %s with value %d'
                    % (page.title(), dictName, value))
                for entryLang, entry in date.formats[dictName].iteritems():
                    if entryLang != page.site.code:
                        if (dictName == 'yearsBC' and
                                entryLang in date.maxyearBC and
                                value > date.maxyearBC[entryLang]):
                            pass
                        elif (dictName == 'yearsAD' and
                              entryLang in date.maxyearAD and
                              value > date.maxyearAD[entryLang]):
                            pass
            else:
                            newname = entry(value)
                            x = pywikibot.Link(
                                newname,
                                pywikibot.getSite(code=entryLang,
                                                  fam=site.family))
                            if x not in result:
                                result.append(x)  # add new page
    return result

bcDateErrors = [u'[[ko:%d년]]']


def appendFormatedDates(result, dictName, value):
    for code, func in date.formats[dictName].iteritems():
        result.append(u'[[%s:%s]]' % (code, func(value)))


def getPoisonedLinks(pl):
    """Returns a list of known corrupted links that should be removed if seen

    """
    result = []
    pywikibot.output(u'getting poisoned links for %s' % pl.title())
    dictName, value = date.getAutoFormat(pl.site.code, pl.title())
    if dictName is not None:
        pywikibot.output(u'date found in %s' % dictName)
        # errors in year BC
        if dictName in date.bcFormats:
            for fmt in bcDateErrors:
                result.append(fmt % value)
        # i guess this is like friday the 13th for the years
        if value == 398 and dictName == 'yearsBC':
            appendFormatedDates(result, dictName, 399)
        if dictName == 'yearsBC':
            appendFormatedDates(result, 'decadesBC', value)
            appendFormatedDates(result, 'yearsAD', value)
        if dictName == 'yearsAD':
            appendFormatedDates(result, 'decadesAD', value)
            appendFormatedDates(result, 'yearsBC', value)
        if dictName == 'centuriesBC':
            appendFormatedDates(result, 'decadesBC', value * 100 + 1)
        if dictName == 'centuriesAD':
            appendFormatedDates(result, 'decadesAD', value * 100 + 1)
    return result
