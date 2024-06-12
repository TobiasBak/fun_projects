import os
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

import pytesseract
from PIL import Image

from consts import OUT_IMAGE_DIR, OUT_TEXT_DIR
from utils import append_to_file

import easyocr

# Set up the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def _process_image_easyocr(image: Image):
    reader = easyocr.Reader(['en'])

    text = reader.readtext(image)

    for detection in text:
        print(detection[1])

    return text


def _process_image_pytesseract(image_path: str):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image, config='-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 3')
    print(text)



def _process_image_microsoft(image_path: str):
    image = Image.open(image_path)

    # Grayscale the image
    image.convert('L')

    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_text)


def process_images(name_of_run: str, directory: str):
    text_on_images = {}
    for file in os.listdir(directory):
        print(file)
        if file.endswith(".jpg"):
            text = _process_image_microsoft(f"{OUT_IMAGE_DIR}/{file}")
            text_on_images[file] = text

    for name, value in text_on_images.items():
        text = f"{name},{value}\n"
        filename = f'{OUT_TEXT_DIR}/{name_of_run}_text_on_pictures.csv'
        append_to_file(filename, text)




from rapidocr_onnxruntime import RapidOCR, VisRes


engine = RapidOCR()
vis = VisRes()

image_path = "out/images/1.0.0.jpg"
img = Image.open(image_path)


result = engine(img)

texts = [item[1] for item in result[0]]
text = " ".join(texts)
print(text)

