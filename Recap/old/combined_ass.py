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