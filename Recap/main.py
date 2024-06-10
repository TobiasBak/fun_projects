from fetchManhwa import download_images
from imageModifier import modify_image


def main():
    download_images('https://toonily.com/webtoon/solo-leveling-005/chapter-1/')
    modify_image('temp/images/image_0.jpg')



if __name__ == "__main__":
    main()