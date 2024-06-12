import os
from PIL import Image
from consts import OUT_IMAGE_DIR, OUT_TEXT_DIR
from utils import append_to_file, get_lines_from_file
from rapidocr_onnxruntime import RapidOCR
from concurrent.futures import ThreadPoolExecutor, as_completed

engine = RapidOCR()


def _process_image_rapidocr(image_path: str):
    image = Image.open(image_path)

    result = engine(image)

    if result == (None, None):
        return ""

    texts = [item[1] for item in result[0]]
    text = " ".join(texts)
    return text


def find_text_on_images(name_of_run: str):
    text_file_name = f'{OUT_TEXT_DIR}/eng.{name_of_run}_text_on_pictures.csv'
    text_file_dict = {}

    lines = get_lines_from_file(text_file_name)
    for line in lines:
        parts = line.split(';')
        text_file_dict[parts[0]] = parts[1].replace('\n', '')

    images_processed = text_file_dict.keys()

    text_on_images = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(_process_image_rapidocr, f"{OUT_IMAGE_DIR}/{file}"): file for file in
                   os.listdir(OUT_IMAGE_DIR) if file.endswith(".jpg") and file not in images_processed}

        for future in as_completed(futures):
            file = futures[future]
            try:
                text = future.result()
                text_on_images[file] = text
                print(f"{file.ljust(10)}{text}")
            except Exception as e:
                print(f"Exception occurred while processing image {file}: {e}")

    for name, value in text_on_images.items():
        text = f"{name};{value}\n"
        append_to_file(text_file_name, text)
