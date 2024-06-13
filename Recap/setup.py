""" PLEASE FILL BELOW """
import os

DOWNLOAD_URL = 'https://toonily.com/webtoon/solo-leveling-005/'
CHAPTERS = [1, 10]
NAME_OF_BOOK = 'solo_leveling'

""" PLEASE DO NOT MODIFY BELOW """
NAME_AND_CHAPTERS = f'{NAME_OF_BOOK}_{CHAPTERS[0]}-{CHAPTERS[1]}'


class FILES:
    DESCRIPTIONS = f'eng.{NAME_AND_CHAPTERS}_generated_text.csv'
    TEXT_ON_PICTURES = f'eng.{NAME_AND_CHAPTERS}_text_on_pictures.csv'
    SENTENCES = f'eng.{NAME_AND_CHAPTERS}_generated_sentences.csv'


class PATHS:
    OUT_IMAGE_DIR = 'out/images'
    OUT_TEXT_DIR = 'out/text'
    OUT_AUDIO_DIR = 'out/audio'
    DESCRIPTIONS = f'{OUT_TEXT_DIR}/{FILES.DESCRIPTIONS}'
    TEXT_ON_PICTURES = f'{OUT_TEXT_DIR}/{FILES.TEXT_ON_PICTURES}'
    SENTENCES = f'{OUT_TEXT_DIR}/{FILES.SENTENCES}'


# Generate directories if they do not exist
for path in [PATHS.OUT_IMAGE_DIR, PATHS.OUT_TEXT_DIR, PATHS.OUT_AUDIO_DIR]:
    os.makedirs(path, exist_ok=True)
