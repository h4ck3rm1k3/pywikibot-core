#!/usr/bin/python
#coding: utf-8
"""
This bot takes its input from a file that contains a number of
pages to be put on the wiki. The pages should all have the same
begin and end text (which may not overlap).

By default the text should have the intended title of the page
as the first text in bold (that is, between ''' and '''),
you can modify this behavior with command line options.

The default is not to include the begin and
end text in the page, if you want to include that text, use
the -include option.

Specific arguments:
-start:xxx      Specify the text that marks the beginning of a page
-end:xxx        Specify the text that marks the end of a page
-file:xxx       Give the filename we are getting our material from
-include        The beginning and end markers should be included
                in the page.
-titlestart:xxx Use xxx in place of ''' for identifying the
                beginning of page title
-titleend:xxx   Use xxx in place of ''' for identifying the
                end of page title
-notitle        do not include the title, including titlestart, and
                titleend, in the page
-nocontent      If page has this statment it dosen't append
                (example: -nocontents:"{{infobox")
-summary:xxx    Use xxx as the edit summary for the upload - if
                a page exists, standard messages are appended
                after xxx for appending, prepending, or replacement
-autosummary    Use MediaWikis autosummary when creating a new page,
                overrides -summary in this case
-minor          set minor edit flag on page edits

If the page to be uploaded already exists:
-safe           do nothing (default)
-appendtop      add the text to the top of it
-appendbottom   add the text to the bottom of it
-force          overwrite the existing page
"""
#
# (C) Andre Engels, 2004
# (C) Pywikipedia bot team, 2005-2010
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import re
import codecs
import pywikibot
from pywikibot import config


class NoTitle(Exception):
    """No title found"""
    def __init__(self, offset):
        self.offset = offset


class PageFromFileRobot:
    """
    Responsible for writing pages to the wiki, with the titles and contents
    given by a PageFromFileReader.
    """

    msg = {
        'ar': 'استيراد تلقائي للمقالات',
        'de': 'Automatischer Import von Artikeln',
        'en': 'Automated import of articles',
        'fa': 'درون‌ریزی خودکار مقاله‌ها',
        'fr': 'Import automatique',
        'he': 'ייבוא ערכים אוטומטי',
        'ia': 'Importation automatic de articulos',
        'id': 'Impor artikel automatis',
        'it': 'Caricamento automatico',
        'ja': '記事の自動取り込み',
        'ksh': 'Bot: automatesch huhjelaade',
        'mzn': 'ربوت:صفحه شه خاد به خاد دله دکته',
        'nl': 'Geautomatiseerde import',
        'no': 'bot: Automatisk import',
        'pl': 'Automatyczny import artykułów',
        'pt': 'Importação automática de artigos',
        'uk': 'Автоматичний імпорт статей',
        'zh': '機器人: 自動匯入頁面',
    }

    # The following messages are added to topic when the page already exists
    msg_top = {
        'ar': 'كتابة على الأعلى',
        'de': 'ergänze am Anfang',
        'en': 'append on top',
        'fa': 'به بالا اضافه شد',
        'he': 'הוספה בראש הדף',
        'fr': 'rajouté en haut',
        'id': 'ditambahkan di atas',
        'it': 'aggiungo in cima',
        'ja': '冒頭への追加',
        'ksh': 'un dofüürjesaz',
        'nl': 'bovenaan toegevoegd',
        'no': 'legger til øverst',
        'pl': 'dodaj na górze',
        'pt': 'adicionado no topo',
        'uk': 'додано зверху',
        'zh': '機器人: 增加至最上層',
    }

    msg_bottom = {
        'ar': 'كتابة على الأسفل',
        'de': 'ergänze am Ende',
        'en': 'append on bottom',
        'fa': 'به پایین اضافه شد',
        'he': 'הוספה בתחתית הדף',
        'fr': 'rajouté en bas',
        'id': 'ditambahkan di bawah',
        'it': 'aggiungo in fondo',
        'ja': '末尾への追加',
        'ksh': 'un aanjehange',
        'nl': 'onderaan toegevoegd',
        'no': 'legger til nederst',
        'pl': 'dodaj na dole',
        'pt': 'adicionando no fim',
        'uk': 'додано знизу',
        'zh': '機器人: 增加至最底層',
    }

    msg_force = {
        'ar': 'تمت الكتابة على النص الموجود',
        'de': 'bestehender Text überschrieben',
        'en': 'existing text overwritten',
        'fa': 'متن جایگزین شد',
        'he': 'הטקסט הישן נמחק',
        'fr': 'texte existant écrasé',
        'id': 'menimpa teks yang ada',
        'it': 'sovrascritto il testo esistente',
        'ja': '存在するテキストの上書き',
        'ksh': 'un komplët ußjetuusch',
        'nl': 'bestaande tekst overschreven',
        'no': 'erstatter eksisterende tekst',
        'pl': 'aktualny tekst nadpisany',
        'pt': 'sobrescrever texto',
        'uk': 'існуючий текст перезаписано',
        'zh': '機器人: 覆寫已存在的文字',
    }

    def __init__(self, reader, force, append, summary, minor, autosummary,
                 dry, nocontents):
        self.reader = reader
        self.force = force
        self.append = append
        self.summary = summary
        self.minor = minor
        self.autosummary = autosummary
        self.dry = dry
        self.nocontents = nocontents

    def run(self):
        for title, contents in self.reader.run():
            self.put(title, contents)

    def put(self, title, contents):
        mysite = pywikibot.getSite()

        page = pywikibot.Page(mysite, title)
        # Show the title of the page we're working on.
        # Highlight the title in purple.
        pywikibot.output(">>> \03{lightpurple}%s\03{default} <<<"
                         % page.title())

        if self.summary:
            comment = self.summary
        else:
            comment = pywikibot.translate(mysite, self.msg)

        comment_top = comment + " - " + pywikibot.translate(mysite,
                                                            self.msg_top)
        comment_bottom = comment + " - " + pywikibot.translate(mysite,
                                                               self.msg_bottom)
        comment_force = comment + " *** " + pywikibot.translate(mysite,
                                                                self.msg_force) + " ***"

        # Remove trailing newlines (cause troubles when creating redirects)
        contents = re.sub('^[\r\n]*', '', contents)

        if page.exists():
            if self.append == "Top":
                if appendtops.find(self.nocontents) == -1 and appendtops.find(self.nocontents.lower()) == -1:
                    contents = contents + appendtops
                    pywikibot.output("Page %s already exists, appending on top!"
                                     % title)
                else:
                    pywikibot.output('Page had %s so it is skipped' % (self.nocontents))
                    return
                contents = contents + page.get()
                comment = comment_top
            elif self.append == "Bottom":
                if appendtops.find(self.nocontents) == -1 and appendtops.find(self.nocontents.lower()) == -1:
                    contents = contents + appendtops
                    pywikibot.output("Page %s already exists, appending on bottom!"
                                     % title)
                else:
                    pywikibot.output('Page had %s so it is skipped' % (self.nocontents))
                    return
                contents = page.get() + contents
                comment = comment_bottom
            elif self.force:
                pywikibot.output("Page %s already exists, ***overwriting!"
                                 % title)
                comment = comment_force
            else:
                pywikibot.output("Page %s already exists, not adding!" % title)
                return
        else:
            if self.autosummary:
                comment = ''
                pywikibot.setAction('')

        if self.dry:
            pywikibot.output("*** Dry mode ***\n" + \
                             "\03{lightpurple}title\03{default}: " + title + "\n" + \
                             "\03{lightpurple}contents\03{default}:\n" + contents + "\n" \
                             "\03{lightpurple}comment\03{default}: " + comment + "\n")
            return

        try:
            page.put(contents, comment=comment, minorEdit=self.minor)
        except pywikibot.LockedPage:
            pywikibot.output("Page %s is locked; skipping." % title)
        except pywikibot.EditConflict:
            pywikibot.output('Skipping %s because of edit conflict' % title)
        except pywikibot.SpamfilterError as error:
            pywikibot.output(
                'Cannot change %s because of spam blacklist entry %s'
                % (title, error.url))


class PageFromFileReader:
    """
    Responsible for reading the file.

    The run() method yields a (title, contents) tuple for each found page.
    """
    def __init__(self, filename, pageStartMarker, pageEndMarker,
                 titleStartMarker, titleEndMarker, include, notitle):
        self.filename = filename
        self.pageStartMarker = pageStartMarker
        self.pageEndMarker = pageEndMarker
        self.titleStartMarker = titleStartMarker
        self.titleEndMarker = titleEndMarker
        self.include = include
        self.notitle = notitle

    def run(self):
        pywikibot.output('Reading \'%s\'...' % self.filename)
        try:
            f = codecs.open(self.filename, 'r',
                            encoding=config.textfile_encoding)
        except IOError as err:
            pywikibot.output(str(err))
            return

        text = f.read()
        position = 0
        length = 0
        while True:
            try:
                length, title, contents = self.findpage(text[position:])
            except AttributeError:
                if not length:
                    pywikibot.output('\nStart or end marker not found.')
                else:
                    pywikibot.output('End of file.')
                break
            except NoTitle as err:
                pywikibot.output('\nNo title found - skipping a page.')
                position += err.offset
                continue

            position += length
            yield title, contents

    def findpage(self, text):
        pageR = re.compile(self.pageStartMarker + "(.*?)" + self.pageEndMarker, re.DOTALL)
        titleR = re.compile(self.titleStartMarker + "(.*?)" + self.titleEndMarker)

        location = pageR.search(text)
        if self.include:
            contents = location.group()
        else:
            contents = location.group(1)
        try:
            title = titleR.search(contents).group(1)
            if self.notitle:
                #Remove title (to allow creation of redirects)
                contents = titleR.sub('', contents, count=1)
        except AttributeError:
            raise NoTitle(location.end())
        else:
            return location.end(), title, contents


def main():
    # Adapt these to the file you are using. 'pageStartMarker' and
    # 'pageEndMarker' are the beginning and end of each entry. Take text that
    # should be included and does not occur elsewhere in the text.

    # TODO: make config variables for these.
    filename = "dict.txt"
    pageStartMarker = "{{-start-}}"
    pageEndMarker = "{{-stop-}}"
    titleStartMarker = "'''"
    titleEndMarker = "'''"
    nocontents = ""
    include = False
    force = False
    append = None
    notitle = False
    summary = None
    minor = False
    autosummary = False

    for arg in pywikibot.handleArgs():
        if arg.startswith("-start:"):
            pageStartMarker = arg[7:]
        elif arg.startswith("-end:"):
            pageEndMarker = arg[5:]
        elif arg.startswith("-file:"):
            filename = arg[6:]
        elif arg == "-include":
            include = True
        elif arg == "-appendtop":
            append = "Top"
        elif arg == "-appendbottom":
            append = "Bottom"
        elif arg == "-force":
            force = True
        elif arg == "-safe":
            force = False
            append = None
        elif arg == '-notitle':
            notitle = True
        elif arg == '-minor':
            minor = True
        elif arg.startswith('-nocontent:'):
            nocontents = arg[11:]
        elif arg.startswith("-titlestart:"):
            titleStartMarker = arg[12:]
        elif arg.startswith("-titleend:"):
            titleEndMarker = arg[10:]
        elif arg.startswith("-summary:"):
            summary = arg[9:]
        elif arg == '-autosummary':
            autosummary = True
        else:
            pywikibot.output("Disregarding unknown argument %s." % arg)

    reader = PageFromFileReader(filename, pageStartMarker, pageEndMarker,
                                titleStartMarker, titleEndMarker, include,
                                notitle)
    bot = PageFromFileRobot(reader, force, append, summary, minor, autosummary,
                            config.simulate, nocontents)
    bot.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
