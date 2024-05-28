import time

import pyautogui
import pytesseract
from PIL import Image

# Set up the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def capture_screenshot(region: tuple[int, int, int, int]) -> Image:
    screenshot: Image = pyautogui.screenshot(region=region)
    return screenshot


def process_screenshot(image: Image):
    # Convert the image to grayscale
    gray_image = image.convert('L')
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(gray_image)
    return text


def read_string_from_game(region: tuple[int, int, int, int]) -> str:
    """
    region is a tuple of 4 integers (x1, y1, x2, y2) representing the region of the screen to capture
    """
    # Capture a screenshot
    screenshot = capture_screenshot(region)
    # Process the screenshot to extract text
    extracted_text = process_screenshot(screenshot)
    return extracted_text


def convert_read_to_int(text: str) -> int:
    text_parts = text.split(' ')
    out = 0
    ints_fount = 0
    for part in text_parts:
        try:
            print(part)
            out += int(part)
            ints_fount += 1
        except ValueError:
            pass
    if ints_fount == 0:
        return 0
    return out
