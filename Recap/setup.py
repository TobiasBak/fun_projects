""" PLEASE FILL BELOW """
import os

DOWNLOAD_URL = 'https://toonily.com/webtoon/solo-leveling-005/'
CHAPTERS = [1, 2]
NAME_OF_BOOK = 'solo_leveling'
TTS_VOICE_LAN_CODE = "en-US"
TTS_VOICE_NAME = "en-US-Neural2-J"
TTS_SPEAKING_RATE = 1.15

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
    DESCRIPTIONS = f'eng.{NAME_AND_CHAPTERS}_generated_text.csv'
    TEXT_ON_PICTURES = f'eng.{NAME_AND_CHAPTERS}_text_on_pictures.csv'
    SENTENCES = f'eng.{NAME_AND_CHAPTERS}_generated_sentences.csv'


class PATHS:
    OUT_IMAGE_DIR = 'out/images'
    OUT_TEXT_DIR = 'out/text'
    OUT_AUDIO_DIR = 'out/audio'
    OUT_SUBTITLE_DIR = 'out/subtitles'
    OUT_VIDEO_DIR = 'out/videos'
    DESCRIPTIONS = f'{OUT_TEXT_DIR}/{FILES.DESCRIPTIONS}'
    TEXT_ON_PICTURES = f'{OUT_TEXT_DIR}/{FILES.TEXT_ON_PICTURES}'
    SENTENCES = f'{OUT_TEXT_DIR}/{FILES.SENTENCES}'


# Generate directories if they do not exist
for path in [PATHS.OUT_IMAGE_DIR, PATHS.OUT_TEXT_DIR, PATHS.OUT_AUDIO_DIR, PATHS.OUT_SUBTITLE_DIR, PATHS.OUT_VIDEO_DIR]:
    os.makedirs(path, exist_ok=True)
