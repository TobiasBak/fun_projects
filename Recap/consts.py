import os

OUT_DIR = 'out'
OUT_IMAGE_DIR = f'{OUT_DIR}/images'
OUT_TEXT_DIR = f'{OUT_DIR}/text'


os.makedirs(OUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUT_TEXT_DIR, exist_ok=True)

