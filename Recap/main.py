import os
import shutil
import time

import setup
from Recap.cleanup import clean_images, clean_text_files_for_unnecessary_lines
from Recap.imageModifier import modify_all_images, modify_images_to_fit_screen
from Recap.utils import get_dict_from_file, get_all_images
from fetchManhwa import download_images
from google.gemini import remove_descriptions_about_voices, optimize_quotes_ending_with_comma, optimize_sentences_errors
from google.googleInterface import GoogleInterface
from subtitles import generate_subtitles

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


def _find_images_with_missing_texts(image_directory: str, text_file_path: str):
    generated_text_dict = get_dict_from_file(text_file_path)

    images = get_all_images(image_directory)

    print(f"Checking images in {image_directory} for missing text...")

    for image in images:
        if image not in generated_text_dict:
            print(f"Image {image} is missing text")
            print(f"Generated text: {generated_text_dict.get(image)}")
            print("")
            raise Exception(f"Image {image} is missing text")


def main():
    google_interface = GoogleInterface()

    google_interface.gemini_client.generate_descriptive_text()
    time.sleep(1)
    _find_images_with_missing_texts(setup.PATHS.IMAGE_DIR, setup.PATHS.DESCRIPTIONS)
    clean_images()
    clean_text_files_for_unnecessary_lines()  # Not necessary, but nice to have
    google_interface.gemini_client.generate_sentences_gemini()
    google_interface.gemini_client.remove_duplicate_sentences()
    remove_descriptions_about_voices()
    optimize_quotes_ending_with_comma()
    optimize_sentences_errors()
    time.sleep(1)
    _find_images_with_missing_texts(setup.PATHS.IMAGE_DIR, setup.PATHS.SENTENCES)

    # FOR ENGLAND!
    google_interface.en_tts_client.generate_audio_files()
    generate_subtitles(setup.LanguageCodes.English)

    # FOR HINDI!
    google_interface.hi_tts_client.generate_audio_files()
    generate_subtitles(setup.LanguageCodes.Hindi)


def test():
    google_interface = GoogleInterface()

    language = setup.LanguageCodes.Hindi
    google_interface.translate_client.translate_sentences_from_file(language)


def download_and_modify_images():
    # _download_chapters()
    modify_all_images()
    modify_images_to_fit_screen()
    # _delete_temp_files()


if __name__ == "__main__":
    # REMEMBER TO RUN THIS FIRST AND THEN DELETE IMAGES
    # download_and_modify_images()

    main()

    # test()
