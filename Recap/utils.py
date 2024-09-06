import os

import setup


def get_name_from_path(path: str):
    # The paths are split by the '/' character or the \ or \\ characters
    # depending on the operating system
    path_parts = path.split('/')
    if len(path_parts) == 1:
        path_parts = path.split('\\')

    if len(path_parts) == 1:
        path_parts = path.split('\\\\')

    return path_parts[-1]


def get_absolute_path(file_path: str):
    return os.path.abspath(os.path.join(file_path))


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
                    decode_line = decode_line.replace('\r', '').replace('\n', '')
                    if decode_line == '\r\n':
                        continue
                    lines.append(decode_line)
                except UnicodeDecodeError as e:
                    print(f"Error occurred while reading line {i} in file {file_path}: {e}")
    except FileNotFoundError:
        pass

    return lines


def get_images_missing_from_files(image_dir: str, text_file_path: str):
    images = get_sorted_list_of_images(image_dir)

    text_file_dict = get_dict_from_file(text_file_path)

    missing_images = []
    for image in images:
        if image not in text_file_dict.keys():
            missing_images.append(image)

    return missing_images


def get_all_images(directory: str = setup.PATHS.IMAGE_DIR):
    images = []
    for file in os.listdir(directory):
        if file.endswith(".jpg"):
            images.append(file)
    return images


def get_sorted_list_of_images(directory: str = setup.PATHS.IMAGE_DIR):
    images = get_all_images(directory)

    def sort_key(image_name: str):
        # Split the filename on '.', convert the parts to integers, and return as a tuple
        parts = image_name.split('.')[:2]
        return tuple(int(part) for part in parts)

    # Sort the images using the custom sort key
    images.sort(key=sort_key)

    return images


def get_dict_from_file(file_path: str):
    file_dict = {}
    lines = get_lines_from_file(file_path)

    if len(lines) == 0:
        return file_dict

    for line in lines:
        parts = line.split(';')

        if len(parts) == 1:
            continue

        file_dict[parts[0]] = parts[1].replace('\n', '')
    return file_dict


def get_sentences_dict(language: setup.LanguageCodes = setup.LanguageCodes.English):
    sentences_dict = {}
    sentences_path = get_sentence_path(language)
    lines = get_lines_from_file(sentences_path)
    for line in lines:
        parts = line.split(';')
        sentences_dict[parts[0]] = parts[1].replace('\n', '')

    return sentences_dict


def get_sentence_path(language: setup.LanguageCodes = setup.LanguageCodes.English):
    parts = setup.PATHS.SENTENCES.split('/')
    path = f"{parts[0]}/{parts[1]}/{language.value}.{parts[2]}"
    return path


def get_elevenlabs_api_keys() -> list:
    lines = get_lines_from_file("hidden/eleven_lab_keys.csv")
    keys = []
    for line in lines:
        parts = line.split(';')
        api_key = parts[2].replace('\n', '')
        keys.append(api_key)

    return keys
