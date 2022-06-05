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

#upload audio
@app.route("/asr/upload", methods=['POST'])
def upload_to_cloud():
    filepath = request.json['filepath']
    filename = request.json['filename']
    return asr.upload_to_cloud(filepath, filename)

#get_meetingscript
@app.route("/meetingscript", methods=['POST'])
def get_meeting_script():
    filepath = request.json['filepath']
    p = request.json["projectTitle"]
    d = request.json["domain"]
    a = request.json["actors"]
    m = request.json["meetingTitle"]
    id = 7#request.json["meetingID"]
    frame_rate = asr.upload_to_cloud(filepath)
    #filepath = "ASRModule/audio_wav/spotify_meeting.wav"  # ex. "ASRModule/audio_wav/batoul_meeting.wav"
    #frame_rate = fb.getFrameRate(id)
    result = asr.getSpeechToText(filepath, frame_rate, p, d, a, m)
    print(result)
    timeStamps = {
        'meetingTitle': m,
        'timeStamps': result['sentsTimeStamp']
    }

    txtTimeStamps = json.dumps(timeStamps, sort_keys=True,
                                indent=4, separators=(',', ': '))
    f = open('Firebase/Transcripts.json', "a")
    f.write(txtTimeStamps)
    f.close()
    fb.setTranscripts()
    response = result['transcript']
    return response

#get Services
@app.route("/services", methods=['POST','GET'])
def get_services():
    meetingscript = request.json['meetingscript']
    actors = request.json['actors']
    meetingTitle = request.json['meetingTitle']
    #projectID = request.json['projectID']
    firebaseID = meetingTitle
    timeStamps = fb.getTranscripts(firebaseID)
    return json.dumps(sds.do(meetingscript, actors, timeStamps))

#get stories
@app.route("/userstories", methods=['POST'])
def get_user_stories():
    services = request.json['services']
    filepath = request.json['filepath']
    if filepath:
        print(services)
        frame_rate = asr.upload_to_cloud(filepath)
        result = asr.getSpeechToText(filepath, frame_rate)
        return json.dumps(uss.getUserStories(services, result))
    print(services)
    resp = json.dumps(uss.getUserStories(services))
    print(resp)
    return resp

if __name__ =="__main__":
    app.run(debug=True)