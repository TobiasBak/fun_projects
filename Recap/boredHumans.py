import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from threading import Semaphore

import setup
from utils import get_name_from_path, append_to_file, get_images_missing_from_files, \
    get_absolute_paths_from_files

url = 'https://boredhumans.com/photo_story.php'
bad_responses = ["Error please try again.", "The server had an error processing your request."]

THREADS = 10
semaphore = Semaphore(10)  # Create a semaphore object


def automate_image_upload(image_path):
    # Set up the WebDriver (assuming ChromeDriver here)
    driver = webdriver.Chrome()

    try:
        # Open the webpage
        driver.get(url)

        # Wait for and accept the cookie consent if it appears
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
            )
            consent_button.click()
        except Exception as e:
            print("No cookie consent form or could not click the consent button:", e)

        # Find the upload element and upload the image
        upload_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        upload_element.send_keys(image_path)

        # Click the upload button
        upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "uploadButt"))
        )
        upload_button.click()

        # Because page generates two 100% similar p tags, we need to wait for second
        while len(WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.m-0"))
        )) < 2:
            time.sleep(1)

        # Fetch all the <p> elements with class m-0
        new_generated_text_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.m-0"))
        )

        # Pop the element that has the text: "Please upload an image"
        for element in new_generated_text_elements:
            if element.text == "Please upload an image":
                new_generated_text_elements.remove(element)
                break

        # Retrieve the generated text
        generated_text = new_generated_text_elements[0].text

        if generated_text not in bad_responses:
            save_important_generated_text(image_path, generated_text)
            return

        automate_image_upload(image_path)

    finally:
        # Close the WebDriver
        driver.quit()


def save_important_generated_text(image_path: str, generated_text: str):
    image_name = get_name_from_path(image_path)

    sentences = generated_text.split('.')
    if len(sentences) > 2:
        generated_text = sentences[0] + '.' + sentences[1] + '.'

    append_to_file(setup.PATHS.DESCRIPTIONS, f'{image_name};{generated_text}\n')


def threaded_automate_image_upload(thread_name, thread_count, image_path):
    # Acquire a semaphore
    semaphore.acquire()
    try:
        print(f"Thread {thread_name}/{thread_count} started.")
        automate_image_upload(image_path)
    finally:
        # Release the semaphore
        semaphore.release()


def generate_text_from_images(directory: str):
    images_missing = get_images_missing_from_files(directory, setup.PATHS.DESCRIPTIONS)
    image_paths = get_absolute_paths_from_files(setup.PATHS.OUT_IMAGE_DIR, images_missing)

    if not image_paths:
        print("No images missing descriptive text.")
        return

    print(f"Generating text for {len(image_paths)} images...")
    thread_count = len(image_paths)

    threads = []
    for i, image_path in enumerate(image_paths):
        thread_name = f"Thread-{i}"
        thread = threading.Thread(target=threaded_automate_image_upload, args=(thread_name, thread_count, image_path))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads finished.")
