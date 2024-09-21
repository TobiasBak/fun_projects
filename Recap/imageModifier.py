import math
import os

import numpy as np
from PIL import Image

import setup
from Recap.utils import get_sorted_list_of_images

TEMP_DIR = 'temp'
TEMP_SPLIT_INDEXES_FILE = f'{TEMP_DIR}/split_indexes.csv'
IMAGE_MAX_HEIGHT = 1000
ALLOWED_SCALING_FACTOR = 1


# Todo make this image height be dependent on the height of the original image


def modify_all_images():
    # if image directory is not empty, skip modifying images
    if os.listdir(setup.PATHS.IMAGE_DIR):
        print("Image directory is not empty, skipping image modification...")
        return

    # if file exists delete it
    if os.path.exists(TEMP_SPLIT_INDEXES_FILE):
        os.remove(TEMP_SPLIT_INDEXES_FILE)

    images = os.listdir(setup.PATHS.RAW_IMAGE_DIR)
    print(f"Modifying {len(images)} images...")

    count = 0
    for image in images:
        _modify_image(f'{setup.PATHS.RAW_IMAGE_DIR}/{image}')

        # Helpful print
        if count % 100 == 0:
            print(f'{count}/{len(images)} images modified.')
        count += 1

    modify_images_to_fit_screen2()


def get_letter_from_count(count: int):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet[count % len(alphabet)]


def modify_images_to_fit_screen():
    images = get_sorted_list_of_images(setup.PATHS.RAW_IMAGE_DIR)

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

            if image_part.height > (4 * IMAGE_MAX_HEIGHT):
                # Split the image into four parts and save each part
                image_part_1 = image_part.crop((0, 0, image_part.width, image_part.height // 4))
                image_part_2 = image_part.crop((0, image_part.height // 4, image_part.width, image_part.height // 2))
                image_part_3 = image_part.crop(
                    (0, image_part.height // 2, image_part.width, 3 * image_part.height // 4))
                image_part_4 = image_part.crop((0, 3 * image_part.height // 4, image_part.width, image_part.height))
                resized_image_1 = _scale_image(image_part_1)
                resized_image_2 = _scale_image(image_part_2)
                resized_image_3 = _scale_image(image_part_3)
                resized_image_4 = _scale_image(image_part_4)
                resized_image_1.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.0.jpg')
                resized_image_2.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.1.jpg')
                resized_image_3.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.2.jpg')
                resized_image_4.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.3.jpg')
                count += 1
                continue
            elif image_part.height > (3 * IMAGE_MAX_HEIGHT):
                # Split the image into three parts and save each part
                image_part_top = image_part.crop((0, 0, image_part.width, image_part.height // 3))
                image_part_middle = image_part.crop(
                    (0, image_part.height // 3, image_part.width, 2 * image_part.height // 3))
                image_part_bottom = image_part.crop(
                    (0, 2 * image_part.height // 3, image_part.width, image_part.height))
                resized_image_top = _scale_image(image_part_top)
                resized_image_middle = _scale_image(image_part_middle)
                resized_image_bottom = _scale_image(image_part_bottom)
                resized_image_top.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.0.jpg')
                resized_image_middle.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.1.jpg')
                resized_image_bottom.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.2.jpg')
                count += 1
                continue
            elif image_part.height > (1.5 * IMAGE_MAX_HEIGHT):
                # Split the image at the middle and save both images
                image_part_top = image_part.crop((0, 0, image_part.width, image_part.height // 2))
                image_part_bottom = image_part.crop((0, image_part.height // 2, image_part.width, image_part.height))
                resized_image_top = _scale_image(image_part_top)
                resized_image_bottom = _scale_image(image_part_bottom)
                resized_image_top.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.0.jpg')
                resized_image_bottom.save(
                    f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.1.jpg')
                count += 1
                continue

            resized_image = _scale_image(image_part)

            if resized_image is None:
                continue

            resized_image.save(f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.jpg')

            count += 1

    raise Exception("Modifying images is complete, please clean images")


def modify_images_to_fit_screen2():
    images = get_sorted_list_of_images(setup.PATHS.RAW_IMAGE_DIR)

    split_indexes = _read_split_indexes()
    buffer = None  # Buffer will be at most 1 image, that is left over
    for image in images:
        image_split_indexes = split_indexes[image.replace('.jpg', '')]
        image_parts = _split_image(image, image_split_indexes)

        count = 0
        print(f"Modifying image {image}...")
        print(f"Image parts: {len(image_parts)}")
        for image_part in image_parts:
            image_part_height = image_part.size[1]
            if image_part_height < IMAGE_MAX_HEIGHT / 2 and buffer is None:
                buffer = image_part
                continue

            if buffer is not None:
                print(f"Created new image part")
                original_image_part = image_part.copy()
                image_part = Image.new('RGB', (image_part.width, image_part.height + buffer.height))
                image_part.paste(buffer, (0, 0))
                image_part.paste(original_image_part, (0, buffer.height))
                buffer = None

            num_images = image_part.height / (IMAGE_MAX_HEIGHT * ALLOWED_SCALING_FACTOR)
            if num_images > 1:
                num_images = math.floor(num_images)
            else:
                num_images = 1

            for i in range(num_images):
                start = i * IMAGE_MAX_HEIGHT * ALLOWED_SCALING_FACTOR
                end = min((i + 1) * IMAGE_MAX_HEIGHT * ALLOWED_SCALING_FACTOR, image_part.height)
                sub_image_part = image_part.crop((0, start, image_part.width, end))
                resized_image = _scale_image(sub_image_part)
                if resized_image is not None:
                    resized_image.save(
                        f'{setup.PATHS.IMAGE_DIR}/{_get_image_name(image)}.{get_letter_from_count(count)}.{i}.jpg')
            count += 1

    raise Exception("Modifying images is complete, please clean images")


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
        if black_pixels / total_pixels > 0.98 or white_pixels / total_pixels > 0.99:
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

    with open(TEMP_SPLIT_INDEXES_FILE, 'a') as file:
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

    with open(TEMP_SPLIT_INDEXES_FILE, 'r') as file:
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
    img = Image.open(f'{setup.PATHS.RAW_IMAGE_DIR}/{image}')

    for i in range(len(split_indexes) - 1):
        start = split_indexes[i]
        end = split_indexes[i + 1]
        image_part = img.crop((0, start, img.width, end))
        image_parts.append(image_part)

    return image_parts


def _resize_image(image: Image, new_width=None, new_height=None) -> Image:
    aspect_ratio = image.width / image.height

    if new_width is None and new_height is None:
        return image

    if new_width is None:
        new_width = int(new_height * aspect_ratio)

    if new_height is None:
        new_height = int(new_width / aspect_ratio)

    # Check if the new height is more than 1.5 times the original height
    if new_height > 1.25 * image.height:
        new_height = int(1.25 * image.height)
        new_width = int(new_height * aspect_ratio)

    return image.resize((new_width, new_height))


def _scale_image(image) -> Image:
    resized_image = None

    # Downscale
    if image.height >= IMAGE_MAX_HEIGHT:
        resized_image = _resize_image(image, new_height=IMAGE_MAX_HEIGHT)

    # Upscale
    if image.height < IMAGE_MAX_HEIGHT:
        resized_image = _resize_image(image, new_height=IMAGE_MAX_HEIGHT)

    return resized_image
