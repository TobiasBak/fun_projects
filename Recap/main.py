import os
import shutil
import time

import setup
from Recap.cleanup import clean_descriptions_for_unnecessary_lines, clean_images
from Recap.imageModifier import modify_all_images
from Recap.utils import get_dict_from_file, get_all_images, get_sentence_path
from fetchManhwa import _download_images_toonily, download_chapters
from google.googleInterface import GoogleInterface
from string_optimizier import optimize_descriptions, optimize_sentences_errors, optimize_description_quotes
from subtitles import generate_subtitles
from videoEditing import generate_image_videos, generate_concated_video, add_music, concate_video_parts

"""
FILL OUT VALUES IN SETUP.PY BEFORE RUNNING SCRIPT
"""


def main():
    google_interface = GoogleInterface()

    # Description generation
    google_interface.gemini_client.generate_descriptive_text()
    optimize_descriptions()
    optimize_description_quotes()

    time.sleep(1)
    _find_images_with_missing_texts(setup.PATHS.IMAGE_DIR, setup.PATHS.DESCRIPTIONS)

    clean_images()
    clean_descriptions_for_unnecessary_lines()  # Not necessary, but nice to have

    # Sentence generation
    google_interface.gemini_client.generate_sentences_gemini()
    google_interface.gemini_client.remove_duplicate_sentences(setup.LanguageCodes.English) #todo: move this to string modifier or sometehing

    # Optimize sentences
    optimize_sentences_errors(setup.LanguageCodes.English)

    # Find images missing texts (Maybe make return a boolean, where of we do shit. But we need to be careful of loops, probably exit if we get harmful etc.
    _find_images_with_missing_texts(setup.PATHS.IMAGE_DIR, get_sentence_path())

    # TTS GENERATION
    google_interface.en_tts_client.generate_audio_files()
    generate_subtitles(setup.LanguageCodes.English)


def hindi():
    google_interface = GoogleInterface()
    google_interface.translate_client.translate_sentences_from_file(setup.LanguageCodes.Hindi)
    google_interface.hi_tts_client.generate_audio_files()
    generate_subtitles(setup.LanguageCodes.Hindi)


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
        if image not in generated_text_dict.keys():
            print(f"Image {image} is missing text in {text_file_path}!")
            print(f"Generated text: {generated_text_dict.get(image)}")
            print("")
            raise Exception(f"Image {image} is missing text")


if __name__ == "__main__":
    # REMEMBER TO RUN THIS FIRST AND THEN DELETE IMAGES
    download_chapters()
    modify_all_images()

    main()

    generate_image_videos(setup.LanguageCodes.English)
    generate_concated_video(setup.LanguageCodes.English)
    add_music(setup.LanguageCodes.English)

    concate_video_parts(setup.LanguageCodes.English)
