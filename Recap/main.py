import os
import shutil

from boredHumans import generate_text_from_images
from consts import OUT_IMAGE_DIR
from fetchManhwa import download_images
from imageModifier import modify_all_images, modify_images_to_fit_screen
from textFinder import process_images

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
    for filename in os.listdir('temp'):
        file_path = os.path.join('temp', filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    os.rmdir('temp')


def main():
    _download_chapters()
    modify_all_images()
    modify_images_to_fit_screen()
    _delete_temp_files()


if __name__ == "__main__":
    print(f"RUNNING SCRIPT FOR {NAME_AND_CHAPTERS}...")
    print(f"=========================================")
    # generate_text_from_images(NAME_AND_CHAPTERS, OUT_IMAGES_DIR)
    print(OUT_IMAGE_DIR)
    process_images(NAME_AND_CHAPTERS, OUT_IMAGE_DIR)
