import spacy 
import regex as re

stopwords = set(w.rstrip() for w in open('stopwords.txt'))
nlp = spacy.load('en_core_web_md', disable=['ner', 'textcat'])

def getUserStories(services):
    text = open("spotify_try.txt", mode='r').read()
    text = text.lower()
    text = re.sub("[.]",'.\n',str(text))
    text = re.sub("[!?]",'?\n',str(text))
    
    services = [ 
        "user should be able to search for music by name and artist the user should be able to see the top songs played in the system",
        "user should be able to choose a specific genre from the genres available in the system for the acceptance criteria the user should be able to",
        "user should be able to search for music by name and artist the user should be able to discover music based on his profile and browse",
        "user should be able to go throw a navigation menu to be able to discover music based on his profile as well as the system should",
        "user should be able to specify whether he wants to display all results songs or artists using buttons displayed under the seach box a user should",
        "user should be registered and the artists in the results should be able to specify whether he wants to display all results in a list by",
        "user shall see the top songs if he does not have any liked songs search history and at least five recently played songs do you like",
        "user shall be able to choose to play a song or open any artists profile from the search box and by typing any input the results",
        "user shall be able to search for music by name genre or artist great do you have any liked songs search history or at least five",
        "user shall see the top songs played in the system for the acceptance criteria in each case in case of searching by name and the artists",
        "user shall see the search box and by typing any input the results should be updated the user should be able to see the search box",
        "system should keep track for users activity including activities like liked songs search history or at least five recently played songs do you like to recommed",
        "system should keep track for users activity including activities like liked songs search history and at least five recently played songs as for the acceptance criteria",
        "system shall print no matches found what about the acceptance criteria what should we consider for the acceptance criteria in each case in case of searching",
        "system shall print no matches found what about the acceptance criteria in each case in case of searching by genre the user the user should see",

        "user, manager, accountant and admin should be able to search for music by name, genre or artist",
        "user should be able to discover music based on his profile and browse the recommended songs"
    ]
    stories = []
    for s in services:
        stories.append(FormatService(s))

    row_lines = text.splitlines()
    pre = []
    acc= []
    nextp = False
    nexta = False
    
    for sent in row_lines:
        if nextp and rule_final(sent):
            nextp = False
            pre.append(sent)    
        elif sent.__contains__('preconditions'):
            if re.search("[?]", sent): 
                nextp = True
            elif rule_final(sent):
                pre.append(sent)
        
        if nexta and rule_final(sent):
            nexta = False
            acc.append(sent)
        elif sent.__contains__('acceptance criteria'):
            if re.search("[?!]", sent): 
                nexta = True
            elif rule_final(sent):
                acc.append(sent)

    # Output
    print("User stories: ")
    print(*stories, sep='\n')
    print()
    print("preconditions: ")
    print(*pre, sep='\n')
    print()
    print("acceptance criteria")
    print(*acc, sep='\n')
    return stories

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

getUserStories()