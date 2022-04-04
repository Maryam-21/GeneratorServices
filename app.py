from flask import Flask
import ASRService as asr
import ServiceDetailsService as sds
import UserStoriesService as uss

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

#get meeting script
@app.route("/meetingscript", methods=['POST'])
def get_meeting_script():
    return asr.test()

#get services
@app.route("/services", methods=['POST'])
def get_services():
    return sds.test()

#get stories
@app.route("/userstories", methods=['POST'])
def get_user_stories():
    return uss.test()

if __name__ =="__main__":
    app.run(debug=True)