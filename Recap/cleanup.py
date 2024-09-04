import os

import setup
from Recap.utils import get_lines_from_file, get_absolute_path, get_all_images, get_dict_from_file, append_to_file

strings_to_remove = ["toonily"]


def clean_images():

    print(f"Cleaning images if they include the following strings: {strings_to_remove}")

    lines = get_lines_from_file(setup.PATHS.DESCRIPTIONS)

    for line in lines:
        parts = line.split(';')
        image_path = get_absolute_path(f"{setup.PATHS.IMAGE_DIR}/{parts[0]}")
        text = parts[1]

        # Force text to lowercase
        text = text.lower()

        for string in strings_to_remove:
            if string in text:
                try:
                    os.remove(image_path)
                    print(f"Removed {image_path}")
                except FileNotFoundError:
                    print(f"File {image_path} not found")


def clean_text_files_for_unnecessary_lines():
    images = get_all_images()

    generated_text_dict = get_dict_from_file(setup.PATHS.DESCRIPTIONS)

    generated_text_file_path = get_absolute_path(setup.PATHS.DESCRIPTIONS)

    if len(generated_text_dict.keys()) == len(images):
        print("No unnecessary lines found in text files.")
        return

    print(f"Unnecessary lines found in text files. Cleaning...")

    with open(generated_text_file_path, 'w') as f:
        f.write('')
        pass

    for key in generated_text_dict.keys():
        if key not in images:
            print(f"Removing {key} from {setup.PATHS.DESCRIPTIONS}")
            continue
        append_to_file(setup.PATHS.DESCRIPTIONS, f"{key};{generated_text_dict[key]}\n")
