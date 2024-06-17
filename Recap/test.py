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


def get_image_string(image: str, animation_direction: int, duration: tuple):
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

        ffmpeg_command = f"""ffmpeg -y -i {audio} -ss {convert_to_hmmssmm(total_duration)} -i {base_video} -loop 1 -i out/images/{image}.jpg -t {convert_float_to_hhmmss(duration)} -filter_complex "[1:v][2:v]{get_image_string(f"{image}.jpg", (i % 4), start_finish)},ass=out/subtitles/{image}.ass[out]" -map 0:a -c:a copy -map "[out]" -c:v libx265 {out_path}"""

        print(ffmpeg_command)
        subprocess.run(ffmpeg_command, shell=True)

        total_duration += duration


def generate_concated_video():
    video_files = os.listdir("temp/videos")
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


def add_subtitles():
    video = "temp/videos/concat_music.mp4"
    combined_subtitle = "temp/combined.ass"
    out_path = f"{setup.PATHS.OUT_VIDEO_DIR}/{setup.NAME_AND_CHAPTERS}.mp4"

    create_combined_ass(combined_subtitle)

    command = f"""ffmpeg -y -i {video} -vf subtitles={combined_subtitle} {out_path}"""
    subprocess.run(command)


def create_combined_ass(combined_subtitle):
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


generate_image_videos()
generate_concated_video()
add_music()
# add_subtitles()
