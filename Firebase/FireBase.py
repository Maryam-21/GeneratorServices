import firebase_admin
from firebase_admin import db
import json

cred_obj = firebase_admin.credentials.Certificate('./Firebase/baia-temp-95d76-firebase-adminsdk-mto5s-14cd82f0ab.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://baia-temp-95d76-default-rtdb.europe-west1.firebasedatabase.app/'
	})


def setTranscripts():
	ref = db.reference("/Stamps")

	with open("./Firebase/Transcripts.json", "r") as f:
		file_contents = json.load(f)
	ref.push(file_contents)
	#important Note

	#-----------
	#delete Transcript content after pushing
	open('./Firebase/Transcripts.json', 'w').close()

def getTranscripts(MeetingID):
	ref = db.reference("/Stamps")
	stamps = ref.order_by_child("meetingID").equal_to(MeetingID).get()
	return stamps #type of stamps (OrderedDictionary)
