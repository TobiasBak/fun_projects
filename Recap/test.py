import setup
from FileInterfacce import FileInterface
from cleanup import clean_descriptions_for_unnecessary_lines
from google.googleInterface import GoogleInterface
from imageModifier import modify_all_images
from main import download_chapters


def test():
    # Use this method to test behaviour
    print("TESTING...")
    clean_descriptions_for_unnecessary_lines()




if __name__ == "__main__":
    test()







def create_intro_audio():
    interface = GoogleInterface()
    interface.en_tts_client.generate_audio("test",
                                           text="Today we are doing another amazing recap. If you enjoy this, please like and subscribe. If you have any requests, please let me know in the comments. Let's begin!")