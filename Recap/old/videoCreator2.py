import subprocess

from PIL import Image
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import ImageClip, CompositeVideoClip, concatenate_videoclips
import os


import setup
from utils import get_absolute_path, get_lines_from_file, get_sorted_list_of_images

clips = []

images = get_sorted_list_of_images()
images = images[:2]


def get_duration_sec(time: str) -> float:
    duration_parts = time.split(':')
    first_part = duration_parts[2].split('.')[0]
    second_part = f"0.{duration_parts[2].split('.')[1].replace(',', '')}"
    duration_sec = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + int(first_part) + float(second_part)
    return duration_sec


def get_audio_duration(image: str):
    duration = 0
    # ass file containing subtitles
    subtitles_file = f"{setup.PATHS.SUBTITLE_DIR}/{image.split('.jpg')[0]}.ass"
    lines = get_lines_from_file(subtitles_file)
    start_times = []
    end_times = []
    for line in lines:
        print(line)
        if not line.startswith('Dialogue:'):
            continue
        line_parts = line.split(',')
        start_time = line_parts[0].replace('Dialogue: ', '')
        end_time = line_parts[1]
        start_times.append(get_duration_sec(start_time))
        end_times.append(get_duration_sec(end_time))

    total_audio_duration = (end_times[0] - start_times[0]) + (end_times[1] - start_times[1])
    return total_audio_duration


for image in images:
    image_name = image.split('.jpg')[0]
    img_path = get_absolute_path(f"{setup.PATHS.IMAGE_DIR}/{image}")
    audio_path = get_absolute_path(f"{setup.PATHS.AUDIO_DIR}/{image_name}.mp3")
    duration = get_audio_duration(image) + 0.5

    # Load the image and resize it to fit within the white background
    img = Image.open(img_path)

    # Base video
    base_video = ImageClip("black_background.jpg").set_duration(duration).set_pos(("center", "center"))

    # Create an ImageClip with the resized image
    img_clip = ImageClip(img_path).set_duration(duration).set_pos(("center", "center"))
    audio_clip = AudioFileClip(audio_path)

    movie_clip = img_clip.set_audio(audio_clip)

    final = CompositeVideoClip([base_video, movie_clip], size=(1920, 1080))
    final.write_videofile(f"{setup.PATHS.OUT_VIDEO_DIR}/{image.split('.jpg')[0]}.mp4", fps=10)
    ffmpeg_cmd = f'ffmpeg -y -i {setup.PATHS.OUT_VIDEO_DIR}/{image_name}.mp4 -vf "subtitles={setup.PATHS.SUBTITLE_DIR}/{image_name}.ass" -c:a copy {setup.PATHS.OUT_VIDEO_DIR}/{image_name}l.mp4'
    subprocess.run(ffmpeg_cmd)

    # Append the video clip to the list
    clips.append(final)

# # Concatenate all the clips into a single video
# concat_clip = concatenate_videoclips(clips, method="compose")
# concat_clip.write_videofile("out/videos/final.mp4", fps=10)


