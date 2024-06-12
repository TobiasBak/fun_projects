import os
import shutil
import time

from Recap.boredHumans import generate_text_from_images
from Recap.cleanup import clean_images, clean_text_files_for_unnecessary_lines
from Recap.imageModifier import modify_all_images, modify_images_to_fit_screen
from Recap.textFinder import find_text_on_images
from Recap.utils import get_lines_from_file
from consts import OUT_IMAGE_DIR, OUT_TEXT_DIR
from fetchManhwa import download_images
from open_ai import openai_generate_text

"""
The following should be set before starting the script:
"""
URL = 'https://toonily.com/webtoon/solo-leveling-005/'
Chapters = [1, 10]
Name = 'solo_leveling'

chapters_string = f'{Chapters[0]}-{Chapters[1]}'
NAME_AND_CHAPTERS = f'{Name}_{chapters_string}'


def _download_chapters():
    for i in range(Chapters[0], Chapters[1] + 1):
        download_images(f'{URL}chapter-{i}/', f'{i}')


def _delete_temp_files():
    if not os.path.exists('temp'):
        return

    for filename in os.listdir('temp'):
        file_path = os.path.join('temp', filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    os.rmdir('temp')


def _find_images_with_missing_texts():
    text_on_pictures_file_path = f'{OUT_TEXT_DIR}/eng.{NAME_AND_CHAPTERS}_text_on_pictures.csv'
    text_on_pictures_dict = {}
    lines = get_lines_from_file(text_on_pictures_file_path)
    for line in lines:
        parts = line.split(';')
        text_on_pictures_dict[parts[0]] = parts[1].replace('\n', '')

    generated_text_file_path = f'{OUT_TEXT_DIR}/eng.{NAME_AND_CHAPTERS}_generated_text.csv'
    generated_text_dict = {}
    lines = get_lines_from_file(generated_text_file_path)
    for line in lines:
        parts = line.split(';')
        generated_text_dict[parts[0]] = parts[1].replace('\n', '')

    images = []
    for file in os.listdir(OUT_IMAGE_DIR):
        if file.endswith(".jpg"):
            images.append(file)

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
    generate_text_from_images(NAME_AND_CHAPTERS, OUT_IMAGE_DIR)
    time.sleep(1)
    find_text_on_images(NAME_AND_CHAPTERS)
    _find_images_with_missing_texts()
    clean_images(NAME_AND_CHAPTERS)
    # clean_text_files_for_unnecessary_lines(NAME_AND_CHAPTERS) #  Not necessary, but nice to have
    openai_generate_text(NAME_AND_CHAPTERS)  # COSTS MONEY!!!!


if __name__ == "__main__":
    print(f"RUNNING SCRIPT FOR {NAME_AND_CHAPTERS}...")
    print(f"=========================================")
    main()

