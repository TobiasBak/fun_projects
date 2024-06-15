import json
import os
import subprocess

import setup
from subtitles import convert_to_seconds
from utils import get_all_images, get_absolute_path, get_lines_from_file

num_threads = 4  # Set this to the number of cores in your CPU

def get_duration_sec(image_name) -> float:
    lines = get_lines_from_file(f"{setup.PATHS.OUT_SUBTITLE_DIR}/{image_name}.ass")
    duration: float = 0
    for line in lines:
        if line.startswith("Dialogue: "):
            line_parts = line.split(',')
            start_time_in_hmmssmm = line_parts[0].replace("Dialogue: ", '')
            end_time_in_hmmssmm = line_parts[1]
            duration += convert_to_seconds(end_time_in_hmmssmm) - convert_to_seconds(start_time_in_hmmssmm)

    return duration


def get_video_duration(video_path):
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        video_path
    ]

    output = subprocess.check_output(command).decode('utf-8')
    output_json = json.loads(output)

    # Get the duration from the format or the first stream
    duration = output_json.get('format', {}).get('duration')
    if duration is None:
        duration = output_json.get('streams', [{}])[0].get('duration')

    return float(duration)


def get_image_names_missing_videos():
    images = get_all_images()
    image_names = [image.split('.jpg')[0] for image in images]

    video_files = os.listdir(setup.PATHS.OUT_VIDEO_DIR)
    print(f"Video files: {video_files}")
    video_file_names = [file.split('.mp4')[0] for file in video_files]

    print(f"Images: {image_names}")
    print(f"Video files: {video_file_names}")

    images_missing_video_files = [name for name in image_names if name not in video_file_names]
    print(f"Images missing video files: {images_missing_video_files}")
    return images_missing_video_files


def generate_videos_for_images():
    # Get the list of images, audio files, and subtitles
    image_file_names_missing_videos = get_image_names_missing_videos()

    ambient_video = "ambientVideos/1"
    ambient_video_1920 = f"{ambient_video}_1920.mp4"
    if not os.path.exists(ambient_video_1920):
        print(f"Path did not exists")
        subprocess.run(f"""ffmpeg -i {ambient_video}.mp4 -vf "scale=1920:1080" -r 24 -an {ambient_video_1920}""")

    base_video = ambient_video_1920


    # black_background = f'ffmpeg -n -f lavfi -i color=c=black:s=1920x1080:d=60 -vf "fps=24" {base_video}'
    # subprocess.run(black_background)

    os.makedirs("temp/videos", exist_ok=True)

    background_video_duration = get_video_duration(base_video)
    total_duration = 0

    # Generate intermediate videos
    for image_name in image_file_names_missing_videos:
        print(f"Generating video for {image_name}")

        image_path = f"{setup.PATHS.OUT_IMAGE_DIR}/{image_name}.jpg"
        audio_file = f"{image_name}.mp3"
        audio_path = f"{setup.PATHS.OUT_AUDIO_DIR}/{audio_file}"
        subtitle_file = f"{image_name}.ass"
        subtitle_path = f"{setup.PATHS.OUT_SUBTITLE_DIR}/{subtitle_file}"

        duration_sec = get_duration_sec(image_name)
        buffer = 1  # ToDo: Use this buffer as whitespace before next video comes. Or something similar. This does not work with values lower than 1 sec
        duration_sec += buffer

        if duration_sec + total_duration > background_video_duration:
            total_duration = 0

        picture = f"""ffmpeg -y -t {str(duration_sec)} -ss {str(total_duration)} -i {base_video} -i {image_path} -filter_complex "[0:v][1:v] overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='gt(t,0)'" -pix_fmt yuv420p -c:a copy -threads {num_threads} temp/videos/{image_name}.mp4"""
        subtitles_and_audio = f"""ffmpeg -y -i temp/videos/{image_name}.mp4 -i {audio_path} -vf "subtitles={subtitle_path}" -threads {num_threads} {setup.PATHS.OUT_VIDEO_DIR}/{image_name}.mp4"""

        print(f"Generating picture video for {image_name}")
        subprocess.run(picture)
        print(f"Generating subtitles and audio for {image_name}")
        subprocess.run(subtitles_and_audio)
        print(f"Done generating video for {image_name}")

        # Delete the intermediate video: temp/{image_name}.mp4
        os.remove(f"temp/videos/{image_name}.mp4")

        total_duration += duration_sec


def concat_video_files():
    # Get the list of video files to concatenate
    video_files = os.listdir(setup.PATHS.OUT_VIDEO_DIR)

    # Sort the video_files
    def sort_key(image_name: str):
        # Split the filename on '.', convert the parts to integers, and return as a tuple
        parts = image_name.split('.')[:2]
        return tuple(int(part) for part in parts)

    video_files.sort(key=sort_key)
    print(f"Video files: {video_files}")

    video_files_copy = video_files.copy()
    for file in video_files_copy:
        if file.startswith(setup.NAME_AND_CHAPTERS):
            video_files.remove(file)

    # Open the concat.txt file in write mode
    with open('temp/concat.txt', 'w') as f:
        # Write each video file to the concat.txt file
        for video_file in video_files:
            abs_path = get_absolute_path(f"{setup.PATHS.OUT_VIDEO_DIR}/{video_file}")
            f.write(f"file '{abs_path}'\n")

    # Generate the final video
    final_video = f"""ffmpeg -y -f concat -safe 0 -i temp/concat.txt -c copy -threads {num_threads} {setup.PATHS.OUT_VIDEO_DIR}/{setup.NAME_AND_CHAPTERS}.mp4"""
    subprocess.run(final_video)


def create_video():
    generate_videos_for_images()
    concat_video_files()
