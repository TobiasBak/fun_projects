from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path
import time


import asyncio
from pyppeteer import launch



import requests

# URL of the page with the form
url = 'https://boredhumans.com/photo_story.php'

# Data to be sent in the form
data = {
    'FileUpload': open('out/images/1.0.0.jpg', 'rb')
}

# Send a POST request with the form data
response = requests.post(url, files=data)

time.sleep(30)

# Print the response
print(response.text)


# # Path to your WebDriver
# driver_path = binary_path
#
# # Initialize the WebDriver
# driver = webdriver.Chrome(service=Service(driver_path))
#
# try:
#     # Open the URL
#     driver.get('https://boredhumans.com/photo_story.php')
#
#     # form = driver.find_element(By.ID, 'uploadForm')
#
#     # Find all elements
#     elements = driver.find_elements(By.XPATH, '//*')
#     print("Number of elements:", len(elements))
#
#     # Print all elements
#     for element in elements:
#         print(f"Tag: {element.tag_name}, ID: {element.get_attribute('id')}, Text: {element.text}")
#
#     # Locate the file input element and upload the image
#     file_input = form.find_element(By.ID, 'FileUpload')
#     file_input.send_keys('/path/to/your/image.jpg')
#
#     # Submit the form
#     submit_button = form.find_element(By.ID, 'uploadButt')
#     submit_button.click()
#
#     # Wait for the response to be generated (you might need to adjust the sleep time)
#     time.sleep(10)
#
#     # Extract the generated text
#     output_div = driver.find_element(By.ID, 'outputDiv')
#     story_text = output_div.text
#
#     print("Generated Story:", story_text)
#
# finally:
#     # Close the WebDriver
#     driver.quit()
