import os

OUT_DIR = 'out'
OUT_IMAGE_DIR = f'{OUT_DIR}/images'
OUT_TEXT_DIR = f'{OUT_DIR}/text'

FILE_NAME_DESCRIPTIVE_TEXT = '_generated_text'
FILE_NAME_TEXT_ON_PICTURES = '_text_on_pictures'
FILE_NAME_GENERATED_SENTENCES = '_generated_sentences'


os.makedirs(OUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUT_TEXT_DIR, exist_ok=True)

