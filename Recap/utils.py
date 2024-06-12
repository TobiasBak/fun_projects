import os

from Recap import consts


def get_name_from_path(path: str):
    # The paths are split by the '/' character or the \ or \\ characters
    # depending on the operating system
    path_parts = path.split('/')
    if len(path_parts) == 1:
        path_parts = path.split('\\')

    if len(path_parts) == 1:
        path_parts = path.split('\\\\')

    return path_parts[-1]


def get_absolute_paths(directory: str) -> list:
    paths = []
    for file in os.listdir(directory):
        abs_path = os.path.abspath(os.path.join(directory, file))
        paths.append(abs_path)
    return paths


def get_absolute_paths_from_files(directory: str, files: list) -> list:
    paths = []
    for file in files:
        abs_path = os.path.abspath(os.path.join(directory, file))
        paths.append(abs_path)
    return paths


def get_absolute_path(directory, file_path: str):
    return os.path.abspath(os.path.join(directory, file_path))


def append_to_file(file_path: str, text: str):
    if text == "" or text == '\r\n':
        return
    text = text.replace('\n', '').replace('\r', '')  # Correctly reassign the result
    with open(file_path, 'a', encoding='utf-8') as file:  # Open the file in text mode with utf-8 encoding
        file.write(text + '\n')


def append_to_file_list(file_path: str, list_of_text: list):
    for text in list_of_text:
        append_to_file(file_path, text)


def get_lines_from_file(file_path: str):
    lines = []
    try:
        with open(file_path, 'rb') as file:
            for i, line in enumerate(file):
                try:
                    decode_line = line.decode('utf-8')
                    if decode_line == '\r\n':
                        continue
                    lines.append(decode_line)
                except UnicodeDecodeError as e:
                    print(f"Error occurred while reading line {i} in file {file_path}: {e}")
    except FileNotFoundError:
        pass

    return lines


def get_images_missing_from_files(image_dir: str, text_file_path: str):
    images = []
    for file in os.listdir(image_dir):
        if file.endswith(".jpg"):
            images.append(file)

    text_file_dict = {}
    lines = get_lines_from_file(text_file_path)
    for line in lines:
        parts = line.split(';')
        text_file_dict[parts[0]] = parts[1].replace('\n', '')

    missing_images = []
    for image in images:
        if image not in text_file_dict.keys():
            missing_images.append(image)

    return missing_images


def get_all_images(directory: str = consts.OUT_IMAGE_DIR):
    images = []
    for file in os.listdir(directory):
        if file.endswith(".jpg"):
            images.append(file)
    return images


def get_dict_from_file(file_path: str):
    file_dict = {}
    lines = get_lines_from_file(file_path)
    for line in lines:
        parts = line.split(';')
        file_dict[parts[0]] = parts[1].replace('\n', '')
    return file_dict
