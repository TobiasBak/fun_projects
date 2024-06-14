import json
import os
import subprocess

import setup
from subtitles import convert_to_seconds
from utils import get_all_images, get_absolute_path, get_lines_from_file


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


# Get the list of images, audio files, and subtitles
image_files = get_all_images()
image_files = image_files[:1]
audio_files = os.listdir(setup.PATHS.OUT_AUDIO_DIR)
subtitle_files = os.listdir(setup.PATHS.OUT_SUBTITLE_DIR)

base_video = "temp/base_video.mp4"
total_duration = 0

ambient_video = "ambientVideos/1"
if not os.path.exists(f"{ambient_video}_1920.mp4"):
    subprocess.run(f"ffmpeg -i {ambient_video}.mp4 -vf 'scale=1920:1080' {ambient_video}_1920.mp4")
    ambient_video = f"{ambient_video}_1920.mp4"

if os.path.exists(f"{ambient_video}_1920.mp4"):
    base_video = ambient_video

# black_background = f'ffmpeg -n -f lavfi -i color=c=black:s=1920x1080:d=60 -vf "fps=30" {base_video}'
# subprocess.run(black_background)

background_video_duration = get_video_duration(base_video)

# Generate intermediate videos
for image_file in image_files:
    image_name = image_file.split('.jpg')[0]
    image_path = f"{setup.PATHS.OUT_IMAGE_DIR}/{image_file}"
    audio_file = f"{image_name}.mp3"
    audio_path = f"{setup.PATHS.OUT_AUDIO_DIR}/{audio_file}"
    subtitle_file = f"{image_name}.ass"
    subtitle_path = f"{setup.PATHS.OUT_SUBTITLE_DIR}/{subtitle_file}"

    duration_sec = get_duration_sec(image_name)
    buffer = 1 #  ToDo: Use this buffer as whitespace before next video comes. Or something similar.
    # buffer_s = buffer / 2  # Convert buffer to seconds and divide by 2 # Todo: This does not work with values lower than 1 sec
    duration_sec += buffer
    # picture = f"""ffmpeg -y -t {str(duration_sec)} -ss {str(total_duration)} -i {base_video} -i out/images/1.0.0.jpg -filter_complex "[1:v]setpts=PTS+{0.0}/TB[out];[0:v][out]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='gt(t,0)'" -pix_fmt yuv420p -c:a copy temp/{image_name}.mp4"""
    # subtitles_and_audio = f"""ffmpeg -y -i temp/{image_name}.mp4 -itsoffset {buffer_s} -i {audio_path} -vf "subtitles={subtitle_path}" {setup.PATHS.OUT_VIDEO_DIR}/{setup.NAME_AND_CHAPTERS}_{image_name}.mp4"""

    if duration_sec + total_duration > background_video_duration:
        total_duration = 0

    fade_in_start_sec = 0  # The start time of the fade in effect in seconds
    fade_in_duration_sec = 2  # The duration of the fade in effect in seconds
    fade_out_start_sec = duration_sec - 1  # The start time of the fade out effect in seconds
    fade_out_duration_sec = 2  # The duration of the fade out effect in seconds

    # picture = f"""ffmpeg -y -t {str(duration_sec)} -ss {str(total_duration)} -i {base_video} -loop 1 -t {str(duration_sec)} -i out/images/1.0.0.jpg -filter_complex "[1:v]format=rgba,split[RGB][A];[A]alphaextract,fade=in:st={fade_in_start_sec}:d={fade_in_duration_sec}:alpha=1,fade=out:st={fade_out_start_sec}:d={fade_out_duration_sec}:alpha=1[Aout];[RGB][Aout]alphamerge[out];[0:v][out]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='gt(t,0)'" -pix_fmt yuv420p -c:a copy temp/{image_name}.mp4"""

    picture = f"""ffmpeg -y -t {str(duration_sec)} -ss {str(total_duration)} -i {base_video} -i {image_path} -filter_complex "[0:v][1:v] overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='gt(t,0)'" -pix_fmt yuv420p -c:a copy temp/{image_name}.mp4"""
    subtitles_and_audio = f"""ffmpeg -y -i temp/{image_name}.mp4 -i {audio_path} -vf "subtitles={subtitle_path}" {setup.PATHS.OUT_VIDEO_DIR}/{setup.NAME_AND_CHAPTERS}_{image_name}.mp4"""

    subprocess.run(picture)
    subprocess.run(subtitles_and_audio)

    # Delete the intermediate video: temp/{image_name}.mp4
    os.remove(f"temp/{image_name}.mp4")

    total_duration += duration_sec

# Get the list of video files to concatenate
video_files = os.listdir(setup.PATHS.OUT_VIDEO_DIR)

# Open the concat.txt file in write mode
with open('temp/concat.txt', 'w') as f:
    # Write each video file to the concat.txt file
    for video_file in video_files:
        abs_path = get_absolute_path(f"{setup.PATHS.OUT_VIDEO_DIR}/{video_file}")
        f.write(f"file '{abs_path}'\n")

# Generate the final video
num_threads = 4  # Set this to the number of cores in your CPU
final_video = f"""ffmpeg -y -f concat -safe 0 -i temp/concat.txt -c copy -threads {num_threads} {setup.PATHS.OUT_VIDEO_DIR}/{setup.NAME_AND_CHAPTERS}.mp4"""
subprocess.run(final_video)
