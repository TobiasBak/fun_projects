import os

import numpy as np
from PIL import Image

TEMP_DIR = 'temp'
SPLIT_INDEXES_FILE = f'{TEMP_DIR}/split_indexes.csv'
IMAGES_DIR = f'{TEMP_DIR}/images'
OUT_DIR = 'out'
OUT_IMAGES_DIR = f'{OUT_DIR}/images'
IMAGE_MAX_HEIGHT = 1000


def modify_all_images():
    # if file exists delete it
    if os.path.exists(SPLIT_INDEXES_FILE):
        os.remove(SPLIT_INDEXES_FILE)

    images = os.listdir(IMAGES_DIR)
    print(f"Modifying {len(images)} images...")

    count = 0
    for image in images:
        _modify_image(f'{IMAGES_DIR}/{image}')

        # Helpful print
        if count % 100 == 0:
            print(f'{count}/{len(images)} images modified.')
        count += 1


def modify_images_to_fit_screen():
    images = os.listdir(IMAGES_DIR)
    images.sort(key=lambda x: int(x.split('.')[1]))

    split_indexes = _read_split_indexes()
    buffer = None  # Buffer will be at most 1 image, that is left over
    for image in images:
        image_split_indexes = split_indexes[image.replace('.jpg', '')]
        image_parts = _split_image(image, image_split_indexes)

        count = 0
        for image_part in image_parts:
            image_part_height = image_part.size[1]
            if image_part_height < IMAGE_MAX_HEIGHT / 2:
                buffer = image_part
                continue

            if buffer is not None:
                original_image_part = image_part.copy()
                image_part = Image.new('RGB', (image_part.width, image_part.height + buffer.height))
                image_part.paste(buffer, (0, 0))
                image_part.paste(original_image_part, (0, buffer.height))
                buffer = None

            # Downscale
            if image_part_height > IMAGE_MAX_HEIGHT:
                resized_image = _resize_image(image_part, new_height=IMAGE_MAX_HEIGHT)

            # Upscale
            if image_part_height < IMAGE_MAX_HEIGHT:
                resized_image = _resize_image(image_part, new_height=IMAGE_MAX_HEIGHT)

            _save_image_to_dir(resized_image, f'{OUT_IMAGES_DIR}/{_get_image_name(image)}.{count}.jpg')
            count += 1


def _remove_redundant_image_parts(img_path) -> list[int] | None:
    """
    Modifies an image by removing black and white rows that are more than 95% of the row.
    Returns the split_index which are the indexes that split the image.
    """
    # Iterate over each row
    black_or_white_rows = _find_black_or_white_rows(img_path)

    split_index_pairs = _get_split_indexes(black_or_white_rows)
    actual_indexes = _get_actual_indexes(split_index_pairs)

    img = Image.open(img_path)
    img_np_array = np.array(img)

    # Remove the black or white rows from the image array
    img_np_array = np.delete(img_np_array, black_or_white_rows, axis=0)

    # If image is empty after removing black or white rows, return
    if len(img_np_array) == 0:
        # Delete image
        os.remove(img_path)
        return None

    # Convert the modified array back to an image
    new_img = Image.fromarray(img_np_array)
    # Save the modified image with a new filename
    new_img.save(img_path)
    return actual_indexes


def _find_black_or_white_rows(img_path):
    # Open the image and convert it to grayscale
    img = Image.open(img_path).convert('L')
    # Convert the image data to a numpy array
    img_array = np.array(img)

    out = []

    i = -1
    for row in img_array:
        i += 1
        # Calculate the percentage of pixels that are black or white
        black_pixels = np.sum(row == 0)
        white_pixels = np.sum(row == 255)
        total_pixels = len(row)
        if black_pixels / total_pixels > 0.98 or white_pixels / total_pixels > 0.995:
            out.append(i)

    return out


def _get_split_indexes(black_or_white_rows) -> list[list]:
    split_indexes_pairs: list[list] = []
    pair_start = 0
    last_index = 0
    for i in black_or_white_rows:

        if i < last_index + 10:
            last_index = i
            continue

        split_indexes_pairs.append([pair_start, last_index])
        pair_start = i
        last_index = i

    split_indexes_pairs.append([pair_start, last_index])

    return split_indexes_pairs


def _get_actual_indexes(split_indexes: list[list]) -> list[int]:
    indexes = []
    pixels_removed = 0

    for start, end in split_indexes:
        indexes.append(start - pixels_removed)
        pixels_removed += end - start

    return indexes


def _write_indexes_to_file(indexes, image_name):
    # Ensure a directory to save the images
    os.makedirs(TEMP_DIR, exist_ok=True)

    with open(SPLIT_INDEXES_FILE, 'a') as file:
        file.write(f'{image_name},')
        file.write(','.join(map(str, indexes)) + '\n')


def _modify_image(image_path):
    actual_indexes = _remove_redundant_image_parts(image_path)
    if actual_indexes is None:
        return
    image = Image.open(image_path)
    end_index = image.height
    actual_indexes.append(end_index)

    # If there is more than one index in actual indexes, then check the difference of the last two indexes.
    # If there is a difference of more than 100 pixels, then remove the second to last index
    if len(actual_indexes) > 1 and actual_indexes[-1] - actual_indexes[-2] < 100:
        actual_indexes.pop(-2)

    image_name = _get_image_name(image_path)
    _write_indexes_to_file(actual_indexes, image_name)


def _get_image_name(image_path):
    return image_path.split('/')[-1].replace('.jpg', '')


def _read_split_indexes() -> dict:
    split_indexes = {}

    with open(SPLIT_INDEXES_FILE, 'r') as file:
        lines = file.readlines()

    for line in lines:
        indexes = line.split(',')
        image_name = indexes.pop(0)
        indexes[-1].replace('\n', '')
        # Convert the indexes from string to int
        indexes = list(map(int, indexes))
        split_indexes[image_name] = indexes

    return split_indexes


def _split_image(image, split_indexes) -> list[Image]:
    image_parts: list[Image] = []
    img = Image.open(f'{IMAGES_DIR}/{image}')

    for i in range(len(split_indexes) - 1):
        start = split_indexes[i]
        end = split_indexes[i + 1]
        image_part = img.crop((0, start, img.width, end))
        image_parts.append(image_part)

    return image_parts


def _save_image_to_dir(image, path):
    os.makedirs(OUT_IMAGES_DIR, exist_ok=True)
    image.save(path)


def _resize_image(image: Image, new_width=None, new_height=None) -> Image:
    aspect_ratio = image.width / image.height

    if new_width is None and new_height is None:
        return image

    if new_width is None:
        new_width = int(new_height * aspect_ratio)

    if new_height is None:
        new_height = int(new_width / aspect_ratio)

    return image.resize((new_width, new_height))

