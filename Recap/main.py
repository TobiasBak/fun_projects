import os
import shutil
import time

import setup
from Recap.boredHumans import generate_text_from_images
from Recap.cleanup import clean_images, clean_text_files_for_unnecessary_lines
from Recap.imageModifier import modify_all_images, modify_images_to_fit_screen
from Recap.textFinder import find_text_on_images
from Recap.utils import get_lines_from_file, get_dict_from_file, get_all_images
from fetchManhwa import download_images
from open_ai import openai_generate_text
from subtitles import generate_subtitles
from textToSpeach import generate_audio_files

"""
FILL OUT VALUES IN SETUP.PY BEFORE RUNNING SCRIPT
"""


def _download_chapters():
    for i in range(setup.CHAPTERS[0], setup.CHAPTERS[1] + 1):
        download_images(f'{setup.DOWNLOAD_URL}chapter-{i}/', f'{i}')


def _delete_temp_files():
    if not os.path.exists('temp'):
        return

    print("Deleting temp files...")

    for filename in os.listdir('temp'):
        file_path = os.path.join('temp', filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    os.rmdir('temp')


def _find_images_with_missing_texts(image_directory: str):
    text_on_pictures_dict = get_dict_from_file(setup.PATHS.TEXT_ON_PICTURES)
    generated_text_dict = get_dict_from_file(setup.PATHS.DESCRIPTIONS)

    images = get_all_images(image_directory)

    print(f"Checking images in {image_directory} for missing text...")

    for image in images:
        if image not in text_on_pictures_dict or image not in generated_text_dict:
            print(f"Image {image} is missing text")
            print(f"Text on pictures: {text_on_pictures_dict.get(image)}")
            print(f"Generated text: {generated_text_dict.get(image)}")
            print("")
            raise Exception(f"Image {image} is missing text")


def main():
    # _download_chapters()
    # modify_all_images()
    # modify_images_to_fit_screen()
    _delete_temp_files()
    generate_text_from_images(setup.PATHS.OUT_IMAGE_DIR)
    time.sleep(1)
    find_text_on_images(setup.PATHS.OUT_IMAGE_DIR)
    _find_images_with_missing_texts(setup.PATHS.OUT_IMAGE_DIR)
    clean_images()
    # clean_text_files_for_unnecessary_lines() #  Not necessary, but nice to have
    openai_generate_text()  # COSTS MONEY!!!!
    # # generate_audio_files()
    # generate_subtitles()


if __name__ == "__main__":
    print(f"RUNNING SCRIPT FOR {setup.NAME_AND_CHAPTERS}...")
    print(f"=========================================")
    main()

