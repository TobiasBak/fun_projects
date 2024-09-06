from enum import Enum

from google.cloud import translate_v2 as translate

import setup
from utils import get_sentences_dict, append_to_file, get_images_missing_from_files, get_sentence_path


class TranslateClient:
    def __init__(self):
        self.client = translate.Client()

    def translate(self, language: setup.LanguageCodes, text: str) -> str:
        response = self.client.translate(text, target_language=language.value)

        return response['translatedText']

    def translate_sentences_from_file(self, language: setup.LanguageCodes):
        sentences_dict = get_sentences_dict()
        out_file = get_sentence_path(language)
        images = self._get_images_missing_for_language(language)
        print(f"Images missing for {language.value}: {images}")

        for key in images:
            print(f"Translating {key}...")
            translated_value = self.translate(language, sentences_dict[key])
            translated_value = translated_value.replace("&quot;", '')
            translated_value = translated_value.replace("&#39", '')
            append_to_file(out_file, f"{key};{translated_value}\n")

    def _get_images_missing_for_language(self, language: setup.LanguageCodes):
        return get_images_missing_from_files(setup.PATHS.IMAGE_DIR, get_sentence_path(language))


