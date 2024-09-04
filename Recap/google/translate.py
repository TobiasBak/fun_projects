from enum import Enum

from google.cloud import translate_v2 as translate

import setup
from utils import get_sentences_dict, append_to_file, get_images_missing_from_files


class LanguageCodes(Enum):
    English = 'en'
    Hindi = 'hi'


class TranslateClient:
    def __init__(self):
        self.client = translate.Client()

    def translate(self, language: LanguageCodes, text: str) -> str:
        response = self.client.translate(text, target_language=language.value)

        return response['translatedText']

    def translate_sentences_from_file(self, language: LanguageCodes):
        sentences_dict = get_sentences_dict()
        out_file = self._get_language_file(language)
        images = self._get_images_missing_for_language(language)

        for key in images:
            print(f"Translating {key}...")
            translated_value = self.translate(language, sentences_dict[key])
            translated_value = translated_value.replace("&quot;", '"')
            append_to_file(out_file, f"{key};{translated_value}\n")

    def _get_images_missing_for_language(self, language: LanguageCodes):
        return get_images_missing_from_files(setup.PATHS.IMAGE_DIR, self._get_language_file(language))

    def _get_language_file(self, language: LanguageCodes):
        parts = setup.PATHS.SENTENCES.split('.')
        return f"{parts[0].replace("eng", f"{language.value}")}.{parts[1]}.{parts[2]}"
