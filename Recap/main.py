import os
import shutil

from fetchManhwa import download_images
from imageModifier import modify_all_images, modify_images_to_fit_screen

URL = 'https://toonily.com/webtoon/solo-leveling-005/'
Chapters = [1, 10]


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
    main()
