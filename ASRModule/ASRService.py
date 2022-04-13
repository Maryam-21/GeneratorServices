filepath = "../audio_wav/"  # Input audio file path
output_filepath = "../Transcripts/"  # Final transcript path
bucketname = "meeting_audios"  # Name of the bucket created in the step before

# Import libraries
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import storage
import os
import wave
import sys

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


def convert():
    audio_file_name = sys.argv[1]
    transcript = google_transcribe(audio_file_name)
    transcript_filename = audio_file_name.split('.')[0] + '.txt'
    write_transcripts(transcript_filename, transcript)


def mp3_to_wav(audio_file_name):
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
        return frame_rate, channels


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


def google_transcribe(audio_file_name):
    file_name = filepath + audio_file_name
    print(file_name)
    mp3_to_wav(file_name)
    # The name of the audio file to transcribe
    frame_rate, channels = frame_rate_channel(file_name)

    if channels > 1:
        stereo_to_mono(file_name)

    bucket_name = bucketname
    source_file_name = filepath + audio_file_name
    destination_blob_name = audio_file_name

    print("Uploading audio commented")
    upload_blob(bucket_name, source_file_name, destination_blob_name)  # Uploading audio file in google cloud

    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    transcript = ''

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code='en-US',
        enable_automatic_punctuation=True,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    result = response.results[-1]
    words_info = result.alternatives[0].words

    for result in response.results:
        transcript += result.alternatives[0].transcript

    # delete_blob(bucket_name, destination_blob_name)
    return transcript


def write_transcripts(transcript_filename, transcript):
    f = open(output_filepath + transcript_filename, "w+")
    f.write(transcript)
    f.close()
