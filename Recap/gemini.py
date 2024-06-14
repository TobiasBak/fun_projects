import google.generativeai as genai

import setup
from open_ai import prompt_beginning, generate_prompts_for_images, propmt_ending
from utils import get_lines_from_file, get_absolute_path, get_all_images, get_sorted_list_of_images, \
    append_to_file_list, get_images_missing_from_files, append_to_file
from PIL import Image

AMOUNT_OF_IMAGES = 10

prompt = f"""
I have gathered a collection of images that I would like to turn into a story.
Some images have text on them, some do not.
Some images have different pictures on them, but you should not return a description for each of them, but rather a single description for the whole image.

You must generate an in depth description for each image that include:
1. Characters: A detailed description of the characters in the image and what they are doing.
2. Setting: A detailed description of the setting in the image.
3. Plot: A detailed description of what is happening in the image.
4. Emotions: A detailed description of the emotions of the characters in the image.
5. Text: A detailed description of the text in the image.

**Return Format:**
image_file_name; generated_text


Please go ahead and iterate over each given image and generate a description for each, but do not give description for sub-images in the image.
Therefore, you should return {AMOUNT_OF_IMAGES} descriptions in total. One for each image sent. 
"""


def get_api_key():
    with open(get_absolute_path('hidden/gemini_key.txt'), 'r') as file:
        lines = file.readlines()
    return lines[0].strip()


genai.configure(api_key=get_api_key())
model = genai.GenerativeModel('gemini-1.5-flash-latest')


def _generate_description_for_images(images: list[Image]):
    content = [prompt]

    for image in images:
        content.append(image)

    responses = model.generate_content(content)
    print(responses.text)

    descriptions = []
    responses = responses.text.split('\n')
    for response in responses:
        if response == '':
            continue
        description = response.split(';')[1]
        descriptions.append(description)

    if len(descriptions) != len(images):
        print("Length of descriptions does not match length of images.")
        print(f"We have to retry the generation of descriptions for the images: {images}")
        return _generate_description_for_images(images)

    return descriptions


def generate_descriptive_text():
    images = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, setup.PATHS.DESCRIPTIONS)
    print(f"Starting generation of descriptions for {len(images)} images: ...")

    images_opened = []
    for image in images:
        img = Image.open(f"{setup.PATHS.OUT_IMAGE_DIR}/{image}")
        images_opened.append(img)

    for i in range(0, len(images_opened), 10):
        _images = images_opened[i:i + 10]
        print(f"Generating descriptions for images: {_images}...")
        responses = _generate_description_for_images(_images)

        lines = []
        for j, response in enumerate(responses):
            lines.append(f"{images[i + j]}; {response}")
        append_to_file_list(setup.PATHS.DESCRIPTIONS, lines)


prompt_unnecessary_lines = """
I have gathered a collection of image descriptions that combined should tell a story.
However, some of the image descriptions describe promotional text or only describe a symbol.
These descriptions are not necessary for the story and should be removed.

The descriptions are formatted as <image_id>; <description>.

**Example of an unnecessary image description:**
1.25.1.jpg;  The image features a green and white background. There is black text in the center of the image. The text reads "Na Joeman Lebeom" in Korean. The emotions in the image are hopeful and determined. The plot in the image suggests the man will be relying on his own strengths and abilities on his mission.
1.4.1.jpg;  The image shows a red kanji character on a black background.
2.21.1.jpg;  A white background with a green and purple aura is shown, with green particles floating around. A large, black circle with white lettering appears in the center. The text in the circle is "Just one more time! Let's do this!" and the text in the aura is "나혼자만 레벨업". The setting is a white background with a green and purple aura. The plot is that the character is ready to fight and is confident they will succeed. The emotion of the character is determination and confidence. The text in the image is "Just one more time! Let's do this!" and "나혼자만 레벨업".


**Return Format:**
[<image_id>, <image_id>, ...]

**List of descriptions:**
"""

prompt_unnecessary_lines_end = """
Please go ahead and return only the image ids of the images are deemed unnecessary.
"""


def get_files_that_gemini_deem_unnecessary():
    _prompt = prompt_unnecessary_lines
    lines_from_file = get_lines_from_file(setup.PATHS.DESCRIPTIONS)
    for line in lines_from_file:
        _prompt += line + '\n'

    print(_prompt)

    print(f"Gemini is finding unnecessary lines in the descriptions...")

    _prompt += prompt_unnecessary_lines_end

    responses = model.generate_content(_prompt)

    if not responses.candidates:
        print("No sentences generated.")
        return

    # If there are candidates, get the first one (usually the best)
    first_candidate = responses.candidates[0]
    print(first_candidate.content)  # Print the generated text
    if first_candidate is None:
        print("No unnecessary lines found.")
        return

    print(responses.text)


def generate_sentences_for_images_gemini(images: list[str]):
    prompt = prompt_beginning

    generated_prompts = generate_prompts_for_images(images)

    if len(generated_prompts) == 0:
        print("No sentences missing. Exiting...")
        return

    for generated_prompt in generated_prompts:
        prompt += generated_prompt

    prompt += propmt_ending

    responses = model.generate_content(prompt)

    if not responses.text:
        print("No sentences generated.")
        return

    replies = responses.text.split('\n')

    for x in replies:
        if x != '':
            print(x)
            append_to_file(f"{setup.PATHS.SENTENCES}_gemini.csv", x)


def generate_sentences_gemini():
    images = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, f"{setup.PATHS.SENTENCES}_gemini.csv")
    if len(images) == 0:
        print("No images missing generated sentences.")
        return []

    # Run generate for images in batches of 50
    for i in range(0, len(images), 50):
        generate_sentences_for_images_gemini(images[i:i + 50])
