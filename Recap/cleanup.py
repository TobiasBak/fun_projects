import os

import setup
from Recap import consts
from Recap.consts import OUT_TEXT_DIR, OUT_IMAGE_DIR
from Recap.utils import get_lines_from_file, get_absolute_path, get_all_images, get_dict_from_file, append_to_file

strings_to_remove = ["toonily"]


def clean_images(directory: str):
    lines = get_lines_from_file(f"{OUT_TEXT_DIR}/{setup.TEXT_ON_PICTURES_FILE}")

    for line in lines:
        parts = line.split(';')
        image_path = get_absolute_path(OUT_IMAGE_DIR, parts[0])
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

    text_on_pictures_file_name = f"{setup.TEXT_ON_PICTURES_FILE}"
    text_on_pictures_dict = get_dict_from_file(f"{consts.OUT_TEXT_DIR}/{text_on_pictures_file_name}")

    generated_text_file_name = f"{setup.GENERATED_DESCRIPTIONS_FILE}"
    generated_text_dict = get_dict_from_file(f"{consts.OUT_TEXT_DIR}/{generated_text_file_name}")

    text_on_pictures_file_path = get_absolute_path(OUT_TEXT_DIR, text_on_pictures_file_name)
    generated_text_file_path = get_absolute_path(OUT_TEXT_DIR, generated_text_file_name)

    if len(text_on_pictures_dict.keys()) == len(generated_text_dict.keys()) and len(text_on_pictures_dict.keys()) == len(images) and len(generated_text_dict.keys()) == len(images):
        print("No unnecessary lines found in text files.")
        return

    print(f"Unnecessary lines found in text files. Cleaning...")

    # Open the files in write mode to clear their contents
    with open(text_on_pictures_file_path, 'w') as f:
        f.write('')
        pass
    with open(generated_text_file_path, 'w') as f:
        f.write('')
        pass

    # Write the necessary lines back to the files
    for key in text_on_pictures_dict.keys():
        if key not in images:
            print(f"Removing {key} from {text_on_pictures_file_name}")
            continue
        append_to_file(f"{consts.OUT_TEXT_DIR}/{text_on_pictures_file_name}", f"{key};{text_on_pictures_dict[key]}\n")

    for key in generated_text_dict.keys():
        if key not in images:
            print(f"Removing {key} from {generated_text_file_name}")
            continue
        append_to_file(f"{consts.OUT_TEXT_DIR}/{generated_text_file_name}", f"{key};{generated_text_dict[key]}\n")
