from flask import Flask
from flask_cors import CORS
from flask import request
from ASRModule import ASRService as asr
from ServicesModule import ServiceDetailsService as sds
from UserStoriesModule import UserStoriesService as uss
from Firebase import FireBase as fb
from ServicesModule import data
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "Hello World"

#get meeting script
#request should include audio file path
#json : {
#         'filepath': "ASRModule/audio_wav/batoul_meeting.wav"
#        }
@app.route("/meetingscript", methods=['POST'])
def get_meeting_script():
    filepath = request.json['filepath']
    p = request.json["projectTitle"]
    d = request.json["domain"]
    a = request.json["actors"]
    m = request.json["meetingTitle"]
    id = request.json["meetingID"]

    #filepath = "ASRModule/audio_wav/spotify_meeting.wav"  # ex. "ASRModule/audio_wav/batoul_meeting.wav"

    result = asr.getSpeechToText(filepath, p, d, a, m)

    timeStamps = {
        'meetingID': id,
        'timeStamps': result['sentsTimeStamp']
    }

    txtTimeStamps = json.dumps(timeStamps, sort_keys=True,
                                indent=4, separators=(',', ': '))
    f = open('Firebase/Transcripts.json', "a")
    f.write(txtTimeStamps)
    f.close()
    fb.setTranscripts()
    response = json.dumps(result['transcript'],indent=4)
    return response
    #return json.dumps(data.getTestData('spotify'))
    #response = json.dumps(asr.convert(filepath),indent=4)
    #return response

#get services
#request should include meeting script and actors
#json : {
#         'meetingscript': "",
#         'actors': ['x','y','z']
#        }

@app.route("/services", methods=['POST','GET'])
def get_services():
    meetingscript = request.json['meetingscript']
    actors = request.json['actors']
    meetingID = request.json['meetingID']
    timeStamps = fb.getTranscripts(meetingID)
    #print(meetingscript)
    #print(actors)
    #response = json.dumps(sds.do(meetingscript,actors), indent=4)
    #return response
    return json.dumps(sds.do(meetingscript, actors, timeStamps))

#get stories
@app.route("/userstories", methods=['POST'])
def get_user_stories():
    return uss.test()


if __name__ =="__main__":
    app.run(debug=True)