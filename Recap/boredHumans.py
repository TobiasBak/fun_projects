import os
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


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

        print("Generated Text:", generated_text)

    finally:
        # Close the WebDriver
        driver.quit()


def threaded_automate_image_upload(thread_name, image_path, url):
    print(f"Thread {thread_name} started.")
    automate_image_upload(image_path, url)
    print(f"Thread {thread_name} finished.")


def _get_image_absolute_paths():
    image_paths = []
    for file in os.listdir("out/images"):
        if file.endswith(".jpg"):
            abs_path = os.path.abspath(os.path.join("out/images", file))
            image_paths.append(abs_path)
    return image_paths


image_paths = _get_image_absolute_paths()

url = 'https://boredhumans.com/photo_story.php'  # Replace with the actual URL of the webpage
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
