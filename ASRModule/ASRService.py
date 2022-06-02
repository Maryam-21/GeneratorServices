bucketname = "meetings_audios"  # Name of the bucket created in the step before

# Import libraries
import json
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import storage
import os
import wave
import regex as re
from Firebase import FireBase as fb

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "ASRModule/credentials.json"

def getSpeechToText(audio_filename, frame_rate, projectTitle, domain, actors, meetingTitle):
    actors = actors.split(',')
    audioKeywords = ['user', 'system', projectTitle, domain, meetingTitle]
    audioKeywords.extend(actors)
    json_result = google_transcribe(audio_filename, frame_rate, audioKeywords)
    return json_result

def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels
    
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage.blob._DEFAULT_CHUNKSIZE = 2 * 1024 * 1024  # 2 MB
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def upload_to_cloud(audioFullpath, audio_filename):
    frame_rate, channels = frame_rate_channel(audioFullpath)
    
    if channels > 1:
        stereo_to_mono(audioFullpath)

    framerate = {
        'framerate': frame_rate
    }
    result = json.dumps(framerate, sort_keys=True,
                        indent=4, separators=(',', ': '))

    f = open('..Firebase/framerate.json', "a")
    f.write(result)
    f.close()
    fb.setFrameRate()

    print("Uploading audio commented")
    # Parameter 1: bucket name, Parameter 2: source filename, Parameter 3: destination blob name
    upload_blob(bucketname, audioFullpath, audio_filename)  # Uploading audio file in google cloud
    
    # Saving frame rate in database for later use
    return 1
    
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

def google_transcribe(audio_file_name, frame_rate, audioKeywords):
    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=frame_rate,
    language_code='en-US',
    enable_automatic_punctuation=True,
    enable_word_time_offsets=True,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)
    
    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    sentsTimeStamp = []
    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript
        sents = re.split('[.!?]', result.alternatives[0].transcript)
        for sent in sents:
            if any(word in sent.lower() for word in audioKeywords):
                first_word = sent.split()[0]
                for word_info in result.alternatives[0].words:
                    if first_word == word_info.word:
                        sentsTimeStamp.append((sent, word_info.start_time.seconds))
                        break
    result = {
        'transcript': transcript,
        'sentsTimeStamp': sentsTimeStamp
    }
    #delete_blob(bucket_name, audio_file_name)
    return result