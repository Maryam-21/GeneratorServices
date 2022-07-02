import spacy
import ServicesModule.data as data
import yake

nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])
stopwords = set(w.rstrip() for w in open('ServicesModule/stopwords.txt'))

def getServices(text):

    servicesdetails = {}                                            #dictionary for different services and their details
    servicesdetails2 = {}                                           #dictionary for different services and their details with a unique title and several details
    sentsOnly = []
    kw_extractor = yake.KeywordExtractor(top=1, stopwords=stopwords)
    
    for t in text:                                                 #loop through the sentences generated by markov chains
        services = []                                              #list for services
        info = subjectverbobjectrule(t)                            #get information extracted from sentence t

        if len(info) != 0:
            for sent in info:
                duplicate = 0
                for v in servicesdetails.values():                #check if info was already extracted
                    if sent in v:
                        duplicate = 1
                        break
                if(not duplicate):
                    if sent:
                        services.append(sent)                        #add new service

            if len(services) != 0:
                sentsOnly.append(t)
                servicesdetails[t] = services
                keywords = kw_extractor.extract_keywords(t)
                if keywords[0][0] in servicesdetails2.keys():
                        servicesdetails2[keywords[0][0]].append(t)
                else:
                    servicesdetails2[keywords[0][0]]= [t]

    return servicesdetails2



def subjectverbobjectrule(text):
    doc = nlp(text)
    sent = []

    for token in doc:
        # if the token is a verb
        index = 0
        if token.pos_ == 'VERB' or token.pos_ == 'AUX':
            phrase = token.text
            # only extract noun or pronoun subjects        
            for subtok in token.rights:
                if phrase:
                    # save the object in the phrase
                    if (subtok.dep_ in ['dobj','attr','prep']) and (subtok.pos_ in ['NOUN', 'PROPN','ADP']):
                        index = subtok.i
                        if adjectiveNounRule(text,index):
                            phrase += adjectiveNounRule(text,index) + ' ' + subtok.text
                        elif subtok.pos_ == 'ADP':
                            phrase = prepositionsRule(subtok.i,text)
                        else:
                            phrase += ' ' + subtok.text
                        for sub_tok in token.lefts:
                            if (sub_tok.dep_ in ['nsubj', 'nsubjpass']) and (sub_tok.pos_ in ['NOUN', 'PROPN', 'PRON']):
                                # add subject to the phrase
                                if phrase:
                                    phrase = sub_tok.text + " " + phrase


                        sent.append(phrase)

    return sent

def adjectiveNounRule(text, index):
    doc = nlp(text)

    phrase = ''

    for token in doc:

        if token.i == index:
            for subtoken in token.children:
                if (subtoken.pos_ == 'ADJ'):
                    phrase += ' ' + subtoken.text
            break

    return phrase


def prepositionsRule(index,text):
    doc = nlp(text)
    token = doc[index]
    sent = []

    # look for prepositions
    phrase = ''

    # if its head word is a noun
    if token.head.pos_ in ['NOUN', 'PROPN','VERB']:

        # append noun and preposition to phrase
        phrase += token.head.text
        phrase += ' ' + token.text

        # check the nodes to the right of the preposition
        for right_tok in token.rights:
            # append if it is a noun or proper noun
            if (right_tok.dep_ == 'pobj'):
                phrase += ' ' + right_tok.text

        if len(phrase) > 2:
           return phrase
