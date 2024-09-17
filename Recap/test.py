import setup
from FileInterfacce import FileInterface
from imageModifier import modify_all_images
from main import _download_chapters


def test():
    # Use this method to test behaviour
    print("TESTING...")
    _download_chapters()
    modify_all_images()

    fi = FileInterface()

    print(fi.get_images_missing_from_file(setup.PATHS.DESCRIPTIONS))




if __name__ == "__main__":
    test()