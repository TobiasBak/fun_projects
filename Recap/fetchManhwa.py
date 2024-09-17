import os
import requests
from bs4 import BeautifulSoup

import setup


def download_chapters():
    # Check if raw image directory is empty, if not, skip downloading
    if os.listdir(setup.PATHS.RAW_IMAGE_DIR):
        print("Raw image directory is not empty, skipping download...")
        return

    for i in range(setup.CHAPTERS[0], setup.CHAPTERS[1] + 1):
        switch_website(f'{setup.DOWNLOAD_URL}chapter-{i}/', str(i))


def _download_images_toonily(url: str, chapter: str, img_tags='div.page-break.no-gaps img'):
    """
    Download images from the specified URL and saves them locally in temp/images directory.
    """
    print(f'Downloading images from chapter {chapter}...')

    # Create a session
    session = requests.Session()

    # Headers to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': url
    }

    # Send a GET request to fetch the HTML content of the page
    response = session.get(url, headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all img tags within the divs with class 'page-break no-gaps'
    img_tags = soup.select('div.page-break.no-gaps img')

    # Extract the 'src' or 'data-src' attribute from each img tag
    img_urls = [img.get('data-src', img.get('src')).strip() for img in img_tags]

    # Download each image and save it locally
    for idx, img_url in enumerate(img_urls):
        img_response = session.get(img_url, headers=headers)
        img_response.raise_for_status()
        img_path = f"{setup.PATHS.RAW_IMAGE_DIR}/{chapter}.{idx}.jpg"

        # The last image is a placeholder image, so we skip it
        if idx == len(img_urls) - 1:
            continue

        with open(img_path, 'wb') as file:
            file.write(img_response.content)


# Dictionary to map website names to their respective URLs and functions
websites = {
    'toonily.com': {
        'url': 'toonily.com',
        'function': _download_images_toonily
    }
}


def switch_website(url: str, chapter: str):
    site_name = url.split('/')[2]
    if site_name in websites:
        site_info = websites[site_name]
        site_info['function'](url, chapter)
    else:
        print(f'Website {site_name} not supported.')
