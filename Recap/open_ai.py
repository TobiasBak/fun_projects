from openai import OpenAI

import setup
from utils import append_to_file, get_dict_from_file, get_images_missing_from_files

prompt_beginning = f"""
You are narrating over pictures in a picture book. 
Each picture will have specific elements provided: 
- A: the filename, 
- B: "Text on picture" (the text written on the picture), 
- C: "Descriptive Text" (a description of what is happening in the picture). 

Your task is to generate a sentence about what is happening in the picture.

**Following is a short description of overall story to guide you in generating sentences.**
{setup.STORY}

**Allowed names in the sentences:**
[{setup.AllOWED_NAMES}]

**Instructions:**
1. Generate a sentence for each picture.
2. Generated sentences must be simple to understand.
3. Generated sentences must be in present tense.
4. Do not generate sentences that start with "In the".
5. Only include names in generated sentences if they are in the allowed names list.
6. Use pronouns like "he", "she", "they", "the man", or "the woman" instead of names.
7. Respond to each picture in the format: `<filename>;<sentence1>`

**Format for each picture:**
- Picture: `<filename>` |
- Text on picture: `<text>` |
- Description of picture: `<description>` |  

**Response format:**
`<filename>;<sentence1>

**Pictures**
Below, all pictures are listed. Please use the provided text for pictures to guide you narration of the story.
Don't use names such as "Kai", "Alex", "Adam", "Hana" that are not in the allowed names list.  

"""

propmt_ending = f"""
Do not include names in the generated sentences unless they are one of [{setup.AllOWED_NAMES}]. 
You must iterate over each of the 50 above pictures and generate an answer for each that includes the short sentences.
"""


def get_openai_api_key():
    with open('hidden/openai_key.txt', 'r') as file:
        return file.read().replace('\n', '')


def get_prompt_from_image(image_name, text_on_picture, description_of_picture) -> str:
    return f"Picture: {image_name} | Text on picture: {text_on_picture} | Description of picture: {description_of_picture} |\n"


def openai_generate_text(images: list):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=get_openai_api_key(),
    )

    prompt = prompt_beginning

    generated_prompts = generate_prompts_for_images(images)

    if len(generated_prompts) == 0:
        print("No sentences missing. Exiting...")
        return

    for generated_prompt in generated_prompts:
        prompt += generated_prompt

    prompt += propmt_ending

    print(prompt)
    print(f"Amount of tokens: {get_amount_of_tokens(prompt)}")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    # Extract the content of the assistant's reply
    reply = chat_completion.choices[0].message.content

    replies = reply.split('\n')

    for x in replies:
        if x != '':
            print(x)
            append_to_file(setup.PATHS.SENTENCES, x)


def generate_prompts_for_images(images: list):
    file_containing_text_on_pictures = setup.PATHS.TEXT_ON_PICTURES
    file_containing_generated_text = setup.PATHS.DESCRIPTIONS

    text_on_pictures_dict = get_dict_from_file(file_containing_text_on_pictures)
    generated_text_dict = get_dict_from_file(file_containing_generated_text)

    prompts = []
    for image_name in images:
        text_on_picture = text_on_pictures_dict[image_name]
        description_of_picture = generated_text_dict[image_name]
        prompt = get_prompt_from_image(image_name, text_on_picture, description_of_picture)
        prompts.append(prompt)

    return prompts


def get_amount_of_tokens(prompt: str) -> float:
    amount_of_words = len(prompt.split(' '))
    return int(amount_of_words * 1.2)


def generate_sentences():
    images = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, setup.PATHS.SENTENCES)
    if len(images) == 0:
        print("No images missing generated sentences.")
        return []

    # Run generate for images in batches of 50
    for i in range(0, len(images), 50):
        openai_generate_text(images[i:i + 50])
