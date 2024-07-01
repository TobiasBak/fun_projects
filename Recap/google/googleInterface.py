import os

from google.cloud import texttospeech_v1beta1 as tts

import setup
from google.gemini import Gemini
from google.tts_google import TTS_Client

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'hidden/credentials.json'

class GoogleInterface:
    _instance = None
    gemini_client = None
    tts_client = None

    def set_audio_config(self, audio_config):
        self._audio_config = audio_config

    def get_instance(self):
        if self._instance is None:
            self._instance = GoogleInterface()
        return self._instance

    def __init__(self):
        self.tts_client = TTS_Client()
        self.gemini_client = Gemini()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GoogleInterface, cls).__new__(cls)
        return cls._instance




