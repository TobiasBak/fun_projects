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


class AnimationDirection(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


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


def get_image_string(animation_direction: int, duration: tuple):
    animation_direction_string = get_overlay_string(AnimationDirection(animation_direction))
    print(animation_direction_string)

    match AnimationDirection(animation_direction):
        case AnimationDirection.LEFT:
            return f"""overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""
        case AnimationDirection.RIGHT:
            return f"""overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""
        case AnimationDirection.UP:
            return f"""overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""
        case AnimationDirection.DOWN:
            return f"""overlay={animation_direction_string}:enable='between(t,{duration[0]},{duration[1]})'"""


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

    out = f"{hours:02}:{minutes:02}:{seconds:02}"
    print(out)

    return out


def get_image_names_missing_videos():
    images = get_sorted_list_of_images()
    image_names = [image.split('.jpg')[0] for image in images]

    video_files = os.listdir("temp/videos")
    video_file_names = [file.split('.mp4')[0] for file in video_files]

    images_missing_video_files = [name for name in image_names if name not in video_file_names]
    return images_missing_video_files


def generate_image_videos():
    images = get_image_names_missing_videos()

    base_video = create_ambience_video("1.mp4", 60, 0, 60)
    print("base_video", base_video)

    total_duration = 0.0

    for i, image in enumerate(images):
        audio = f"out/audio/{image}.mp3"
        duration = get_audio_duration(audio)
        start_finish = (0, duration)

        print(image)
        out_path = f"temp/videos/{image}.mp4"
        print(out_path)

        if total_duration + duration > 60:
            total_duration = 0.0

        ffmpeg_command = f"""ffmpeg -y -fps_mode 0 -hwaccel cuda -hwaccel_output_format cuda -i {audio} -ss {convert_to_hmmssmm(total_duration)} -i {base_video} -loop 1 -i out/images/{image}.jpg -t {convert_float_to_hhmmss(duration)} -filter_complex "[1:v][2:v]{get_image_string(1, start_finish)},ass=out/subtitles/{image}.ass[out]" -map 0:a -c:a copy -map "[out]" -c:v h264_nvenc {out_path}"""

        print(ffmpeg_command)
        subprocess.run(ffmpeg_command, shell=True)

        total_duration += duration


def generate_concated_video():
    video_files = os.listdir("temp/videos")

    def sort_key(image_name: str):
        # Split the filename on '.', convert the parts to integers, and return as a tuple
        parts = image_name.split('.')[:2]
        return tuple(int(part) for part in parts)

    video_files.sort(key=sort_key)

    print(video_files)
    with open('temp/concat.txt', 'w') as f:
        for file in video_files:
            if file.endswith(".mp4") and file[0].isdigit():
                f.write(f"file 'videos/{file}'\n")

    out_path = "temp/videos/concat.mp4"

    command = f"""ffmpeg -y -f concat -safe 0 -i temp/concat.txt -c copy {out_path}"""
    subprocess.run(command)


def add_music():
    video = "temp/videos/concat.mp4"
    music = "backgroundAudio/1_decreased.mp3"
    out_path = "temp/videos/concat_music.mp4"

    command = f"""ffmpeg -y -i {video} -stream_loop -1 -i {music} -shortest -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -ac 2 {out_path}"""
    subprocess.run(command)


def decrease_volume_of_audio(file_path: str, volume: float):
    audio_path = file_path
    out = f"{file_path.split('.mp3')[0]}_decreased.mp3"

    decrease_volume = f"""ffmpeg -y -i {audio_path} -filter:a "volume={str(volume)}" {out}"""
    subprocess.run(decrease_volume)

generate_image_videos()
# generate_concated_video()
# add_music()
# decrease_volume_of_audio("backgroundAudio/1.mp3", 0.05)
