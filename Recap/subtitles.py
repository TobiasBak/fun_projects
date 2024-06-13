import os

import vosk
import json
import wave
import json

from pydub import AudioSegment

import setup
from utils import get_absolute_path, get_absolute_paths, get_all_images, get_lines_from_file, get_sentences_dict

temp_audio_file = f"temp/temp_audio.wav"
audio_file_name = "1.0.0.mp3"

AudioSegment.converter = get_absolute_path("ffmpeg/bin/ffmpeg.exe")
AudioSegment.ffprobe = get_absolute_path("ffmpeg/bin/ffprobe.exe")
print(f"ffmpeg: {AudioSegment.converter}")

# Load the model
model = vosk.Model("vosk-model")


def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(wav_file_path), exist_ok=True)

    audio.export(wav_file_path, format="wav")


def create_timings_for_subtitles():
    print(f"Generating timings for subtitles...")

    audio_file_paths = os.listdir(setup.PATHS.OUT_AUDIO_DIR)
    for audio_file in audio_file_paths:
        json_file_path = f"temp/{audio_file.split('.mp3')[0]}.json"

        # Check if json file already exists
        if os.path.exists(get_absolute_path(json_file_path)):
            continue

        audio_file_abs_path = get_absolute_path(f"{setup.PATHS.OUT_AUDIO_DIR}/{audio_file}")
        # Generate temp_audio.wav file
        convert_mp3_to_wav(audio_file_abs_path, temp_audio_file)

        # Open the audio file
        wf = wave.open(temp_audio_file, "rb")

        # Create a recognizer with word timings
        rec = vosk.KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        # Transcribe the audio
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print(rec.Result())

        # Get the final result
        result = json.loads(rec.FinalResult())

        # Write json result to file in temp folder
        with open(get_absolute_path(json_file_path), "w") as f:
            json.dump(result, f, indent=4)


def get_sentences_from_string(sentences: str):
    out = []
    for sentence in sentences.split("."):
        if sentence == "":
            continue
        if sentence.startswith(" "):
            sentence = sentence[1:]
        out.append(sentence + ".")
    return out


def get_words_in_sentence(sentence: str):
    words = sentence.split(" ")
    out = []
    for word in words:
        out.append(word.replace(",", "").replace(".", "").replace("!", "").replace("?", ""))
    return out


def generate_subtitle_files():
    print(f"Generating subtitle files...")

    audio_files = os.listdir(setup.PATHS.OUT_AUDIO_DIR)
    sentences_dict = get_sentences_dict()

    for audio_file in audio_files:
        audio_file_name = audio_file.split('.mp3')[0]
        json_file_path = get_absolute_path("temp" + f"/{audio_file_name}.json")
        ass_file_path = f"{setup.PATHS.OUT_SUBTITLE_DIR}/{audio_file_name}.ass"
        sentences = get_sentences_from_string(sentences_dict[f"{audio_file_name}.jpg"])

        # Load the transcriptions and timings
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Open the .ass file
        with open(ass_file_path, 'w') as f:
            # Write the .ass file header
            f.write("[Script Info]\n")
            # f.write("ScriptType: v4.00+\n")
            f.write("PlayResY: 600\n")
            f.write("WrapStyle: 1\n")
            # f.write("ScaledBorderAndShadow: yes\n")
            # f.write("YCbCr Matrix: TV.601\n")
            f.write("[V4+ Styles]\n")
            f.write(
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold\n")
            f.write("Style: Info,Futura,30,&H00F5F5F5,&H00F5F5F5,&H000A0A0A,&H000A0A0A,-1\n")
            f.write("[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

            amount_of_words = 0
            # For each sentence
            for sentence in sentences:
                words = get_words_in_sentence(sentence)

                amount_of_words += len(words)

                # For each word in the sentence
                if amount_of_words == len(words):
                    start_time = data['result'][0]['start']
                    end_time = data['result'][len(words)]['end']
                else:
                    start_time = data['result'][amount_of_words - len(words) + 1]['start']
                    end_time = data['result'][-1]['end']

                # Write the sentence to the .ass file along with its start and end times
                f.write(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{sentence}\n")


def generate_subtitles():
    create_timings_for_subtitles()
    generate_subtitle_files()
