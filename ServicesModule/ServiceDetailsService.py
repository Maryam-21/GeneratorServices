import ServicesModule.InformationExtraction as IE
import ServicesModule.MarkovChains as MC
#import PreprocessingModule.discourse as disc
import ServicesModule.AssignTimestamps as AT

def do(meetingscript, actors, timeStamps):
    #editedmeetingscript = disc.coref_resolved(meetingscript)
    sentences = MC.services(meetingscript) #meeting script #actors
    print(sentences)
    serviceDetails = IE.getServices(sentences)
    serviceDetailsStamped = AT.AssignTimestamps(serviceDetails, timeStamps)
    return sentences