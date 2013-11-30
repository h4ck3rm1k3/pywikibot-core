# -*- coding: utf-8  -*-
__version__ = '$Id$'


class transliterator(object):
    def __init__(self, encoding):
        self.trans = {}
        for char in "ÀÁÂẦẤẪẨẬÃĀĂẰẮẴẶẲȦǠẠḀȂĄǍẢ":
            self.trans[char] = "A"
        for char in "ȀǞ":
            self.trans[char] = "Ä"
        self.trans["Ǻ"] = "Å"
        self.trans["Ä"] = "Ae"
        self.trans["Å"] = "Aa"
        for char in "àáâầấẫẩậãāăằắẵặẳȧǡạḁȃąǎảẚ":
            self.trans[char] = "a"
        for char in "ȁǟ":
            self.trans[char] = "ä"
        self.trans["ǻ"] = "å"
        self.trans["ä"] = "ae"
        self.trans["å"] = "aa"
        for char in "ḂḄḆƁƂ":
            self.trans[char] = "B"
        for char in "ḃḅḇƀɓƃ":
            self.trans[char] = "b"
        for char in "ĆĈĊÇČƇ":
            self.trans[char] = "C"
        for char in "ćĉċçčƈȼ":
            self.trans[char] = "c"
        self.trans["Ḉ"] = "Ç"
        self.trans["ḉ"] = "ç"
        self.trans["Ð"] = "Dh"
        self.trans["ð"] = "dh"
        for char in "ĎḊḌḎḐḒĐƉƊƋ":
            self.trans[char] = "D"
        for char in "ďḋḍḏḑḓđɖɗƌ":
            self.trans[char] = "d"
        for char in "ÈȄÉÊḚËĒḔḖĔĖẸE̩ȆȨḜĘĚẼḘẺ":
            self.trans[char] = "E"
        for char in "ỀẾỄỆỂ":
            self.trans[char] = "Ê"
        for char in "èȅéêḛëēḕḗĕėẹe̩ȇȩḝęěẽḙẻ":
            self.trans[char] = "e"
        for char in "ềếễệể":
            self.trans[char] = "ê"
        for char in "ḞƑ":
            self.trans[char] = "F"
        for char in "ḟƒ":
            self.trans[char] = "f"
        for char in "ǴḠĞĠĢǦǤƓ":
            self.trans[char] = "G"
        for char in "ǵḡğġģǧǥɠ":
            self.trans[char] = "g"
        self.trans["Ĝ"] = "Gx"
        self.trans["ĝ"] = "gx"
        for char in "ḢḤḦȞḨḪH̱ĦǶ":
            self.trans[char] = "H"
        for char in "ḣḥḧȟḩḫ̱ẖħƕ":
            self.trans[char] = "h"
        for char in "IÌȈÍÎĨḬÏḮĪĬȊĮǏİỊỈƗ":
            self.trans[char] = "I"
        for char in "ıìȉíîĩḭïḯīĭȋįǐiịỉɨ":
            self.trans[char] = "i"
        for char in "ĴJ":
            self.trans[char] = "J"
        for char in "ɟĵ̌ǰ":
            self.trans[char] = "j"
        for char in "ḰǨĶḲḴƘ":
            self.trans[char] = "K"
        for char in "ḱǩķḳḵƙ":
            self.trans[char] = "k"
        for char in "ĹĻĽḶḸḺḼȽŁ":
            self.trans[char] = "L"
        for char in "ĺļľḷḹḻḽƚłɫ":
            self.trans[char] = "l"
        for char in "ḾṀṂ":
            self.trans[char] = "M"
        for char in "ḿṁṃɱ":
            self.trans[char] = "m"
        for char in "ǸŃÑŅŇṄṆṈṊŊƝɲȠ":
            self.trans[char] = "N"
        for char in "ǹńñņňṅṇṉṋŋɲƞ":
            self.trans[char] = "n"
        for char in "ÒÓÔÕṌṎȬÖŌṐṒŎǑȮȰỌǪǬƠỜỚỠỢỞỎƟØǾ":
            self.trans[char] = "O"
        for char in "òóôõṍṏȭöōṑṓŏǒȯȱọǫǭơờớỡợởỏɵøǿ":
            self.trans[char] = "o"
        for char in "ȌŐȪ":
            self.trans[char] = "Ö"
        for char in "ȍőȫ":
            self.trans[char] = "ö"
        for char in "ỒỐỖỘỔȎ":
            self.trans[char] = "Ô"
        for char in "ồốỗộổȏ":
            self.trans[char] = "ô"
        for char in "ṔṖƤ":
            self.trans[char] = "P"
        for char in "ṕṗƥ":
            self.trans[char] = "p"
        self.trans["ᵽ"] = "q"
        for char in "ȐŔŖŘȒṘṚṜṞ":
            self.trans[char] = "R"
        for char in "ȑŕŗřȓṙṛṝṟɽ":
            self.trans[char] = "r"
        for char in "ŚṤŞȘŠṦṠṢṨ":
            self.trans[char] = "S"
        for char in "śṥşșšṧṡṣṩȿ":
            self.trans[char] = "s"
        self.trans["Ŝ"] = "Sx"
        self.trans["ŝ"] = "sx"
        for char in "ŢȚŤṪṬṮṰŦƬƮ":
            self.trans[char] = "T"
        for char in "ţțťṫṭṯṱŧȾƭʈ":
            self.trans[char] = "t"
        for char in "ÙÚŨṸṴÜṲŪṺŬỤŮŲǓṶỦƯỮỰỬ":
            self.trans[char] = "U"
        for char in "ùúũṹṵüṳūṻŭụůųǔṷủưữựửʉ":
            self.trans[char] = "u"
        for char in "ȔŰǛǗǕǙ":
            self.trans[char] = "Ü"
        for char in "ȕűǜǘǖǚ":
            self.trans[char] = "ü"
        self.trans["Û"] = "Ux"
        self.trans["û"] = "ux"
        self.trans["Ȗ"] = "Û"
        self.trans["ȗ"] = "û"
        self.trans["Ừ"] = "Ù"
        self.trans["ừ"] = "ù"
        self.trans["Ứ"] = "Ú"
        self.trans["ứ"] = "ú"
        for char in "ṼṾ":
            self.trans[char] = "V"
        for char in "ṽṿ":
            self.trans[char] = "v"
        for char in "ẀẂŴẄẆẈ":
            self.trans[char] = "W"
        for char in "ẁẃŵẅẇẉ":
            self.trans[char] = "w"
        for char in "ẊẌ":
            self.trans[char] = "X"
        for char in "ẋẍ":
            self.trans[char] = "x"
        for char in "ỲÝŶŸỸȲẎỴỶƳ":
            self.trans[char] = "Y"
        for char in "ỳýŷÿỹȳẏỵỷƴ":
            self.trans[char] = "y"
        for char in "ŹẐŻẒŽẔƵȤ":
            self.trans[char] = "Z"
        for char in "źẑżẓžẕƶȥ":
            self.trans[char] = "z"
        self.trans["ɀ"] = "zv"

        # Latin: extended Latin alphabet
        self.trans["ɑ"] = "a"
        for char in "ÆǼǢ":
            self.trans[char] = "AE"
        for char in "æǽǣ":
            self.trans[char] = "ae"
        self.trans["Ð"] = "Dh"
        self.trans["ð"] = "dh"
        for char in "ƎƏƐ":
            self.trans[char] = "E"
        for char in "ǝəɛ":
            self.trans[char] = "e"
        for char in "ƔƢ":
            self.trans[char] = "G"
        for char in "ᵷɣƣᵹ":
            self.trans[char] = "g"
        self.trans["Ƅ"] = "H"
        self.trans["ƅ"] = "h"
        self.trans["Ƕ"] = "Wh"
        self.trans["ƕ"] = "wh"
        self.trans["Ɩ"] = "I"
        self.trans["ɩ"] = "i"
        self.trans["Ŋ"] = "Ng"
        self.trans["ŋ"] = "ng"
        self.trans["Œ"] = "OE"
        self.trans["œ"] = "oe"
        self.trans["Ɔ"] = "O"
        self.trans["ɔ"] = "o"
        self.trans["Ȣ"] = "Ou"
        self.trans["ȣ"] = "ou"
        self.trans["Ƽ"] = "Q"
        for char in "ĸƽ":
            self.trans[char] = "q"
        self.trans["ȹ"] = "qp"
        self.trans[""] = "r"
        self.trans["ſ"] = "s"
        self.trans["ß"] = "ss"
        self.trans["Ʃ"] = "Sh"
        for char in "ʃᶋ":
            self.trans[char] = "sh"
        self.trans["Ʉ"] = "U"
        self.trans["ʉ"] = "u"
        self.trans["Ʌ"] = "V"
        self.trans["ʌ"] = "v"
        for char in "ƜǷ":
            self.trans[char] = "W"
        for char in "ɯƿ":
            self.trans[char] = "w"
        self.trans["Ȝ"] = "Y"
        self.trans["ȝ"] = "y"
        self.trans["Ĳ"] = "IJ"
        self.trans["ĳ"] = "ij"
        self.trans["Ƨ"] = "Z"
        for char in "ʮƨ":
            self.trans[char] = "z"
        self.trans["Ʒ"] = "Zh"
        self.trans["ʒ"] = "zh"
        self.trans["Ǯ"] = "Dzh"
        self.trans["ǯ"] = "dzh"
        for char in "ƸƹʔˀɁɂ":
            self.trans[char] = "'"
        for char in "Þ":
            self.trans[char] = "Th"
        for char in "þ":
            self.trans[char] = "th"
        for char in "Cʗǃ":
            self.trans[char] = "!"

        #Punctuation and typography
        for char in "«»“”„¨":
            self.trans[char] = '"'
        for char in "‘’′":
            self.trans[char] = "'"
        self.trans["•"] = "*"
        self.trans["@"] = "(at)"
        self.trans["¤"] = "$"
        self.trans["¢"] = "c"
        self.trans["€"] = "E"
        self.trans["£"] = "L"
        self.trans["¥"] = "yen"
        self.trans["†"] = "+"
        self.trans["‡"] = "++"
        self.trans["°"] = ":"
        self.trans["¡"] = "!"
        self.trans["¿"] = "?"
        self.trans["‰"] = "o/oo"
        self.trans["‱"] = "o/ooo"
        for char in "¶§":
            self.trans[char] = ">"
        for char in "…":
            self.trans[char] = "..."
        for char in "‒–—―":
            self.trans[char] = "-"
        for char in "·":
            self.trans[char] = " "
        self.trans["¦"] = "|"
        self.trans["⁂"] = "***"
        self.trans["◊"] = "<>"
        self.trans["‽"] = "?!"
        self.trans["؟"] = ";-)"
        self.trans["¹"] = "1"
        self.trans["²"] = "2"
        self.trans["³"] = "3"

        # Cyrillic
        self.trans.update({"А": "A", "а": "a", "Б": "B", "б": "b",
                           "В": "V", "в": "v", "Г": "G", "г": "g",
                           "Д": "D", "д": "d", "Е": "E", "е": "e",
                           "Ж": "Zh", "ж": "zh", "З": "Z", "з": "z",
                           "И": "I", "и": "i", "Й": "J", "й": "j",
                           "К": "K", "к": "k", "Л": "L", "л": "l",
                           "М": "M", "м": "m", "Н": "N", "н": "n",
                           "О": "O", "о": "o", "П": "P", "п": "p",
                           "Р": "R", "р": "r", "С": "S", "с": "s",
                           "Т": "T", "т": "t", "У": "U", "у": "u",
                           "Ф": "F", "ф": "f", "х": "kh", "Ц": "C",
                           "ц": "c", "Ч": "Ch", "ч": "ch", "Ш": "Sh",
                           "ш": "sh", "Щ": "Shch", "щ": "shch", "Ь": "'",
                           "ь": "'", "Ъ": '"', "ъ": '"', "Ю": "Yu",
                           "ю": "yu", "Я": "Ya", "я": "ya", "Х": "Kh",
                           "Χ": "Kh"})

        # Additional Cyrillic letters, most occuring in only one or a few languages
        self.trans.update({"Ы": "Y", "ы": "y", "Ё": "Ë", "ё": "ë",
                           "Э": "È", "Ѐ": "È", "э": "è", "ѐ": "è",
                           "І": "I", "і": "i", "Ї": "Ji", "ї": "ji",
                           "Є": "Je", "є": "je", "Ґ": "G", "Ҝ": "G",
                           "ґ": "g", "ҝ": "g", "Ђ": "Dj", "ђ": "dj",
                           "Ӣ": "Y", "ӣ": "y", "Љ": "Lj", "љ": "lj",
                           "Њ": "Nj", "њ": "nj", "Ћ": "Cj", "ћ": "cj",
                           "Җ": "Zhj", "җ": "zhj", "Ѓ": "Gj", "ѓ": "gj",
                           "Ќ": "Kj", "ќ": "kj", "Ӣ": "Ii", "ӣ": "ii",
                           "Ӯ": "U", "ӯ": "u", "Ҳ": "H", "ҳ": "h",
                           "Ҷ": "Dz", "ҷ": "dz", "Ө": "Ô", "Ӫ": "Ô",
                           "ө": "ô", "ӫ": "ô", "Ү": "Y", "ү": "y", "Һ": "H",
                           "һ": "h", "Ә": "AE", "Ӕ": "AE", "ә": "ae",
                           "Ӛ": "Ë", "Ӭ": "Ë", "ӛ": "ë", "ӭ": "ë", "Җ": "Zhj",
                           "җ": "zhj", "Ұ": "U", "ұ": "u", "ў": "ù", "Ў": "Ù",
                           "ѝ": "ì", "Ѝ": "Ì", "Ӑ": "A", "ă": "a", "Ӓ": "Ä",
                           "ҿ": "ä", "Ҽ": "Ts", "Ҿ": "Ts", "ҽ": "ts", "ҿ": "ts",
                           "Ҙ": "Dh", "ҙ": "dh", "Ӏ": "", "ӏ": "", "Ӆ": "L",
                           "ӆ": "l", "Ӎ": "M", "ӎ": "m", "Ӧ": "Ö", "ӧ": "ö",
                           "Ҩ": "u", "ҩ": "u", "Ҧ": "Ph", "ҧ": "ph", "Ҏ": "R",
                           "ҏ": "r", "Ҫ": "Th", "ҫ": "th", "Ҭ": "T", "ҭ": "t",
                           "Ӯ": "Û", "ӯ": "û", "Ұ": "U", "Ӹ": "U", "ұ": "u",
                           "ӹ": "u", "Ҵ": "Tts", "ҵ": "tts", "Ӵ": "Ch", "ӵ": "ch"})

        for char in "ЈӤҊ":
            self.trans[char] = "J"
        for char in "јӥҋ":
            self.trans[char] = "j"
        for char in "ЏӁӜҶ":
            self.trans[char] = "Dzh"
        for char in "џӂӝҷ":
            self.trans[char] = "dzh"
        for char in "ЅӞӠӋҸ":
            self.trans[char] = "Dz"
        for char in "ѕӟӡӌҹ":
            self.trans[char] = "dz"
        for char in "ҒӶҔ":
            self.trans[char] = "G"
        for char in "ғӷҕ":
            self.trans[char] = "g"
        for char in "ҚҞҠӃ":
            self.trans[char] = "Q"
        for char in "қҟҡӄ":
            self.trans[char] = "q"
        for char in "ҢҤӉӇ":
            self.trans[char] = "Ng"
        for char in "ңҥӊӈ":
            self.trans[char] = "ng"
        for char in "ӖѢҌ":
            self.trans[char] = "E"
        for char in "ӗѣҍ":
            self.trans[char] = "e"
        for char in "ӲӰҮ":
            self.trans[char] = "Ü"
        for char in "ӳӱү":
            self.trans[char] = "ü"

        # Archaic Cyrillic letters
        self.trans.update({"Ѹ": "Ou", "ѹ": "ou", "Ѡ": "O", "Ѻ": "O", "ѡ": "o",
                           "ѻ": "o", "Ѿ": "Ot", "ѿ": "ot", "Ѣ": "E", "ѣ": "e",
                           "Ѥ": "Ei", "Ѧ": "Ei", "ѥ": "ei", "ѧ": "ei", "Ѫ": "Ai",
                           "ѫ": "ai", "Ѯ": "X", "ѯ": "x", "Ѱ": "Ps", "ѱ": "ps",
                           "Ѳ": "Th", "ѳ": "th", "Ѵ": "Ü", "Ѷ": "Ü", "ѵ": "ü"})

        # Hebrew alphabet
        for char in "אע":
            self.trans[char] = "'"
        self.trans["ב"] = "b"
        self.trans["ג"] = "g"
        self.trans["ד"] = "d"
        self.trans["ה"] = "h"
        self.trans["ו"] = "v"
        self.trans["ז"] = "z"
        self.trans["ח"] = "kh"
        self.trans["ט"] = "t"
        self.trans["י"] = "y"
        for char in "ךכ":
            self.trans[char] = "k"
        self.trans["ל"] = "l"
        for char in "םמ":
            self.trans[char] = "m"
        for char in "ןנ":
            self.trans[char] = "n"
        self.trans["ס"] = "s"
        for char in "ףפ":
            self.trans[char] = "ph"
        for char in "ץצ":
            self.trans[char] = "ts"
        self.trans["ק"] = "q"
        self.trans["ר"] = "r"
        self.trans["ש"] = "sh"
        self.trans["ת"] = "th"

        # Arab alphabet
        for char in "اﺍﺎ":
            self.trans[char] = "a"
        for char in "بﺏﺐﺒﺑ":
            self.trans[char] = "b"
        for char in "تﺕﺖﺘﺗ":
            self.trans[char] = "t"
        for char in "ثﺙﺚﺜﺛ":
            self.trans[char] = "th"
        for char in "جﺝﺞﺠﺟ":
            self.trans[char] = "g"
        for char in "حﺡﺢﺤﺣ":
            self.trans[char] = "h"
        for char in "خﺥﺦﺨﺧ":
            self.trans[char] = "kh"
        for char in "دﺩﺪ":
            self.trans[char] = "d"
        for char in "ذﺫﺬ":
            self.trans[char] = "dh"
        for char in "رﺭﺮ":
            self.trans[char] = "r"
        for char in "زﺯﺰ":
            self.trans[char] = "z"
        for char in "سﺱﺲﺴﺳ":
            self.trans[char] = "s"
        for char in "شﺵﺶﺸﺷ":
            self.trans[char] = "sh"
        for char in "صﺹﺺﺼﺻ":
            self.trans[char] = "s"
        for char in "ضﺽﺾﻀﺿ":
            self.trans[char] = "d"
        for char in "طﻁﻂﻄﻃ":
            self.trans[char] = "t"
        for char in "ظﻅﻆﻈﻇ":
            self.trans[char] = "z"
        for char in "عﻉﻊﻌﻋ":
            self.trans[char] = "'"
        for char in "غﻍﻎﻐﻏ":
            self.trans[char] = "gh"
        for char in "فﻑﻒﻔﻓ":
            self.trans[char] = "f"
        for char in "قﻕﻖﻘﻗ":
            self.trans[char] = "q"
        for char in "كﻙﻚﻜﻛک":
            self.trans[char] = "k"
        for char in "لﻝﻞﻠﻟ":
            self.trans[char] = "l"
        for char in "مﻡﻢﻤﻣ":
            self.trans[char] = "m"
        for char in "نﻥﻦﻨﻧ":
            self.trans[char] = "n"
        for char in "هﻩﻪﻬﻫ":
            self.trans[char] = "h"
        for char in "وﻭﻮ":
            self.trans[char] = "w"
        for char in "یيﻱﻲﻴﻳ":
            self.trans[char] = "y"
        # Arabic - additional letters, modified letters and ligatures
        self.trans["ﺀ"] = "'"
        for char in "آﺁﺂ":
            self.trans[char] = "'a"
        for char in "ةﺓﺔ":
            self.trans[char] = "th"
        for char in "ىﻯﻰ":
            self.trans[char] = "á"
        for char in "یﯼﯽﯿﯾ":
            self.trans[char] = "y"
        self.trans["؟"] = "?"
        # Arabic - ligatures
        for char in "ﻻﻼ":
            self.trans[char] = "la"
        self.trans["ﷲ"] = "llah"
        for char in "إأ":
            self.trans[char] = "a'"
        self.trans["ؤ"] = "w'"
        self.trans["ئ"] = "y'"
        for char in "◌◌":
            self.trans[char] = ""  # indicates absence of vowels
        # Arabic vowels
        self.trans["◌"] = "a"
        self.trans["◌"] = "u"
        self.trans["◌"] = "i"
        self.trans["◌"] = "a"
        self.trans["◌"] = "ay"
        self.trans["◌"] = "ay"
        self.trans["◌"] = "u"
        self.trans["◌"] = "iy"
        # Arab numerals
        for char in "٠۰":
            self.trans[char] = "0"
        for char in "١۱":
            self.trans[char] = "1"
        for char in "٢۲":
            self.trans[char] = "2"
        for char in "٣۳":
            self.trans[char] = "3"
        for char in "٤۴":
            self.trans[char] = "4"
        for char in "٥۵":
            self.trans[char] = "5"
        for char in "٦۶":
            self.trans[char] = "6"
        for char in "٧۷":
            self.trans[char] = "7"
        for char in "٨۸":
            self.trans[char] = "8"
        for char in "٩۹":
            self.trans[char] = "9"
        # Perso-Arabic
        for char in "پﭙﭙپ":
            self.trans[char] = "p"
        for char in "چچچچ":
            self.trans[char] = "ch"
        for char in "ژژ":
            self.trans[char] = "zh"
        for char in "گﮔﮕﮓ":
            self.trans[char] = "g"

        # Greek
        self.trans.update({"Α": "A", "α": "a", "Β": "B", "β": "b", "Γ": "G",
                           "γ": "g", "Δ": "D", "δ": "d", "Ε": "E", "ε": "e",
                           "Ζ": "Z", "ζ": "z", "Η": "I", "η": "i", "θ": "th",
                           "Θ": "Th", "Ι": "I", "ι": "i", "Κ": "K", "κ": "k",
                           "Λ": "L", "λ": "l", "Μ": "M", "μ": "m", "Ν": "N",
                           "ν": "n", "Ξ": "X", "ξ": "x", "Ο": "O", "ο": "o",
                           "Π": "P", "π": "p", "Ρ": "R", "ρ": "r", "Σ": "S",
                           "σ": "s", "ς": "s", "Τ": "T", "τ": "t", "Υ": "Y",
                           "υ": "y", "Φ": "F", "φ": "f", "Ψ": "Ps", "ψ": "ps",
                           "Ω": "O", "ω": "o", "ϗ": "&", "Ϛ": "St", "ϛ": "st",
                           "Ϙ": "Q", "Ϟ": "Q", "ϙ": "q", "ϟ": "q", "Ϻ": "S",
                           "ϻ": "s", "Ϡ": "Ss", "ϡ": "ss", "Ϸ": "Sh", "ϸ": "sh",
                           "·": ":", "Ά": "Á", "ά": "á", "Έ": "É", "Ή": "É",
                           "έ": "é", "ή": "é", "Ί": "Í", "ί": "í", "Ϊ": "Ï",
                           "ϊ": "ï", "ΐ": "ï", "Ό": "Ó", "ό": "ó", "Ύ": "Ý",
                           "ύ": "ý", "Ϋ": "Y", "ϋ": "ÿ", "ΰ": "ÿ", "Ώ": "Ó",
                           "ώ": "ó"})

        # Japanese (katakana and hiragana)
        for char in "アァあ":
            self.trans[char] = "a"
        for char in "イィい":
            self.trans[char] = "i"
        for char in "ウう":
            self.trans[char] = "u"
        for char in "エェえ":
            self.trans[char] = "e"
        for char in "オォお":
            self.trans[char] = "o"
        for char in "ャや":
            self.trans[char] = "ya"
        for char in "ュゆ":
            self.trans[char] = "yu"
        for char in "ョよ":
            self.trans[char] = "yo"
        for char in "カか":
            self.trans[char] = "ka"
        for char in "キき":
            self.trans[char] = "ki"
        for char in "クく":
            self.trans[char] = "ku"
        for char in "ケけ":
            self.trans[char] = "ke"
        for char in "コこ":
            self.trans[char] = "ko"
        for char in "サさ":
            self.trans[char] = "sa"
        for char in "シし":
            self.trans[char] = "shi"
        for char in "スす":
            self.trans[char] = "su"
        for char in "セせ":
            self.trans[char] = "se"
        for char in "ソそ":
            self.trans[char] = "so"
        for char in "タた":
            self.trans[char] = "ta"
        for char in "チち":
            self.trans[char] = "chi"
        for char in "ツつ":
            self.trans[char] = "tsu"
        for char in "テて":
            self.trans[char] = "te"
        for char in "トと":
            self.trans[char] = "to"
        for char in "ナな":
            self.trans[char] = "na"
        for char in "ニに":
            self.trans[char] = "ni"
        for char in "ヌぬ":
            self.trans[char] = "nu"
        for char in "ネね":
            self.trans[char] = "ne"
        for char in "ノの":
            self.trans[char] = "no"
        for char in "ハは":
            self.trans[char] = "ha"
        for char in "ヒひ":
            self.trans[char] = "hi"
        for char in "フふ":
            self.trans[char] = "fu"
        for char in "ヘへ":
            self.trans[char] = "he"
        for char in "ホほ":
            self.trans[char] = "ho"
        for char in "マま":
            self.trans[char] = "ma"
        for char in "ミみ":
            self.trans[char] = "mi"
        for char in "ムむ":
            self.trans[char] = "mu"
        for char in "メめ":
            self.trans[char] = "me"
        for char in "モも":
            self.trans[char] = "mo"
        for char in "ラら":
            self.trans[char] = "ra"
        for char in "リり":
            self.trans[char] = "ri"
        for char in "ルる":
            self.trans[char] = "ru"
        for char in "レれ":
            self.trans[char] = "re"
        for char in "ロろ":
            self.trans[char] = "ro"
        for char in "ワわ":
            self.trans[char] = "wa"
        for char in "ヰゐ":
            self.trans[char] = "wi"
        for char in "ヱゑ":
            self.trans[char] = "we"
        for char in "ヲを":
            self.trans[char] = "wo"
        for char in "ンん":
            self.trans[char] = "n"
        for char in "ガが":
            self.trans[char] = "ga"
        for char in "ギぎ":
            self.trans[char] = "gi"
        for char in "グぐ":
            self.trans[char] = "gu"
        for char in "ゲげ":
            self.trans[char] = "ge"
        for char in "ゴご":
            self.trans[char] = "go"
        for char in "ザざ":
            self.trans[char] = "za"
        for char in "ジじ":
            self.trans[char] = "ji"
        for char in "ズず":
            self.trans[char] = "zu"
        for char in "ゼぜ":
            self.trans[char] = "ze"
        for char in "ゾぞ":
            self.trans[char] = "zo"
        for char in "ダだ":
            self.trans[char] = "da"
        for char in "ヂぢ":
            self.trans[char] = "dji"
        for char in "ヅづ":
            self.trans[char] = "dzu"
        for char in "デで":
            self.trans[char] = "de"
        for char in "ドど":
            self.trans[char] = "do"
        for char in "バば":
            self.trans[char] = "ba"
        for char in "ビび":
            self.trans[char] = "bi"
        for char in "ブぶ":
            self.trans[char] = "bu"
        for char in "ベべ":
            self.trans[char] = "be"
        for char in "ボぼ":
            self.trans[char] = "bo"
        for char in "パぱ":
            self.trans[char] = "pa"
        for char in "ピぴ":
            self.trans[char] = "pi"
        for char in "プぷ":
            self.trans[char] = "pu"
        for char in "ペぺ":
            self.trans[char] = "pe"
        for char in "ポぽ":
            self.trans[char] = "po"
        for char in "ヴゔ":
            self.trans[char] = "vu"
        self.trans["ヷ"] = "va"
        self.trans["ヸ"] = "vi"
        self.trans["ヹ"] = "ve"
        self.trans["ヺ"] = "vo"

        # Japanese and Chinese punctuation and typography
        for char in "・·":
            self.trans[char] = " "
        for char in "〃『』《》":
            self.trans[char] = '"'
        for char in "「」〈〉〘〙〚〛":
            self.trans[char] = "'"
        for char in "（〔":
            self.trans[char] = "("
        for char in "）〕":
            self.trans[char] = ")"
        for char in "［【〖":
            self.trans[char] = "["
        for char in "］】〗":
            self.trans[char] = "]"
        for char in "｛":
            self.trans[char] = "{"
        for char in "｝":
            self.trans[char] = "}"
        for char in "っ":
            self.trans[char] = ":"
        for char in "ー":
            self.trans[char] = "h"
        for char in "゛":
            self.trans[char] = "'"
        for char in "゜":
            self.trans[char] = "p"
        for char in "。":
            self.trans[char] = ". "
        for char in "、":
            self.trans[char] = ", "
        for char in "・":
            self.trans[char] = " "
        for char in "〆":
            self.trans[char] = "shime"
        for char in "〜":
            self.trans[char] = "-"
        for char in "…":
            self.trans[char] = "..."
        for char in "‥":
            self.trans[char] = ".."
        for char in "ヶ":
            self.trans[char] = "months"
        for char in "•◦":
            self.trans[char] = "_"
        for char in "※＊":
            self.trans[char] = "*"
        for char in "Ⓧ":
            self.trans[char] = "(X)"
        for char in "Ⓨ":
            self.trans[char] = "(Y)"
        for char in "！":
            self.trans[char] = "!"
        for char in "？":
            self.trans[char] = "?"
        for char in "；":
            self.trans[char] = ";"
        for char in "：":
            self.trans[char] = ":"
        for char in "。":
            self.trans[char] = "."
        for char in "，、":
            self.trans[char] = ","

        # Georgian
        for char in "ა":
            self.trans[char] = "a"
        for char in "ბ":
            self.trans[char] = "b"
        for char in "გ":
            self.trans[char] = "g"
        for char in "დ":
            self.trans[char] = "d"
        for char in "ეჱ":
            self.trans[char] = "e"
        for char in "ვ":
            self.trans[char] = "v"
        for char in "ზ":
            self.trans[char] = "z"
        for char in "თ":
            self.trans[char] = "th"
        for char in "ი":
            self.trans[char] = "i"
        for char in "კ":
            self.trans[char] = "k"
        for char in "ლ":
            self.trans[char] = "l"
        for char in "მ":
            self.trans[char] = "m"
        for char in "ნ":
            self.trans[char] = "n"
        for char in "ო":
            self.trans[char] = "o"
        for char in "პ":
            self.trans[char] = "p"
        for char in "ჟ":
            self.trans[char] = "zh"
        for char in "რ":
            self.trans[char] = "r"
        for char in "ს":
            self.trans[char] = "s"
        for char in "ტ":
            self.trans[char] = "t"
        for char in "უ":
            self.trans[char] = "u"
        for char in "ფ":
            self.trans[char] = "ph"
        for char in "ქ":
            self.trans[char] = "q"
        for char in "ღ":
            self.trans[char] = "gh"
        for char in "ყ":
            self.trans[char] = "q'"
        for char in "შ":
            self.trans[char] = "sh"
        for char in "ჩ":
            self.trans[char] = "ch"
        for char in "ც":
            self.trans[char] = "ts"
        for char in "ძ":
            self.trans[char] = "dz"
        for char in "წ":
            self.trans[char] = "ts'"
        for char in "ჭ":
            self.trans[char] = "ch'"
        for char in "ხ":
            self.trans[char] = "kh"
        for char in "ჯ":
            self.trans[char] = "j"
        for char in "ჰ":
            self.trans[char] = "h"
        for char in "ჳ":
            self.trans[char] = "w"
        for char in "ჵ":
            self.trans[char] = "o"
        for char in "ჶ":
            self.trans[char] = "f"

        # Devanagari
        for char in "पप":
            self.trans[char] = "p"
        for char in "अ":
            self.trans[char] = "a"
        for char in "आा":
            self.trans[char] = "aa"
        for char in "प":
            self.trans[char] = "pa"
        for char in "इि":
            self.trans[char] = "i"
        for char in "ईी":
            self.trans[char] = "ii"
        for char in "उु":
            self.trans[char] = "u"
        for char in "ऊू":
            self.trans[char] = "uu"
        for char in "एे":
            self.trans[char] = "e"
        for char in "ऐै":
            self.trans[char] = "ai"
        for char in "ओो":
            self.trans[char] = "o"
        for char in "औौ":
            self.trans[char] = "au"
        for char in "ऋृर":
            self.trans[char] = "r"
        for char in "ॠॄ":
            self.trans[char] = "rr"
        for char in "ऌॢल":
            self.trans[char] = "l"
        for char in "ॡॣ":
            self.trans[char] = "ll"
        for char in "क":
            self.trans[char] = "k"
        for char in "ख":
            self.trans[char] = "kh"
        for char in "ग":
            self.trans[char] = "g"
        for char in "घ":
            self.trans[char] = "gh"
        for char in "ङ":
            self.trans[char] = "ng"
        for char in "च":
            self.trans[char] = "c"
        for char in "छ":
            self.trans[char] = "ch"
        for char in "ज":
            self.trans[char] = "j"
        for char in "झ":
            self.trans[char] = "jh"
        for char in "ञ":
            self.trans[char] = "ñ"
        for char in "टत":
            self.trans[char] = "t"
        for char in "ठथ":
            self.trans[char] = "th"
        for char in "डद":
            self.trans[char] = "d"
        for char in "ढध":
            self.trans[char] = "dh"
        for char in "णन":
            self.trans[char] = "n"
        for char in "फ":
            self.trans[char] = "ph"
        for char in "ब":
            self.trans[char] = "b"
        for char in "भ":
            self.trans[char] = "bh"
        for char in "म":
            self.trans[char] = "m"
        for char in "य":
            self.trans[char] = "y"
        for char in "व":
            self.trans[char] = "v"
        for char in "श":
            self.trans[char] = "sh"
        for char in "षस":
            self.trans[char] = "s"
        for char in "ह":
            self.trans[char] = "h"
        for char in "क":
            self.trans[char] = "x"
        for char in "त":
            self.trans[char] = "tr"
        for char in "ज":
            self.trans[char] = "gj"
        for char in "क़":
            self.trans[char] = "q"
        for char in "फ":
            self.trans[char] = "f"
        for char in "ख":
            self.trans[char] = "hh"
        for char in "H":
            self.trans[char] = "gh"
        for char in "ज":
            self.trans[char] = "z"
        for char in "डढ":
            self.trans[char] = "r"
        # Devanagari ligatures (possibly incomplete and/or incorrect)
        for char in "ख्":
            self.trans[char] = "khn"
        for char in "त":
            self.trans[char] = "tn"
        for char in "द्":
            self.trans[char] = "dn"
        for char in "श":
            self.trans[char] = "cn"
        for char in "ह्":
            self.trans[char] = "fn"
        for char in "अँ":
            self.trans[char] = "m"
        for char in "॒॑":
            self.trans[char] = ""
        for char in "०":
            self.trans[char] = "0"
        for char in "१":
            self.trans[char] = "1"
        for char in "२":
            self.trans[char] = "2"
        for char in "३":
            self.trans[char] = "3"
        for char in "४":
            self.trans[char] = "4"
        for char in "५":
            self.trans[char] = "5"
        for char in "६":
            self.trans[char] = "6"
        for char in "७":
            self.trans[char] = "7"
        for char in "८":
            self.trans[char] = "8"
        for char in "९":
            self.trans[char] = "9"

        # Armenian
        for char in "Ա":
            self.trans[char] = "A"
        for char in "ա":
            self.trans[char] = "a"
        for char in "Բ":
            self.trans[char] = "B"
        for char in "բ":
            self.trans[char] = "b"
        for char in "Գ":
            self.trans[char] = "G"
        for char in "գ":
            self.trans[char] = "g"
        for char in "Դ":
            self.trans[char] = "D"
        for char in "դ":
            self.trans[char] = "d"
        for char in "Ե":
            self.trans[char] = "Je"
        for char in "ե":
            self.trans[char] = "e"
        for char in "Զ":
            self.trans[char] = "Z"
        for char in "զ":
            self.trans[char] = "z"
        for char in "Է":
            self.trans[char] = "É"
        for char in "է":
            self.trans[char] = "é"
        for char in "Ը":
            self.trans[char] = "Ë"
        for char in "ը":
            self.trans[char] = "ë"
        for char in "Թ":
            self.trans[char] = "Th"
        for char in "թ":
            self.trans[char] = "th"
        for char in "Ժ":
            self.trans[char] = "Zh"
        for char in "ժ":
            self.trans[char] = "zh"
        for char in "Ի":
            self.trans[char] = "I"
        for char in "ի":
            self.trans[char] = "i"
        for char in "Լ":
            self.trans[char] = "L"
        for char in "լ":
            self.trans[char] = "l"
        for char in "Խ":
            self.trans[char] = "Ch"
        for char in "խ":
            self.trans[char] = "ch"
        for char in "Ծ":
            self.trans[char] = "Ts"
        for char in "ծ":
            self.trans[char] = "ts"
        for char in "Կ":
            self.trans[char] = "K"
        for char in "կ":
            self.trans[char] = "k"
        for char in "Հ":
            self.trans[char] = "H"
        for char in "հ":
            self.trans[char] = "h"
        for char in "Ձ":
            self.trans[char] = "Dz"
        for char in "ձ":
            self.trans[char] = "dz"
        for char in "Ղ":
            self.trans[char] = "R"
        for char in "ղ":
            self.trans[char] = "r"
        for char in "Ճ":
            self.trans[char] = "Cz"
        for char in "ճ":
            self.trans[char] = "cz"
        for char in "Մ":
            self.trans[char] = "M"
        for char in "մ":
            self.trans[char] = "m"
        for char in "Յ":
            self.trans[char] = "J"
        for char in "յ":
            self.trans[char] = "j"
        for char in "Ն":
            self.trans[char] = "N"
        for char in "ն":
            self.trans[char] = "n"
        for char in "Շ":
            self.trans[char] = "S"
        for char in "շ":
            self.trans[char] = "s"
        for char in "Շ":
            self.trans[char] = "Vo"
        for char in "շ":
            self.trans[char] = "o"
        for char in "Չ":
            self.trans[char] = "Tsh"
        for char in "չ":
            self.trans[char] = "tsh"
        for char in "Պ":
            self.trans[char] = "P"
        for char in "պ":
            self.trans[char] = "p"
        for char in "Ջ":
            self.trans[char] = "Dz"
        for char in "ջ":
            self.trans[char] = "dz"
        for char in "Ռ":
            self.trans[char] = "R"
        for char in "ռ":
            self.trans[char] = "r"
        for char in "Ս":
            self.trans[char] = "S"
        for char in "ս":
            self.trans[char] = "s"
        for char in "Վ":
            self.trans[char] = "V"
        for char in "վ":
            self.trans[char] = "v"
        for char in "Տ":
            self.trans[char] = "T'"
        for char in "տ":
            self.trans[char] = "t'"
        for char in "Ր":
            self.trans[char] = "R"
        for char in "ր":
            self.trans[char] = "r"
        for char in "Ց":
            self.trans[char] = "Tsh"
        for char in "ց":
            self.trans[char] = "tsh"
        for char in "Ւ":
            self.trans[char] = "V"
        for char in "ւ":
            self.trans[char] = "v"
        for char in "Փ":
            self.trans[char] = "Ph"
        for char in "փ":
            self.trans[char] = "ph"
        for char in "Ք":
            self.trans[char] = "Kh"
        for char in "ք":
            self.trans[char] = "kh"
        for char in "Օ":
            self.trans[char] = "O"
        for char in "օ":
            self.trans[char] = "o"
        for char in "Ֆ":
            self.trans[char] = "F"
        for char in "ֆ":
            self.trans[char] = "f"
        for char in "և":
            self.trans[char] = "&"
        for char in "՟":
            self.trans[char] = "."
        for char in "՞":
            self.trans[char] = "?"
        for char in "՝":
            self.trans[char] = ";"
        for char in "՛":
            self.trans[char] = ""

        # Tamil
        for char in "க்":
            self.trans[char] = "k"
        for char in "ஙண்ந்ன்":
            self.trans[char] = "n"
        for char in "ச":
            self.trans[char] = "c"
        for char in "ஞ்":
            self.trans[char] = "ñ"
        for char in "ட்":
            self.trans[char] = "th"
        for char in "த":
            self.trans[char] = "t"
        for char in "ப":
            self.trans[char] = "p"
        for char in "ம்":
            self.trans[char] = "m"
        for char in "ய்":
            self.trans[char] = "y"
        for char in "ர்ழ்ற":
            self.trans[char] = "r"
        for char in "ல்ள":
            self.trans[char] = "l"
        for char in "வ்":
            self.trans[char] = "v"
        for char in "ஜ":
            self.trans[char] = "j"
        for char in "ஷ":
            self.trans[char] = "sh"
        for char in "ஸ":
            self.trans[char] = "s"
        for char in "ஹ":
            self.trans[char] = "h"
        for char in "க்ஷ":
            self.trans[char] = "x"
        for char in "அ":
            self.trans[char] = "a"
        for char in "ஆ":
            self.trans[char] = "aa"
        for char in "இ":
            self.trans[char] = "i"
        for char in "ஈ":
            self.trans[char] = "ii"
        for char in "உ":
            self.trans[char] = "u"
        for char in "ஊ":
            self.trans[char] = "uu"
        for char in "எ":
            self.trans[char] = "e"
        for char in "ஏ":
            self.trans[char] = "ee"
        for char in "ஐ":
            self.trans[char] = "ai"
        for char in "ஒ":
            self.trans[char] = "o"
        for char in "ஓ":
            self.trans[char] = "oo"
        for char in "ஔ":
            self.trans[char] = "au"
        for char in "ஃ":
            self.trans[char] = ""

        # Bengali
        for char in "অ":
            self.trans[char] = "ô"
        for char in "আা":
            self.trans[char] = "a"
        for char in "ইিঈী":
            self.trans[char] = "i"
        for char in "উুঊূ":
            self.trans[char] = "u"
        for char in "ঋৃ":
            self.trans[char] = "ri"
        for char in "এেয়":
            self.trans[char] = "e"
        for char in "ঐৈ":
            self.trans[char] = "oi"
        for char in "ওো":
            self.trans[char] = "o"
        for char in "ঔৌ":
            self.trans[char] = "ou"
        for char in "্":
            self.trans[char] = ""
        for char in "ৎ":
            self.trans[char] = "t"
        for char in "ং":
            self.trans[char] = "n"
        for char in "ঃ":
            self.trans[char] = "h"
        for char in "ঁ":
            self.trans[char] = "ñ"
        for char in "ক":
            self.trans[char] = "k"
        for char in "খ":
            self.trans[char] = "kh"
        for char in "গ":
            self.trans[char] = "g"
        for char in "ঘ":
            self.trans[char] = "gh"
        for char in "ঙ":
            self.trans[char] = "ng"
        for char in "চ":
            self.trans[char] = "ch"
        for char in "ছ":
            self.trans[char] = "chh"
        for char in "জ":
            self.trans[char] = "j"
        for char in "ঝ":
            self.trans[char] = "jh"
        for char in "ঞ":
            self.trans[char] = "n"
        for char in "টত":
            self.trans[char] = "t"
        for char in "ঠথ":
            self.trans[char] = "th"
        for char in "ডদ":
            self.trans[char] = "d"
        for char in "ঢধ":
            self.trans[char] = "dh"
        for char in "ণন":
            self.trans[char] = "n"
        for char in "প":
            self.trans[char] = "p"
        for char in "ফ":
            self.trans[char] = "ph"
        for char in "ব":
            self.trans[char] = "b"
        for char in "ভ":
            self.trans[char] = "bh"
        for char in "ম":
            self.trans[char] = "m"
        for char in "য":
            self.trans[char] = "dzh"
        for char in "র":
            self.trans[char] = "r"
        for char in "ল":
            self.trans[char] = "l"
        for char in "শ":
            self.trans[char] = "s"
        for char in "হ":
            self.trans[char] = "h"
        for char in "য়":
            self.trans[char] = "-"
        for char in "ড়":
            self.trans[char] = "r"
        for char in "ঢ":
            self.trans[char] = "rh"
        for char in "০":
            self.trans[char] = "0"
        for char in "১":
            self.trans[char] = "1"
        for char in "২":
            self.trans[char] = "2"
        for char in "৩":
            self.trans[char] = "3"
        for char in "৪":
            self.trans[char] = "4"
        for char in "৫":
            self.trans[char] = "5"
        for char in "৬":
            self.trans[char] = "6"
        for char in "৭":
            self.trans[char] = "7"
        for char in "৮":
            self.trans[char] = "8"
        for char in "৯":
            self.trans[char] = "9"

        # Thai (because of complications of the alphabet, self.transliterations
        #       are very imprecise here)
        for char in "ก":
            self.trans[char] = "k"
        for char in "ขฃคฅฆ":
            self.trans[char] = "kh"
        for char in "ง":
            self.trans[char] = "ng"
        for char in "จฉชฌ":
            self.trans[char] = "ch"
        for char in "ซศษส":
            self.trans[char] = "s"
        for char in "ญย":
            self.trans[char] = "y"
        for char in "ฎด":
            self.trans[char] = "d"
        for char in "ฏต":
            self.trans[char] = "t"
        for char in "ฐฑฒถทธ":
            self.trans[char] = "th"
        for char in "ณน":
            self.trans[char] = "n"
        for char in "บ":
            self.trans[char] = "b"
        for char in "ป":
            self.trans[char] = "p"
        for char in "ผพภ":
            self.trans[char] = "ph"
        for char in "ฝฟ":
            self.trans[char] = "f"
        for char in "ม":
            self.trans[char] = "m"
        for char in "ร":
            self.trans[char] = "r"
        for char in "ฤ":
            self.trans[char] = "rue"
        for char in "ๅ":
            self.trans[char] = ":"
        for char in "ลฬ":
            self.trans[char] = "l"
        for char in "ฦ":
            self.trans[char] = "lue"
        for char in "ว":
            self.trans[char] = "w"
        for char in "หฮ":
            self.trans[char] = "h"
        for char in "อ":
            self.trans[char] = ""
        for char in "ร":
            self.trans[char] = "ü"
        for char in "ว":
            self.trans[char] = "ua"
        for char in "อวโิ":
            self.trans[char] = "o"
        for char in "ะัา":
            self.trans[char] = "a"
        for char in "ว":
            self.trans[char] = "u"
        for char in "ำ":
            self.trans[char] = "am"
        for char in "ิ":
            self.trans[char] = "i"
        for char in "ี":
            self.trans[char] = "i:"
        for char in "ึ":
            self.trans[char] = "ue"
        for char in "ื":
            self.trans[char] = "ue:"
        for char in "ุ":
            self.trans[char] = "u"
        for char in "ู":
            self.trans[char] = "u:"
        for char in "เ็":
            self.trans[char] = "e"
        for char in "แ":
            self.trans[char] = "ae"
        for char in "ใไ":
            self.trans[char] = "ai"
        for char in "่้๊๋็์":
            self.trans[char] = ""
        for char in "ฯ":
            self.trans[char] = "."
        for char in "ๆ":
            self.trans[char] = "(2)"

        # Korean (Revised Romanization system within possible, incomplete)
        for char in "국":
            self.trans[char] = "guk"
        for char in "명":
            self.trans[char] = "myeong"
        for char in "검":
            self.trans[char] = "geom"
        for char in "타":
            self.trans[char] = "ta"
        for char in "분":
            self.trans[char] = "bun"
        for char in "사":
            self.trans[char] = "sa"
        for char in "류":
            self.trans[char] = "ryu"
        for char in "포":
            self.trans[char] = "po"
        for char in "르":
            self.trans[char] = "reu"
        for char in "투":
            self.trans[char] = "tu"
        for char in "갈":
            self.trans[char] = "gal"
        for char in "어":
            self.trans[char] = "eo"
        for char in "노":
            self.trans[char] = "no"
        for char in "웨":
            self.trans[char] = "we"
        for char in "이":
            self.trans[char] = "i"
        for char in "라":
            self.trans[char] = "ra"
        for char in "틴":
            self.trans[char] = "tin"
        for char in "루":
            self.trans[char] = "ru"
        for char in "마":
            self.trans[char] = "ma"
        for char in "니":
            self.trans[char] = "ni"
        for char in "아":
            self.trans[char] = "a"
        for char in "독":
            self.trans[char] = "dok"
        for char in "일":
            self.trans[char] = "il"
        for char in "모":
            self.trans[char] = "mo"
        for char in "크":
            self.trans[char] = "keu"
        for char in "샤":
            self.trans[char] = "sya"
        for char in "영":
            self.trans[char] = "yeong"
        for char in "불":
            self.trans[char] = "bul"
        for char in "가":
            self.trans[char] = "ga"
        for char in "리":
            self.trans[char] = "ri"
        for char in "그":
            self.trans[char] = "geu"
        for char in "지":
            self.trans[char] = "ji"
        for char in "야":
            self.trans[char] = "ya"
        for char in "바":
            self.trans[char] = "ba"
        for char in "슈":
            self.trans[char] = "syu"
        for char in "키":
            self.trans[char] = "ki"
        for char in "프":
            self.trans[char] = "peu"
        for char in "랑":
            self.trans[char] = "rang"
        for char in "스":
            self.trans[char] = "seu"
        for char in "로":
            self.trans[char] = "ro"
        for char in "메":
            self.trans[char] = "me"
        for char in "역":
            self.trans[char] = "yeok"
        for char in "도":
            self.trans[char] = "do"

        # Kannada
        self.trans["ಅ"] = "a"
        for char in "ಆಾ":
            self.trans[char] = "aa"
        for char in "ಇಿ":
            self.trans[char] = "i"
        for char in "ಈೀ":
            self.trans[char] = "ii"
        for char in "ಉು":
            self.trans[char] = "u"
        for char in "ಊೂ":
            self.trans[char] = "uu"
        for char in "ಋೂ":
            self.trans[char] = "r'"
        for char in "ಎೆ":
            self.trans[char] = "e"
        for char in "ಏೇ":
            self.trans[char] = "ee"
        for char in "ಐೈ":
            self.trans[char] = "ai"
        for char in "ಒೊ":
            self.trans[char] = "o"
        for char in "ಓೋ":
            self.trans[char] = "oo"
        for char in "ಔೌ":
            self.trans[char] = "au"
        self.trans["ಂ"] = "m'"
        self.trans["ಃ"] = "h'"
        self.trans["ಕ"] = "k"
        self.trans["ಖ"] = "kh"
        self.trans["ಗ"] = "g"
        self.trans["ಘ"] = "gh"
        self.trans["ಙ"] = "ng"
        self.trans["ಚ"] = "c"
        self.trans["ಛ"] = "ch"
        self.trans["ಜ"] = "j"
        self.trans["ಝ"] = "ny"
        self.trans["ಟ"] = "tt"
        self.trans["ಠ"] = "tth"
        self.trans["ಡ"] = "dd"
        self.trans["ಢ"] = "ddh"
        self.trans["ಣ"] = "nn"
        self.trans["ತ"] = "t"
        self.trans["ಥ"] = "th"
        self.trans["ದ"] = "d"
        self.trans["ಧ"] = "dh"
        self.trans["ನ"] = "n"
        self.trans["ಪ"] = "p"
        self.trans["ಫ"] = "ph"
        self.trans["ಬ"] = "b"
        self.trans["ಭ"] = "bh"
        self.trans["ಮ"] = "m"
        self.trans["ಯ"] = "y"
        self.trans["ರ"] = "r"
        self.trans["ಲ"] = "l"
        self.trans["ವ"] = "v"
        self.trans["ಶ"] = "sh"
        self.trans["ಷ"] = "ss"
        self.trans["ಸ"] = "s"
        self.trans["ಹ"] = "h"
        self.trans["ಳ"] = "ll"
        self.trans["೦"] = "0"
        self.trans["೧"] = "1"
        self.trans["೨"] = "2"
        self.trans["೩"] = "3"
        self.trans["೪"] = "4"
        self.trans["೫"] = "5"
        self.trans["೬"] = "6"
        self.trans["೭"] = "7"
        self.trans["೮"] = "8"
        self.trans["೯"] = "9"
        # Telugu
        for char in "అ":
            self.trans[char] = "a"
        for char in "ఆా":
            self.trans[char] = "aa"
        for char in "ఇి":
            self.trans[char] = "i"
        for char in "ఈీ":
            self.trans[char] = "ii"
        for char in "ఉు":
            self.trans[char] = "u"
        for char in "ఊూ":
            self.trans[char] = "uu"
        for char in "ఋృ":
            self.trans[char] = "r'"
        for char in "ౠౄ":
            self.trans[char] = 'r"'
        self.trans["ఌ"] = "l'"
        self.trans["ౡ"] = 'l"'
        for char in "ఎె":
            self.trans[char] = "e"
        for char in "ఏే":
            self.trans[char] = "ee"
        for char in "ఐై":
            self.trans[char] = "ai"
        for char in "ఒొ":
            self.trans[char] = "o"
        for char in "ఓో":
            self.trans[char] = "oo"
        for char in "ఔౌ":
            self.trans[char] = "au"
        self.trans["ం"] = "'"
        self.trans["ః"] = '"'
        self.trans["క"] = "k"
        self.trans["ఖ"] = "kh"
        self.trans["గ"] = "g"
        self.trans["ఘ"] = "gh"
        self.trans["ఙ"] = "ng"
        self.trans["చ"] = "ts"
        self.trans["ఛ"] = "tsh"
        self.trans["జ"] = "j"
        self.trans["ఝ"] = "jh"
        self.trans["ఞ"] = "ñ"
        for char in "టత":
            self.trans[char] = "t"
        for char in "ఠథ":
            self.trans[char] = "th"
        for char in "డద":
            self.trans[char] = "d"
        for char in "ఢధ":
            self.trans[char] = "dh"
        for char in "ణన":
            self.trans[char] = "n"
        self.trans["ప"] = "p"
        self.trans["ఫ"] = "ph"
        self.trans["బ"] = "b"
        self.trans["భ"] = "bh"
        self.trans["మ"] = "m"
        self.trans["య"] = "y"
        for char in "రఱ":
            self.trans[char] = "r"
        for char in "లళ":
            self.trans[char] = "l"
        self.trans["వ"] = "v"
        self.trans["శ"] = "sh"
        for char in "షస":
            self.trans[char] = "s"
        self.trans["హ"] = "h"
        self.trans["్"] = ""
        for char in "ంఁ":
            self.trans[char] = "^"
        self.trans["ః"] = "-"
        self.trans["౦"] = "0"
        self.trans["౧"] = "1"
        self.trans["౨"] = "2"
        self.trans["౩"] = "3"
        self.trans["౪"] = "4"
        self.trans["౫"] = "5"
        self.trans["౬"] = "6"
        self.trans["౭"] = "7"
        self.trans["౮"] = "8"
        self.trans["౯"] = "9"
        self.trans["౹"] = "1/4"
        self.trans["౺"] = "1/2"
        self.trans["౻"] = "3/4"
        self.trans["౼"] = "1/16"
        self.trans["౽"] = "1/8"
        self.trans["౾"] = "3/16"
        # Lao - note: pronounciation in initial position is used;
        # different pronounciation in final position is ignored
        self.trans["ກ"] = "k"
        for char in "ຂຄ":
            self.trans[char] = "kh"
        self.trans["ງ"] = "ng"
        self.trans["ຈ"] = "ch"
        for char in "ສຊ":
            self.trans[char] = "s"
        self.trans["ຍ"] = "ny"
        self.trans["ດ"] = "d"
        self.trans["ຕ"] = "t"
        for char in "ຖທ":
            self.trans[char] = "th"
        self.trans["ນ"] = "n"
        self.trans["ບ"] = "b"
        self.trans["ປ"] = "p"
        for char in "ຜພ":
            self.trans[char] = "ph"
        for char in "ຝຟ":
            self.trans[char] = "f"
        for char in "ມໝ":
            self.trans[char] = "m"
        self.trans["ຢ"] = "y"
        for char in "ຣຼ":
            self.trans[char] = "r"
        for char in "ລຼ":
            self.trans[char] = "l"
        self.trans["ວ"] = "v"
        for char in "ຮ":
            self.trans[char] = "h"
        self.trans["ອ"] = "'"
        for char in "ະັ":
            self.trans[char] = "a"
        self.trans["ິ"] = "i"
        self.trans["ຶ"] = "ue"
        self.trans["ຸ"] = "u"
        self.trans["ເ"] = "é"
        self.trans["ແ"] = "è"
        for char in "ໂົາໍ":
            self.trans[char] = "o"
        self.trans["ຽ"] = "ia"
        self.trans["ເຶ"] = "uea"
        self.trans["ຍ"] = "i"
        for char in "ໄໃ":
            self.trans[char] = "ai"
        self.trans["ຳ"] = "am"
        self.trans["າ"] = "aa"
        self.trans["ີ"] = "ii"
        self.trans["ື"] = "yy"
        self.trans["ູ"] = "uu"
        self.trans["ເ"] = "e"
        self.trans["ແ"] = "ei"
        self.trans["໐"] = "0"
        self.trans["໑"] = "1"
        self.trans["໒"] = "2"
        self.trans["໓"] = "3"
        self.trans["໔"] = "4"
        self.trans["໕"] = "5"
        self.trans["໖"] = "6"
        self.trans["໗"] = "7"
        self.trans["໘"] = "8"
        self.trans["໙"] = "9"
        # from: http://www.wikidata.org/wiki/MediaWiki:Gadget-SimpleTransliterate.js
        self.trans["ଂ"] = "anusvara"
        self.trans["ઇ"] = "i"
        self.trans["എ"] = "e"
        self.trans["ગ"] = "ga"
        self.trans["ਜ"] = "ja"
        self.trans["ഞ"] = "nya"
        self.trans["ଢ"] = "ddha"
        self.trans["ધ"] = "dha"
        self.trans["ਬ"] = "ba"
        self.trans["മ"] = "ma"
        self.trans["ଲ"] = "la"
        self.trans["ષ"] = "ssa"
        self.trans["਼"] = "nukta"
        self.trans["ാ"] = "aa"
        self.trans["ୂ"] = "uu"
        self.trans["ે"] = "e"
        self.trans["ੌ"] = "au"
        self.trans["ൎ"] = "reph"
        self.trans["ੜ"] = "rra"
        self.trans["՞"] = "?"
        self.trans["ୢ"] = "l"
        self.trans["૧"] = "1"
        self.trans["੬"] = "6"
        self.trans["൮"] = "8"
        self.trans["୲"] = "quarter"
        self.trans["ൾ"] = "ll"
        self.trans["ਇ"] = "i"
        self.trans["ഉ"] = "u"
        self.trans["ઌ"] = "l"
        self.trans["ਗ"] = "ga"
        self.trans["ങ"] = "nga"
        self.trans["ଝ"] = "jha"
        self.trans["જ"] = "ja"
        self.trans["؟"] = "?"
        self.trans["ਧ"] = "dha"
        self.trans["ഩ"] = "nnna"
        self.trans["ଭ"] = "bha"
        self.trans["બ"] = "ba"
        self.trans["ഹ"] = "ha"
        self.trans["ଽ"] = "avagraha"
        self.trans["઼"] = "nukta"
        self.trans["ੇ"] = "ee"
        self.trans["୍"] = "virama"
        self.trans["ૌ"] = "au"
        self.trans["੧"] = "1"
        self.trans["൩"] = "3"
        self.trans["୭"] = "7"
        self.trans["૬"] = "6"
        self.trans["൹"] = "mark"
        self.trans["ਖ਼"] = "khha"
        self.trans["ਂ"] = "bindi"
        self.trans["ഈ"] = "ii"
        self.trans["ઍ"] = "e"
        self.trans["ଌ"] = "l"
        self.trans["ഘ"] = "gha"
        self.trans["ઝ"] = "jha"
        self.trans["ଡ଼"] = "rra"
        self.trans["ਢ"] = "ddha"
        self.trans["ന"] = "na"
        self.trans["ભ"] = "bha"
        self.trans["ବ"] = "ba"
        self.trans["ਲ"] = "la"
        self.trans["സ"] = "sa"
        self.trans["ઽ"] = "avagraha"
        self.trans["଼"] = "nukta"
        self.trans["ੂ"] = "uu"
        self.trans["ൈ"] = "ai"
        self.trans["્"] = "virama"
        self.trans["ୌ"] = "au"
        self.trans["൨"] = "2"
        self.trans["૭"] = "7"
        self.trans["୬"] = "6"
        self.trans["ੲ"] = "iri"
        self.trans["ഃ"] = "visarga"
        self.trans["ં"] = "anusvara"
        self.trans["ଇ"] = "i"
        self.trans["ഓ"] = "oo"
        self.trans["ଗ"] = "ga"
        self.trans["ਝ"] = "jha"
        self.trans["？"] = "?"
        self.trans["ണ"] = "nna"
        self.trans["ઢ"] = "ddha"
        self.trans["ଧ"] = "dha"
        self.trans["ਭ"] = "bha"
        self.trans["ള"] = "lla"
        self.trans["લ"] = "la"
        self.trans["ଷ"] = "ssa"
        self.trans["ൃ"] = "r"
        self.trans["ૂ"] = "uu"
        self.trans["େ"] = "e"
        self.trans["੍"] = "virama"
        self.trans["ୗ"] = "mark"
        self.trans["ൣ"] = "ll"
        self.trans["ૢ"] = "l"
        self.trans["୧"] = "1"
        self.trans["੭"] = "7"
        self.trans["൳"] = "1/4"
        self.trans["୷"] = "sixteenths"
        self.trans["ଆ"] = "aa"
        self.trans["ઋ"] = "r"
        self.trans["ഊ"] = "uu"
        self.trans["ਐ"] = "ai"
        self.trans["ଖ"] = "kha"
        self.trans["છ"] = "cha"
        self.trans["ച"] = "ca"
        self.trans["ਠ"] = "ttha"
        self.trans["ଦ"] = "da"
        self.trans["ફ"] = "pha"
        self.trans["പ"] = "pa"
        self.trans["ਰ"] = "ra"
        self.trans["ଶ"] = "sha"
        self.trans["ഺ"] = "ttta"
        self.trans["ੀ"] = "ii"
        self.trans["ો"] = "o"
        self.trans["ൊ"] = "o"
        self.trans["ୖ"] = "mark"
        self.trans["୦"] = "0"
        self.trans["૫"] = "5"
        self.trans["൪"] = "4"
        self.trans["ੰ"] = "tippi"
        self.trans["୶"] = "eighth"
        self.trans["ൺ"] = "nn"
        self.trans["ଁ"] = "candrabindu"
        self.trans["അ"] = "a"
        self.trans["ઐ"] = "ai"
        self.trans["ക"] = "ka"
        self.trans["ਸ਼"] = "sha"
        self.trans["ਛ"] = "cha"
        self.trans["ଡ"] = "dda"
        self.trans["ઠ"] = "ttha"
        self.trans["ഥ"] = "tha"
        self.trans["ਫ"] = "pha"
        self.trans["ર"] = "ra"
        self.trans["വ"] = "va"
        self.trans["ୁ"] = "u"
        self.trans["ી"] = "ii"
        self.trans["ੋ"] = "oo"
        self.trans["ૐ"] = "om"
        self.trans["ୡ"] = "ll"
        self.trans["ૠ"] = "rr"
        self.trans["੫"] = "5"
        self.trans["ୱ"] = "wa"
        self.trans["૰"] = "sign"
        self.trans["൵"] = "quarters"
        self.trans["ਫ਼"] = "fa"
        self.trans["ઁ"] = "candrabindu"
        self.trans["ਆ"] = "aa"
        self.trans["ઑ"] = "o"
        self.trans["ଐ"] = "ai"
        self.trans["ഔ"] = "au"
        self.trans["ਖ"] = "kha"
        self.trans["ડ"] = "dda"
        self.trans["ଠ"] = "ttha"
        self.trans["ത"] = "ta"
        self.trans["ਦ"] = "da"
        self.trans["ର"] = "ra"
        self.trans["ഴ"] = "llla"
        self.trans["ુ"] = "u"
        self.trans["ୀ"] = "ii"
        self.trans["ൄ"] = "rr"
        self.trans["ૡ"] = "ll"
        self.trans["ୠ"] = "rr"
        self.trans["੦"] = "0"
        self.trans["૱"] = "sign"
        self.trans["୰"] = "isshar"
        self.trans["൴"] = "1/2"
        self.trans["ਁ"] = "bindi"
        self.trans["આ"] = "aa"
        self.trans["ଋ"] = "r"
        self.trans["ഏ"] = "ee"
        self.trans["ખ"] = "kha"
        self.trans["ଛ"] = "cha"
        self.trans["ട"] = "tta"
        self.trans["ਡ"] = "dda"
        self.trans["દ"] = "da"
        self.trans["ଫ"] = "pha"
        self.trans["യ"] = "ya"
        self.trans["શ"] = "sha"
        self.trans["ി"] = "i"
        self.trans["ੁ"] = "u"
        self.trans["ୋ"] = "o"
        self.trans["ੑ"] = "udaat"
        self.trans["૦"] = "0"
        self.trans["୫"] = "5"
        self.trans["൯"] = "9"
        self.trans["ੱ"] = "addak"
        self.trans["ൿ"] = "k"
        self.trans["ആ"] = "aa"
        self.trans["ଊ"] = "uu"
        self.trans["એ"] = "e"
        self.trans["ਔ"] = "au"
        self.trans["ഖ"] = "kha"
        self.trans["ଚ"] = "ca"
        self.trans["ટ"] = "tta"
        self.trans["ਤ"] = "ta"
        self.trans["ദ"] = "da"
        self.trans["ପ"] = "pa"
        self.trans["ય"] = "ya"
        self.trans["ശ"] = "sha"
        self.trans["િ"] = "i"
        self.trans["െ"] = "e"
        self.trans["൦"] = "0"
        self.trans["୪"] = "4"
        self.trans["૯"] = "9"
        self.trans["ੴ"] = "onkar"
        self.trans["ଅ"] = "a"
        self.trans["ਏ"] = "ee"
        self.trans["କ"] = "ka"
        self.trans["ઔ"] = "au"
        self.trans["ਟ"] = "tta"
        self.trans["ഡ"] = "dda"
        self.trans["ଥ"] = "tha"
        self.trans["ત"] = "ta"
        self.trans["ਯ"] = "ya"
        self.trans["റ"] = "rra"
        self.trans["ଵ"] = "va"
        self.trans["ਿ"] = "i"
        self.trans["ു"] = "u"
        self.trans["ૄ"] = "rr"
        self.trans["ൡ"] = "ll"
        self.trans["੯"] = "9"
        self.trans["൱"] = "100"
        self.trans["୵"] = "sixteenth"
        self.trans["અ"] = "a"
        self.trans["ਊ"] = "uu"
        self.trans["ഐ"] = "ai"
        self.trans["ક"] = "ka"
        self.trans["ଔ"] = "au"
        self.trans["ਚ"] = "ca"
        self.trans["ഠ"] = "ttha"
        self.trans["થ"] = "tha"
        self.trans["ତ"] = "ta"
        self.trans["ਪ"] = "pa"
        self.trans["ര"] = "ra"
        self.trans["વ"] = "va"
        self.trans["ീ"] = "ii"
        self.trans["ૅ"] = "e"
        self.trans["ୄ"] = "rr"
        self.trans["ൠ"] = "rr"
        self.trans["ਜ਼"] = "za"
        self.trans["੪"] = "4"
        self.trans["൰"] = "10"
        self.trans["୴"] = "quarters"
        self.trans["ਅ"] = "a"
        self.trans["ഋ"] = "r"
        self.trans["ઊ"] = "uu"
        self.trans["ଏ"] = "e"
        self.trans["ਕ"] = "ka"
        self.trans["ഛ"] = "cha"
        self.trans["ચ"] = "ca"
        self.trans["ଟ"] = "tta"
        self.trans["ਥ"] = "tha"
        self.trans["ഫ"] = "pha"
        self.trans["પ"] = "pa"
        self.trans["ଯ"] = "ya"
        self.trans["ਵ"] = "va"
        self.trans["ି"] = "i"
        self.trans["ോ"] = "oo"
        self.trans["ୟ"] = "yya"
        self.trans["൫"] = "5"
        self.trans["૪"] = "4"
        self.trans["୯"] = "9"
        self.trans["ੵ"] = "yakash"
        self.trans["ൻ"] = "n"
        self.trans["ઃ"] = "visarga"
        self.trans["ം"] = "anusvara"
        self.trans["ਈ"] = "ii"
        self.trans["ઓ"] = "o"
        self.trans["ഒ"] = "o"
        self.trans["ਘ"] = "gha"
        self.trans["ଞ"] = "nya"
        self.trans["ણ"] = "nna"
        self.trans["ഢ"] = "ddha"
        self.trans["ਲ਼"] = "lla"
        self.trans["ਨ"] = "na"
        self.trans["ମ"] = "ma"
        self.trans["ળ"] = "lla"
        self.trans["ല"] = "la"
        self.trans["ਸ"] = "sa"
        self.trans["¿"] = "?"
        self.trans["ା"] = "aa"
        self.trans["ૃ"] = "r"
        self.trans["ൂ"] = "uu"
        self.trans["ੈ"] = "ai"
        self.trans["ૣ"] = "ll"
        self.trans["ൢ"] = "l"
        self.trans["੨"] = "2"
        self.trans["୮"] = "8"
        self.trans["൲"] = "1000"
        self.trans["ਃ"] = "visarga"
        self.trans["ଉ"] = "u"
        self.trans["ઈ"] = "ii"
        self.trans["ਓ"] = "oo"
        self.trans["ଙ"] = "nga"
        self.trans["ઘ"] = "gha"
        self.trans["ഝ"] = "jha"
        self.trans["ਣ"] = "nna"
        self.trans["ન"] = "na"
        self.trans["ഭ"] = "bha"
        self.trans["ଜ"] = "ja"
        self.trans["ହ"] = "ha"
        self.trans["સ"] = "sa"
        self.trans["ഽ"] = "avagraha"
        self.trans["ૈ"] = "ai"
        self.trans["്"] = "virama"
        self.trans["୩"] = "3"
        self.trans["૨"] = "2"
        self.trans["൭"] = "7"
        self.trans["ੳ"] = "ura"
        self.trans["ൽ"] = "l"
        self.trans["ઉ"] = "u"
        self.trans["ଈ"] = "ii"
        self.trans["ഌ"] = "l"
        self.trans["ઙ"] = "nga"
        self.trans["ଘ"] = "gha"
        self.trans["ജ"] = "ja"
        self.trans["ਞ"] = "nya"
        self.trans["ନ"] = "na"
        self.trans["ബ"] = "ba"
        self.trans["ਮ"] = "ma"
        self.trans["હ"] = "ha"
        self.trans["ସ"] = "sa"
        self.trans["ਾ"] = "aa"
        self.trans["ૉ"] = "o"
        self.trans["ୈ"] = "ai"
        self.trans["ൌ"] = "au"
        self.trans["૩"] = "3"
        self.trans["୨"] = "2"
        self.trans["൬"] = "6"
        self.trans["੮"] = "8"
        self.trans["ർ"] = "rr"
        self.trans["ଃ"] = "visarga"
        self.trans["ഇ"] = "i"
        self.trans["ਉ"] = "u"
        self.trans["ଓ"] = "o"
        self.trans["ഗ"] = "ga"
        self.trans["ਙ"] = "nga"
        self.trans["ઞ"] = "nya"
        self.trans["ଣ"] = "nna"
        self.trans["ധ"] = "dha"
        self.trans["મ"] = "ma"
        self.trans["ଳ"] = "lla"
        self.trans["ഷ"] = "ssa"
        self.trans["ਹ"] = "ha"
        self.trans["ਗ਼"] = "ghha"
        self.trans["ા"] = "aa"
        self.trans["ୃ"] = "r"
        self.trans["േ"] = "ee"
        self.trans["ൗ"] = "mark"
        self.trans["ଢ଼"] = "rha"
        self.trans["ୣ"] = "ll"
        self.trans["൧"] = "1"
        self.trans["੩"] = "3"
        self.trans["૮"] = "8"
        self.trans["୳"] = "half"
        for char in self.trans:
            value = self.trans[char]
            if value == "?":
                continue
            while value.encode(encoding, 'replace').decode(encoding) == "?" and value in self.trans:
                assert value != self.trans[value], "%r == self.trans[%r]!" % (value, value)
                value = self.trans[value]
            self.trans[char] = value

    def transliterate(self, char, default="?", prev="-", next="-"):
        if char in self.trans:
            return self.trans[char]
        #Arabic
        if char == "◌":
            return prev
        #Japanese
        if char == "ッ":
            return self.transliterate(next)[0]
        if char in "々仝ヽヾゝゞ〱〲〳〵〴〵":
            return prev
        #Lao
        if char == "ຫ":
            if next in "ງຍນຣລຼຼວ":
                return ""
            else:
                return "h"
        return default
