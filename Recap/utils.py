import os


def get_name_from_path(path: str):
    # The paths are split by the '/' character or the \ or \\ characters
    # depending on the operating system
    path_parts = path.split('/')
    if len(path_parts) == 1:
        path_parts = path.split('\\')

    if len(path_parts) == 1:
        path_parts = path.split('\\\\')

    return path_parts[-1]


def get_absolute_paths(directory: str):
    paths = []
    for file in os.listdir(directory):
        abs_path = os.path.abspath(os.path.join(directory, file))
        paths.append(abs_path)
    return paths


def append_to_file(file_path: str, text: str):
    with open(file_path, 'a') as file:
        file.write(text)
