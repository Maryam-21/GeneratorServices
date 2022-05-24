bucketname = "meetings_audios"  # Name of the bucket created in the step before

# Import libraries
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import storage
import os
import wave
import regex as re

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "ASRModule/credentials.json"

def getSpeechToText(audioFullpath, p, d, a, m):  # ASRModule/audio_wav/batoul.wav
    audioKeywords = ['user', 'system', p, d, a, m]
    audio_filename = re.findall("[.\w]+", audioFullpath)[-1]
    print(audioFullpath)
    print(audio_filename)
    json_result = google_transcribe(audio_filename, audioFullpath, audioKeywords)
    return json_result

def mp3_to_wav(audio_file_name, ):
    if audio_file_name.split('.')[1] == 'mp3':    
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

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

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

def google_transcribe(audio_file_name, file_name, audioKeywords):
    #mp3_to_wav(file_name)
    frame_rate, channels = frame_rate_channel(file_name)
    
    if channels > 1:
        stereo_to_mono(file_name)
    
    bucket_name = bucketname
    source_file_name = file_name
    destination_blob_name = audio_file_name
    
    # Audio keywords that will help to extract beneficial sentences to save their timestamps
    #audioKeywords = ['user', 'system', 'projectTitle', 'projectDomain', 'actors', 'meetingTitle']  # They are variables but set to string so it can run
    
    print("Uploading audio commented")
    #upload_blob(bucket_name, source_file_name, destination_blob_name)  # Uploading audio file in google cloud 
    
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
    #delete_blob(bucket_name, destination_blob_name)
    return result