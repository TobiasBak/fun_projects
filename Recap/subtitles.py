import os

import json

from pydub import AudioSegment

import setup
from tts_google import get_senteces_from_string
from utils import get_absolute_path, get_sentences_dict

temp_audio_file = f"temp/temp_audio.wav"
audio_file_name = "1.0.0.mp3"

AudioSegment.converter = get_absolute_path("ffmpeg/bin/ffmpeg.exe")
AudioSegment.ffprobe = get_absolute_path("ffmpeg/bin/ffprobe.exe")


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


def get_audio_files_missing_ass():
    audio_files = os.listdir(setup.PATHS.OUT_AUDIO_DIR)
    ass_files = os.listdir(setup.PATHS.OUT_SUBTITLE_DIR)

    audio_names = [name.split('.mp3')[0] for name in audio_files]
    ass_names = [name.split('.ass')[0] for name in ass_files]

    missing_audio_files = []
    for audio_name in audio_names:
        if audio_name not in ass_names:
            missing_audio_files.append(f"{audio_name}.mp3")

    return missing_audio_files



def generate_subtitles():

    audio_files = get_audio_files_missing_ass()
    sentences_dict = get_sentences_dict()

    print(f"Generating subtitle files: {len(audio_files)}...")

    for audio_file in audio_files:
        audio_file_name = audio_file.split('.mp3')[0]
        json_file_path = get_absolute_path("temp/timings/" + f"{audio_file_name}.json")
        ass_file_path = f"{setup.PATHS.OUT_SUBTITLE_DIR}/{audio_file_name}.ass"
        sentence: str = sentences_dict[f"{audio_file_name}.jpg"]
        sentences = get_senteces_from_string(sentence)

        if 'é' in sentence or 'è' in sentence:
            sentence = sentence.replace('è', 'e').replace('é', 'e')

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

            start_timings = data[:-1]

            for i, element in enumerate(start_timings):
                start_time = element['sec']
                finish_time = data[(i + 1)]['sec']

                print(f"Start time: {start_time}")
                print(f"Finish time: {finish_time}")

                if i == 0 and start_time >= 0.2:
                    start_time = start_time - 0.2
                elif i == 0:
                    start_time = 0.0

                start_time = convert_to_hmmssmm(start_time)
                finish_time = convert_to_hmmssmm(finish_time)

                f.write(f"Dialogue: {start_time},{finish_time},Info,{sentences[i]}\n")
