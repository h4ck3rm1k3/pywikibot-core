u'''
from https://gist.github.com/322906/90dea659c04570757cccf0ce1e6d26c9d06f9283
'''

import nltk
from pywikibot.families.wikipedia_family import Family as WikipediaFamily
from pywikibot.page import Page
#from pywikibot.site.base import BaseSite as Site
from pywikibot.site.apisite import APISite as Site
from pywikibot.bot import debug
def page(name):
    enwiki = Site("en", WikipediaFamily())
    p = Page(enwiki, name)

#    data = enwiki.loadrevisions(p, getText=True)

    data = p.get()
    #print("Data:%s" % data)
    return data
    #link = Link(u"Kosovo", self.enwiki)

def extract_entity_names(t):
    entity_names = []
    #    if hasattr(t, 'label') and t.label():
    #        print ("Label:%s" % t.label())
    
    for child in t:

        if len(child) == 1:
            entity_names.append(
                child[0][0]
            )
            #print ("child:%s" % str(child))

        #for child2 in child:
        #print ("child2:%s" % str(child2))
          

#        if t.node == 'NE':

#        else:
#            for child in t:
#                entity_names.extend(extract_entity_names(child))
    return entity_names

def parse_page(name):
    sample = page(name)
#    sample = "this is a test. that is a dog. that is Kosovo."
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.batch_ne_chunk(tagged_sentences, binary=True)
    
    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)
        entity_names.extend(extract_entity_names(tree))
 
    # Print all entity names
#    print (entity_names)
 
    # Print unique entity names
    debug ("RESULT %s " % str(set(entity_names)).encode("utf-8"))



parse_page("Kosovo")

    # example output
entities = {'Refugees', 'Ramesh', 'Howard', 'Society', 'Eagle', 'Frederick', 'Eurasian', 'Statistics', 'Assembly', 'SFRY', 'Mines', 'Montenegro', 'Bosnian', '\xc4\x90eravica', 'Skopje', 'Balkans', 'SANU', 'Conflict', 'Trial', 'Christian', 'Ottoman', 'Jenny', 'Organization', 'Kemalist', 'North', 'Merlot', 'EconMin', 'Ottomans', 'Vardar', 'Lanham', 'Middle', 'Euro', 'Scranton', 'Axis', 'Western', 'Troika', '\xc5\xbdidas', 'Merkel', 'Illyrian', 'Dyrrachium', 'Carol', 'OSCE', 'Belgrade', 'KLA', 'Turkey', 'China', 'Rome', 'Nazi', 'Reversal', 'Russian', '\xd0\x9a\xd0\xbe\xd1\x81\xd0\xbc\xd0\xb5\xd1\x82', 'Serbian', 'Sand\xc5\xbeak', '\xd0\x9a\xd0\xbe\xd1\x81\xd0\xbe\xd0\xb2\xd0\xbe', 'World', 'Wilkes', 'German', 'Germany', 'Martin', 'Craig', 'Roma', 'Indiana', 'Paris', 'France', 'English', 'Publisher', 'Banac', 'Pluto', 'EULEX', 'COMMITTEE', 'FDI', 'EU', 'Slavs', 'Children', 'Jill', 'Census', 'Hungarian', 'RSD', 'Slovenes', 'CIA', 'Austria', 'Slavic', 'Romani', 'Italian', 'NATO', 'Balkan', 'People', 'Kosova', 'KPEC', 'Yugoslavia', 'Routledge', 'Kosovo', 'Bloomington', 'League', 'International', 'LDK', 'Dukagjini', 'Communist', 'SOEs', 'longEW', 'Historian', 'Abdul', 'IDPs', 'UNODC', 'Ashkali', 'Drugs', 'Dayton', 'Islamification', 'Security', 'Moesians', 'Fatos', 'Carole', 'London', 'Dardanians', 'UK', 'Greek', 'Kosovar', 'Illyria', 'Herzegovina', 'Nemanja', 'Bulgarian', 'IMMEDIATE', 'Albanians', 'Roman', 'Independence', 'Croat', 'Lausanne', 'Macedonia', 'Europe', 'US', 'Robert', 'Croatia', 'Milo\xc5\xa1evi\xc4\x87', 'Geneva', 'Byzantine', 'Anscombe', 'Minerals', 'Kosovan', 'GDP_nominal_per_capita', 'Australia', 'MooreD', 'European', 'Gorani', 'Pec', 'Zeta', 'Sar', 'Serb', 'UNMIK', 'Kratovo', '\xc4\x90akovica', 'Russia', 'Strasbourg', 'Slovenians', 'Countries', 'Collaboration', 'Page', 'Ted', 'Metohija', 'Kingdom', 'Berberi\xc5\xa1te', 'httpEnvelopes', 'Croats', 'Ahtisaari', 'Guardian', 'Empire', 'USCRI', 'Romania', 'Clinton', 'Zagreb', 'Pe\xc4\x87', 'Mass', 'Le\xc5\xa1ak', 'Islamicisation', 'Pristina', 'Deutschmark', 'Trepca', 'Turk', 'Bala', 'Multimedia', 'Sally', 'Denis', 'Dancer', 'Territory', 'Bitola', 'Hupchik', 'Greeks', 'Sabrina', 'Study', 'Prizren', 'Yugoslav', 'Justice', 'Prishtina', 'Montenegrin', 'Weight', 'Monaco', 'Reference', 'Bulgaria', 'Ayd\xc4\xb1n', 'Turdus', 'Vol', 'Economy', 'Marc', 'Inflation', 'PDK', 'Chicago', 'Bosnia', 'Thakur', 'Milutinovic', 'UN', 'Harsh', 'AAK', 'Sciences', 'Italy', 'Bosnians', 'Brankovi\xc4\x87', 'Committee', 'Ashkaelia', 'Vra\xc4\x8devo', 'IBAN', '\xc4\x8cu\xc5\xa1ka', 'ICJ', 'March', 'Linguistics', 'Whilst', 'Know', 'Musliu', 'Lazar', 'Milosevic', 'Slovene', 'Basingstoke', 'Tha\xc3\xa7i', 'Autariatae', 'USAID', 'GDP_nominal_rank', 'Croatian', 'Commerce', 'Switzerland', 'Albrecht', 'Taiwan', 'Muslim', 'Malcolm', 'ARBITRATION', 'Yugoslavian', 'IDMC', 'NEVER', 'Morava', 'Nerodimka', 'Kosovska', 'Catholic', 'Arts', 'GDP_PPP_per_capita', 'Limaj', 'Kruje', 'II', 'Lezh\xc3\xab', 'Bank', 'Upon', 'Pennsylvania', 'Stojiljkovi\xc4\x87', 'EUR', 'Pri\xc5\xa1tina', 'Law', 'Adriatic', 'Poland', '\xc3\x9csk\xc3\xbcp', 'Turks', 'Caution', 'Vlachs', 'Prishtin\xc3\xab', 'Kosovars', 'Canadian', 'Culture', 'Rankovi\xc4\x87', 'IMF', 'July', 'Methodist', 'Alexiade', '\xc3\x81lvaro', 'Yemen', 'Vojvodina', 'Islam', 'Interior', 'Byzantines', 'Zica', 'Albania', 'Turkish', 'University', 'GDP_nominal_per_capita_rank', 'VERY', 'Albanian', 'GDP_PPP', 'Union', 'Immigrants', 'Goljak', 'Please', 'Slovenia', 'Sultan', 'Ramet', 'Bosniak', 'Babuna', 'GDP', 'USCR', 'Ethnicity', 'Baldwin', 'Comparative', 'ENGAGE', 'Cambridge', 'Opinion', 'Egyptian', 'Serbs', 'Serbia', 'Noel', 'Scordisci', 'Austrian', 'Constantinople'}
