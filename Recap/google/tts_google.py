import json
import os

import nltk
from nltk.tokenize import sent_tokenize

from google.cloud import texttospeech_v1beta1 as tts

import setup
from utils import get_all_images, get_sentences_dict

# Make sure to download the necessary resources
nltk.download('punkt')
nltk.download('punkt_tab')


class TTS_Client:
    def __init__(self):
        self._tts_client = tts.TextToSpeechClient()
        self._tts_voice = tts.VoiceSelectionParams(
            language_code=setup.TTS_VOICE_LAN_CODE,
            name=setup.TTS_VOICE_NAME,
        )
        self._tts_audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3,
            speaking_rate=setup.TTS_SPEAKING_RATE,
            pitch=setup.TTS_PITCH,
        )

    def generate_audio(self, audio_filename: str, text: str = None, ssml: str = None):
        if text is None and ssml is None:
            raise Exception("Text or SSML must be provided")

        if text is not None and ssml is not None:
            raise Exception("Only one of text or SSML can be provided")

        response = None

        if text is not None:
            synthesis_input = tts.SynthesisInput(text=text)
            response = self._generate_audio_from_text(synthesis_input)

        elif ssml is not None:
            synthesis_input = tts.SynthesisInput(ssml=ssml)
            response = self._generate_audio_from_ssml(synthesis_input)

        if response is None:
            print(f"Audio file {audio_filename} was not generated")
            return

        with open(f"{setup.PATHS.OUT_AUDIO_DIR}/{audio_filename}.mp3", "wb") as out:
            out.write(response.audio_content)

        if response.timepoints:
            marks = [dict(sec=t.time_seconds, name=t.mark_name)
                     for t in response.timepoints]

            with open(f"temp/timings/{audio_filename}.json", 'w') as out:
                json.dump(marks, out)

    def _generate_audio_from_text(self, synthesis_input: tts.SynthesisInput):
        response = self._tts_client.synthesize_speech(
            request=tts.SynthesizeSpeechRequest(
                input=synthesis_input,
                voice=self._tts_voice,
                audio_config=self._tts_audio_config
            )
        )

        return response

    def _generate_audio_from_ssml(self, synthesis_input: tts.SynthesisInput):

        response = self._tts_client.synthesize_speech(
            request=tts.SynthesizeSpeechRequest(
                input=synthesis_input,
                voice=self._tts_voice,
                audio_config=self._tts_audio_config,
                enable_time_pointing=[tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
            )
        )

        return response

    def generate_audio_files(self):
        sentences_dict = get_sentences_dict()

        missing_audio_file_names = get_missing_audio_file_names()
        print(f"Missing audio files: {missing_audio_file_names}")

        for audio_file_name in missing_audio_file_names:
            text = sentences_dict.get(f"{audio_file_name}.jpg")
            print(f"Generating audio for {audio_file_name}.jpg with text: {text}")
            ssml = generate_ssml_from_text(text, audio_file_name)
            self.generate_audio(audio_file_name, ssml=ssml)


def get_senteces_from_string(sentences: str) -> list:
    return sent_tokenize(sentences)


def split_sentence(sentence, max_length=64):
    print(f"Testing: {sentence}")
    if len(sentence) > max_length:
        split_points = [i for i in range(max_length, -1, -1) if sentence[i] in {',', '"', ' '}]
        if split_points:
            split_point = split_points[0]
            return [sentence[:split_point], sentence[split_point + 1:]]
        else:
            return [sentence[:max_length], sentence[max_length:]]
    else:
        return [sentence]


def generate_ssml_from_text(sentences: str, audio_file_name: str) -> str:
    # Get sentences from string
    # The cases that are troublesome

    sentence_array = get_senteces_from_string(sentences)
    print(sentence_array)

    sentences_with_marks = ""

    for i, sentence in enumerate(sentence_array):
        s_sentence = split_sentence(sentence)

        for j, s in enumerate(s_sentence):
            sentences_with_marks += f'<mark name="{audio_file_name}:{i}.{j}"/> {s}'

    out = f"""
    <speak>
    <break time="300ms"/>
    {sentences_with_marks}
    <break time="200ms"/>
    <mark name="finish"/>
    </speak>
    """
    print(out)

    return out


def get_missing_audio_file_names():
    images = get_all_images()
    audio_files = os.listdir(setup.PATHS.OUT_AUDIO_DIR)
    audio_file_names = [file.split('.mp3')[0].replace(' ', '') for file in audio_files]
    image_file_names = [file.split('.jpg')[0] for file in images]

    missing_audio_files = [name for name in image_file_names if name not in audio_file_names]
    return missing_audio_files
