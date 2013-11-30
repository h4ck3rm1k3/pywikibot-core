#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot cleans a (user) sandbox by replacing the current contents with
predefined text.

This script understands the following command-line arguments:

    -hours:#       Use this parameter if to make the script repeat itself
                   after # hours. Hours can be defined as a decimal. 0.01
                   hours are 36 seconds; 0.1 are 6 minutes.

    -delay:#       Use this parameter for a wait time after the last edit
                   was made. If no parameter is given it takes it from
                   hours and limits it between 5 and 15 minutes.
                   The minimum delay time is 5 minutes.

    -user          Use this parameter to run the script in the user name-
                   space.
                   > ATTENTION: on most wiki THIS IS FORBIDEN FOR BOTS ! <
                   > (please talk with your admin first)                 <
                   Since it is considered bad style to edit user page with-
                   out permission, the 'user_sandboxTemplate' for given
                   language has to be set-up (no fall-back will be used).
                   All pages containing that template will get cleaned.
                   Please be also aware that the rules when to clean the
                   user sandbox differ from those for project sandbox.

"""
#
# (C) Leonardo Gregianin, 2006
# (C) Wikipedian, 2006-2007
# (C) Andre Engels, 2007
# (C) Siebrand Mazeland, 2007
# (C) xqt, 2009-2013
# (C) Dr. Trigon, 2012
# (C) Pywikibot team, 2012-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import time
import datetime
import sys
import pywikibot
from pywikibot import i18n

content = {
    'commons': '{{Sandbox}}\n<!-- Please edit only below this line. -->',
    'als': '{{subst:/Vorlage}}',
    'ar': '{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->',
    'az': '<!--- LÜTFƏN, BU SƏTRƏ TOXUNMAYIN --->\n{{Qaralama dəftəri}}\n<!-- AŞAĞIDAKI XƏTTİN ALTINDAN YAZA BİLƏRSİNİZ --->',
    'bar': '{{Bitte erst NACH dieser Zeile schreiben! (Begrüßungskasten)}}\r\n',
    'cs': '{{subst:/uhrabat}}',
    'da': '{{subst:Sandkasse tekst}}',
    'de': '{{Bitte erst NACH dieser Zeile schreiben! (Begrüßungskasten)}}\r\n',
    'en': '{{Sandbox heading}}\n<!-- Hello! Feel free to try your formatting and editing skills below this line. As this page is for editing experiments, this page will automatically be cleaned every 12 hours. -->',
    'fa': '{{subst:User:Amirobot/sandbox}}',
    'fi': '{{subst:Hiekka}}',
    'he': '{{ארגז חול}}\n<!-- נא לערוך מתחת לשורה זו בלבד, תודה. -->',
    'id': '{{Bakpasir}}\n<!-- Uji coba dilakukan di baris di bawah ini -->',
    'it': '{{sandbox}}<!-- Scrivi SOTTO questa riga senza cancellarla. Grazie. -->',
    'ja': '{{subst:サンドボックス}}',
    'ko': '{{연습장 안내문}}',
    'ksh': '{{subst:/Schablon}}',
    'mzn': '{{ویکی‌پدیا:چنگ‌مویی صفحه/پیغوم}}\n<!-- سلام!اگه خواننی شه دچی‌ین مهارتون وسه تمرین هاکنین بتوننی اینتا صفحه جا ایستفاده هاکنین، اته لطف هاکنین اینتا پیغوم ره شه بقیه رفقون وسه بیلین. اینتا صفحه هرچند ساعت ربوت جا پاک بونه.-->',
    'nds': '{{subst:/Vörlaag}}',
    'nl': '{{subst:Wikipedia:Zandbak/schoon zand}}',
    'nn': '{{sandkasse}}\n<!-- Ver snill og IKKJE FJERN DENNE LINA OG LINA OVER ({{sandkasse}}) Nedanføre kan du derimot ha det artig og prøve deg fram! Lykke til! :-)  -->',
    'no': '{{Sandkasse}}\n<!-- VENNLIGST EKSPERIMENTER NEDENFOR DENNE SKJULTE TEKSTLINJEN! SANDKASSEMALEN {{Sandkasse}} SKAL IKKE FJERNES! -->}}',
    'pl': '{{Prosimy - NIE ZMIENIAJ, NIE KASUJ, NIE PRZENOŚ tej linijki - pisz niżej}}',
    'pt': '<!--não apague esta linha-->{{página de testes}}<!--não apagar-->\r\n',
    'ru': '{{/Пишите ниже}}\n<!-- Не удаляйте, пожалуйста, эту строку, тестируйте ниже -->',
    'simple': '{{subst:/Text}}',
    'sco': 'Feel free tae test here',
    'sr': '{{песак}}\n<!-- Молимо, испробавајте испод ове линије. Хвала. -->',
    'sv': '{{subst:Sandlådan}}',
    'th': '{{กระบะทราย}}\n<!-- กรุณาอย่าแก้ไขบรรทัดนี้ ขอบคุณครับ/ค่ะ -- Please leave this line as they are. Thank you! -->',
    'tr': '{{/Bu satırı değiştirmeden bırakın}}',
    'zh': '{{subst:User:Sz-iwbot/sandbox}}\r\n',
}

sandboxTitle = {
    'commons': 'Project:Sandbox',
    'als': 'Project:Sandchaschte',
    'ar': 'Project:ملعب',
    'az': 'Vikipediya:Qaralama dəftəri',
    'bar': 'Project:Spuiwiesn',
    'cs': 'Project:Pískoviště',
    'da': 'Project:Sandkassen',
    'de': 'Project:Spielwiese',
    'en': 'Project:Sandbox',
    'fa': ['Project:صفحه تمرین', 'Project:آشنایی با ویرایش'],
    'fi': 'Project:Hiekkalaatikko',
    'fr': 'Project:Bac à sable',
    'he': 'Project:ארגז חול',
    'id': 'Project:Bak pasir',
    'it': 'Project:Pagina delle prove',
    'ja': 'Project:サンドボックス',
    'ko': 'Project:연습장',
    'ksh': 'Project:Shpillplaz',
    'mzn': 'Project:چنگ‌مویی صفحه',
    'nds': 'Project:Speelwisch',
    'nl': 'Project:Zandbak',
    'no': 'Project:Sandkasse',
    'pl': 'Project:Brudnopis',
    'pt': 'Project:Página de testes',
    'ru': 'Project:Песочница',
    'simple': 'Project:Sandbox',
    'sco': 'Project:Saundpit',
    'sr': 'Project:Песак',
    'sv': 'Project:Sandlådan',
    'th': 'Project:ทดลองเขียน',
    'tr': 'Vikipedi:Deneme tahtası',
    'zh': 'Project:沙盒',
}

user_content = {
    'de': '{{Benutzer:DrTrigonBot/Spielwiese}}',
}

user_sandboxTemplate = {
    'de': 'User:DrTrigonBot/Spielwiese',
}


class SandboxBot(pywikibot.Bot):
    availableOptions = {
        'hours': 1,
        'no_repeat': True,
        'delay': None,
        'delay_td': None,
        'user': False,
    }

    def __init__(self, **kwargs):
        super(SandboxBot, self).__init__(**kwargs)
        if self.getOption('delay') is None:
            d = min(15, max(5, int(self.getOption('hours') * 60)))
            self.availableOptions['delay_td'] = datetime.timedelta(minutes=d)
        else:
            d = max(5, self.getOption('delay'))
            self.availableOptions['delay_td'] = datetime.timedelta(minutes=d)

        self.site = pywikibot.Site()
        self.site.login()
        if self.getOption('user'):
            localSandboxTitle = pywikibot.translate(self.site,
                                                    user_sandboxTemplate,
                                                    fallback=False)
            localSandbox = pywikibot.Page(self.site, localSandboxTitle)
            content.update(user_content)
            sandboxTitle[self.site.lang] = [item.title() for item in
                                            localSandbox.getReferences(
                                                onlyTemplateInclusion=True)]
            if self.site.lang not in user_sandboxTemplate:
                content[self.site.code] = None
                pywikibot.output(
                    'Not properly set-up to run in user namespace!')
        if sandboxTitle.get(self.site.code) is None or content.get(
                self.site.code) is None:
            pywikibot.output('This bot is not configured for the given site '
                             '(%s), exiting.' % self.site)
            sys.exit(0)

    def run(self):
        while True:
            wait = False
            now = time.strftime("%d %b %Y %H:%M:%S (UTC)", time.gmtime())
            localSandboxTitle = pywikibot.translate(self.site, sandboxTitle,
                                                    fallback=False)
            if type(localSandboxTitle) is list:
                titles = localSandboxTitle
            else:
                titles = [localSandboxTitle]
            for title in titles:
                sandboxPage = pywikibot.Page(self.site, title)
                pywikibot.output('Preparing to process sandbox page %s'
                                 % sandboxPage.title(asLink=True))
                try:
                    text = sandboxPage.get()
                    translatedContent = pywikibot.translate(self.site, content,
                                                            fallback=False)
                    translatedMsg = i18n.twtranslate(self.site,
                                                     'clean_sandbox-cleaned')
                    subst = 'subst:' in translatedContent
                    pos = text.find(translatedContent.strip())
                    if text.strip() == translatedContent.strip():
                        pywikibot.output(
                            'The sandbox is still clean, no change necessary.')
                    elif subst and \
                         sandboxPage.userName() == self.site.user():
                        pywikibot.output(
                            'The sandbox might be clean, no change necessary.')
                    elif pos != 0 and not subst:
                        if self.getOption('user'):
                            endpos = pos + len(translatedContent.strip())
                            if (pos < 0) or (endpos == len(text)):
                                pywikibot.output('The user sandbox is still '
                                                 'clean, no change necessary.')
                            else:
                                sandboxPage.put(text[:endpos], translatedMsg)
                                pywikibot.showDiff(text, text[:endpos])
                                pywikibot.output(
                                    'Standard content was changed, user '
                                    'sandbox cleaned.')
                        else:
                            sandboxPage.put(translatedContent, translatedMsg)
                            pywikibot.showDiff(text, translatedContent)
                            pywikibot.output('Standard content was changed, '
                                             'sandbox cleaned.')
                    else:
                        edit_delta = datetime.datetime.utcnow() - \
                            pywikibot.Timestamp.fromISOformat(sandboxPage.editTime())
                        delta = self.getOption('delay_td') - edit_delta
                        # Is the last edit more than 'delay' minutes ago?
                        if delta <= datetime.timedelta(0):
                            sandboxPage.put(translatedContent, translatedMsg)
                            pywikibot.showDiff(text, translatedContent)
                            pywikibot.output('Standard content was changed, '
                                             'sandbox cleaned.')
                        else:  # wait for the rest
                            pywikibot.output(
                                'Sandbox edited %.1f minutes ago...'
                                % (edit_delta.seconds / 60.0))
                            pywikibot.output('Sleeping for %d minutes.'
                                             % (delta.seconds / 60))
                            time.sleep(delta.seconds)
                            wait = True
                except pywikibot.EditConflict:
                    pywikibot.output(
                        '*** Loading again because of edit conflict.\n')
                except pywikibot.NoPage:
                    pywikibot.output(
                        '*** The sandbox is not existent, skipping.')
                    continue
            if self.getOption('no_repeat'):
                pywikibot.output('\nDone.')
                return
            elif not wait:
                if self.getOption('hours') < 1.0:
                    pywikibot.output('\nSleeping %s minutes, now %s'
                                     % ((self.getOption('hours') * 60), now))
                else:
                    pywikibot.output('\nSleeping %s hours, now %s'
                                     % (self.getOption('hours'), now))
                time.sleep(self.getOption('hours') * 60 * 60)


def main():
    opts = {}
    for arg in pywikibot.handleArgs():
        if arg.startswith('-hours:'):
            opts['hours'] = float(arg[7:])
            opts['no_repeat'] = False
        elif arg.startswith('-delay:'):
            opts['delay'] = int(arg[7:])
        elif arg == '-user':
            opts['user'] = True
        else:
            pywikibot.showHelp('clean_sandbox')
            return

    bot = SandboxBot(**opts)
    try:
        bot.run()
    except KeyboardInterrupt:
        pywikibot.output('\nQuitting program...')

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
