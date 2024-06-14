import json
import os
import sys

from google.cloud import texttospeech_v1beta1 as tts

import setup
from utils import get_all_images, get_sentences_dict

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'hidden/credentials.json'
client = tts.TextToSpeechClient()

voice = tts.VoiceSelectionParams(
    language_code=setup.TTS_VOICE_LAN_CODE,
    name=setup.TTS_VOICE_NAME,
)

audio_config = tts.AudioConfig(
    audio_encoding=tts.AudioEncoding.MP3,
    speaking_rate=setup.TTS_SPEAKING_RATE
)

os.makedirs("temp/timings", exist_ok=True)


def _generate_text_to_speach(audio_filename: str, text: str):
    synthesis_input = tts.SynthesisInput(ssml=text)

    # Calculate the size of the request body
    request_body_size = sys.getsizeof(synthesis_input)

    response = client.synthesize_speech(
        request=tts.SynthesizeSpeechRequest(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
            enable_time_pointing=[tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
        )
    )

    if response is not None:
        with open(f"{setup.PATHS.OUT_AUDIO_DIR}/{audio_filename}.mp3", "wb") as out:
            out.write(response.audio_content)

        marks = [dict(sec=t.time_seconds, name=t.mark_name)
                 for t in response.timepoints]

        with open(f"temp/timings/{audio_filename}.json", 'w') as out:
            json.dump(marks, out)

    else:
        print(f"Something fucked up in google tts. Audio_filename: {audio_filename}")

    return None


def generate_ssml_from_text(sentence: str) -> str:
    out = f"""
    <speak>
    <mark name="start_0"/> {sentence} <mark name="finish_0"/>
    </speak>
    """
    return out


def get_missing_audio_files():
    images = get_all_images()
    audio_files = os.listdir(setup.PATHS.OUT_AUDIO_DIR)
    audio_file_names = [file.split('.mp3')[0].replace(' ', '') for file in audio_files]
    image_file_names = [file.split('.jpg')[0] for file in images]

    missing_audio_files = [name for name in image_file_names if name not in audio_file_names]
    return missing_audio_files


def google_tts_generate_audio_files():
    sentences_dict = get_sentences_dict()
    print(sentences_dict)

    missing_audio_files = get_missing_audio_files()
    print(f"Missing audio files: {missing_audio_files}")

    for audio_file_name in missing_audio_files:
        text = sentences_dict.get(f"{audio_file_name}.jpg")
        print(f"Generating audio for {audio_file_name}.jpg with text: {text}")
        ssml = generate_ssml_from_text(text)
        _generate_text_to_speach(audio_file_name, ssml)
