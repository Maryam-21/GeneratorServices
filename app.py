from flask import Flask
from flask import request
from ASRModule import ASRService as asr
from ServicesModule import ServiceDetailsService as sds
from UserStoriesModule import UserStoriesService as uss
import json

app = Flask(__name__)

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
    filepath = request.json['filepath']     #"ASRModule/audio_wav/batoul_meeting.wav"
    response = json.dumps(asr.convert(filepath),indent=4)
    return response

#get services
#request should include meeting script and actors
#json : {
#         'meetingscript': "",
#         'actors': ['x','y','z']
#        }
@app.route("/services", methods=['POST'])
def get_services():
    meetingscript = request.json['meetingscript']
    actors = request.json['actors']
    response = json.dumps(sds.do(meetingscript,actors), indent=4)
    return response

#get stories
@app.route("/userstories", methods=['POST'])
def get_user_stories():
    return uss.test()


if __name__ =="__main__":
    app.run(debug=True)