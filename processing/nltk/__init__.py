import nltk
from pywikibot.families.wikipedia_family import Family as WikipediaFamily
from pywikibot.page import Page
#from pywikibot.site.base import BaseSite as Site
from pywikibot.site.apisite import APISite as Site
from pywikibot.bot import debug
import os 

def page(name):
    enwiki = Site("en", WikipediaFamily())
    p = Page(enwiki, name)

#    data = enwiki.loadrevisions(p, getText=True)

    data = p.get()
    #print("Data:%s" % data)
    return data
    #link = Link(u"Kosovo", self.enwiki)

def extract_entity_names(t, depth=0):
    entity_names = []
    #    if hasattr(t, 'label') and t.label():
    #        print ("Label:%s" % t.label())
    sep = "|" * depth
    for child in t:

        if isinstance(child, nltk.tree.Tree):
            entity_names.extend( 
                extract_entity_names(
                    child,
                    depth=+1
                )
            )

        elif isinstance(child, tuple):
            if len(child) == 1:
                entity_names.append(
                    child[0][0]
                )
            else:
#                print ("type:%s" % type(child))
#                print ("dir:%s" % dir(child))
                print ("%s child:%s" % (sep, str(child)))
        else :
            print ("%s child:%s" % (sep, str(child)))

        #for child2 in child:
        #print ("child2:%s" % str(child2))
          
#        if t.node == 'NE':

#        else:
#            for child in t:
#                entity_names.extend(extract_entity_names(child))
    return entity_names


def process_text(sample):
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.batch_ne_chunk(tagged_sentences)
  
    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)
        entity_names.extend(extract_entity_names(tree))
 
    # Print all entity names
#    print (entity_names)
 
    # Print unique entity names
    debug ("RESULT %s " % str(set(entity_names)).encode("utf-8"))
    return entity_names



def parse_page(name):
    print ("processing %s" % name)
    filename="data/%s.wiki" % name
    if not os.path.exists(filename):
        sample = page(name)
        of  = open(filename, 'wb')
        of.write(sample.encode("utf-8"))
    else:
        of  = open(filename, 'rb')
        sample = of.read().decode("utf-8")
    of.close
    return process_text(sample)
