# Import necessary libraries
import os

import requests  # Used for making HTTP requests
import json  # Used for working with JSON data

import setup
from Recap.utils import get_elevenlabs_api_keys, get_lines_from_file, get_dict_from_file, get_all_images, \
    get_sentences_dict

# Define constants for the script
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time

def _generate_text_to_speach(api_key: str, voice_id: str, audio_filename: str, text: str):
    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": api_key
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.9,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(f"{setup.PATHS.OUT_AUDIO_DIR}/{audio_filename}.mp3", "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
    else:
        # Print the error message if the request was not successful
        print(response.text)


def get_missing_audio_file_names() -> list[str]:
    audio_file_names = []
    for file in os.listdir(setup.PATHS.OUT_AUDIO_DIR):
        name = file.split('.jpg')[0].replace(' ', '')
        audio_file_names.append(name)

    missing_file_names = []
    for file in get_all_images():
        name = file.split('.jpg')[0]
        if name not in audio_file_names:
            missing_file_names.append(name)

    return missing_file_names


def generate_audio_files():
    sentences_dict = get_sentences_dict()

    missing_audio_files = get_missing_audio_file_names()
    missing_audio_files = missing_audio_files[:10]
    print(f"Missing audio files: {missing_audio_files}")

    for audio_file_name in missing_audio_files:
        text = sentences_dict.get(f"{audio_file_name}.jpg")
        print(f"Generating audio for {audio_file_name}.jpg with text: {text}")
        _generate_text_to_speach(get_elevenlabs_api_keys()[0], setup.TTS_VOICE_ID, audio_file_name, text)







