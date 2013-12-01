# -*- coding: utf-8  -*-
from pywikibot.family import WikimediaFamily 

__version__ = '$Id$'


# The Wikimedia family that is known as Wikipedia, the Free Encyclopedia
class Family(WikimediaFamily):
    def __init__(self):
        self.alphabetic = []
        self.alphabetic_revised = []
        self.langs = {}
        self.known_families={}
        self.crossnamespace = {}
        self.fyinterwiki = {}

        WikimediaFamily.__init__(self)
        self.name = 'wikipedia'

        self.languages_by_size = [
            'en', 'nl', 'de', 'sv', 'fr', 'it', 'ru', 'es', 'pl', 'war', 'ceb',
            'vi', 'ja', 'pt', 'zh', 'uk', 'ca', 'no', 'fi', 'fa', 'id', 'cs',
            'ko', 'hu', 'ar', 'ms', 'ro', 'sr', 'min', 'tr', 'kk', 'sk', 'eo',
            'da', 'eu', 'lt', 'bg', 'he', 'hr', 'sl', 'uz', 'vo', 'et', 'hi',
            'gl', 'nn', 'simple', 'la', 'hy', 'az', 'el', 'sh', 'oc', 'th',
            'ka', 'mk', 'new', 'be', 'pms', 'tl', 'ta', 'te', 'ht', 'cy', 'tt',
            'be-x-old', 'lv', 'sq', 'bs', 'br', 'mg', 'jv', 'lb', 'mr', 'is',
            'ml', 'my', 'ba', 'yo', 'an', 'af', 'lmo', 'fy', 'pnb', 'ga', 'bn',
            'zh-yue', 'ur', 'sw', 'io', 'bpy', 'ne', 'ky', 'gu', 'scn', 'tg',
            'nds', 'ku', 'cv', 'ast', 'qu', 'sco', 'su', 'als', 'kn', 'ia',
            'bug', 'nap', 'bat-smg', 'am', 'ckb', 'wa', 'map-bms', 'gd', 'hif',
            'mn', 'arz', 'zh-min-nan', 'mzn', 'yi', 'vec', 'sah', 'ce', 'nah',
            'sa', 'si', 'roa-tara', 'os', 'bar', 'pam', 'hsb', 'pa', 'se', 'li',
            'mi', 'fo', 'co', 'ilo', 'gan', 'bo', 'frr', 'glk', 'rue', 'bcl',
            'nds-nl', 'fiu-vro', 'mrj', 'tk', 'ps', 'vls', 'xmf', 'gv', 'or',
            'diq', 'zea', 'kv', 'km', 'pag', 'mhr', 'csb', 'dv', 'vep', 'nrm',
            'hak', 'rm', 'koi', 'udm', 'lad', 'wuu', 'lij', 'zh-classical',
            'sc', 'fur', 'stq', 'mt', 'ug', 'ay', 'so', 'pi', 'nov', 'bh',
            'ksh', 'gn', 'gag', 'kw', 'ang', 'as', 'pcd', 'eml', 'ace', 'nv',
            'szl', 'ext', 'frp', 'ie', 'mwl', 'ln', 'pfl', 'lez', 'krc', 'xal',
            'haw', 'pdc', 'rw', 'crh', 'dsb', 'to', 'arc', 'kl', 'myv', 'kab',
            'sn', 'bjn', 'pap', 'tpi', 'kbd', 'lo', 'lbe', 'wo', 'mdf', 'jbo',
            'cbk-zam', 'av', 'srn', 'ty', 'kg', 'ab', 'na', 'tet', 'ltg', 'ig',
            'bxr', 'nso', 'za', 'kaa', 'zu', 'chy', 'rmy', 'cu', 'chr', 'tn',
            'cdo', 'roa-rup', 'bi', 'got', 'pih', 'sm', 'bm', 'iu', 'ss', 'sd',
            'pnt', 'ki', 'tyv', 'ee', 'ha', 'om', 'fj', 'ti', 'ts', 'ks', 'tw',
            'sg', 've', 'st', 'ff', 'rn', 'cr', 'dz', 'ak', 'tum', 'ik', 'lg',
            'ny', 'ch', 'xh',
        ]

        langs = self.languages_by_size + ['test', 'test2']  # Sites we want to edit but not count as real languages

        self.langs = dict([(lang, '%s.wikipedia.org' % lang)
                           for lang in langs])

        self.category_redirect_templates = {
            '_default': (),
            'ar': ('تحويل تصنيف',
                   'تحويلة تصنيف',
                   'Category redirect',),
            'arz': ('تحويل تصنيف',),
            'cs': ('Zastaralá kategorie',),
            'da': ('Kategoriomdirigering',),
            'en': ('Category redirect',),
            'es': ('Categoría redirigida',),
            'eu': ('Kategoria redirect',),
            'fa': ('رده بهتر',
                   'انتقال رده',
                   'فیلم‌های امریکایی',),
            'fr': ('Redirection de catégorie',),
            'gv': ('Aastiurey ronney',),
            'hi': ('श्रेणीअनुप्रेषित',
                   'Categoryredirect',),
            'hu': ('Kat-redir',
                   'Katredir',
                   'Kat-redirekt',),
            'id': ('Alih kategori',
                   'Alihkategori',),
            'ja': ('Category redirect',),
            'ko': ('분류 넘겨주기',),
            'mk': ('Премести категорија',),
            'ml': ('Category redirect',),
            'ms': ('Pengalihan kategori',
                   'Categoryredirect',
                   'Category redirect',),
            'mt': ('Redirect kategorija',),
            'no': ('Category redirect',
                   'Kategoriomdirigering',
                   'Kategori-omdirigering',),
            'pl': ('Przekierowanie kategorii',
                   'Category redirect',),
            'pt': ('Redirecionamento de categoria',
                   'Redircat',
                   'Redirect-categoria',),
            'ro': ('Redirect categorie',),
            'ru': ('Переименованная категория',
                   'Categoryredirect',
                   'CategoryRedirect',
                   'Category redirect',
                   'Catredirect',),
            'simple': ('Category redirect',
                       'Categoryredirect',
                       'Catredirect',),
            'sl': ('Category redirect',),
            'sq': ('Kategori e zhvendosur',
                   'Category redirect',),
            'sv': ('Kategoriomdirigering',
                   'Omdirigering kategori',),
            'tl': ('Category redirect',),
            'tr': ('Kategori yönlendirme',
                   'Kat redir',),
            'uk': ('Categoryredirect',),
            'vi': ('Đổi hướng thể loại',
                   'Thể loại đổi hướng',
                   'Chuyển hướng thể loại',
                   'Categoryredirect',
                   'Category redirect',
                   'Catredirect',),
            'yi': ('קאטעגאריע אריבערפירן',),
            'zh': ('分类重定向',
                   'Cr',
                   'CR',
                   'Cat-redirect',),
            'zh-yue': ('Category redirect',
                       '分類彈去',
                       '分類跳轉',),
        }

        self.disambiguationTemplates = {
            # If no templates are given, retrieve names from  the live wiki
            # ([[MediaWiki:Disambiguationspage]])
            # first char must be in uppercase
            '_default': ['Disambig'],  # for default MediaWiki message only
            'haw': ['Huaʻōlelo puana like'],
            'no':  ['Peker', 'Etternavn', 'Disambig',
                    'Tobokstavsforkortelse', 'Trebokstavsforkortelse',
                    'Flertydig', 'Pekerside'],
            'nov': ['Desambig'],
            'qu':  ["Sut'ichana qillqa", 'Disambig', 'SJM'],
            'rmy': ['Dudalipen'],
            'sk':  ['Disambig', 'Rozlišovacia stránka', 'Disambiguation'],
            'tg':  ['Ибҳомзудоӣ', 'Disambig', 'Рафъи ибҳом',
                    'Disambiguation'],
            'tr':  ['Anlam ayrım', 'Disambig', 'Anlam ayrımı',
                    'Kişi adları (anlam ayrımı)',
                    'Yerleşim yerleri (anlam ayrımı)',
                    'kısaltmalar (anlam ayrımı)', 'Coğrafya (anlam ayrımı)',
                    'Yerleşim yerleri (anlam ayrımı)', 'Sayılar (anlam ayrımı)',
                    "ABD'deki iller (anlam ayrımı)"],
            'wo':  ['Bokktekki'],
            'yi':  ['באדייטען'],
            'zea': ['Dp', 'Deurverwiespagina'],
            'zh-classical':  ['釋義', '消歧義', 'Disambig'],
        }

        self.disambcatname = {
            'af':  'dubbelsinnig',
            'als': 'Begriffsklärung',
            'ang': 'Scīrung',
            'ast': 'Dixebra',
            'ar':  'صفحات توضيح',
            'be':  'Disambig',
            'be-x-old':  'Вікіпэдыя:Неадназначнасьці',
            'bg':  'Пояснителни страници',
            'ca':  'Pàgines de desambiguació',
            'cbk-zam': 'Desambiguo',
            'cs':  'Rozcestníky',
            'cy':  'Gwahaniaethu',
            'da':  'Flertydig',
            'de':  'Begriffsklärung',
            'el':  'Αποσαφήνιση',
            'en':  'All disambiguation pages',
            'eo':  'Apartigiloj',
            'es':  'Desambiguación',
            'et':  'Täpsustusleheküljed',
            'eu':  'Argipen orriak',
            'fa':  'صفحه‌های ابهام‌زدایی',
            'fi':  'Täsmennyssivut',
            'fo':  'Fleiri týdningar',
            'fr':  'Homonymie',
            'fy':  'Trochferwiisside',
            'ga':  'Idirdhealáin',
            'gl':  'Homónimos',
            'he':  'פירושונים',
            'hu':  'Egyértelműsítő lapok',
            'ia':  'Disambiguation',
            'id':  'Disambiguasi',
            'io':  'Homonimi',
            'is':  'Aðgreiningarsíður',
            'it':  'Disambigua',
            'ja':  '曖昧さ回避',
            'ka':  'მრავალმნიშვნელოვანი',
            'kw':  'Folennow klerheans',
            'ko':  '동음이의어 문서',
            'ku':  'Rûpelên cudakirinê',
            'krc': 'Кёб магъаналы терминле',
            'ksh': 'Woot met mieh wi ëijnem Senn',
            'la':  'Discretiva',
            'lb':  'Homonymie',
            'li':  'Verdudelikingspazjena',
            'ln':  'Bokokani',
            'lt':  'Nuorodiniai straipsniai',
            'ms':  'Nyahkekaburan',
            'mt':  'Diżambigwazzjoni',
            'nds': 'Mehrdüdig Begreep',
            'nds-nl': 'Wikipedie:Deurverwiespagina',
            'nl':  'Wikipedia:Doorverwijspagina',
            'nn':  'Fleirtydingssider',
            'no':  'Pekere',
            'pl':  'Strony ujednoznaczniające',
            'pt':  'Desambiguação',
            'ro':  'Dezambiguizare',
            'ru':  'Многозначные термины',
            'scn': 'Disambigua',
            'sk':  'Rozlišovacie stránky',
            'sl':  'Razločitev',
            'sq':  'Kthjellime',
            'sr':  'Вишезначна одредница',
            'su':  'Disambiguasi',
            'sv':  'Förgreningssider',
            'szl': 'Zajty ujydnoznačńajůnce',
            'th':  'การแก้ความกำกวม',
            'tl':  'Paglilinaw',
            'tr':  'Anlam ayrım',
            'uk':  'Багатозначні геопункти',
            'vi':  'Trang định hướng',
            'vo':  'Telplänovapads',
            'wa':  'Omonimeye',
            'zea': 'Wikipedia:Deurverwiespagina',
            'zh':  '消歧义',
            'zh-min-nan': 'Khu-pia̍t-ia̍h',
        }

        # families that redirect their interlanguage links here.
        self.interwiki_forwarded_from = [
            'commons',
            'incubator',
            'meta',
            'species',
            'strategy',
            'test',
        ]

        # Global bot allowed languages on
        # http://meta.wikimedia.org/wiki/Bot_policy/Implementation#Current_implementation
        self.cross_allowed = [
            'ab', 'ace', 'af', 'ak', 'als', 'am', 'an', 'ang', 'ar', 'arc',
            'arz', 'as', 'ast', 'av', 'ay', 'az', 'ba', 'bar', 'bat-smg', 'bcl',
            'be', 'be-x-old', 'bg', 'bh', 'bi', 'bjn', 'bm', 'bo', 'bpy', 'bug',
            'bxr', 'ca', 'cbk-zam', 'cdo', 'ce', 'ceb', 'ch', 'chr', 'chy',
            'ckb', 'co', 'cr', 'crh', 'csb', 'cu', 'cv', 'cy', 'da', 'diq',
            'dsb', 'dz', 'ee', 'el', 'eml', 'en', 'eo', 'et', 'eu', 'ext', 'fa',
            'ff', 'fi', 'fj', 'fo', 'frp', 'frr', 'fur', 'ga', 'gag', 'gan',
            'gd', 'glk', 'gn', 'got', 'gu', 'gv', 'ha', 'hak', 'haw', 'he',
            'hi', 'hif', 'hr', 'hsb', 'ht', 'hu', 'hy', 'ia', 'ie', 'ig', 'ik',
            'ilo', 'io', 'iu', 'ja', 'jbo', 'jv', 'ka', 'kaa', 'kab', 'kdb',
            'kg', 'ki', 'kk', 'kl', 'km', 'kn', 'ko', 'koi', 'krc', 'ks', 'ku',
            'kv', 'kw', 'ky', 'la', 'lad', 'lb', 'lbe', 'lez', 'lg', 'li',
            'lij', 'lmo', 'ln', 'lo', 'lt', 'ltg', 'lv', 'map-bms', 'mdf', 'mg',
            'mhr', 'mi', 'mk', 'ml', 'mn', 'mrj', 'ms', 'mwl', 'my', 'myv',
            'mzn', 'na', 'nah', 'nap', 'nds-nl', 'ne', 'new', 'nl', 'no', 'nov',
            'nrm', 'nso', 'nv', 'ny', 'oc', 'om', 'or', 'os', 'pa', 'pag',
            'pam', 'pap', 'pdc', 'pfl', 'pi', 'pih', 'pms', 'pnb', 'pnt', 'ps',
            'qu', 'rm', 'rmy', 'rn', 'roa-rup', 'roa-tara', 'ru', 'rue', 'rw',
            'sa', 'sah', 'sc', 'scn', 'sco', 'sd', 'se', 'sg', 'sh', 'si',
            'simple', 'sk', 'sm', 'sn', 'so', 'srn', 'ss', 'st', 'stq', 'su',
            'sv', 'sw', 'szl', 'ta', 'te', 'tet', 'tg', 'th', 'ti', 'tk', 'tl',
            'tn', 'to', 'tpi', 'tr', 'ts', 'tt', 'tum', 'tw', 'ty', 'udm', 'ug',
            'uz', 've', 'vec', 'vep', 'vls', 'vo', 'wa', 'war', 'wo', 'wuu',
            'xal', 'xh', 'yi', 'yo', 'za', 'zea', 'zh', 'zh-classical',
            'zh-min-nan', 'zh-yue', 'zu',
        ]

        # On most Wikipedias page names must start with a capital letter,
        # but some languages don't use this.
        self.nocapitalize = ['jbo']

        # Which languages have a special order for putting interlanguage links,
        # and what order is it? If a language is not in interwiki_putfirst,
        # alphabetical order on language code is used. For languages that are in
        # interwiki_putfirst, interwiki_putfirst is checked first, and
        # languages are put in the order given there. All other languages are
        # put after those, in code-alphabetical order.

        self.alphabetic_sr = [
            'ace', 'kbd', 'af', 'ak', 'als', 'am', 'ang', 'ab', 'ar', 'an',
            'arc', 'roa-rup', 'frp', 'arz', 'as', 'ast', 'gn', 'av', 'ay', 'az',
            'bjn', 'id', 'ms', 'bg', 'bm', 'zh-min-nan', 'nan', 'map-bms', 'jv',
            'su', 'ba', 'be', 'be-x-old', 'bh', 'bcl', 'bi', 'bn', 'bo', 'bar',
            'bs', 'bpy', 'br', 'bug', 'bxr', 'ca', 'ceb', 'ch', 'cbk-zam', 'sn',
            'tum', 'ny', 'cho', 'chr', 'co', 'cy', 'cv', 'cs', 'da', 'dk',
            'pdc', 'de', 'nv', 'dsb', 'na', 'dv', 'dz', 'mh', 'et', 'el', 'eml',
            'en', 'myv', 'es', 'eo', 'ext', 'eu', 'ee', 'fa', 'hif', 'fo', 'fr',
            'fy', 'ff', 'fur', 'ga', 'gv', 'sm', 'gag', 'gd', 'gl', 'gan', 'ki',
            'glk', 'got', 'gu', 'ha', 'hak', 'xal', 'haw', 'he', 'hi', 'ho',
            'hsb', 'hr', 'hy', 'io', 'ig', 'ii', 'ilo', 'ia', 'ie', 'iu', 'ik',
            'os', 'xh', 'zu', 'is', 'it', 'ja', 'ka', 'kl', 'kr', 'pam', 'krc',
            'csb', 'kk', 'kw', 'rw', 'ky', 'mrj', 'rn', 'sw', 'km', 'kn', 'ko',
            'kv', 'kg', 'ht', 'ks', 'ku', 'kj', 'lad', 'lbe', 'la', 'ltg', 'lv',
            'to', 'lb', 'lez', 'lt', 'lij', 'li', 'ln', 'lo', 'jbo', 'lg',
            'lmo', 'hu', 'mk', 'mg', 'mt', 'mi', 'min', 'cdo', 'mwl', 'ml',
            'mdf', 'mo', 'mn', 'mr', 'mus', 'my', 'mzn', 'nah', 'fj', 'ne',
            'nl', 'nds-nl', 'cr', 'new', 'nap', 'ce', 'frr', 'pih', 'no', 'nb',
            'nn', 'nrm', 'nov', 'oc', 'mhr', 'or', 'om', 'ng', 'hz', 'uz', 'pa',
            'pfl', 'pag', 'pap', 'koi', 'pi', 'pcd', 'pms', 'nds', 'pnb', 'pl',
            'pt', 'pnt', 'ps', 'aa', 'kaa', 'crh', 'ty', 'ksh', 'ro', 'rmy',
            'rm', 'qu', 'ru', 'rue', 'sa', 'sah', 'se', 'sg', 'sc', 'sco', 'sd',
            'stq', 'st', 'nso', 'tn', 'sq', 'si', 'scn', 'simple', 'ss', 'sk',
            'sl', 'cu', 'szl', 'so', 'ckb', 'srn', 'sr', 'sh', 'fi', 'sv', 'ta',
            'shi', 'tl', 'kab', 'roa-tara', 'tt', 'te', 'tet', 'th', 'ti', 'vi',
            'tg', 'tokipona', 'tp', 'tpi', 'chy', 've', 'tr', 'tk', 'tw', 'tyv',
            'udm', 'uk', 'ur', 'ug', 'za', 'vec', 'vep', 'vo', 'fiu-vro', 'wa',
            'vls', 'war', 'wo', 'wuu', 'ts', 'xmf', 'yi', 'yo', 'diq', 'zea',
            'zh', 'zh-tw', 'zh-cn', 'zh-classical', 'zh-yue', 'bat-smg',
        ]

        self.interwiki_putfirst = {
            'be-x-old': self.alphabetic,
            'en': self.alphabetic,
            'et': self.alphabetic_revised,
            'fi': self.alphabetic_revised,
            'fiu-vro': self.alphabetic_revised,
            'fy': self.fyinterwiki,
            'he': ['en'],
            'hu': ['en'],
            'lb': self.alphabetic,
            'mk': self.alphabetic,
            'ms': self.alphabetic_revised,
            'nds': ['nds-nl'],
            'nds-nl': ['nds'],
            'nn': ['no', 'sv', 'da'] + self.alphabetic,
            'no': self.alphabetic,
            'nv': ['en', 'es'] + self.alphabetic,
            'pdc': ['de', 'en'],
            'pl': self.alphabetic,
            'simple': self.alphabetic,
            'sr': self.alphabetic_sr,
            'sv': self.alphabetic,
            'te': ['en', 'hi', 'kn', 'ta', 'ml'],
            'ur': ['ar', 'fa', 'en'] + self.alphabetic,
            'vi': self.alphabetic_revised,
            'yi': ['en', 'he', 'de']
        }

        self.obsolete = {
            'aa': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Afar_Wikipedia
            'cho': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Choctaw_Wikipedia
            'dk': 'da',
            'ho': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Hiri_Motu_Wikipedia
            'hz': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Herero_Wikipedia
            'ii': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Yi_Wikipedia
            'kj': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Kwanyama_Wikipedia
            'kr': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Kanuri_Wikipedia
            'mh': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Marshallese_Wikipedia
            'minnan': 'zh-min-nan',
            'mo': 'ro',  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Moldovan_Wikipedia
            'mus': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Muscogee_Wikipedia
            'nan': 'zh-min-nan',
            'nl_nds': 'nl-nds',  # miss-spelling
            'nb': 'no',
            'ng': None,  # (not reachable) http://meta.wikimedia.org/wiki/Inactive_wikis
            'jp': 'ja',
            'ru-sib': None,  # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Siberian_Wikipedia
            'tlh': None,
            'tokipona': None,
            'zh-tw': 'zh',
            'zh-cn': 'zh'
        }

        # Languages that used to be coded in iso-8859-1
        self.latin1old = [
            'de', 'en', 'et', 'es', 'ia', 'la', 'af', 'cs', 'fr', 'pt', 'sl',
            'bs', 'fy', 'vi', 'lt', 'fi', 'it', 'no', 'simple', 'gl', 'eu',
            'nds', 'co', 'mi', 'mr', 'id', 'lv', 'sw', 'tt', 'uk', 'vo', 'ga',
            'na', 'es', 'nl', 'da', 'dk', 'sv', 'test']

        self.crossnamespace[0] = {
            '_default': {
                'pt': [102],
                'als': [104],
                'ar': [104],
                'de': [4],
                'en': [12],
                'es': [104],
                'fi': [4],
                'fr': [104],
                'hr': [102],
                'lt': [104],
            },
            'km': {
                '_default': [0, 4, 12],
            },
            #wrong wikipedia namespace alias
            'mzn': {
                '_default': [0, 4],

            },
        }
        self.crossnamespace[1] = {
            '_default': {
                'pt': [103],
                'als': [105],
                'ar': [105],
                'en': [13],
                'es': [105],
                'fi': [5],
                'fr': [105],
                'hr': [103],
                'lt': [105],
            },
        }
        self.crossnamespace[4] = {
            '_default': {
                '_default': [12],
            },
            'de': {
                '_default': [0, 10, 12],
                'el': [100, 12],
                'es': [104, 12],
            },
            'fi': {
                '_default': [0, 12]
            },
            'mzn': {
                '_default': [0, 12]
            },
        }
        self.crossnamespace[5] = {
            'fi': {
                '_default': [1]}
        }
        self.crossnamespace[12] = {
            '_default': {
                '_default': [4],
            },
            'en': {
                '_default': [0, 4],
            },
        }
        self.crossnamespace[13] = {
            'en': {
                '_default': [0],
            },
        }
        self.crossnamespace[102] = {
            'pt': {
                '_default': [0],
                'als': [0, 104],
                'ar': [0, 104],
                'es': [0, 104],
                'fr': [0, 104],
                'lt': [0, 104]
            },
            'hr': {
                '_default': [0],
                'als': [0, 104],
                'ar': [0, 104],
                'es': [0, 104],
                'fr': [0, 104],
                'lt': [0, 104]
            },
        }
        self.crossnamespace[103] = {
            'pt': {
                '_default': [1],
                'als': [1, 105],
                'es': [1, 105],
                'fr': [1, 105],
                'lt': [1, 105]
            },
            'hr': {
                '_default': [1],
                'als': [1, 105],
                'es': [1, 105],
                'fr': [1, 105],
                'lt': [1, 105]
            },
        }
        self.crossnamespace[104] = {
            'als': {
                '_default': [0],
                'pt': [0, 102],
                'hr': [0, 102],
            },
            'ar': {
                '_default': [0, 100],
                'hr': [0, 102],
                'pt': [0, 102],
            },
            'es': {
                '_default': [0],
                'pt': [0, 102],
                'hr': [0, 102],
            },
            'fr': {
                '_default': [0],
                'pt': [0, 102],
                'hr': [0, 102],
            },
            'lt': {
                '_default': [0],
                'pt': [0, 102],
                'hr': [0, 102],
            },
        }
        self.crossnamespace[105] = {
            'als': {
                '_default': [1],
                'pt': [0, 103],
                'hr': [0, 103],
            },
            'ar': {
                '_default': [1, 101],
            },
            'es': {
                '_default': [1],
                'pt': [0, 103],
                'hr': [0, 103],
            },
            'fr': {
                '_default': [1],
                'pt': [0, 103],
                'hr': [0, 103],
            },
            'lt': {
                '_default': [1],
                'pt': [0, 103],
                'hr': [0, 103],
            },
        }

    def get_known_families(self, site):
        # In Swedish Wikipedia 's:' is part of page title not a family
        # prefix for 'wikisource'.
        if site.language() == 'sv':
            d = self.known_families.copy()
            d.pop('s')
            d['src'] = 'wikisource'
            return d
        else:
            return self.known_families

    def code2encoding(self, code):
        """Return the encoding for a specific language wiki"""
        # Most wikis nowadays use UTF-8, but change this if yours uses
        # a different encoding
        return 'utf-8'

    def code2encodings(self, code):
        """Return a list of historical encodings for a specific language
           wikipedia"""
        # Historic compatibility
        if code == 'pl':
            return 'utf-8', 'iso8859-2'
        if code == 'ru':
            return 'utf-8', 'iso8859-5'
        if code in self.latin1old:
            return 'utf-8', 'iso-8859-1'
        return self.code2encoding(code),

    def shared_data_repository(self, code, transcluded=False):
        return ('wikidata', 'wikidata')
