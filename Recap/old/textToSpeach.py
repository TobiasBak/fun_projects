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
            "stability": 0.65,
            "similarity_boost": 0.85,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)
    if not response.ok:
        response_json = response.json()
        status_message = response_json["detail"]["status"]
        if status_message == "quota_exceeded":
            print("Quota exceeded")
            return status_message


    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(f"{setup.PATHS.AUDIO_DIR}/{audio_filename}.mp3", "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
    else:
        # Print the error message if the request was not successful
        print(response.text)

    return None


def get_missing_audio_files():
    images = get_all_images()
    audio_files = os.listdir(setup.PATHS.AUDIO_DIR)
    audio_file_names = [file.split('.mp3')[0].replace(' ', '') for file in audio_files]
    image_file_names = [file.split('.jpg')[0] for file in images]

    missing_audio_files = [name for name in image_file_names if name not in audio_file_names]
    return missing_audio_files


def generate_audio_files():
    sentences_dict = get_sentences_dict()

    missing_audio_files = get_missing_audio_files()
    print(f"Missing audio files: {missing_audio_files}")
    api_keys_used = 0
    api_key = get_elevenlabs_api_keys()[api_keys_used]

    for audio_file_name in missing_audio_files:
        text = sentences_dict.get(f"{audio_file_name}.jpg")
        print(f"Generating audio for {audio_file_name}.jpg with text: {text}")
        response = _generate_text_to_speach(api_key, setup.TTS_VOICE_ID, audio_file_name, text)
        if response is not None:
            api_keys_used += 1
            if api_keys_used >= len(get_elevenlabs_api_keys()):
                print("All API keys used. Exiting...")
                break
            api_key = get_elevenlabs_api_keys()[api_keys_used]
            response = _generate_text_to_speach(api_key, setup.TTS_VOICE_ID, audio_file_name, text)
