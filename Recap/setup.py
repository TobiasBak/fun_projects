""" PLEASE FILL BELOW """
import os
from enum import Enum

DOWNLOAD_URL = 'https://toonily.com/webtoon/wife-demon-queen/chapter-1/'
CHAPTERS = [1, 1]
NAME_OF_BOOK = 'test'  # Has to be lowercase

""" PLEASE DO NOT MODIFY BELOW """
NAME_AND_CHAPTERS = f'{NAME_OF_BOOK}_{CHAPTERS[0]}-{CHAPTERS[1]}'


class LanguageCodes(Enum):
    English = 'en'
    Hindi = 'hi'


class FILES:
    DESCRIPTIONS = f'{NAME_AND_CHAPTERS}_descriptions.csv'
    SENTENCES = f'{NAME_AND_CHAPTERS}_generated_sentences.csv'


class PATHS:
    OUT_TEXT_DIR = 'out/text'
    OUT_VIDEO_PARTS_DIR = 'out/videos/video_parts'
    OUT_VIDEO_DIR = 'out/videos'
    RAW_IMAGE_DIR = 'temp/images/raw'
    IMAGE_DIR = 'temp/images/altered'
    AUDIO_DIR = 'temp/audio'
    SUBTITLE_DIR = 'temp/subtitles'
    VIDEO_DIR = 'temp/videos'
    TIMINGS_DIR = 'temp/timings'
    DESCRIPTIONS = f'{OUT_TEXT_DIR}/{FILES.DESCRIPTIONS}'


# Generate directories if they do not exist
for path in [PATHS.RAW_IMAGE_DIR, PATHS.IMAGE_DIR, PATHS.OUT_TEXT_DIR, PATHS.AUDIO_DIR, PATHS.SUBTITLE_DIR,
             PATHS.VIDEO_DIR, PATHS.TIMINGS_DIR, PATHS.OUT_VIDEO_PARTS_DIR, PATHS.OUT_VIDEO_DIR]:
    os.makedirs(path, exist_ok=True)

for value in LanguageCodes:
    os.makedirs(f'{PATHS.TIMINGS_DIR}/{value.value}', exist_ok=True)
    os.makedirs(f'{PATHS.AUDIO_DIR}/{value.value}', exist_ok=True)
    os.makedirs(f'{PATHS.VIDEO_DIR}/{value.value}', exist_ok=True)
    os.makedirs(f'{PATHS.SUBTITLE_DIR}/{value.value}', exist_ok=True)
    os.makedirs(f'{PATHS.OUT_VIDEO_PARTS_DIR}/{value.value}', exist_ok=True)
    os.makedirs(f'{PATHS.OUT_VIDEO_DIR}/{value.value}', exist_ok=True)
