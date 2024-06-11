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
            print("Accepted cookie consent")
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

        # Wait for the text to change from the default value
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "p.m-0"), "In the dimly lit alley")
        )

        # Retrieve the generated text
        generated_text_element = driver.find_element(By.CSS_SELECTOR, "p.m-0")

        # Retrieve the generated text
        generated_text = generated_text_element.text

        print("Generated Text:", generated_text)

    finally:
        # Close the WebDriver
        driver.quit()

# Usage
image_path = 'C:/0-uni/fun_projects/Recap/out/images/1.0.0.jpg'
url = 'https://boredhumans.com/photo_story.php'  # Replace with the actual URL of the webpage
automate_image_upload(image_path, url)
