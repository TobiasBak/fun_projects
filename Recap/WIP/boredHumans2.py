import os
import subprocess
import threading
import time

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder



def upload_image_and_get_response(image_path, url):
    with open(image_path, 'rb') as f:
        m = MultipartEncoder(fields={'file': (os.path.basename(image_path), f, 'image/jpeg')})
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Content-Type': m.content_type,
            'Cookie': 'boredHuman=2024-06-11; boredagi2=19',
            'Origin': 'https://boredhumans.com',
            'Referer': 'https://boredhumans.com/photo_story.php',
            'Sec-Ch-Ua': '"Chromium";v="124", "Opera";v="110", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # The actual upload URL
        post_url = 'https://boredhumans.com/apis/boredagi_upload.php'

        # Use a session to maintain cookies and other session-level headers
        session = requests.Session()

        # Send a GET request to establish the session (optional, depending on the site)
        session.get('https://boredhumans.com/photo_story.php', headers=headers)

        # Send the POST request to upload the image
        response = session.post(post_url, data=m, headers=headers)
        response.raise_for_status()
        return response.text

def threaded_upload_image(thread_name, image_path, url):
    print(f"Thread {thread_name} started.")
    response = upload_image_and_get_response(image_path, url)
    print(f"Thread {thread_name} finished. Response: {response}")

def _get_image_absolute_paths():
    image_paths = []
    for file in os.listdir("../out/images"):
        if file.endswith(".jpg"):
            abs_path = os.path.abspath(os.path.join("../out/images", file))
            image_paths.append(abs_path)
    return image_paths

url = 'https://boredhumans.com/photo_story.php'  # Replace with the actual URL of the webpage
image_path = "/out/images/1.0.0.jpg"

# upload_image_and_get_response(image_path, url)

# image_paths = _get_image_absolute_paths()
# threads = []
# for i, image_path in enumerate(image_paths):
#     thread_name = f"Thread-{i}"
#     thread = threading.Thread(target=threaded_upload_image, args=(thread_name, image_path, url))
#     thread.start()
#     threads.append(thread)
#
# # Wait for all threads to finish
# for thread in threads:
#     thread.join()

# print("All threads finished.")


# def execute_curl_command():
#     curl_command = [
#         "curl",
#         "https://boredhumans.com/apis/boredagi_upload.php",
#         "-H", "accept: */*",
#         "-H", "accept-language: en-GB,en-US;q=0.9,en;q=0.8",
#         "-H", "content-type: multipart/form-data; boundary=----WebKitFormBoundaryqtzb5A4gV12uImcw",
#         "-H", "cookie: boredHuman=2024-06-11; boredagi2=19",
#         "-H", "origin: https://boredhumans.com",
#         "-H", "priority: u=1, i",
#         "-H", "referer: https://boredhumans.com/photo_story.php",
#         "-H", 'sec-ch-ua: "Chromium";v="124", "Opera";v="110", "Not-A.Brand";v="99"',
#         "-H", "sec-ch-ua-mobile: ?0",
#         "-H", 'sec-ch-ua-platform: "Windows"',
#         "-H", "sec-fetch-dest: empty",
#         "-H", "sec-fetch-mode: cors",
#         "-H", "sec-fetch-site: same-origin",
#         "-H", "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0",
#         "-H", "x-requested-with: XMLHttpRequest",
#         "--data-raw", "------WebKitFormBoundaryqtzb5A4gV12uImcw\n"
#                       "Content-Disposition: form-data; name=\"file\"; filename=\"1.0.0.jpg\"\n"
#                       "Content-Type: image/jpeg\n\n\n------WebKitFormBoundaryqtzb5A4gV12uImcw--\n"
#     ]
#
#     result = subprocess.run(curl_command, capture_output=True, text=True)
#     if result.returncode == 0:
#         print("Curl command executed successfully.")
#         print(result.stdout)
#     else:
#         print("Curl command failed with error:")
#         print(result.stderr)
#
# execute_curl_command()

def execute_curl_command(curl_command):
    result = subprocess.run(curl_command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        raise Exception(f"Curl command failed with error: {result.stderr}")


def main():
    # Step 1: Upload the image
    upload_command = [
        "curl", "https://boredhumans.com/apis/boredagi_upload.php",
        "-H", "accept: */*",
        "-H", "accept-language: en-GB,en-US;q=0.9,en;q=0.8",
        "-H", "content-type: multipart/form-data; boundary=----WebKitFormBoundaryqtzb5A4gV12uImcw",
        "-H", "cookie: boredHuman=2024-06-11; boredagi2=19",
        "-H", "origin: https://boredhumans.com",
        "-H", "priority: u=1, i",
        "-H", "referer: https://boredhumans.com/photo_story.php",
        "-H", 'sec-ch-ua: "Chromium";v="124", "Opera";v="110", "Not-A.Brand";v="99"',
        "-H", "sec-ch-ua-mobile: ?0",
        "-H", 'sec-ch-ua-platform: "Windows"',
        "-H", "sec-fetch-dest: empty",
        "-H", "sec-fetch-mode: cors",
        "-H", "sec-fetch-site: same-origin",
        "-H",
        "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0",
        "-H", "x-requested-with: XMLHttpRequest",
        "--data-raw", "------WebKitFormBoundaryqtzb5A4gV12uImcw\n"
                      "Content-Disposition: form-data; name=\"file\"; filename=\"1.0.0.jpg\"\n"
                      "Content-Type: image/jpeg\n\n\n------WebKitFormBoundaryqtzb5A4gV12uImcw--\n"
    ]

    print("Uploading the image...")
    execute_curl_command(upload_command)
    print("Image uploaded successfully.")

    # Wait for some time to ensure the server processes the image
    time.sleep(20)

    # Step 2: Send the API request to get the generated text
    api_command = [
        "curl", 'https://boredhumans.com/apis/boredagi_api.php',
        "-H", "accept: */*",
        "-H", "accept-language: en-GB,en-US;q=0.9,en;q=0.8",
        "-H", "content-type: application/x-www-form-urlencoded; charset=UTF-8",
        "-H", "cookie: boredHuman=2024-06-11; boredagi2=19",
        "-H", "origin: https://boredhumans.com",
        "-H", "priority: u=1, i",
        "-H", "referer: https://boredhumans.com/photo_story.php",
        "-H", 'sec-ch-ua: "Chromium";v="124", "Opera";v="110", "Not-A.Brand";v="99"',
        "-H", "sec-ch-ua-mobile: ?0",
        "-H", 'sec-ch-ua-platform: "Windows"',
        "-H", "sec-fetch-dest: empty",
        "-H", "sec-fetch-mode: cors",
        "-H", "sec-fetch-site: same-origin",
        "-H",
        "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0",
        "-H", "x-requested-with: XMLHttpRequest",
        "--data-raw",
        'prompt=https%253A%252F%252Fboredhumans.com%252Fboredagi_files%252F6668a6e65e247.jpg&uid=lxasqi6rq9kx18bvhv&sesh_id=880c54a4-caa5-427e-83e7-5ecf86de67e7&get_tool=false&tool_num=107'
    ]

    print("Fetching the generated text...")
    response = execute_curl_command(api_command)
    print("Generated text response:")
    print(response)


if __name__ == "__main__":
    main()