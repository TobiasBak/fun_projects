# The goal of this file is to take all images from temp/images and cut them at 1700 pixels height if they are taller than that.
import os

import numpy as np
from PIL import Image

def remove_redundant_image_parts(img_path) -> list[int]:
    """
    Modifies an image by removing black and white rows that are more than 95% of the row.
    Returns the split_index which are the indexes that split the image.
    """
    # Iterate over each row
    black_or_white_rows = find_black_or_white_rows(img_path)

    split_index_pairs = get_split_indexes(black_or_white_rows)
    actual_indexes = get_actual_indexes(split_index_pairs)

    img = Image.open(img_path)
    img_np_array = np.array(img)

    # Remove the black or white rows from the image array
    img_np_array = np.delete(img_np_array, black_or_white_rows, axis=0)
    # Convert the modified array back to an image
    new_img = Image.fromarray(img_np_array)
    # Save the modified image with a new filename
    new_img.save(img_path)
    return actual_indexes


def find_black_or_white_rows(img_path):
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
        if black_pixels / total_pixels > 0.95 or white_pixels / total_pixels > 0.95:
            out.append(i)
    print(f"Returning {out}")
    return out


def get_split_indexes(black_or_white_rows) -> list[list]:
    split_indexes_pairs: list[list] = []
    pair_start = 0
    last_index = 0
    for i in black_or_white_rows:
        print(f"i: {i}, pair_start: {pair_start}, last_index: {last_index}")

        if i < last_index + 10:
            last_index = i
            continue

        split_indexes_pairs.append([pair_start, last_index])
        pair_start = i
        last_index = i

    split_indexes_pairs.append([pair_start, last_index])

    print(f"Split indexes pairs: {split_indexes_pairs}")

    return split_indexes_pairs


def get_actual_indexes(split_indexes: list[list]) -> list[int]:
    indexes = []
    pixels_removed = 0

    for start, end in split_indexes:
        indexes.append(start - pixels_removed)
        pixels_removed += end - start

    indexes.pop(0) # First index is always 0
    return indexes


def write_indexes_to_file(indexes, image_name):
    dir_name = 'temp/image_split_indexes'

    # Ensure a directory to save the images
    os.makedirs(dir_name, exist_ok=True)

    with open(f'{dir_name}/{image_name}.csv', 'w') as file:
        file.write(','.join(map(str, indexes)))


def modify_image(image_path):
    actual_indexes = remove_redundant_image_parts(image_path)
    image = Image.open(image_path)
    end_index = image.height
    actual_indexes.append(end_index)

    image_name = image_path.split('/')[-1].replace('.jpg', '')
    write_indexes_to_file(actual_indexes, image_name)



