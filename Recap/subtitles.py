import os

import vosk
import json
import wave
import json

from pydub import AudioSegment

import setup
from utils import get_absolute_path, get_sentences_dict

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
        json_file_path = f"temp/json/{audio_file.split('.mp3')[0]}.json"

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


def convert_to_hmmssmm(time: float) -> str:
    """
    The function takes a float time in seconds and converts it to a string in the format h:mm:ss.mm
    """

    # Get the hours, minutes, and seconds
    hours = int(time / 3600)
    minutes = int((time % 3600) / 60)
    seconds = time % 60

    # Get the milliseconds
    milliseconds = int((seconds - int(seconds)) * 1000)

    # Ensure miliseconds are only 2 digits
    milliseconds = f"{milliseconds:02}"

    # Return the time in the format h:mm:ss.mm
    out = f"{hours:01}:{minutes:02}:{int(seconds):02}.{milliseconds[:2]}"
    return out


def convert_to_seconds(time: str) -> float:
    """
    The function takes a string time in the format h:mm:ss.mm and converts it to a float in seconds
    """
    # Split the time into hours, minutes, seconds, and milliseconds
    time_parts = time.split(":")
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = float(time_parts[2])

    # Convert the time to seconds
    time = (hours * 3600 + minutes * 60 + seconds)

    return time

def generate_subtitle_files():
    print(f"Generating subtitle files...")

    audio_files = os.listdir(setup.PATHS.OUT_AUDIO_DIR)
    sentences_dict = get_sentences_dict()

    for audio_file in audio_files:
        audio_file_name = audio_file.split('.mp3')[0]
        json_file_path = get_absolute_path("temp/json/" + f"/{audio_file_name}.json")
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
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
            f.write("Style: Info,Futura,20,&H00F5F5F5,&H00F5F5F5,&H000A0A0A,&H000A0A0A,-1,0,1,2,1,2,250,250,40,0\n")
            f.write("[Events]\n")
            f.write("Format: Start, End, Style, Text\n")

            amount_of_words = 0
            # For each sentence
            for sentence in sentences:
                words = get_words_in_sentence(sentence)

                amount_of_words += len(words)

                # For each word in the sentence
                if amount_of_words == len(words):
                    start_time = data['result'][0]['start']
                    end_time = data['result'][len(words) - 1]['end']
                else:
                    start_time = data['result'][amount_of_words - len(words)]['start']
                    end_time = data['result'][-1]['end']

                # Convert start_time and end_time to hrs:minutes:secs:ms format
                start_time = convert_to_hmmssmm(start_time)
                end_time = convert_to_hmmssmm(end_time)

                # Write the sentence to the .ass file along with its start and end times
                f.write(f"Dialogue: {start_time},{end_time},Info,{sentence}\n")


def generate_subtitles():
    create_timings_for_subtitles()
    generate_subtitle_files()
