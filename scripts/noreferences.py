#!/usr/bin/python
# -*- coding: utf-8  -*-

"""
This script goes over multiple pages, searches for pages where <references />
is missing although a <ref> tag is present, and in that case adds a new
references section.

These command line parameters can be used to specify which pages to work on:

&params;

    -xml          Retrieve information from a local XML dump (pages-articles
                  or pages-meta-current, see http://download.wikimedia.org).
                  Argument can also be given as "-xml:filename".

    -namespace:n  Number or name of namespace to process. The parameter can be
                  used multiple times. It works in combination with all other
                  parameters, except for the -start parameter. If you e.g.
                  want to iterate over all categories starting at M, use
                  -start:Category:M.

    -always       Don't prompt you for each replacement.

All other parameters will be regarded as part of the title of a single page,
and the bot will only work on that single page.

If neither a page title nor a page generator is given, it takes all pages from
the default maintenance category.

It is strongly recommended not to run this script over the entire article
namespace (using the -start) parameter, as that would consume too much
bandwidth. Instead, use the -xml parameter, or use another way to generate
a list of affected articles
"""

__version__ = '$Id$'

import re
#import sys
import pywikibot
from pywikibot import i18n
from pywikibot import pagegenerators, catlib
#import editarticle

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;':     pagegenerators.parameterHelp,
}

# References sections are usually placed before further reading / external
# link sections. This dictionary defines these sections, sorted by priority.
# For example, on an English wiki, the script would place the "References"
# section in front of the "Further reading" section, if that existed.
# Otherwise, it would try to put it in front of the "External links" section,
# or if that fails, the "See also" section, etc.
placeBeforeSections = {
    'ar': [              # no explicit policy on where to put the references
        'وصلات خارجية',
        'انظر أيضا',
        'ملاحظات'
    ],
    'cs': [
        'Reference',
        'Poznámky',
    ],
    'da': [              # no explicit policy on where to put the references
        'Eksterne links'
    ],
    'de': [              # no explicit policy on where to put the references
        'Literatur',
        'Weblinks',
        'Siehe auch',
        'Weblink',      # bad, but common singular form of Weblinks
    ],
    'dsb': [
        'Nožki',
    ],
    'en': [              # no explicit policy on where to put the references
        'Further reading',
        'External links',
        'See also',
        'Notes'
    ],
    'ru': [
        'Ссылки',
        'Литература',
    ],
    'eo': [
        'Eksteraj ligiloj',
        'Ekstera ligilo',
        'Eksteraj ligoj',
        'Ekstera ligo',
        'Rete'
    ],
    'es': [
        'Enlaces externos',
        'Véase también',
        'Notas',
    ],
    'fa': [
        'پیوند به بیرون',
        'پانویس',
        'جستارهای وابسته'
    ],
    'fi': [
        'Kirjallisuutta',
        'Aiheesta muualla',
        'Ulkoiset linkit',
        'Linkkejä',
    ],
    'fr': [
        'Liens externes',
        'Voir aussi',
        'Notes'
    ],
    'hsb': [
        'Nóžki',
    ],
    'hu': [
        'Külső hivatkozások',
        'Lásd még',
    ],
    'it': [
        'Bibliografia',
        'Voci correlate',
        'Altri progetti',
        'Collegamenti esterni',
        'Vedi anche',
    ],
    'ja': [
        '関連項目',
        '参考文献',
        '外部リンク',
    ],
    'ko': [              # no explicit policy on where to put the references
        '외부 링크',
        '외부링크',
        '바깥 고리',
        '바깥고리',
        '바깥 링크',
        '바깥링크'
        '외부 고리',
        '외부고리'
    ],
    'lt': [              # no explicit policy on where to put the references
        'Nuorodos'
    ],
    'nl': [              # no explicit policy on where to put the references
        'Literatuur',
        'Zie ook',
        'Externe verwijzingen',
        'Externe verwijzing',
    ],
    'pdc': [
        'Beweisunge',
        'Quelle unn Literatur',
        'Gwelle',
        'Gwuelle',
        'Auswenniche Gleecher',
        'Gewebbgleecher',
        'Guckt mol aa',
        'Seh aa',
    ],
    'pl': [
        'Źródła',
        'Bibliografia',
        'Zobacz też',
        'Linki zewnętrzne',
    ],
    'pt': [
        'Ligações externas',
        'Veja também',
        'Ver também',
        'Notas',
    ],
    'sk': [
        'Pozri aj',
    ],
    'szl': [
        'Przipisy',
        'Připisy',
    ],
    'zh': [
        '外部链接',
        '外部連结',
        '外部連結',
        '外部连接',
    ],
}

# Titles of sections where a reference tag would fit into.
# The first title should be the preferred one: It's the one that
# will be used when a new section has to be created.
referencesSections = {
    'ar': [             # not sure about which ones are preferred.
        'مراجع',
        'ملاحظات',
    ],
    'da': [
        'Noter',
    ],
    'de': [             # see [[de:WP:REF]]
        'Einzelnachweise',
        'Anmerkungen',
        'Belege',
        'Endnoten',
        'Fußnoten',
        'Fuß-/Endnoten',
        'Quellen',
        'Quellenangaben',
    ],
    'dsb': [
        'Nožki',
    ],
    'en': [             # not sure about which ones are preferred.
        'References',
        'Footnotes',
        'Notes',
    ],
    'ru': [
        'Примечания',
        'Сноски',
        'Источники',
    ],
    'eo': [
        'Referencoj',
    ],
    'es': [
        'Referencias',
        'Notas',
    ],
    'fa': [
        'منابع',
        'منبع'
    ],
    'fi': [
        'Lähteet',
        'Viitteet',
    ],
    'fr': [             # [[fr:Aide:Note]]
        'Notes et références',
        'Références',
        'References',
        'Notes'
    ],
    'he': [
        'הערות שוליים',
    ],
    'hsb': [
        'Nóžki',
    ],
    'hu': [
        'Források és jegyzetek',
        'Források',
        'Jegyzetek',
        'Hivatkozások',
        'Megjegyzések',
    ],
    'is': [
        'Heimildir',
        'Tilvísanir',
    ],
    'it': [
        'Note',
        'Riferimenti',
    ],
    'ja': [
        '脚注',
        '脚注欄',
        '脚注・出典',
        '出典',
        '注釈',
        '註',
    ],
    'ko': [
        '주석',
        '각주'
        '주석 및 참고 자료'
        '주석 및 참고자료',
        '주석 및 참고 출처'
    ],
    'lt': [             # not sure about which ones are preferred.
        'Šaltiniai',
        'Literatūra',
    ],
    'nl': [             # not sure about which ones are preferred.
        'Voetnoten',
        'Voetnoot',
        'Referenties',
        'Noten',
        'Bronvermelding',
    ],
    'pdc': [
        'Aamarrickunge',
    ],
    'pl': [
        'Przypisy',
        'Uwagi',
    ],
    'pt': [
        'Referências',
    ],
    'sk': [
        'Referencie',
    ],
    'szl': [
        'Przipisy',
        'Připisy',
    ],
    'zh': [
        '參考資料',
        '参考资料',
        '參考文獻',
        '参考文献',
        '資料來源',
        '资料来源',
    ],
}

# Templates which include a <references /> tag. If there is no such template
# on your wiki, you don't have to enter anything here.
referencesTemplates = {
    'wikipedia': {
        'ar': ['Reflist', 'ثبت المراجع', 'قائمة المراجع'],
        'be': ['Зноскі', 'Примечания', 'Reflist', 'Спіс заўваг',
               'Заўвагі'],
        'be-x-old': ['Зноскі'],
        'da': ['Reflist'],
        'dsb': ['Referency'],
        'en': ['Reflist', 'Refs', 'FootnotesSmall', 'Reference',
               'Ref-list', 'Reference list', 'References-small', 'Reflink',
               'Footnotes', 'FootnotesSmall'],
        'eo': ['Referencoj'],
        'es': ['Listaref', 'Reflist', 'muchasref'],
        'fa': ['Reflist', 'Refs', 'FootnotesSmall', 'Reference',
               'پانویس', 'پانویس‌ها ', 'پانویس ۲', 'پانویس۲',
               'فهرست منابع'],
        'fi': ['Viitteet', 'Reflist'],
        'fr': ['Références', 'Notes', 'References', 'Reflist'],
        'hsb': ['Referency'],
        'hu': ['reflist', 'források', 'references', 'megjegyzések'],
        'is': ['reflist'],
        'it': ['References'],
        'ja': ['Reflist', '脚注リスト'],
        'ko': ['주석', 'Reflist'],
        'lt': ['Reflist', 'Ref', 'Litref'],
        'nl': ['Reflist', 'Refs', 'FootnotesSmall', 'Reference',
               'Ref-list', 'Reference list', 'References-small', 'Reflink',
               'Referenties', 'Bron', 'Bronnen/noten/referenties', 'Bron2',
               'Bron3', 'ref', 'references', 'appendix',
               'Noot', 'FootnotesSmall'],
        'pl': ['Przypisy', 'Przypisy-lista', 'Uwagi'],
        'pt': ['Notas', 'ref-section', 'Referências', 'Reflist'],
        'ru': ['Reflist', 'Ref-list', 'Refs', 'Sources',
               'Примечания', 'Список примечаний',
               'Сноска', 'Сноски'],
        'szl': ['Przipisy', 'Připisy'],
        'zh': ['Reflist', 'RefFoot', 'NoteFoot'],
    },
}

# Text to be added instead of the <references /> tag.
# Define this only if required by your wiki.
referencesSubstitute = {
    'wikipedia': {
        'be': '{{зноскі}}',
        'da': '{{reflist}}',
        'dsb': '{{referency}}',
        'fa': '{{پانویس}}',
        'fi': '{{viitteet}}',
        'hsb': '{{referency}}',
        'hu': '{{Források}}',
        'pl': '{{Przypisy}}',
        'ru': '{{примечания}}',
        'szl': '{{Przipisy}}',
        'zh': '{{reflist}}',
    },
}

# Sites where no title is required for references template
# as it is already included there
# like pl.wiki where {{Przypisy}} generates
# == Przypisy ==
# <references />
noTitleRequired = ['pl', 'be', 'szl']

maintenance_category = {
    'wikipedia': {
        'be-x-old': 'Вікіпэдыя:Старонкі з адсутным сьпісам зносак',
        'de': 'Wikipedia:Seite mit fehlendem References-Tag',
        'en': 'Pages with missing references list',
        'fa': 'صفحه‌های با یادکرد خراب (فقدان پانویس)',
        'ja': 'Refタグがあるのにreferencesタグがないページ',
        'simple': 'Wikipedia pages with broken references',
        'zh': '参考资料格式错误的页面',
    },
}


class XmlDumpNoReferencesPageGenerator:
    """
    Generator which will yield Pages that might lack a references tag.
    These pages will be retrieved from a local XML dump file
    (pages-articles or pages-meta-current).
    """
    def __init__(self, xmlFilename):
        """
        Arguments:
            * xmlFilename  - The dump's path, either absolute or relative
        """
        self.xmlFilename = xmlFilename
        self.refR = re.compile('</ref>', re.IGNORECASE)
        # The references tab can contain additional spaces and a group
        # attribute.
        self.referencesR = re.compile('<references.*?/>', re.IGNORECASE)

    def __iter__(self):
        import xmlreader
        dump = xmlreader.XmlDump(self.xmlFilename)
        for entry in dump.parse():
            text = pywikibot.removeDisabledParts(entry.text)
            if self.refR.search(text) and not self.referencesR.search(text):
                yield pywikibot.Page(pywikibot.getSite(), entry.title)


class NoReferencesBot:

    def __init__(self, generator, always=False):
        self.generator = generator
        self.always = always
        self.site = pywikibot.getSite()
        self.refR = re.compile('</ref>', re.IGNORECASE)
        self.referencesR = re.compile('<references.*?/>', re.IGNORECASE)
        self.referencesTagR = re.compile('<references>.*?</references>',
                                         re.IGNORECASE | re.DOTALL)
        try:
            self.referencesTemplates = referencesTemplates[
                pywikibot.getSite().family.name][pywikibot.getSite().lang]
        except KeyError:
            self.referencesTemplates = []
        try:
            self.referencesText = referencesSubstitute[
                pywikibot.getSite().family.name][pywikibot.getSite().lang]
        except KeyError:
            self.referencesText = '<references />'

    def lacksReferences(self, text, verbose=True):
        """
        Checks whether or not the page is lacking a references tag.
        """
        oldTextCleaned = pywikibot.removeDisabledParts(text)
        if self.referencesR.search(oldTextCleaned) or \
           self.referencesTagR.search(oldTextCleaned):
            if verbose:
                pywikibot.output('No changes necessary: references tag found.')
            return False
        elif self.referencesTemplates:
            templateR = '{{(' + '|'.join(self.referencesTemplates) + ')'
            if re.search(templateR, oldTextCleaned, re.IGNORECASE | re.UNICODE):
                if verbose:
                    pywikibot.output(
                        'No changes necessary: references template found.')
                return False
        if not self.refR.search(oldTextCleaned):
            if verbose:
                pywikibot.output('No changes necessary: no ref tags found.')
            return False
        else:
            if verbose:
                pywikibot.output('Found ref without references.')
            return True

    def addReferences(self, oldText):
        """
        Tries to add a references tag into an existing section where it fits
        into. If there is no such section, creates a new section containing
        the references tag.
        * Returns : The modified pagetext

        """
        # Is there an existing section where we can add the references tag?
        for section in pywikibot.translate(self.site, referencesSections):
            sectionR = re.compile(r'\r?\n=+ *%s *=+ *\r?\n' % section)
            index = 0
            while index < len(oldText):
                match = sectionR.search(oldText, index)
                if match:
                    if pywikibot.isDisabled(oldText, match.start()):
                        pywikibot.output(
                            'Existing  %s section is commented out, skipping.'
                            % section)
                        index = match.end()
                    else:
                        pywikibot.output(
                            'Adding references tag to existing %s section...\n'
                            % section)
                        newText = (
                            oldText[:match.end()] + '\n' +
                            self.referencesText + '\n' +
                            oldText[match.end():]
                        )
                        return newText
                else:
                    break

        # Create a new section for the references tag
        for section in pywikibot.translate(self.site, placeBeforeSections):
            # Find out where to place the new section
            sectionR = re.compile(r'\r?\n(?P<ident>=+) *%s *(?P=ident) *\r?\n'
                                  % section)
            index = 0
            while index < len(oldText):
                match = sectionR.search(oldText, index)
                if match:
                    if pywikibot.isDisabled(oldText, match.start()):
                        pywikibot.output(
                            'Existing  %s section is commented out, won\'t add '
                            'the references in front of it.' % section)
                        index = match.end()
                    else:
                        pywikibot.output(
                            'Adding references section before %s section...\n'
                            % section)
                        index = match.start()
                        ident = match.group('ident')
                        return self.createReferenceSection(oldText, index,
                                                           ident)
                else:
                    break
        # This gets complicated: we want to place the new references
        # section over the interwiki links and categories, but also
        # over all navigation bars, persondata, and other templates
        # that are at the bottom of the page. So we need some advanced
        # regex magic.
        # The strategy is: create a temporary copy of the text. From that,
        # keep removing interwiki links, templates etc. from the bottom.
        # At the end, look at the length of the temp text. That's the position
        # where we'll insert the references section.
        catNamespaces = '|'.join(self.site.category_namespaces())
        categoryPattern = r'\[\[\s*(%s)\s*:[^\n]*\]\]\s*' % catNamespaces
        interwikiPattern = r'\[\[([a-zA-Z\-]+)\s?:([^\[\]\n]*)\]\]\s*'
        # won't work with nested templates
        # the negative lookahead assures that we'll match the last template
        # occurence in the temp text.
        ### fix me:
        ### {{commons}} or {{commonscat}} are part of Weblinks section
        ### * {{template}} is mostly part of a section
        ### so templatePattern must be fixed
        templatePattern = r'\r?\n{{((?!}}).)+?}}\s*'
        commentPattern = r'<!--((?!-->).)*?-->\s*'
        metadataR = re.compile(r'(\r?\n)?(%s|%s|%s|%s)$'
                               % (categoryPattern, interwikiPattern,
                                  templatePattern, commentPattern), re.DOTALL)
        tmpText = oldText
        while True:
            match = metadataR.search(tmpText)
            if match:
                tmpText = tmpText[:match.start()]
            else:
                break
        pywikibot.output(
            'Found no section that can be preceeded by a new references '
            'section.\nPlacing it before interwiki links, categories, and '
            'bottom templates.')
        index = len(tmpText)
        return self.createReferenceSection(oldText, index)

    def createReferenceSection(self, oldText, index, ident='=='):
        if self.site.language() in noTitleRequired:
            newSection = '\n%s\n' % (self.referencesText)
        else:
            newSection = '\n%s %s %s\n%s\n' % (ident,
                                                pywikibot.translate(
                                                    self.site,
                                                    referencesSections)[0],
                                                ident, self.referencesText)
        return oldText[:index] + newSection + oldText[index:]

    def save(self, page, newText):
        """
        Saves the page to the wiki, if the user accepts the changes made.
        """
        pywikibot.showDiff(page.get(), newText)
        if not self.always:
            choice = pywikibot.inputChoice(
                'Do you want to accept these changes?',
                ['Yes', 'No', 'Always yes'], ['y', 'N', 'a'], 'Y')
            if choice == 'n':
                return
            elif choice == 'a':
                self.always = True

        if self.always:
            try:
                page.put(newText)
            except pywikibot.EditConflict:
                pywikibot.output('Skipping %s because of edit conflict'
                                 % (page.title(),))
            except pywikibot.SpamfilterError as e:
                pywikibot.output(
                    'Cannot change %s because of blacklist entry %s'
                    % (page.title(), e.url))
            except pywikibot.LockedPage:
                pywikibot.output('Skipping %s (locked page)' % (page.title(),))
        else:
            # Save the page in the background. No need to catch exceptions.
            page.put_async(newText)
        return

    def run(self):
        comment = i18n.twtranslate(self.site, 'noreferences-add-tag')
        pywikibot.setAction(comment)

        for page in self.generator:
            # Show the title of the page we're working on.
            # Highlight the title in purple.
            pywikibot.output("\n\n>>> \03{lightpurple}%s\03{default} <<<"
                             % page.title())
            try:
                text = page.get()
            except pywikibot.NoPage:
                pywikibot.output("Page %s does not exist?!"
                                 % page.title(asLink=True))
                continue
            except pywikibot.IsRedirectPage:
                pywikibot.output("Page %s is a redirect; skipping."
                                 % page.title(asLink=True))
                continue
            except pywikibot.LockedPage:
                pywikibot.output("Page %s is locked?!"
                                 % page.title(asLink=True))
                continue
            if pywikibot.getSite().sitename() == 'wikipedia:en' and \
               page.isIpEdit():
                pywikibot.output(
                    "Page %s is edited by IP. Possible vandalized"
                    % page.title(asLink=True))
                continue
            if self.lacksReferences(text):
                newText = self.addReferences(text)
                self.save(page, newText)


def main():
    #page generator
    gen = None
    # This temporary array is used to read the page title if one single
    # page to work on is specified by the arguments.
    pageTitle = []
    # Which namespaces should be processed?
    # default to [] which means all namespaces will be processed
    namespaces = []
    # Never ask before changing a page
    always = False
    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()

    for arg in pywikibot.handleArgs():
        if arg.startswith('-xml'):
            if len(arg) == 4:
                xmlFilename = i18n.input('pywikibot-enter-xml-filename')
            else:
                xmlFilename = arg[5:]
            gen = XmlDumpNoReferencesPageGenerator(xmlFilename)
        elif arg.startswith('-namespace:'):
            try:
                namespaces.append(int(arg[11:]))
            except ValueError:
                namespaces.append(arg[11:])
        elif arg == '-always':
            always = True
        else:
            if not genFactory.handleArg(arg):
                pageTitle.append(arg)

    if pageTitle:
        page = pywikibot.Page(pywikibot.getSite(), ' '.join(pageTitle))
        gen = iter([page])
    if not gen:
        gen = genFactory.getCombinedGenerator()
    if not gen:
        site = pywikibot.getSite()
        try:
            cat = maintenance_category[site.family.name][site.lang]
        except:
            pass
        else:
            if not namespaces:
                namespaces = [0]
            cat = pywikibot.Category(site, "%s:%s" % (
                site.category_namespace(), cat))
            gen = pagegenerators.CategorizedPageGenerator(cat)
    if not gen:
        pywikibot.showHelp('noreferences')
    else:
        if namespaces:
            gen = pagegenerators.NamespaceFilterPageGenerator(gen, namespaces)
        preloadingGen = pagegenerators.PreloadingGenerator(gen)
        bot = NoReferencesBot(preloadingGen, always)
        bot.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
