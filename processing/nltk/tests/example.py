u'''
from https://gist.github.com/322906/90dea659c04570757cccf0ce1e6d26c9d06f9283
'''

import nltk
from pywikibot.families.wikipedia_family import Family as WikipediaFamily
from pywikibot.page import Page
#from pywikibot.site.base import BaseSite as Site
from pywikibot.site.apisite import APISite as Site

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
    print (set(entity_names))

parse_page("Kosovo")
