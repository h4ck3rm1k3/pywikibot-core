#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
With this tool you can add the template {{commonscat}} to categories.
The tool works by following the interwiki links. If the template is present on
another langauge page, the bot will use it.

You could probably use it at articles as well, but this isn't tested.

This bot uses pagegenerators to get a list of pages. The following options are
supported:

&params;

-always           Don't prompt you for each replacement. Warning message
                  has not to be confirmed. ATTENTION: Use this with care!

-summary:XYZ      Set the action summary message for the edit to XYZ,
                  otherwise it uses messages from add_text.py as default.

-checkcurrent     Work on all category pages that use the primary commonscat
                  template.

For example to go through all categories:
commonscat.py -start:Category:!
"""
"""
Commonscat bot:

Take a page. Follow the interwiki's and look for the commonscat template
*Found zero templates. Done.
*Found one template. Add this template
*Found more templates. Ask the user <- still have to implement this

TODO:
*Update interwiki's at commons
*Collect all possibilities also if local wiki already has link.
*Better support for other templates (translations) / redundant templates.
*Check mode, only check pages which already have the template
*More efficient like interwiki.py
*Possibility to update other languages in the same run
"""

"""
Porting notes:

*Ported from compat to core
*Replaced now-deprecated Page methods
*Fixed way of finding interlanguage links in findCommonscatLink()
*Removed unused and now possibly broken updateInterwiki() method

Ported by Allen Guo <Guoguo12@gmail.com>
November 2013
"""

#
# (C) Multichill, 2008-2009
# (C) Xqt, 2009-2013
# (C) Pywikipedia bot team, 2008-2012
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import re
from pywikibot.bot import log
from . import add_text
import pywikibot
#from pywikibot import config
from pywikibot import pagegenerators

docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}

# Primary template, list of alternatives
# No entry needed if it is like _default
commonscatTemplates = {
    '_default': ('Commonscat', []),
    'af': ('CommonsKategorie', ['commonscat']),
    'an': ('Commonscat', ['Commons cat']),
    'ar': ('تصنيف كومنز',
           ['Commonscat', 'تصنيف كومونز', 'Commons cat', 'CommonsCat']),
    'arz': ('Commons cat', ['Commoncat']),
    'az': ('CommonsKat', ['Commonscat']),
    'bn': ('কমন্সক্যাট', ['Commonscat']),
    'ca': ('Commonscat', ['Commons cat', 'Commons category']),
    'crh': ('CommonsKat', ['Commonscat']),
    'cs': ('Commonscat', ['Commons cat']),
    'da': ('Commonscat',
           ['Commons cat', 'Commons category', 'Commonscat left',
            'Commonscat2']),
    'de': ('Commonscat', ['Commons cat']),
    'en': ('Commons category',
           ['Commoncat', 'Commonscat', 'Commons cat', 'Commons+cat',
            'Commonscategory', 'Commons and category', 'Commonscat-inline',
            'Commons category-inline', 'Commons2', 'Commons category multi',
            'Cms-catlist-up', 'Catlst commons', 'Commonscat show2',
            'Sister project links']),
    'es': ('Commonscat',
           ['Ccat', 'Commons cat', 'Categoría Commons',
            'Commonscat-inline']),
    'et': ('Commonsi kategooria',
           ['Commonscat', 'Commonskat', 'Commons cat', 'Commons category']),
    'eu': ('Commonskat', ['Commonscat']),
    'fa': ('ویکی‌انبار-رده',
           ['Commonscat', 'Commons cat', 'انبار رده', 'Commons category',
            'انبار-رده', 'جعبه پیوند به پروژه‌های خواهر',
            'در پروژه‌های خواهر', 'پروژه‌های خواهر']),
    'fr': ('Commonscat', ['CommonsCat', 'Commons cat', 'Commons category']),
    'frp': ('Commonscat', ['CommonsCat']),
    'ga': ('Catcómhaoin', ['Commonscat']),
    'hi': ('Commonscat', ['Commons2', 'Commons cat', 'Commons category']),
    'hu': ('Commonskat', ['Közvagyonkat']),
    'hy': ('Վիքիպահեստ կատեգորիա',
           ['Commonscat', 'Commons cat', 'Commons category']),
    'id': ('Commonscat',
           ['Commons cat', 'Commons2', 'CommonsCat', 'Commons category']),
    'is': ('CommonsCat', ['Commonscat']),
    'ja': ('Commonscat', ['Commons cat', 'Commons category']),
    'jv': ('Commonscat', ['Commons cat']),
    'kaa': ('Commons cat', ['Commonscat']),
    'kk': ('Commonscat', ['Commons2']),
    'ko': ('Commonscat', ['Commons cat', '공용분류']),
    'la': ('CommuniaCat', []),
    'mk': ('Ризница-врска',
           ['Commonscat', 'Commons cat', 'CommonsCat', 'Commons2',
            'Commons category']),
    'ml': ('Commonscat', ['Commons cat', 'Commons2']),
    'ms': ('Kategori Commons', ['Commonscat', 'Commons category']),
    'nn': ('Commonscat', ['Commons cat']),
    'os': ('Commonscat', ['Commons cat']),
    'pt': ('Commonscat', ['Commons cat']),
    'ro': ('Commonscat', ['Commons cat']),
    'ru': ('Commonscat', ['Викисклад-кат', 'Commons category']),
    'simple': ('Commonscat',
               ['Commons cat',  'Commons cat multi', 'Commons category',
                'Commons category multi', 'CommonsCompact',
                'Commons-inline']),
    'sh': ('Commonscat', ['Commons cat']),
    'sl': ('Kategorija v Zbirki',
           ['Commonscat', 'Kategorija v zbirki', 'Commons cat',
            'Katzbirke']),
    'sv': ('Commonscat',
           ['Commonscat-rad', 'Commonskat', 'Commons cat', 'Commonscatbox',
            'Commonscat-box']),
    'sw': ('Commonscat', ['Commons2', 'Commons cat']),
    'te': ('Commonscat', ['Commons cat']),
    'tr': ('Commons kategori',
           ['CommonsKat', 'Commonscat', 'Commons cat']),
    'uk': ('Commonscat', ['Commons cat', 'Category', 'Commonscat-inline']),
    'vi': ('Commonscat',
           ['Commons2', 'Commons cat', 'Commons category', 'Commons+cat']),
    'zh': ('Commonscat', ['Commons cat', 'Commons category']),
    'zh-classical': ('共享類', ['Commonscat']),
    'zh-yue': ('同享類',
               ['Commonscat', '共享類 ', 'Commons cat', 'Commons category']),
}

ignoreTemplates = {
    'af': ['commons'],
    'ar': ['تحويلة تصنيف', 'كومنز', 'كومونز', 'Commons'],
    'be-x-old': ['Commons', 'Commons category'],
    'cs': ['Commons', 'Sestřičky', 'Sisterlinks'],
    'da': ['Commons', 'Commons left', 'Commons2', 'Commonsbilleder',
           'Commonskat', 'Commonscat2', 'GalleriCommons', 'Søsterlinks'],
    'de': ['Commons', 'ZhSZV', 'Bauwerk-stil-kategorien',
           'Bauwerk-funktion-kategorien', 'KsPuB',
           'Kategoriesystem Augsburg-Infoleiste',
           'Kategorie Ge', 'Kategorie v. Chr. Ge',
           'Kategorie Geboren nach Jh. v. Chr.', 'Kategorie Geboren nach Jh.',
           '!Kategorie Gestorben nach Jh. v. Chr.',
           '!Kategorie Gestorben nach Jh.',
           'Kategorie Jahr', 'Kategorie Jahr v. Chr.',
           'Kategorie Jahrzehnt', 'Kategorie Jahrzehnt v. Chr.',
           'Kategorie Jahrhundert', 'Kategorie Jahrhundert v. Chr.',
           'Kategorie Jahrtausend', 'Kategorie Jahrtausend v. Chr.'],
    'en': ['Category redirect', 'Commons', 'Commonscat1A', 'Commoncats',
           'Commonscat4Ra',
           'Sisterlinks', 'Sisterlinkswp', 'Sister project links',
           'Tracking category', 'Template category', 'Wikipedia category'],
    'eo': ['Commons',
           ('Projekto/box', 'commons='),
           ('Projekto', 'commons='),
           ('Projektoj', 'commons='),
           ('Projektoj', 'commonscat=')],
    'es': ['Commons', 'IprCommonscat'],
    'eu': ['Commons'],
    'fa': ['Commons', 'ویکی‌انبار', 'Category redirect', 'رده بهتر',
           'جعبه پیوند به پروژه‌های خواهر', 'در پروژه‌های خواهر',
           'پروژه‌های خواهر'],
    'fi': ['Commonscat-rivi', 'Commons-rivi', 'Commons'],
    'fr': ['Commons', 'Commons-inline', ('Autres projets', 'commons=')],
    'fy': ['Commons', 'CommonsLyts'],
    'hr': ['Commons', ('WProjekti', 'commonscat=')],
    'is': ['Systurverkefni', 'Commons'],
    'it': [('Ip', 'commons='), ('Interprogetto', 'commons=')],
    'ja': ['CommonscatS', 'SisterlinksN', 'Interwikicat'],
    'ms': ['Commons', 'Sisterlinks', 'Commons cat show2'],
    'nds-nl': ['Commons'],
    'nl': ['Commons', 'Commonsklein', 'Commonscatklein', 'Catbeg',
           'Catsjab', 'Catwiki'],
    'om': ['Commons'],
    'pt': ['Correlatos'],
    'simple': ['Sisterlinks'],
    'ru': ['Навигация', 'Навигация для категорий', 'КПР', 'КБР',
           'Годы в России', 'commonscat-inline'],
    'tt': ['Навигация'],
    'zh': ['Category redirect', 'cr', 'Commons',
           'Sisterlinks', 'Sisterlinkswp',
           'Tracking category', 'Trackingcatu',
           'Template category', 'Wikipedia category'
           '分类重定向', '追蹤分類', '共享資源', '追蹤分類'],
}

msg_change = {
    'be-x-old': 'Робат: зьмяніў шаблён [[:Commons:Category:%(oldcat)s|%(oldcat)s]] на [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'cs': 'Robot změnil šablonu Commonscat z [[:Commons:Category:%(oldcat)s|%(oldcat)s]] na [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'da': 'Robot: Ændrer commonscat link fra [[:Commons:Category:%(oldcat)s|%(oldcat)s]] til [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'de': 'Bot: Ändere commonscat link von [[:Commons:Category:%(oldcat)s|%(oldcat)s]] zu [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'en': 'Bot: Changing commonscat link from [[:Commons:Category:%(oldcat)s|%(oldcat)s]] to [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'fa': 'ربات: تغییر پیوند به انبار از [[:Commons:Category:%(oldcat)s|%(oldcat)s]] به [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'fr': 'Robot: Changé commonscat link de [[:Commons:Category:%(oldcat)s|%(oldcat)s]] à [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'frr': 'Bot: Feranere commonscat link faan [[:Commons:Category:%(oldcat)s|%(oldcat)s]] tu [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'is': 'Vélmenni: Breyti Commonscat tengli frá [[:Commons:Category:%(oldcat)s|%(oldcat)s]] í [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'pdc': 'Waddefresser: commonscat Gleecher vun [[:Commons:Category:%(oldcat)s|%(oldcat)s]] nooch [[:Commons:Category:%(newcat)s|%(newcat)s]] geennert',
    'ru': 'Бот: Изменение commonscat-ссылки с [[:Commons:Category:%(oldcat)s|%(oldcat)s]] на [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'sk': 'Robot zmenil šablónu Commonscat z [[:Commons:Category:%(oldcat)s|%(oldcat)s]] na [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'uk': 'Бот: Зміна commonscat-посилання з [[:Commons:Category:%(oldcat)s|%(oldcat)s]] на [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'th': 'บอต: เปลี่ยนลิงก์หมวดหมู่คอมมอนส์จาก [[:Commons:Category:%(oldcat)s|%(oldcat)s]] เป็น [[:Commons:Category:%(newcat)s|%(newcat)s]]',
    'zh': '機器人：更改 commonscat 連結，從 %(oldcat)s 至 %(newcat)s',
}


class CommonscatBot:

    def __init__(self, generator, always, summary=None):
        self.generator = generator
        self.always = always
        self.summary = summary
        self.site = pywikibot.getSite()

    def run(self):
        for page in self.generator:
            self.treat(page)

    def treat(self, page):
        """ Loads the given page, does some changes, and saves it. """
        if not page.exists():
            pywikibot.output('Page %s does not exist. Skipping.'
                             % page.title(asLink=True))
        elif page.isRedirectPage():
            pywikibot.output('Page %s is a redirect. Skipping.'
                             % page.title(asLink=True))
        elif page.isCategoryRedirect():
            pywikibot.output('Page %s is a category redirect. Skipping.'
                             % page.title(asLink=True))
        elif page.isDisambig():
            pywikibot.output('Page %s is a disambiguation. Skipping.'
                             % page.title(asLink=True))
        else:
            (status, always) = self.addCommonscat(page)
        return

    def load(self, page):
        """ Loads the given page, does some changes, and saves it. """
        try:
            text = page.get()
        except pywikibot.NoPage:
            pywikibot.output("Page %s does not exist; skipping."
                             % page.title(asLink=True))
        except pywikibot.IsRedirectPage:
            pywikibot.output("Page %s is a redirect; skipping."
                             % page.title(asLink=True))
        else:
            return text
        return None

    def save(self, text, page, comment, minorEdit=True, botflag=True):
        # only save if something was changed
        if text != page.get():
            # Show the title of the page we're working on.
            # Highlight the title in purple.
            pywikibot.output("\n\n>>> \03{lightpurple}%s\03{default} <<<"
                             % page.title())
            # show what was changed
            pywikibot.showDiff(page.get(), text)
            pywikibot.output('Comment: %s' % comment)
            if not self.always:
                choice = pywikibot.inputChoice(
                    'Do you want to accept these changes?',
                    ['Yes', 'No', 'Always', 'Quit'],
                    ['y', 'N', 'a', 'q'], 'N')
                if choice == 'a':
                    self.always = True
                elif choice == 'q':
                    import sys
                    sys.exit()
            if self.always or choice == 'y':
                try:
                    # Save the page
                    page.put(text, comment=comment,
                             minorEdit=minorEdit, botflag=botflag)
                except pywikibot.LockedPage:
                    pywikibot.output("Page %s is locked; skipping."
                                     % page.title(asLink=True))
                except pywikibot.EditConflict:
                    pywikibot.output(
                        'Skipping %s because of edit conflict'
                        % (page.title()))
                except pywikibot.SpamfilterError as error:
                    pywikibot.output(
                        'Cannot change %s because of spam blacklist entry %s'
                        % (page.title(), error.url))
                else:
                    return True
        return False

    @classmethod
    def getCommonscatTemplate(self, lang=None):
        """Get the template name in a language. Expects the language code.
        Return as tuple containing the primary template and it's alternatives

        """
        if lang in commonscatTemplates:
            return commonscatTemplates[lang]
        else:
            return commonscatTemplates['_default']

    def skipPage(self, page):
        '''
        Do we want to skip this page?
        '''
        if page.site.language() in ignoreTemplates:
            templatesInThePage = page.templates()
            templatesWithParams = page.templatesWithParams()
            for template in ignoreTemplates[page.site.language()]:
                if type(template) != tuple:
                    for pageTemplate in templatesInThePage:
                        if pageTemplate.title(withNamespace=False) == template:
                            return True
                else:
                    for (inPageTemplate, param) in templatesWithParams:
                        if inPageTemplate.title(withNamespace=False) == template[0] \
                           and template[1] in param[0].replace(' ', ''):
                            return True
        return False

    def addCommonscat(self, page):
        """Take a page. Go to all the interwiki page looking for a commonscat
        template. When all the interwiki's links are checked and a proper
        category is found add it to the page.

        """
        pywikibot.output('Working on ' + page.title())
        # Get the right templates for this page
        primaryCommonscat, commonscatAlternatives = self.getCommonscatTemplate(
            page.site.language())
        commonscatLink = self.getCommonscatLink(page)
        if commonscatLink:
            pywikibot.output('Commonscat template is already on %s'
                             % page.title())
            (currentCommonscatTemplate,
             currentCommonscatTarget, LinkText, Note) = commonscatLink
            checkedCommonscatTarget = self.checkCommonscatLink(
                currentCommonscatTarget)
            if (currentCommonscatTarget == checkedCommonscatTarget):
                # The current commonscat link is good
                pywikibot.output('Commonscat link at %s to Category:%s is ok'
                                 % (page.title(), currentCommonscatTarget))
                return (True, self.always)
            elif checkedCommonscatTarget != '':
                # We have a new Commonscat link, replace the old one
                self.changeCommonscat(page, currentCommonscatTemplate,
                                      currentCommonscatTarget,
                                      primaryCommonscat,
                                      checkedCommonscatTarget, LinkText, Note)
                return (True, self.always)
            else:
                #Commonscat link is wrong
                commonscatLink = self.findCommonscatLink(page)
                if (commonscatLink != ''):
                    self.changeCommonscat(page, currentCommonscatTemplate,
                                          currentCommonscatTarget,
                                          primaryCommonscat, commonscatLink)
                #else
                #Should i remove the commonscat link?

        elif self.skipPage(page):
            pywikibot.output("Found a template in the skip list. Skipping %s"
                             % page.title())
        else:
            commonscatLink = self.findCommonscatLink(page)
            if (commonscatLink != ''):
                if commonscatLink == page.title():
                    textToAdd = '{{%s}}' % primaryCommonscat
                else:
                    textToAdd = '{{%s|%s}}' % (primaryCommonscat,
                                                commonscatLink)
                (success, status, self.always) = add_text.add_text(page,
                                                                   textToAdd,
                                                                   self.summary,
                                                                   None, None,
                                                                   self.always)
                return (True, self.always)
        return (True, self.always)

    def changeCommonscat(self, page=None, oldtemplate='', oldcat='',
                         newtemplate='', newcat='', linktitle='',
                         description=''):
        """ Change the current commonscat template and target. """
        if oldcat == '3=S' or linktitle == '3=S':
            return  # additional param on de-wiki, TODO: to be handled
        if not linktitle and (page.title().lower() in oldcat.lower() or
                              oldcat.lower() in page.title().lower()):
            linktitle = oldcat
        if linktitle and newcat != page.title(withNamespace=False):
            newtext = re.sub('(?i)\{\{%s\|?[^{}]*(?:\{\{.*\}\})?\}\}'
                             % oldtemplate,
                             '{{%s|%s|%s}}' % (newtemplate, newcat, linktitle),
                             page.get())
        elif newcat == page.title(withNamespace=False):
            newtext = re.sub('(?i)\{\{%s\|?[^{}]*(?:\{\{.*\}\})?\}\}'
                             % oldtemplate,
                             '{{%s}}' % newtemplate,
                             page.get())
        elif oldcat.strip() != newcat:  # strip trailing white space
            newtext = re.sub('(?i)\{\{%s\|?[^{}]*(?:\{\{.*\}\})?\}\}'
                             % oldtemplate,
                             '{{%s|%s}}' % (newtemplate, newcat),
                             page.get())
        else:  # nothing left to do
            return
        if self.summary:
            comment = self.summary
        else:
            comment = pywikibot.translate(page.site(),
                                          msg_change) % {'oldcat': oldcat,
                                                         'newcat': newcat}
        self.save(newtext, page, comment)

    def findCommonscatLink(self, page=None):
        # In Pywikibot 2.0, page.interwiki() now returns Link objects, not Page objects
        for ipageLink in page.langlinks():
            ipage = Page(ipageLink)
            log("Looking for template on %s" % (ipage.title()))
            try:
                if(ipage.exists() and not ipage.isRedirectPage()
                   and not ipage.isDisambig()):
                    commonscatLink = self.getCommonscatLink(ipage)
                    if commonscatLink:
                        (currentTemplate,
                         possibleCommonscat, linkText, Note) = commonscatLink
                        checkedCommonscat = self.checkCommonscatLink(
                            possibleCommonscat)
                        if (checkedCommonscat != ''):
                            pywikibot.output(
                                "Found link for %s at [[%s:%s]] to %s."
                                % (page.title(), ipage.site.language(),
                                   ipage.title(), checkedCommonscat))
                            return checkedCommonscat
            except pywikibot.BadTitle:
                #The interwiki was incorrect
                return ''
        return ''

    def getCommonscatLink(self, wikipediaPage=None):
        '''
        Go through the page and return a tuple of (<templatename>, <target>)
        '''
        primaryCommonscat, commonscatAlternatives = self.getCommonscatTemplate(
            wikipediaPage.site.language())
        commonscatTemplate = ''
        commonscatTarget = ''
        commonscatLinktext = ''
        commonscatNote = ''
        # See if commonscat is present
        for template in wikipediaPage.templatesWithParams():
            templateTitle = template[0].title(withNamespace=False)
            if templateTitle == primaryCommonscat \
               or templateTitle in commonscatAlternatives:
                commonscatTemplate = templateTitle
                if (len(template[1]) > 0):
                    commonscatTarget = template[1][0]
                    if len(template[1]) > 1:
                        commonscatLinktext = template[1][1]
                    if len(template[1]) > 2:
                        commonscatNote = template[1][2]
                else:
                    commonscatTarget = wikipediaPage.title(withNamespace=False)
                return (commonscatTemplate, commonscatTarget,
                        commonscatLinktext, commonscatNote)
        return None

    def checkCommonscatLink(self, name=""):
        """ This function will return the name of a valid commons category
        If the page is a redirect this function tries to follow it.
        If the page doesnt exists the function will return an empty string

        """
        log("getCommonscat: " + name)
        try:
            commonsSite = self.site.image_repository()
            #This can throw a pywikibot.BadTitle
            commonsPage = pywikibot.Page(commonsSite, "Category:" + name)

            if not commonsPage.exists():
                pywikibot.output('Commons category does not exist. Examining deletion log...')
                logpages = commonsSite.logevents(logtype='delete', page=commonsPage)
                for logitem in logpages:
                    logitem = next(logpages)
                    (logpage, loguser, logtimestamp, logcomment) = logitem
                    # Some logic to extract the target page.
                    regex = 'moved to \[\[\:?Category:(?P<newcat1>[^\|\}]+)(\|[^\}]+)?\]\]|Robot: Changing Category:(.+) to Category:(?P<newcat2>.+)'
                    m = re.search(regex, logcomment, flags=re.I)
                    if m:
                        if m.group('newcat1'):
                            return self.checkCommonscatLink(m.group('newcat1'))
                        elif m.group('newcat2'):
                            return self.checkCommonscatLink(m.group('newcat2'))
                    else:
                        pywikibot.output(
                            'getCommonscat: Deleted by %s. Couldn\'t find '
                            'move target in "%s"'
                            % (loguser, logcomment))
                        return ''
                return ''
            elif commonsPage.isRedirectPage():
                log("getCommonscat: The category is a redirect")
                return self.checkCommonscatLink(
                    commonsPage.getRedirectTarget().title(withNamespace=False))
            elif "Category redirect" in commonsPage.templates():
                log("getCommonscat: The category is a category redirect")
                for template in commonsPage.templatesWithParams():
                    if (template[0] == "Category redirect" and
                            len(template[1]) > 0):
                        return self.checkCommonscatLink(template[1][0])
            elif commonsPage.isDisambig():
                log("getCommonscat: The category is disambiguation")
                return ''
            else:
                return commonsPage.title(withNamespace=False)
        except pywikibot.BadTitle:
            # Funky title so not correct
            return ''
        except pywikibot.PageNotFound:
            return ''


def main():
    """ Parse the command line arguments and get a pagegenerator to work on.
    Iterate through all the pages.
    """

    summary = None
    generator = None
    #checkcurrent = False
    always = False
    ns = []
    ns.append(14)
    # Load a lot of default generators
    genFactory = pagegenerators.GeneratorFactory()

    for arg in pywikibot.handleArgs():
        if arg.startswith('-summary'):
            if len(arg) == 8:
                summary = pywikibot.input('What summary do you want to use?')
            else:
                summary = arg[9:]
        elif arg.startswith('-checkcurrent'):
            #checkcurrent = True
            primaryCommonscat, commonscatAlternatives = \
                CommonscatBot.getCommonscatTemplate(
                    pywikibot.getSite().language())
            generator = pagegenerators.NamespaceFilterPageGenerator(
                pagegenerators.ReferringPageGenerator(
                    pywikibot.Page(pywikibot.getSite(),
                                   'Template:' + primaryCommonscat),
                    onlyTemplateInclusion=True), ns)

        elif arg == '-always':
            always = True
        else:
            genFactory.handleArg(arg)

    if not generator:
        generator = genFactory.getCombinedGenerator()
    if not generator:
        raise add_text.NoEnoughData('You have to specify the generator you '
                                    'want to use for the script!')

    pregenerator = pagegenerators.PreloadingGenerator(generator)
    bot = CommonscatBot(pregenerator, always, summary)
    bot.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
