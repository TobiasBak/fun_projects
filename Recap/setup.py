""" PLEASE FILL BELOW """
import os
from enum import Enum

DOWNLOAD_URL = 'https://toonily.com/webtoon/solo-leveling-005/'
CHAPTERS = [41, 41]
NAME_OF_BOOK = 'solo_leveling'


class LanguageCodes(Enum):
    English = 'en'
    Hindi = 'hi'


STORY = f"""
The story is about a young man, who lives in a world where you raid dungeons to get stronger. 
One day he finds himself in a dungeon, where he dies but gets resurrected.
After the resurrection, he starts getting stronger by doing tasks and killing beasts in dungeons.
He has no limit to his strength but all other hunters are limited.
"""
AllOWED_NAMES = f"""Sung Jin-Woo, Miss Ju-Hee"""


""" PLEASE DO NOT MODIFY BELOW """
NAME_AND_CHAPTERS = f'{NAME_OF_BOOK}_{CHAPTERS[0]}-{CHAPTERS[1]}'


class FILES:
    DESCRIPTIONS = f'en.{NAME_AND_CHAPTERS}_descriptions.csv'
    SENTENCES = f'en.{NAME_AND_CHAPTERS}_generated_sentences.csv'


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
for path in [PATHS.RAW_IMAGE_DIR, PATHS.IMAGE_DIR, PATHS.OUT_TEXT_DIR, PATHS.AUDIO_DIR, PATHS.SUBTITLE_DIR, PATHS.OUT_VIDEO_DIR]:
    os.makedirs(path, exist_ok=True)

for value in LanguageCodes:
    os.makedirs(f'temp/timings/{value.value}', exist_ok=True)
    os.makedirs(f'temp/audio/{value.value}', exist_ok=True)
    os.makedirs(f'temp/videos/{value.value}', exist_ok=True)
    os.makedirs(f'temp/subtitles/{value.value}', exist_ok=True)


os.makedirs('temp/timings', exist_ok=True)
os.makedirs('temp/videos', exist_ok=True)