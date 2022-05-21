import spacy
import json
import ASRModule.ASRService as asr

nlp = spacy.load("en_core_web_sm")

def AssignTimestamps():
    servicesdetails = getServicesdetails()
    stamps = getStamps()
    minscore = 0.5
    out = {}
    for i in servicesdetails:
        print(servicesdetails[i])
        
        for j in servicesdetails[i]:  # Markov sentence
            similaritylist = []
            sent1 = nlp(j)
            max = 0 
            index = 0
            for eachstamp in stamps:
                sent2 = nlp(eachstamp[0])
                similaritylist.append(sent1.similarity(sent2))
                if max < sent1.similarity(sent2) and sent1.similarity(sent2) >= minscore:
                    index = eachstamp
                    max = sent1.similarity(sent2)
            if i in out.keys():
                out[i].append({
                "service" : j,
                "stamp" : index[1]        
            })
            else:
                out[i] = [{
                "service" : j,
                "stamp" : index[1]        
            }]
    print(out)

def getServicesdetails():  # Markov output with title
    f = open('output.json')
    servicesdetails = json.load(f)
    return servicesdetails

def getStamps():  # Sentences fetched from ASR with its timestamps
    stamps = asr.main()
    return stamps