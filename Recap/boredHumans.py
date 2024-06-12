import os
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from threading import Semaphore

from utils import get_name_from_path, get_absolute_paths

OUT_TEXT_DIR = 'out/text'
OUT_IMAGES_DIR = 'out/images'
os.makedirs(OUT_TEXT_DIR, exist_ok=True)

url = 'https://boredhumans.com/photo_story.php'  # Replace with the actual URL of the webpage

# Create a semaphore object
semaphore = Semaphore(5)


def automate_image_upload(image_path, url):
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

        if generated_text == "Error please try again.":
            automate_image_upload(image_path, url)

        if "The server had an error processing your request." in generated_text:
            automate_image_upload(image_path, url)

        # Append the generated text to a file. The file should be comma seperated with image file as first
        # element and the generated text as second element
        with open('out/text/generated_text.csv', 'a') as file:
            file.write(f'{get_name_from_path(image_path)},{generated_text}\n')


    finally:
        # Close the WebDriver
        driver.quit()


def threaded_automate_image_upload(thread_name, image_path, url):
    print(f"Thread {thread_name} started.")
    # Acquire a semaphore
    semaphore.acquire()
    try:
        automate_image_upload(image_path, url)
    finally:
        # Release the semaphore
        semaphore.release()
    print(f"Thread {thread_name} finished.")


def generate_text_from_images(image_paths):
    threads = []
    for i, image_path in enumerate(image_paths):
        thread_name = f"Thread-{i}"
        thread = threading.Thread(target=threaded_automate_image_upload, args=(thread_name, image_path, url))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads finished.")
