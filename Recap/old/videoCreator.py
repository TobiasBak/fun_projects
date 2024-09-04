import json
import math
import os
import subprocess
import time

import setup
from subtitles import convert_to_seconds
from utils import get_all_images, get_absolute_path, get_lines_from_file, get_sorted_list_of_images

num_threads = 4  # Set this to the number of cores in your CPU


def get_duration_sec(image_name) -> float:
    lines = get_lines_from_file(f"{setup.PATHS.SUBTITLE_DIR}/{image_name}.ass")
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

    print(f"Video: {video_path}: Duration: {duration}")

    return float(duration)


def get_image_names_missing_videos():
    images = get_sorted_list_of_images()
    image_names = [image.split('.jpg')[0] for image in images]

    video_files = os.listdir(setup.PATHS.OUT_VIDEO_DIR)
    video_file_names = [file.split('.mp4')[0] for file in video_files]

    images_missing_video_files = [name for name in image_names if name not in video_file_names]
    return images_missing_video_files


def create_ambience_video(name: str, start: float, duration: float) -> str:
    ambient_video_path = f"ambientVideos/{name}"
    ambient_video_1920_path = f"ambientVideos/{name.split('.mp3')[0]}_1920.mp4"

    if os.path.exists(ambient_video_1920_path):
        return ambient_video_1920_path

    # Generate a video with the duration of time based on ambient_video_path
    subprocess.run(
        f"""ffmpeg -y -t {duration} -ss {start}  -i {ambient_video_path} -vf "scale=1920:1080" -r 24 -an temp/ambient_video.mp4""")

    # Generate a video with a 60 second duration, based on temp/ambient_video
    subprocess.run(f"""ffmpeg -y -stream_loop -1 -i temp/ambient_video.mp4 -t 60 -an {ambient_video_1920_path}""")

    return ambient_video_1920_path


def generate_videos_for_images():
    # Get the list of images, audio files, and subtitles
    image_file_names_missing_videos = get_image_names_missing_videos()
    image_file_names_missing_videos = image_file_names_missing_videos[:5]

    base_video = create_ambience_video("1.mp4", 13, 3)

    os.makedirs("../temp/videos", exist_ok=True)

    background_video_duration = get_video_duration(base_video)
    total_duration = 0

    # Generate intermediate videos
    for image_name in image_file_names_missing_videos:
        print(f"Generating video for {image_name}")

        image_path = f"{setup.PATHS.IMAGE_DIR}/{image_name}.jpg"
        audio_file = f"{image_name}.mp3"
        audio_path = f"{setup.PATHS.AUDIO_DIR}/{audio_file}"
        subtitle_file = f"{image_name}.ass"
        subtitle_path = f"{setup.PATHS.SUBTITLE_DIR}/{subtitle_file}"

        duration_sec = get_duration_sec(image_name)
        buffer = 1  # ToDo: Use this buffer as whitespace before next video comes. Or something similar. This does not work with values lower than 1 sec
        duration_sec += buffer

        if duration_sec + total_duration > background_video_duration:
            total_duration = 0

        # picture = f"""ffmpeg -y -t {str(duration_sec)} -ss {str(total_duration)} -i {base_video} -i {image_path} -filter_complex "[0:v][1:v] overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='gt(t,{duration_sec})'" -an temp/videos/{image_name}.mp4"""
        picture = f"""ffmpeg -y -t {str(duration_sec)} -ss {str(total_duration)} -i {base_video} -i {image_path} -filter_complex "overlay=10:10" temp/videos/{image_name}.mp4"""
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

    # Remove videofiles that do not start with numbers
    video_files_copy = video_files.copy()
    for file in video_files_copy:
        if not file[0].isdigit():
            video_files.remove(file)

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
    with open('../temp/concat.txt', 'w') as f:
        # Write each video file to the concat.txt file
        for video_file in video_files:
            abs_path = get_absolute_path(f"{setup.PATHS.OUT_VIDEO_DIR}/{video_file}")
            f.write(f"file '{abs_path}'\n")

    video_path = f"{setup.PATHS.OUT_VIDEO_DIR}/{setup.NAME_AND_CHAPTERS}.mp4"
    audio_path = "../backgroundAudio/1_decreased.mp3"
    video_no_audio = f"temp/no_audio.mkv"
    video_path_combined_audio = f"{setup.PATHS.OUT_VIDEO_DIR}/{setup.NAME_AND_CHAPTERS}_combined_audio.mkv"""
    #
    # # Generate the final video
    # final_video = f"""ffmpeg -y -f concat -safe 0 -i temp/concat.txt -c copy -threads {num_threads} {video_path}"""
    # subprocess.run(final_video)
    #
    # # Extract audio stream
    # audio_stream = f"""ffmpeg -y -i {video_path} -map 0:a:0 -c copy out.m4a"""
    # subprocess.run(audio_stream)
    #
    # # Extract length of audio_stream
    # audio_length_command = f"""ffprobe -i out.m4a -show_entries format=duration -v quiet -of csv="p=0" """
    # audio_length = subprocess.check_output(audio_length_command, shell=True).decode('utf-8')
    # print(f"Audio length: {audio_length}")
    # audio_length = math.ceil(float(audio_length))
    #
    # # Create background music that loops over song and is the same length as the audio track
    # background_music = f"""ffmpeg -y -stream_loop -1 -i {audio_path} -t {audio_length} -c copy out_background.mp3"""
    # subprocess.run(background_music)
    #
    # # Combine audio tracks.
    # combine_audio_tracks = f"""ffmpeg -y -i out.m4a -i out_background.mp3 -filter_complex "[0][1]amerge=inputs=2,pan=stereo|FL<c0+c1|FR<c2+c3[a]" -map "[a]" temp/output.m4a"""
    # subprocess.run(combine_audio_tracks)
    #
    # # Create a video from the original but with no audio
    # video_no_audio = f"""ffmpeg -y -i {video_path} -c copy -an {video_no_audio}"""
    # subprocess.run(video_no_audio)

    # Combine output.m4a with video, but only keep the audio from output.m4a
    combine_audio_with_video = f"""ffmpeg -y -i {video_no_audio} -i temp/output.m4a -c:v copy -c:a aac output.mp4"""
    subprocess.run(combine_audio_with_video)

    #
    # # Add audio track to video
    # # combine_video_with_audio = f"""ffmpeg -y -i {video_path} -stream_loop -1 -i {audio_path} -map 0 -map 1:a -c:v libx264 -shortest {video_with_audio_path}"""
    # combine_video_with_audio = f"""ffmpeg -y -i {video_path} -stream_loop -1 -i {audio_path} -map 0 -map 1:a -c:v copy -shortest {video_with_audio_path}"""
    # # combine_video_with_audio = f"""ffmpeg -y -i {video_path} -stream_loop -1 -i {audio_path} -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -ac 2 -shortest {video_with_audio_path}"""
    # subprocess.run(combine_video_with_audio)

    # new_video_mp4 = video_with_audio_path.replace(".mkv", ".mp4")
    # # turn_into_mp4 = f"""ffmpeg -y -i {video_with_audio_path} -c:v copy -c:a copy {new_video_mp4}"""
    # turn_into_mp4 = f"""ffmpeg -i {video_with_audio_path} -c:v copy -c:a aac -b:a 160k -ac 2 -filter_complex amerge=inputs=2 {new_video_mp4}"""
    # subprocess.run(turn_into_mp4)



    # Delete the video_with_audio_path
# concat_video_files()




# decrease_volume_of_audio(f"backgroundAudio/1.mp3", 0.1)

def test_logo():
    test_video = "out/videos/1.0.A.mp4"
    logo = "out/images/1.1.A.jpg"

    my_string = f""" ffmpeg -i test.mp4 -loop 1 -i logo.png -filter_complex "[1][0]scale2ref=w=oh*mdar:h=ih/10[logo][input0]; [logo]format=rgba, fade=in: st=1: d=0.5: alpha=1 ,fade=out:st=6:d=0.5:alpha=1 [logo2]; [input0][logo2]overlay=x=main_w*0.05:(main_h-overlay_h)-(main_h * 0.1):" output.mp4"""

    subprocess.run(my_string)


# test_logo()


def create_video():
    generate_videos_for_images()
    concat_video_files()
