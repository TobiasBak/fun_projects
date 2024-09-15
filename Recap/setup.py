""" PLEASE FILL BELOW """
import os
from enum import Enum

DOWNLOAD_URL = 'https://toonily.com/webtoon/sss-class-suicide-hunter/'
CHAPTERS = [11, 20]
NAME_OF_BOOK = 'suicide_hunter'

""" PLEASE DO NOT MODIFY BELOW """
NAME_AND_CHAPTERS = f'{NAME_OF_BOOK}_{CHAPTERS[0]}-{CHAPTERS[1]}'


class LanguageCodes(Enum):
    English = 'en'
    Hindi = 'hi'


class FILES:
    DESCRIPTIONS = f'{NAME_AND_CHAPTERS}_descriptions.csv'
    SENTENCES = f'{NAME_AND_CHAPTERS}_generated_sentences.csv'


class PATHS:
    RAW_IMAGE_DIR = 'temp/images/raw'
    IMAGE_DIR = 'temp/images/altered'
    OUT_TEXT_DIR = 'out/text'
    AUDIO_DIR = 'temp/audio'
    SUBTITLE_DIR = 'temp/subtitles'
    OUT_VIDEO_DIR = 'out/videos'
    DESCRIPTIONS = f'{OUT_TEXT_DIR}/{FILES.DESCRIPTIONS}'
    SENTENCES = f'{OUT_TEXT_DIR}/{FILES.SENTENCES}'


# Generate directories if they do not exist
for path in [PATHS.RAW_IMAGE_DIR, PATHS.IMAGE_DIR, PATHS.OUT_TEXT_DIR, PATHS.AUDIO_DIR, PATHS.SUBTITLE_DIR,
             PATHS.OUT_VIDEO_DIR]:
    os.makedirs(path, exist_ok=True)

for value in LanguageCodes:
    os.makedirs(f'temp/timings/{value.value}', exist_ok=True)
    os.makedirs(f'temp/audio/{value.value}', exist_ok=True)
    os.makedirs(f'temp/videos/{value.value}', exist_ok=True)
    os.makedirs(f'temp/subtitles/{value.value}', exist_ok=True)
    os.makedirs(f'out/videos/video_parts/{value.value}', exist_ok=True)


