import ServicesModule.InformationExtraction as IE
import ServicesModule.MarkovChains as MC
import PreprocessingModule.discourse as disc
def do(meetingscript,actors):
    editedmeetingscript = disc.main(meetingscript)
    text = MC.get(editedmeetingscript,actors) #meeting script #actors
    return IE.getServices()