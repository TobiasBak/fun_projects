import json

import google.generativeai as genai
from google.ai.generativelanguage_v1 import HarmCategory
from google.generativeai.types import HarmBlockThreshold

import setup
from old.open_ai import generate_prompts_for_images
from utils import get_lines_from_file, get_absolute_path, append_to_file_list, get_images_missing_from_files, \
    append_to_file
from PIL import Image, ImageDraw, ImageFont

AMOUNT_OF_IMAGES = 10

prompt = f"""
You are tasked with describing a picture in detail.
The picture is taken from a manhwa. 
The picture can have multiple areas and whitespace. 
You must never mention the viewer or reader in the descriptions.

**Instructions:**
1. Generate a detailed description for each of the sub-pictures in the jpg.
2. If the image have multiple areas, describe each area in detail. However, combine all descriptions into a single string.
3. Combine all the descriptions into a single description for the jpg.

**How to describe jpgs in detail:**
You must generate an in depth description for each jpg that include the following elements combined in a single string:
1. Characters: A detailed description of visible characters including what parts of the character that is visible. Describe the different parts in detail. 
2. Setting: A detailed description of the setting in the pictures. Where are we?
3. Plot: A detailed description of what is happening in the pictures.
4. Feeling: A detailed description of the feeling the pictures conveys. 
5. Text: A detailed description of the text in the pictures. All text should be interpreted in lowercase. Such that when it in the picture says "HELLO", you should write "Hello". An example of how to describe the text in the image is: "At the top of the image, there is text that says 'Hello'. Below the character there is more text that says 'Goodbye'."

**Return Format:**
The combined description must be returned in the following format. This means remove all newlines and replace them with a space.:
`<file_name>`; `<combined descriptions>`
You must only return 1 string containing all the details from the descriptions.

**Input:**
"""

def get_api_key():
    with open(get_absolute_path('hidden/gemini_key.txt'), 'r') as file:
        lines = file.readlines()
    return lines[0].strip()


genai.configure(api_key=get_api_key())
model = genai.GenerativeModel('gemini-1.5-flash-latest')


def get_image_with_name_on_top(image: str):
    # Open the original image
    img = Image.open(get_absolute_path(f"{setup.PATHS.OUT_IMAGE_DIR}/{image}"))

    # Create a new image with a white background and 50 pixels added at the top
    new_img = Image.new("RGB", (img.width, img.height + 100), "white")

    # Paste the original image onto the new image
    new_img.paste(img, (0, 100))

    # Prepare to draw the text
    draw = ImageDraw.Draw(new_img)

    font_size = 36

    font = ImageFont.truetype("arial.ttf", font_size)

    # Optionally, use a custom font if a font path is provided

    # Calculate text width and position to center it
    bbox = draw.textbbox((0, 0), image, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (img.width - text_width) // 2
    text_y = (100 - text_height) // 2

    # Draw the text on the new image
    draw.text((text_x, text_y), image, fill="black", font=font)

    return new_img


def _generate_description_for_images(image: str) -> list[str]:
    content = []

    img_data = Image.open(get_absolute_path(f"{setup.PATHS.OUT_IMAGE_DIR}/{image}"))
    content.append(img_data)

    modified_prompt = prompt + f"You are describing {image} in detail. \n"

    content.append(modified_prompt)

    result = model.generate_content(
        content,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    # print(result)
    print(result.text)

    responses = result.text.split('\n')
    out = []
    for response in responses:
        if response != '':
            out.append(response)

    return out


def generate_descriptive_text():
    images = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, setup.PATHS.DESCRIPTIONS)
    print(f"Starting generation of descriptions for {len(images)} images: ...")

    for image in images:
        print(f"Generating descriptions for {image}...")
        responses = _generate_description_for_images(image)

        print(responses)

        out = ""
        out += responses[0].split(';')[0] + ';'
        for response in responses:
            file_name = response.split(';')[0]
            if file_name not in images:
                raise Exception(f"File name {file_name} not in images.")
            out += response.split(';')[1] + ' '

        append_to_file(setup.PATHS.DESCRIPTIONS, out)


prompt_unnecessary_lines = """
I have gathered a collection of image descriptions that combined should tell a story.
However, some of the image descriptions describe promotional text or only describe a symbol.
These descriptions are not necessary for the story and should be removed.

The descriptions are formatted as `<image_id>`; `<description>`.

**Example of an unnecessary image description:**
1.25.1.jpg;  The image features a green and white background. There is black text in the center of the image. The text reads "Na Joeman Lebeom" in Korean. The emotions in the image are hopeful and determined. The plot in the image suggests the man will be relying on his own strengths and abilities on his mission.
1.4.1.jpg;  The image shows a red kanji character on a black background.
2.21.1.jpg;  A white background with a green and purple aura is shown, with green particles floating around. A large, black circle with white lettering appears in the center. The text in the circle is "Just one more time! Let's do this!" and the text in the aura is "나혼자만 레벨업". The setting is a white background with a green and purple aura. The plot is that the character is ready to fight and is confident they will succeed. The emotion of the character is determination and confidence. The text in the image is "Just one more time! Let's do this!" and "나혼자만 레벨업".


**Return Format:**
[`<image_id>`, `<image_id>`, ...]

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

    print(f"Gemini is finding unnecessary lines in the descriptions...")

    _prompt += prompt_unnecessary_lines_end

    tokens = model.count_tokens(_prompt)
    print(f"Amount of tokens: {tokens}")

    responses = model.generate_content(_prompt)

    print(responses)

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


prompt_beginning = f"""
**AI Mission Brief:** Turning Image Descriptions into a Narrative
**Mission Objective:**
You are tasked with transforming a series of detailed image descriptions into a coherent, flowing story. Each sentence generated should contribute to the overall narrative and provide a seamless transition between images. The resulting story should read as a unified and engaging piece, capturing the essence and emotions of the scenes depicted. Each image should be described by two precise sentences.

**Task Outline:**
1. Image Descriptions: You will be given descriptions of 100 images. Each description includes specific details about the visual elements, emotions conveyed, and context of the image.
2. Narrative Transformation: Based on these descriptions, generate sentences that collectively form a continuous story.
3. Story Flow: Ensure the sentences flow logically from one to the next, maintaining a coherent and engaging narrative.

**Rules and Guidelines:**
1. Avoid Direct References to the Image: Do not use phrases like "In the picture" or "The image shows." Instead, focus on narrating the events and emotions as if they are happening in real-time.
2. Character Consistency: Maintain consistency in characters' names, attributes, and roles throughout the story. Introduce characters smoothly and keep their actions and descriptions coherent across sentences.
3. Emotion and Context: Highlight the emotions and context described in the images to enrich the story. Use descriptive language to convey the atmosphere, characters' feelings, and settings.
4. Natural Transitions: Create smooth transitions between sentences and scenes. Ensure each sentence logically follows the previous one, building a continuous and engaging narrative.
5. Descriptive Detail: Incorporate specific details from the descriptions into the story, enhancing the imagery and helping readers visualize the scenes.
6. Avoid Mentioning Speech Bubbles: They are merely there to describe the scene and not something the characters can see.
7. Avoid Spoilers: Reveal information gradually as it happens. Ensure that no critical plot points are disclosed prematurely.
8. Vary Sentence Structure: Avoid starting too many sentences with quotes. Use a variety of sentence structures to keep the narrative engaging and dynamic.

**Example Input Description:**
"1.0.B.jpg; There is text above him that says 'E-Rank Hunter.' There is more text below him that says 'The Hunter Guild's' and 'Haa.' The image conveys a feeling of despair and determination. A young man is lying on the ground, bleeding profusely from multiple wounds. He is wearing a blue hoodie with the hood up. His hair is short and dark. His face is contorted in pain, but he has a determined look in his eyes. The background is dark, and it appears he is in some sort of abandoned building."

**Example Output Sentence:**
"1.0.B.jpg; Clutching his bleeding wounds, the young man struggled to rise from the cold, dark floor. Despite the pain etched across his face, Sung Jin-Woo's eyes burned with determination."

**Process:**
1. Read the Description: Carefully read and understand each image description.
2. Extract Key Elements: Identify key elements such as characters, emotions, settings, and actions.
3. Generate Sentence: Formulate a sentence that incorporates these elements and contributes to the overall narrative.
4. Ensure Continuity: Ensure each generated sentence logically follows the previous one, maintaining narrative coherence.
5. Avoid Premature Context: Introduce context gradually, ensuring a smooth and natural unfolding of the story.
By adhering to these guidelines, you will create a compelling and seamless story that effectively translates the visual and emotional content of the images into a written narrative.

**Output:**
For each of the inputted lines, generate a return string in the following format:
`<image_name>`; `<sentences>`
The return should be plaintext, not in JSON format.

**Inputs:**
You will be provided with the filenames and descriptions below:
"""



def generate_sentences_for_images_gemini(images: list[str]):
    prompt = prompt_beginning

    generated_prompts = generate_prompts_for_images(images)

    if len(generated_prompts) == 0:
        print("No sentences missing. Exiting...")
        return

    for generated_prompt in generated_prompts:
        prompt += generated_prompt

    tokens = model.count_tokens(prompt, generation_config={"temperature": 1})
    print(f"Amount of tokens: {tokens}")
    print(prompt)

    responses = model.generate_content(prompt)
    print(f"RAW RESPONSE=================")
    print(responses.text)

    if not responses.text:
        print("No sentences generated.")
        return

    replies = responses.text.split('\n')

    # Remove first and last index if it is json
    if replies[0] == '```json':
        replies.pop(0)

    if replies[-1] == '```':
        replies.pop(-1)


    for x in replies:
        if x == '':
            continue

        parts = x.split(';')
        description = parts[1]
        if description[:1] == '"' and description[-1:] == '"':
            description = description[1:-1]

        append_to_file(setup.PATHS.SENTENCES, f"{parts[0]}; {description}")


def generate_sentences_gemini():
    images = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, setup.PATHS.SENTENCES)
    if len(images) == 0:
        print("No images missing generated sentences.")
        return []

    print(f"Starting generation of sentences for {len(images)} images: ...")

    # Run generate for images in batches of 100
    # generate_sentences_for_images_gemini(images)
    for i in range(0, len(images), 100):
        generate_sentences_for_images_gemini(images[i:i + 100])
