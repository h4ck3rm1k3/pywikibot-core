#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Script to delete files that are also present on Wikimedia Commons on a local
wiki. Do not run this script on Wikimedia Commons itself. It works based on
a given array of templates defined below.

Files are downloaded and compared. If the files match, it can be deleted on
the source wiki. If multiple versions of the file exist, the script will not
delete. If the MD5 comparison is not equal, the script will not delete.

A sysop account on the local wiki is required if you want all features of
this script to work properly.

This script understands various command-line arguments:
    -autonomous:    run automatically, do not ask any questions. All files
                    that qualify for deletion are deleted. Reduced screen
                    output.

    -replace:       replace links if the files are equal and the file names
                    differ

    -replacealways: replace links if the files are equal and the file names
                    differ without asking for confirmation

    -replaceloose:  Do loose replacements.  This will replace all occurences
                    of the name of the image (and not just explicit image
                    syntax).  This should work to catch all instances of the
                    file, including where it is used as a template parameter
                    or in galleries.  However, it can also make more
                    mistakes.

    -replaceonly:   Use this if you do not have a local sysop account, but do
                    wish to replace links from the NowCommons template.

    -hash:          Use the hash to identify the images that are the same. It
                    doesn't work always, so the bot opens two tabs to let to
                    the user to check if the images are equal or not.

-- Example --
python nowcommons.py -replaceonly -hash -replace -replaceloose -replacealways

-- Known issues --
Please fix these if you are capable and motivated:
- if a file marked nowcommons is not present on Wikimedia Commons, the bot
  will exit.
"""
#
# (C) Wikipedian, 2006-2007
# (C) Siebrand Mazeland, 2007-2008
# (C) xqt, 2010-2012
# (C) Pywikipedia bot team, 2006-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import sys
import re
import webbrowser
import urllib.request, urllib.parse, urllib.error
import pywikibot
from pywikibot import i18n
from pywikibot import pagegenerators as pg
from . import image
# only for nowCommonsMessage
# from imagetransfer import nowCommonsMessage
# nowCommonsMessage defined on line #163
# taken from imagetransfer.py (compat)
autonomous = False
replace = False
replacealways = False
replaceloose = False
replaceonly = False
use_hash = False

nowCommons = {
    '_default': [
        'NowCommons'
    ],
    'ar': [
        'الآن كومنز',
        'الآن كومونز',
    ],
    'de': [
        'NowCommons',
        'NC',
        'NCT',
        'Nowcommons',
        'NowCommons/Mängel',
        'NowCommons-Überprüft',
    ],
    'en': [
        'NowCommons',
        'Ncd',
    ],
    'eo': [
        'Nun en komunejo',
        'NowCommons',
    ],
    'fa': [
        'موجود در انبار',
        'NowCommons',
    ],
    'fr': [
        'Image sur Commons',
        'DoublonCommons',
        'Déjà sur Commons',
        'Maintenant sur commons',
        'Désormais sur Commons',
        'NC',
        'NowCommons',
        'Nowcommons',
        'Sharedupload',
        'Sur Commons',
        'Sur Commons2',
    ],
    'he': [
        'גם בוויקישיתוף'
    ],
    'hu': [
        'Azonnali-commons',
        'NowCommons',
        'Nowcommons',
        'NC'
    ],
    'ia': [
        'OraInCommons'
    ],
    'it': [
        'NowCommons',
    ],
    'ja': [
        'NowCommons',
    ],
    'ko': [
        'NowCommons',
        '공용중복',
        '공용 중복',
        'Nowcommons',
    ],
    'nds-nl': [
        'NoenCommons',
        'NowCommons',
    ],
    'nl': [
        'NuCommons',
        'Nucommons',
        'NowCommons',
        'Nowcommons',
        'NCT',
        'Nct',
    ],
    'ro': [
        'NowCommons'
    ],
    'ru': [
        'NowCommons',
        'NCT',
        'Nowcommons',
        'Now Commons',
        'Db-commons',
        'Перенесено на Викисклад',
        'На Викискладе',
    ],
    'zh': [
        'NowCommons',
        'Nowcommons',
        'NCT',
    ],
}

nowCommonsMessage = {
    'ar': 'Ø§Ù„Ù…Ù„Ù Ø§Ù„Ø¢Ù† Ù…ØªÙˆÙØ± ÙÙŠ ÙˆÙŠÙƒÙŠÙ…ÙŠØ¯ÙŠØ§ ÙƒÙˆÙ…Ù†Ø².',
    'de': 'Datei ist jetzt auf Wikimedia Commons verfÃ¼gbar.',
    'en': 'File is now available on Wikimedia Commons.',
    'eo': 'Dosiero nun estas havebla en la Wikimedia-Komunejo.',
    'fa': 'Ù¾Ø±ÙˆÙ†Ø¯Ù‡ Ø§Ú©Ù†ÙˆÙ† Ø¯Ø± Ø§Ù†Ø¨Ø§Ø± Ø§Ø³Øª',
    'he': '×”×§×•×‘×¥ ×–×ž×™×Ÿ ×›×¢×ª ×‘×•×•×™×§×™×©×™×ª×•×£.',
    'hu': 'A fÃ¡jl most mÃ¡r elÃ©rhetÅ‘ a Wikimedia Commonson',
    'ia': 'Le file es ora disponibile in Wikimedia Commons.',
    'ja': 'ãƒ•ã‚¡ã‚¤ãƒ«ã¯ã‚¦ã‚£ã‚­ãƒ¡ãƒ‡ã‚£ã‚¢ãƒ»ã‚³ãƒ¢ãƒ³ã‚ºã«ã‚ã‚Šã¾ã™',
    'it': 'L\'immagine Ã¨ adesso disponibile su Wikimedia Commons.',
    'kk': 'Ð¤Ð°Ð¹Ð»Ð´Ñ‹ ÐµÐ½Ð´Ñ– Wikimedia ÐžÑ€Ñ‚Ð°Ò›Ò›Ð¾Ñ€Ñ‹Ð½Ð°Ð½ Ò›Ð°Ñ‚Ñ‹Ð½Ð°ÑƒÒ“Ð° Ð±Ð¾Ð»Ð°Ð´Ñ‹.',
    'lt': 'Failas Ä¯keltas Ä¯ Wikimedia Commons projektÄ….',
    'nl': 'Dit bestand staat nu op [[w:nl:Wikimedia Commons|Wikimedia Commons]].',
    'pl': 'Plik jest teraz dostÄ™pny na Wikimedia Commons.',
    'pt': 'Arquivo estÃ¡ agora na Wikimedia Commons.',
    'ru': '[[Ð’ÐŸ:ÐšÐ‘Ð£#Ð¤8|Ð¤.8]]: Ð´Ð¾ÑÑ‚ÑƒÐ¿Ð½Ð¾ Ð½Ð° [[Ð’Ð¸ÐºÐ¸ÑÐºÐ»Ð°Ð´]]Ðµ',
    'sr': 'Ð¡Ð»Ð¸ÐºÐ° Ñ˜Ðµ ÑÐ°Ð´Ð° Ð´Ð¾ÑÑ‚ÑƒÐ¿Ð½Ð° Ð¸ Ð½Ð° Ð’Ð¸ÐºÐ¸Ð¼ÐµÐ´Ð¸Ñ˜Ð° ÐžÑÑ‚Ð°Ð²Ð¸.',
    'zh': 'æª”æ¡ˆå·²å­˜åœ¨æ–¼ç¶­åŸºå…±äº«è³‡æºã€‚',
}

namespaceInTemplate = [
    'en',
    'ia',
    'it',
    'ja',
    'ko',
    'lt',
    'ro',
    'zh',
]

# Stemma and stub are images not to be deleted (and are a lot) on it.wikipedia
# if your project has images like that, put the word often used here to skip them
word_to_skip = {
    'en': [],
    'it': ['stemma', 'stub', 'hill40 '],
}

#nowCommonsMessage = imagetransfer.nowCommonsMessage


class NowCommonsDeleteBot:
    def __init__(self):
        self.site = pywikibot.getSite()
        if repr(self.site) == 'commons:commons':
            sys.exit('Do not run this bot on Commons!')

    def ncTemplates(self):
        if self.site.lang in nowCommons:
            return nowCommons[self.site.lang]
        else:
            return nowCommons['_default']

    def useHashGenerator(self):
        # http://toolserver.org/~multichill/nowcommons.php?language=it&page=2&filter=
        lang = self.site.lang
        num_page = 0
        word_to_skip_translated = i18n.translate(self.site, word_to_skip)
        images_processed = list()
        while 1:
            url = ('http://toolserver.org/~multichill/nowcommons.php?'
                   'language=%s&page=%s&filter=') % (lang, num_page)
            HTML_text = self.site.getUrl(url, no_hostname=True)
            reg = r'<[Aa] href="(?P<urllocal>.*?)">(?P<imagelocal>.*?)</[Aa]> +?</td><td>\n\s*?'
            reg += r'<[Aa] href="(?P<urlcommons>http://commons.wikimedia.org/.*?)" \
                   >Image:(?P<imagecommons>.*?)</[Aa]> +?</td><td>'
            regex = re.compile(reg, re.UNICODE)
            found_something = False
            change_page = True
            for x in regex.finditer(HTML_text):
                found_something = True
                image_local = x.group('imagelocal')
                image_commons = x.group('imagecommons')
                if image_local in images_processed:
                    continue
                change_page = False
                images_processed.append(image_local)
                # Skip images that have something in the title (useful for it.wiki)
                image_to_skip = False
                for word in word_to_skip_translated:
                    if word.lower() in image_local.lower():
                        image_to_skip = True
                if image_to_skip:
                    continue
                url_local = x.group('urllocal')
                url_commons = x.group('urlcommons')
                pywikibot.output("\n\n>>> \03{lightpurple}%s\03{default} <<<"
                                 % image_local)
                pywikibot.output('Local: %s\nCommons: %s\n'
                                 % (url_local, url_commons))
                #result1 = 
                webbrowser.open(url_local, 0, 1)
                #result2 = 
                webbrowser.open(url_commons, 0, 1)
                if image_local.split('Image:')[1] == image_commons:
                    choice = pywikibot.inputChoice(
                        'The local and the commons images have the same name, continue?',
                        ['Yes', 'No'], ['y', 'N'], 'N')
                else:
                    choice = pywikibot.inputChoice(
                        'Are the two images equal?',
                        ['Yes', 'No'], ['y', 'N'], 'N')
                if choice.lower() in ['y', 'yes']:
                    yield [image_local, image_commons]
                else:
                    continue
            # The page is dinamically updated, so we may don't need to change it
            if change_page:
                num_page += 1
            # If no image found means that there aren't anymore, break.
            if not found_something:
                break

    def getPageGenerator(self):
        if use_hash:
            gen = self.useHashGenerator()
        else:
            nowCommonsTemplates = [pywikibot.Page(self.site, title,
                                                  defaultNamespace=10)
                                   for title in self.ncTemplates()]
            gens = [pg.ReferringPageGenerator(t, followRedirects=True,
                                              onlyTemplateInclusion=True)
                    for t in nowCommonsTemplates]
            gen = pg.CombinedPageGenerator(gens)
            gen = pg.NamespaceFilterPageGenerator(gen, [6])
            gen = pg.DuplicateFilterPageGenerator(gen)
            gen = pg.PreloadingGenerator(gen)
        return gen

    def findFilenameOnCommons(self, localImagePage):
        filenameOnCommons = None
        for templateName, params in localImagePage.templatesWithParams():
            if templateName in self.ncTemplates():
                if params == []:
                    filenameOnCommons = localImagePage.title(withNamespace=False)
                elif self.site.lang in namespaceInTemplate:
                    skip = False
                    filenameOnCommons = None
                    for par in params:
                        val = par.split('=')
                        if len(val) == 1 and not skip:
                            filenameOnCommons = par[par.index(':') + 1:]
                            break
                        if val[0].strip() == '1':
                            filenameOnCommons = val[1].strip()[val[1].strip().index(':') + 1:]
                            break
                        skip = True
                    if not filenameOnCommons:
                        filenameOnCommons = localImagePage.title(withNamespace=False)
                else:
                    val = params[0].split('=')
                    if len(val) == 1:
                        filenameOnCommons = params[0].strip()
                    else:
                        filenameOnCommons = val[1].strip()
                return filenameOnCommons

    # Function stolen from wikipedia.py and modified. Really needed?
    def urlname(self, talk_page):
        """The name of the page this Page refers to, in a form suitable for the
        URL of the page.

        """
        title = talk_page.replace(" ", "_")
        encodedTitle = title.encode(self.site.encoding())
        return urllib.parse.quote(encodedTitle)

    def run(self):
        commons = pywikibot.getSite('commons', 'commons')
        comment = i18n.translate(self.site, nowCommonsMessage)

        for page in self.getPageGenerator():
            if use_hash:
                # Page -> Has the namespace | commons image -> Not
                images_list = page    # 0 -> local image, 1 -> commons image
                page = pywikibot.Page(self.site, images_list[0])
            else:
                # If use_hash is true, we have already print this before, no need
                # Show the title of the page we're working on.
                # Highlight the title in purple.
                pywikibot.output("\n\n>>> \03{lightpurple}%s\03{default} <<<"
                                 % page.title())
            try:
                localImagePage = pywikibot.ImagePage(self.site, page.title())
                if localImagePage.fileIsOnCommons():
                    pywikibot.output('File is already on Commons.')
                    continue
                md5 = localImagePage.getFileMd5Sum()
                if use_hash:
                    filenameOnCommons = images_list[1]
                else:
                    filenameOnCommons = self.findFilenameOnCommons(
                        localImagePage)
                if not filenameOnCommons and not use_hash:
                    pywikibot.output('NowCommons template not found.')
                    continue
                commonsImagePage = pywikibot.ImagePage(commons, 'Image:%s'
                                                       % filenameOnCommons)
                if localImagePage.title(withNamespace=False) == \
                 commonsImagePage.title(withNamespace=False) and use_hash:
                    pywikibot.output(
                        'The local and the commons images have the same name')
                if localImagePage.title(withNamespace=False) != \
                 commonsImagePage.title(withNamespace=False):
                    usingPages = list(localImagePage.usingPages())
                    if usingPages and usingPages != [localImagePage]:
                        pywikibot.output(
                            '\"\03{lightred}%s\03{default}\" is still used in %i pages.'
                            % (localImagePage.title(withNamespace=False),
                               len(usingPages)))
                        if replace is True:
                                pywikibot.output(
                                    'Replacing \"\03{lightred}%s\03{default}\" by \
                                    \"\03{lightgreen}%s\03{default}\".'
                                    % (localImagePage.title(withNamespace=False),
                                       commonsImagePage.title(withNamespace=False)))
                                oImageRobot = image.ImageRobot(
                                    pg.FileLinksGenerator(localImagePage),
                                    localImagePage.title(withNamespace=False),
                                    commonsImagePage.title(withNamespace=False),
                                    '', replacealways, replaceloose)
                                oImageRobot.run()
                                # If the image is used with the urlname the
                                # previous function won't work
                                if len(list(pywikibot.ImagePage(self.site,
                                                                page.title()).usingPages())) > 0 and \
                                                                replaceloose:
                                    oImageRobot = image.ImageRobot(
                                        pg.FileLinksGenerator(
                                            localImagePage),
                                        self.urlname(
                                            localImagePage.title(
                                                withNamespace=False)),
                                        commonsImagePage.title(
                                            withNamespace=False),
                                        '', replacealways, replaceloose)
                                    oImageRobot.run()
                                # refresh because we want the updated list
                                usingPages = len(list(pywikibot.ImagePage(
                                    self.site, page.title()).usingPages()))
                                if usingPages > 0 and use_hash:
                                    # just an enter
                                    pywikibot.input(
                                        'There are still %s pages with this \
                                        image, confirm the manual removal from them please.'
                                        % usingPages)

                        else:
                            pywikibot.output('Please change them manually.')
                        continue
                    else:
                        pywikibot.output(
                            'No page is using \"\03{lightgreen}%s\03{default}\" anymore.'
                            % localImagePage.title(withNamespace=False))
                commonsText = commonsImagePage.get()
                if replaceonly is False:
                    if md5 == commonsImagePage.getFileMd5Sum():
                        pywikibot.output(
                            'The image is identical to the one on Commons.')
                        if len(localImagePage.getFileVersionHistory()) > 1 and not use_hash:
                            pywikibot.output(
                                "This image has a version history. Please \
                                delete it manually after making sure that the \
                                old versions are not worth keeping.""")
                            continue
                        if autonomous is False:
                            pywikibot.output(
                                '\n\n>>>> Description on \03{lightpurple}%s\03{default} <<<<\n'
                                % page.title())
                            pywikibot.output(localImagePage.get())
                            pywikibot.output(
                                '\n\n>>>> Description on \03{lightpurple}%s\03{default} <<<<\n'
                                % commonsImagePage.title())
                            pywikibot.output(commonsText)
                            choice = pywikibot.inputChoice('Does the description \
                                                           on Commons contain all required source and license\n'
                                                           'information?',
                                                           ['yes', 'no'], ['y', 'N'], 'N')
                            if choice.lower() in ['y', 'yes']:
                                localImagePage.delete(
                                    comment + ' [[:commons:Image:%s]]'
                                    % filenameOnCommons, prompt=False)
                        else:
                            localImagePage.delete(
                                comment + ' [[:commons:Image:%s]]'
                                % filenameOnCommons, prompt=False)
                    else:
                        pywikibot.output(
                            'The image is not identical to the one on Commons.')
            except (pywikibot.NoPage, pywikibot.IsRedirectPage) as e:
                pywikibot.output('%s' % e[0])
                continue


def main():
    global autonomous
    global replace, replacealways, replaceloose, replaceonly
    global use_hash
    autonomous = False
    replace = False
    replacealways = False
    replaceloose = False
    replaceonly = False
    use_hash = False

    for arg in pywikibot.handleArgs():
        if arg == '-autonomous':
            autonomous = True
        if arg == '-replace':
            replace = True
        if arg == '-replacealways':
            replace = True
            replacealways = True
        if arg == '-replaceloose':
            replaceloose = True
        if arg == '-replaceonly':
            replaceonly = True
        if arg == '-hash':
            use_hash = True
    bot = NowCommonsDeleteBot()
    bot.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
