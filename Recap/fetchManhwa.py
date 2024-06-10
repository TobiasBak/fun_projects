import os
import requests
from bs4 import BeautifulSoup


def download_images(url, img_tags='div.page-break.no-gaps img'):
    """
    Download images from the specified URL and saves them locally in temp/images directory.
    """
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

    # Ensure a directory to save the images
    os.makedirs('temp/images', exist_ok=True)

    # Download each image and save it locally
    for idx, img_url in enumerate(img_urls):
        img_response = session.get(img_url, headers=headers)
        img_response.raise_for_status()
        img_path = os.path.join('temp', 'images', f'image_{idx}.jpg')
        with open(img_path, 'wb') as file:
            file.write(img_response.content)
        print(f'Downloaded {img_url} as {img_path}')