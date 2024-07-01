import os
from PIL import Image

import setup
from utils import append_to_file, get_dict_from_file
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


def find_text_on_images(directory: str):
    text_file_dict = get_dict_from_file(setup.PATHS.TEXT_ON_PICTURES)
    images_processed = text_file_dict.keys()

    print(f"Finding text on images in {directory}...")

    text_on_images = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(_process_image_rapidocr, f"{directory}/{file}"): file for file in
                   os.listdir(directory) if file.endswith(".jpg") and file not in images_processed}

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
        append_to_file(setup.PATHS.TEXT_ON_PICTURES, text)
