from fetchManhwa import download_images
from imageModifier import modify_all_images, modify_images_to_fit_screen

URL = 'https://toonily.com/webtoon/solo-leveling-005/'
Chapters = [1, 1]

def download_chapters():
    for i in range(Chapters[0], Chapters[1] + 1):
        download_images(f'{URL}chapter-{i}/', f'{i}')


def main():
    download_chapters()
    modify_all_images()
    modify_images_to_fit_screen()



if __name__ == "__main__":
    main()