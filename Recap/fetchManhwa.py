import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

import setup


def download_chapters():
    # Check if raw image directory is empty, if not, skip downloading
    if os.listdir(setup.PATHS.RAW_IMAGE_DIR):
        print("Raw image directory is not empty, skipping download...")
        return

    for i in range(setup.CHAPTERS[0], setup.CHAPTERS[1] + 1):
        switch_website(f'{setup.DOWNLOAD_URL}chapter-{i}/', str(i))


def _download_images_toonily(url: str, chapter: list[int]):
    """
    Download images from the specified URL and saves them locally in temp/images directory.
    """
    print(f'Downloading images from chapter {chapter}...')
    for chapter_index in range(chapter[0], chapter[1] + 1):
        _url = f'{url}chapter-{chapter_index}/'
        print(f'Scraping images from {_url}...')

        # Create a session
        session = requests.Session()

        # Headers to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': _url
        }

        # Send a GET request to fetch the HTML content of the page
        response = session.get(_url, headers=headers)
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
            img_path = f"{setup.PATHS.RAW_IMAGE_DIR}/{chapter_index}.{idx}.jpg"

            # The last image is a placeholder image, so we skip it
            if idx == len(img_urls) - 1:
                continue

            with open(img_path, 'wb') as file:
                file.write(img_response.content)



def _get_chapter_urls_mangadex_selenium(url):
    """
    Scrape the main page of the manga to extract chapter URLs using Selenium.
    """
    print(f'Scraping chapter URLs from {url}...')

    # Set up Selenium WebDriver (make sure to specify the path to your WebDriver)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        # Wait for the page to load and the chapter links to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/chapter/"]'))
        )
        time.sleep(2)  # Additional wait to ensure all elements are loaded

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Adjust the selector based on the actual HTML structure of the Mangadex page
        chapter_links = soup.select('a[href*="/chapter/"]')

        chapter_urls = {}
        for link in chapter_links:
            # Check if the link has a subelement which is an image with title "English"
            img = link.find('img', {'title': 'English'})
            if img:
                title = link.get('title', '')
                if len(title.split(' ')) > 1:
                    chapter_num = title.split(' ')[1].strip('.')  # Extract chapter number
                else:
                    chapter_num = 'Unknown'  # Default value if the title format is unexpected
                chapter_url = "https://mangadex.org" + link['href']  # Form complete chapter URL

                # Find the datetime element within the same parent element
                parent = link.find_parent()
                time_element = parent.find('time', {'datetime': True})
                if time_element:
                    datetime = time_element['datetime']
                else:
                    datetime = 'Unknown'  # Default value if datetime is not found

                chapter_urls[chapter_url] = (chapter_num, datetime)

        return chapter_urls

    finally:
        driver.quit()



def select_newest_upload(chapter_dict):
    """
    Select the newest upload for each chapter from the given dictionary.

    :param chapter_dict: Dictionary with chapter URLs as keys and tuples (chapter_num, datetime) as values.
    :return: Dictionary with the newest upload for each chapter.
    """
    newest_chapters = {}

    for url, (chapter_num, dt_str) in chapter_dict.items():
        dt = datetime.fromisoformat(dt_str)
        if chapter_num not in newest_chapters or dt > newest_chapters[chapter_num][1]:
            newest_chapters[chapter_num] = (url, dt)

    # Convert back to the desired format
    result = {url: (chapter_num, dt.isoformat()) for chapter_num, (url, dt) in newest_chapters.items()}
    return result


def _download_images_mangadex(url: str, chapter: list[int, int]):
    """
    Download images from the specified Mangadex URL and saves them locally in temp/images directory.
    """
    print(f'Downloading images from chapter {chapter}...')

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': url
    }

    response = session.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Adjust this based on Mangadex's structure for image containers
    img_tags = soup.select('div.some-image-class img')  # Update this CSS selector as needed

    img_urls = [img.get('data-src', img.get('src')).strip() for img in img_tags]

    # Download each image and save it locally
    for idx, img_url in enumerate(img_urls):
        img_response = session.get(img_url, headers=headers)
        img_response.raise_for_status()

        img_path = f"{setup.PATHS.RAW_IMAGE_DIR}/{chapter}.{idx}.jpg"

        with open(img_path, 'wb') as file:
            file.write(img_response.content)


# Extend the website dictionary for Mangadex
websites = {
    'toonily.com': {
        'url': 'toonily.com',
        'function': _download_images_toonily
    },
    'mangadex.org': {
        'url': 'mangadex.org',
        'function': _download_images_mangadex
    }
}


def switch_website(url: str, chapter: str):
    site_name = url.split('/')[2]
    if site_name in websites:
        site_info = websites[site_name]
        site_info['function'](url, chapter)
    else:
        print(f'Website {site_name} not supported.')
