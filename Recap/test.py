import setup
from FileInterfacce import FileInterface
from cleanup import clean_descriptions_for_unnecessary_lines
from fetchManhwa import _get_chapter_urls_mangadex_selenium, select_newest_upload, _download_images_toonily
from google.googleInterface import GoogleInterface
from imageModifier import modify_all_images
from main import download_chapters
from string_optimizier import optimize_sentences_errors
from videoEditing import generate_image_videos, generate_concated_video, add_music


def test():
    # Use this method to test behaviour
    print("TESTING...")
    # download_chapters()
    # _get_chapter_urls_mangadex("https://mangadex.org/title/de3745b8-4a77-4f2c-8929-68395360793f/the-ranker-s-guide-to-living-an-ordinary-life")
    # chapter_dict = _get_chapter_urls_mangadex_selenium("https://mangadex.org/title/de3745b8-4a77-4f2c-8929-68395360793f/the-ranker-s-guide-to-living-an-ordinary-life")
    # new_chapter_dict = select_newest_upload(chapter_dict)
    # print(new_chapter_dict)
    # _get_chapter_urls_mangadex("https://toonily.com/webtoon/the-rankers-guide-to-live-an-ordinary-life/")
    _download_images_toonily("https://toonily.com/webtoon/the-rankers-guide-to-live-an-ordinary-life/", [1, 1])




if __name__ == "__main__":
    test()







def create_intro_audio():
    interface = GoogleInterface()
    interface.en_tts_client.generate_audio("test",
                                           text="Today we are doing another amazing recap. If you enjoy this, please like and subscribe. If you have any requests, please let me know in the comments. Let's begin!")