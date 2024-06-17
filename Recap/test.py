import json
import os
import subprocess
from enum import Enum

import setup
from subtitles import convert_to_seconds, convert_to_hmmssmm
from utils import get_sorted_list_of_images, get_lines_from_file, append_to_file


def create_ambience_video(name: str, fps: int, start: float, duration: float) -> str:
    ambient_video_path = f"ambientVideos/{name}"
    ambient_video_1920_path = f"ambientVideos/{name.split('.mp3')[0]}_1920.mp4"

    if os.path.exists(ambient_video_1920_path):
        return ambient_video_1920_path

    # Generate a video with the duration of time based on ambient_video_path
    subprocess.run(
        f"""ffmpeg -y -t {duration} -ss {start}  -i {ambient_video_path} -vf "scale=1920:1080" -r {str(fps)} -an temp/ambient_video.mp4""")

    # Generate a video with a 60 second duration, based on temp/ambient_video
    subprocess.run(f"""ffmpeg -y -stream_loop -1 -i temp/ambient_video.mp4 -t 60 -an {ambient_video_1920_path}""")

    return ambient_video_1920_path


video = create_ambience_video("1.mp4", 60, 13, 3)


class AnimationDirection(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


def get_overlay_string(animation_direction: AnimationDirection):
    middle_of_screen_x = "(main_w-overlay_w)/2"
    middle_of_screen_y = "(main_h-overlay_h)/2"
    animation_duration = 0.25
    match animation_direction:
        case AnimationDirection.LEFT:
            return f"""'if(lt(t,{animation_duration}),{middle_of_screen_x}*2 + (t*-{middle_of_screen_x}*{1 / animation_duration}),{middle_of_screen_x})':{middle_of_screen_y}"""
        case AnimationDirection.RIGHT:
            return f"""'if(lt(t,{animation_duration}),t*{middle_of_screen_x}*{1 / animation_duration},{middle_of_screen_x})':{middle_of_screen_y}"""
        case AnimationDirection.UP:
            return f"""{middle_of_screen_x}:'if(lt(t,{animation_duration}),{middle_of_screen_y}*20 + t*-{middle_of_screen_y}*{20 / animation_duration},{middle_of_screen_y})'"""
        case AnimationDirection.DOWN:
            return f"""{middle_of_screen_x}:'if(lt(t,{animation_duration}),{middle_of_screen_y}*-20 + t*{middle_of_screen_y}*{20 / animation_duration},{middle_of_screen_y})'"""


def get_image_string(image: str, animation_direction: int, duration: tuple):
    animation_direction_string = get_overlay_string(AnimationDirection(animation_direction))
    print(animation_direction_string)

    match AnimationDirection(animation_direction):
        case AnimationDirection.LEFT:
            return f"""movie=out/images/{image}[{image}];[in][{image}]overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""
        case AnimationDirection.RIGHT:
            return f"""movie=out/images/{image}[{image}];[in][{image}]overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""
        case AnimationDirection.UP:
            return f"""movie=out/images/{image}[{image}];[in][{image}]overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""
        case AnimationDirection.DOWN:
            return f"""movie=out/images/{image}[{image}];[in][{image}]overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""


def get_audio_duration(audio_path):
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        audio_path
    ]

    output = subprocess.check_output(command).decode('utf-8')
    output_json = json.loads(output)

    # Get the duration from the format or the first stream
    duration = output_json.get('format', {}).get('duration')
    if duration is None:
        duration = output_json.get('streams', [{}])[0].get('duration')

    print(f"Video: {audio_path}: Duration: {duration}")

    return float(duration)


def convert_float_to_hhmmss(time: float) -> str:
    hours = int(time / 3600)
    minutes = int((time % 3600) / 60)
    seconds = time % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def generate_image_videos():
    images = get_sorted_list_of_images()
    images = images[:4]

    print(images)

    for i, image in enumerate(images):
        image_name = image.split('.jpg')[0]

        audio = f"out/audio/{image_name}.mp3"
        duration = get_audio_duration(audio)
        start_finish = (0, duration)

        ffmpeg_command = f"""ffmpeg -y -i {audio} -i {video} -t {convert_float_to_hhmmss(duration)} -c:v libx265 -vf "{get_image_string(image, (i % 4), start_finish)}" {image_name}.mp4"""
        print(ffmpeg_command)
        subprocess.run(ffmpeg_command, shell=True)

        # subtitles_command = f"""ffmpeg -y -i {image_name}.mp4 -vf subtitles={subtitles} {image_name}_subtitles.mp4"""
        # subprocess.run(subtitles_command)


def generate_concated_video():
    video_files = os.listdir("./")
    print(video_files)
    with open('concat.txt', 'w') as f:
        for file in video_files:
            if file.endswith(".mp4") and file[0].isdigit():
                f.write(f"file '{file}'\n")

    command = f"""ffmpeg -f concat -safe 0 -i concat.txt -c:v libx265 output.mp4"""
    subprocess.run(command)

def add_music():
    video = "output.mp4"
    music = "backgroundAudio/1_decreased.mp3"
    command = f"""ffmpeg -i {video} -i {music} -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v libx265 -ac 2 -shortest output_music.mp4"""
    subprocess.run(command)


def add_subtitles():
    video = "output_music.mp4"
    combined_subtitle = "temp/combined.ass"

    subtitle_files = os.listdir(f"out/subtitles")

    first_file = f"out/subtitles/{subtitle_files[0]}"
    last_line_added = 0.0

    # Open and write to file to clear it
    with open(combined_subtitle, 'w') as f:
        f.write('')

    for line in get_lines_from_file(first_file):
        print(line)
        if line.startswith("Dialogue:"):
            continue
        append_to_file(combined_subtitle, line)

    for file in subtitle_files:
        duration = 0.0
        for line in get_lines_from_file(f"out/subtitles/{file}"):
            if not line.startswith("Dialogue:"):
                continue
            parts = line.split(',')
            start_time = parts[0].replace("Dialogue: ", '')
            end_time = parts[1]

            start_time_sec = convert_to_seconds(start_time)
            end_time_sec = convert_to_seconds(end_time)

            new_start_time_sec = start_time_sec + last_line_added
            new_end_time_sec = end_time_sec + last_line_added

            new_start_time = convert_to_hmmssmm(new_start_time_sec)
            new_end_time = convert_to_hmmssmm(new_end_time_sec)

            duration += end_time_sec - start_time_sec

            string = f"Dialogue: {new_start_time},{new_end_time},{parts[2]},{','.join(parts[3:])}"
            append_to_file(combined_subtitle, string)
        last_line_added += duration

    command = f"""ffmpeg -y -i {video} -vf "subtitles={combined_subtitle}" -c:v libx265 output_subtitles.mp4"""
    subprocess.run(command)


# generate_image_videos()
# generate_concated_video()
# add_music()
add_subtitles()
