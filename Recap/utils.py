import os


def get_name_from_path(path: str):
    # The paths are split by the '/' character
    return path.split('/')[-1]


def get_absolute_paths(directory: str):
    paths = []
    for file in os.listdir(directory):
        abs_path = os.path.abspath(os.path.join(directory, file))
        paths.append(abs_path)
    return paths
