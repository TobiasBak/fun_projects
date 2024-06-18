import json
import threading

import google.generativeai as genai
from google.ai.generativelanguage_v1 import HarmCategory
from google.generativeai.types import HarmBlockThreshold

import setup
from old.open_ai import generate_prompts_for_images
from utils import get_lines_from_file, get_absolute_path, append_to_file_list, get_images_missing_from_files, \
    append_to_file, get_dict_from_file
from PIL import Image, ImageDraw, ImageFont

AMOUNT_OF_IMAGES = 10
THREADS = 5
semaphore = threading.Semaphore(THREADS)  # Create a semaphore object

prompt_describe_image_1 = f"""
You are tasked with describing a picture in detail.
The picture is taken from a manhwa. 
You must never mention the viewer or reader in the descriptions.

**Instructions:**
1. Generate a detailed description for each of the sub-pictures in the jpg.
2. If the image have multiple areas, describe each area in detail. However, combine all descriptions into a single string.
3. Do not describe Speech Bubbles.
4. Combine all the descriptions into a single description for the jpg.

Return "Understood" when understood.
"""

prompt_describe_image_2 = f"""
**How to describe jpgs in detail:**
You must generate an in depth description for each jpg that include the following elements combined in a single string:
1. Characters: Visible characters should be described in detail. Do not describe where they are looking. 
2. Setting: The setting and area in the picture must be described. 
3. Plot: The actions and what is generally happening must be described. 
4. Feeling: A detailed description of the feeling the pictures conveys. 
5. Text: English text should be extracted from the image with a starting capital letter and the rest in lowercase. The text should be followed by where it is positioned relative to the characters.

Notes: Background and speech bubbles should not be described.

Return "Understood" when understood.
"""

prompt_describe_image_3 = f"""
An example detailed description and the expected output will be explained.
**Example detailed description:**
A man with ginger hair is visible in the image. Only the face of the man is visible. He has an open mouth and it looks like he is speaking. Above the man it says "If The Other Hunters Get To It First, Our Profits Would Dwindle." The man looks very worried and concerned.



**Return Format:**
The combined description must be returned in the following format. This means remove all newlines and replace them with a space.:
`<file_name>`; `<combined descriptions>`
You must only return 1 string containing all the details from the descriptions.

Return "Understood" when understood.
"""


def get_api_key():
    with open(get_absolute_path('hidden/gemini_key.txt'), 'r') as file:
        lines = file.readlines()
    return lines[0].strip()


genai.configure(api_key=get_api_key())
model = genai.GenerativeModel('gemini-1.5-flash')


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


def _generate_description_for_images(images: list[str]):
    prompts = [prompt_describe_image_1, prompt_describe_image_2, prompt_describe_image_3]

    chat = model.start_chat(history=[])
    for p in prompts:
        r = chat.send_message(p, generation_config={"temperature": 1})
        print(r.text)

    for image in images:

        content = []
        img_data = Image.open(get_absolute_path(f"{setup.PATHS.OUT_IMAGE_DIR}/{image}"))
        content.append(img_data)
        content.append(f"You are describing {image} in detail. \n")

        response = chat.send_message(
            content,
            generation_config={"temperature": 1},
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
        )
        print(response.text)

        responses = response.text.split('\n')
        for r in responses:
            if r == '':
                continue

            append_to_file(setup.PATHS.DESCRIPTIONS, r)


def optimize_descriptions():
    description_dict = get_dict_from_file(setup.PATHS.DESCRIPTIONS)
    for key, value in description_dict.items():
        description = value
        description = description.replace('a speech bubble', 'text')
        description = description.replace('speech bubble', 'text')
        description = description.replace('~', '').replace('(','').replace(')','')
        description_dict[key] = description

    with open(setup.PATHS.DESCRIPTIONS, 'w') as file:
        for key, value in description_dict.items():
            file.write(f"{key}; {value}\n")


def should_remove_quote(quote: str):
    # If quote only contains dots or commas, remove it
    if quote.replace('.', '').replace(',', '').replace(' ', '') == '':
        return True



def optimize_description_quotes():
    description_dict = get_dict_from_file(setup.PATHS.DESCRIPTIONS)
    for key, value in description_dict.items():
        description = value
        parts = description.split('"')
        quote_indexes_to_remove = []
        # Every second part is a quote
        for i in range(1, len(parts), 2):
            if should_remove_quote(parts[i]):
                quote_indexes_to_remove.append(i)

        # Rebuild the description based on parts and removed quotes
        new_description = ""
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_description += part
            else:
                if i not in quote_indexes_to_remove:
                    new_description += '"' + part + '"'

        description_dict[key] = new_description

    with open(setup.PATHS.DESCRIPTIONS, 'w') as file:
        for key, value in description_dict.items():
            file.write(f"{key}; {value}\n")


def threaded_generate_description(thread_name, images):
    # Acquire a semaphore
    semaphore.acquire()
    try:
        print(f"Starting thread: {thread_name}")
        _generate_description_for_images(images)
    finally:
        # Release the semaphore
        semaphore.release()


def generate_descriptive_text():
    images = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, setup.PATHS.DESCRIPTIONS)
    print(f"Starting generation of descriptions for {len(images)} images: ...")

    if len(images) == 0:
        print("No images missing descriptions. Exiting...")
        return

    threads = []
    for i in range(0, len(images), 10):
        thread_name = f"{i}/{len(images)}"
        thread = threading.Thread(target=threaded_generate_description, args=(thread_name, images[i:i + 10]))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    if len(get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, setup.PATHS.DESCRIPTIONS)) > 0:
        print("Some images are still missing descriptions. Will start generation again.")
        generate_descriptive_text()

    print("All threads finished. Will start optimize_descriptions")
    optimize_descriptions()
    optimize_description_quotes()


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


p_1 = f"""
**AI Mission Brief:** Turning Image Descriptions into a Narrative
**Mission Objective:**
You are tasked with transforming a series of detailed image descriptions into a coherent, flowing story in english. 
Each sentence generated should contribute to the overall narrative and provide seamless transitions. 
Each image should be described by two sentences that contribute to the overall narrative.

**Task Outline:**
1. You will be given descriptions of 100 images. Each description includes specific details about the visual elements, emotions conveyed, and context of the image.
2. Based on these descriptions, generate two sentences for each image that collectively form a continuous story. Do not mention the words "scene", "setting" or "image" in the sentences.
3. Ensure the sentences flow logically from one to the next, maintaining a coherent and engaging narrative.

Return "Understood" when read
"""

p_2 = f"""
You must uphold the following rules and guidelines

**Rules and Guidelines:**
1. Avoid Direct References to the Image: Do not use phrases like "In the picture" or "The image shows." or "The speech bubble". 
2. Emotion and Context: Use descriptive language to convey the atmosphere, characters' feelings, and settings.
3. Natural Transitions: Create smooth transitions between sentences and scenes. Ensure each sentence logically follows the previous one, building a continuous and engaging narrative.
4. Text from descriptions: When using conversations from descriptions add: "[pronoun] [action].". 
5. Vary Sentence Structure: Use a variety of words to start sentences to keep the narrative engaging and dynamic.
6. Sentence lengths.: Each image should be described by two simple sentences focusing on setting and what is happening.
7. Vary sentence structure: Avoid starting multiple sentences with the same word. Vary the sentence structure to maintain reader interest.
8. Do not reference where the text is located or that you are referencing text, just use text as part of the story. 
9. If the character has recently been described, you can refer to the character using "The man", "The woman", "The character" etc.
10. Avoid Mentioning Speech Bubbles: They are merely there to describe the scene and not something the characters can see.


Return "Understood" when the rules and guidelines are understood.
"""

p_3 = f"""
You must follow the process when generating sentences based on the descriptions

**Process:**
1. Read the Description: Carefully read and understand each image description.
2. Extract Key Elements: Identify key elements such as characters, emotions, settings, and actions.
3. Generate Sentence: Formulate a sentence in present tense that incorporates these elements and contributes to the overall narrative.
4. Ensure Continuity: Ensure each generated sentence logically follows the previous one, maintaining narrative coherence.
5. Following Rules and Guidelines: Ensure generated sentence follow rules and guidelines.
By adhering to these guidelines, you will create a compelling and seamless story that effectively translates the visual and emotional content of the images into a written narrative.

Return "Understood" when it is understood.
"""

p_4 = f"""
Following is examples on input and output and the expected output format.

**Example Input Description:**
"1.0.B.jpg; There is text above him that says 'E-Rank Hunter.' There is more text below him that says 'The Hunter Guild's' and 'Haa.' The image conveys a feeling of despair and determination. A young man is lying on the ground, bleeding profusely from multiple wounds. He is wearing a blue hoodie with the hood up. His hair is short and dark. His face is contorted in pain, but he has a determined look in his eyes. The background is dark, and it appears he is in some sort of abandoned building."

**Example Output Sentence:**
"1.0.B.jpg; Clutching his bleeding wounds, the young man struggled to rise from the cold, dark floor. Despite the pain etched across his face, Sung Jin-Woo's eyes burned with determination."

**Output:**
For each of the inputted lines, generate a single return string in the following format:
`<image_name>`; `<story>`
`<story>` should include all the generated sentences about the image.
The return should be plaintext, not in JSON format.

Return "Understood" when read. 
"""


def generate_sentences_for_images_gemini(images: list[str]):
    generated_prompts = generate_prompts_for_images(images)
    prompts = [p_1, p_2, p_3, p_4]

    if len(generated_prompts) == 0:
        print("No sentences missing. Exiting...")
        return

    chat = model.start_chat(history=[])

    for p in prompts:
        r = chat.send_message(p, generation_config={"temperature": 1})
        print(r.text)

    g_prompt = ""
    # Go through generated prompts 10 by 10
    for i in range(0, len(generated_prompts), 10):
        for generated_prompt in generated_prompts[i:i + 10]:
            g_prompt += generated_prompt
        tokens = model.count_tokens(g_prompt)
        print(f"Amount of tokens: {tokens}")
        print(g_prompt)

        responses = chat.send_message(g_prompt, generation_config={"temperature": 1})
        print(f"RAW RESPONSE=================")
        print(responses.text)

        if not responses.text:
            print("No sentences generated.")
            return

        replies = responses.text.split('\n')

        # Remove first and last index if it is json
        if replies[0] == '```json' or replies[0] == '```':
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

        g_prompt = ""


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


optimize_prompt = prompt = f"""
Your task is to rewrite sentences based that are not good enough for my project.
You will be rewriting the sentences in steps from most important to least important.
After a sentence have been rewritten you must return it in the format: `<image_name>`;`<new sentences>`

Step 1: Quotes.
Some sentences include quotes while others start with quotes.
However, quotes do not work with the mission I am trying to achieve.
Therefore you must rewrite the sentences such that they do not include quotes. However the sentences must still include all the details as before the quotes are removed.
This means that a conversation or if someone is saying something the sentences should still mention that the person says this, without including quotes.

Return "Understood" when read.
"""


def generate_optimized_sentences_gemini(images: list[str]):
    optimized_sentences_path = f"{setup.PATHS.OUT_TEXT_DIR}/optimized_sentences.txt"

    sentences_dict = get_dict_from_file(setup.PATHS.SENTENCES)
    prompts = []

    for image_name in images:
        description_of_picture = sentences_dict[image_name]
        _prompt = f"{image_name}; {description_of_picture}\n"
        prompts.append(_prompt)

    chat = model.start_chat(history=[])
    chat.send_message(optimize_prompt, generation_config={"temperature": 1})

    for i in range(0, len(prompts), 10):
        o_prompt = ""
        for p in prompts[i:i + 10]:
            o_prompt += p

        tokens = model.count_tokens(o_prompt, generation_config={"temperature": 1})
        print(f"Amount of tokens: {tokens}")
        print(o_prompt)

        response = chat.send_message(o_prompt, generation_config={"temperature": 1})
        print(f"RAW RESPONSE=================")
        print(response.text)

        responses = response.text.split('\n')
        for r in responses:
            if r == '':
                continue

            append_to_file(optimized_sentences_path, r)


def optimize_sentences_gemini():
    optimized_sentences_path = f"{setup.PATHS.OUT_TEXT_DIR}/optimized_sentences.txt"
    images = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, optimized_sentences_path)
    generate_optimized_sentences_gemini(images)
