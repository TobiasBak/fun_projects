# Import necessary libraries
import os

import requests  # Used for making HTTP requests
import json  # Used for working with JSON data

from Recap import consts
from Recap.utils import get_elevenlabs_api_keys, get_lines_from_file

# Define constants for the script
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time

def _generate_text_to_speach(api_key: str, voice_id: str, image_name: str, text: str):
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
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(f"{consts.OUT_AUDIO_DIR}/{image_name}", "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
    else:
        # Print the error message if the request was not successful
        print(response.text)

def generate_audio_files(name:str, voice_id: str):
    lines = get_lines_from_file(f'{consts.OUT_TEXT_DIR}/eng.{consts.NAME_AND_CHAPTERS}_generated_text.csv')





