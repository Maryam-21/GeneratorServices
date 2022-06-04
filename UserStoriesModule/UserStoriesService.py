import spacy 
import regex as re

stopwords = set(w.rstrip() for w in open('./ServicesModule/stopwords.txt'))
nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])

def getUserStories(services, text=''):
    stories = []
    for s in services:
        stories.append(FormatService(s))

    if text == '':
        return stories
    
    text = text.lower()
    text = re.sub("[.]",'.\n',str(text))
    text = re.sub("[!?]",'?\n',str(text))
    
    row_lines = text.splitlines()
    preconditions = []
    acceptanceCriteria = []
    nextp = False
    nexta = False
    
    for sent in row_lines:
        if nextp and rule_final(sent):
            nextp = False
            preconditions.append(sent)    
        elif sent.__contains__('preconditions'):
            if re.search("[?]", sent): 
                nextp = True
            elif rule_final(sent):
                preconditions.append(sent)
        
        if nexta and rule_final(sent):
            nexta = False
            acceptanceCriteria.append(sent)
        elif sent.__contains__('acceptance criteria'):
            if re.search("[?!]", sent): 
                nexta = True
            elif rule_final(sent):
                acceptanceCriteria.append(sent)

    '''
    # Output
    print("User stories: ")
    print(*stories, sep='\n')
    print()
    print("preconditions: ")
    print(*pre, sep='\n')
    print()
    print("acceptance criteria")
    print(*acc, sep='\n')
    '''
    result = {
        "stories": stories,
        "preconditions": preconditions,
        "acceptanceCriteria": acceptanceCriteria
    }
    return result

def FormatService(service):
    doc = nlp(service)
    phrase = 'As a'
    i = 0
    conj = False
    for token in doc:
        # Extract first noun or pronoun subjects
        if token.pos_ in ['NOUN', 'PROPN']:
            for sub_tok in token.lefts:
                phrase += sub_tok.text
                i += 1
            phrase += ' ' + token.lemma_ + ', '
            for child in token.children:
                if child.pos_ in ['NOUN', 'PROPN'] and child.text not in phrase:
                    phrase += child.text + ', '
                    conj = True
                    i += 1
                for conjunct in child.conjuncts:
                    if conjunct.text not in phrase:
                        phrase += conjunct.text + ', '
                    i += 1
            break
        i += 1
    if conj:
        phrase += 'they'
    else:
        phrase += 'I'
    
    cont = False
    for j in range(i, len(doc)):
        if cont or doc[j].pos_ in ['VERB', 'AUX']:
            cont =True
            phrase += ' ' + doc[j].text
    return phrase

def rule_final(text):
    doc = nlp(text)

    for token in doc:
        # If the token is a verb
        if token.pos_ == 'VERB' or token.pos_ == 'AUX':
            # Only extract noun or pronoun subjects
            for subtok in token.rights:
                if (subtok.dep_ in ['dobj','attr','prep']) and (subtok.pos_ in ['NOUN', 'PROPN','ADP']):
                    return "half way"
    return 0

#getUserStories()

