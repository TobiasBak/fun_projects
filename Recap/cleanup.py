import os

import setup
from FileInterfacce import FileInterface
from utils import get_lines_from_file, get_absolute_path, get_all_images

strings_to_remove = ["toonily", "discord"]


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
                    # os.remove(image_path)
                    print(f"{image_path} should be removed")
                except FileNotFoundError:
                    print(f"File {image_path} not found")


def clean_descriptions_for_unnecessary_lines():
    file_interface = FileInterface()
    images = get_all_images()
    description_dict = file_interface.get_dict_from_file(setup.PATHS.DESCRIPTIONS)

    keys_to_remove = []

    for key in description_dict.keys():
        if key not in images:
            print(f"Removing {key} from {setup.PATHS.DESCRIPTIONS}")
            keys_to_remove.append(key)

    for key in keys_to_remove:
        description_dict.pop(key)

    file_interface.write_dict_to_file(setup.PATHS.DESCRIPTIONS, description_dict)


