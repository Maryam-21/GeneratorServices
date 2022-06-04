import spacy

nlp = spacy.load("en_core_web_sm")

def AssignTimestamps(servicesdetails, stamps):
    minscore = 0.5
    out = {}
    for serviceKey in servicesdetails:  # Single Service
        for sent in servicesdetails[serviceKey]:  # Markov sentence
            similaritylist = []
            sent1 = nlp(sent)
            max = 0 
            index = 0
            for eachstamp in stamps:
                sent2 = nlp(eachstamp[0])
                similaritylist.append(sent1.similarity(sent2))
                if max < sent1.similarity(sent2) and sent1.similarity(sent2) >= minscore:
                    index = eachstamp[1]
                    max = sent1.similarity(sent2)
            if serviceKey in out.keys():
                out[serviceKey].append({
                "ServiceDetailString" : sent,
                "Timestamp" : str(index)
            })
            else:
                out[serviceKey] = [{
                "ServiceDetailString" : sent,
                "Timestamp" : str(index)
            }]
    payload = []
    for t in out.keys():
        payload.append({
            "serviceTitle": t,
            "serviceDetails": out[t]
        })
    print(payload)
    return payload