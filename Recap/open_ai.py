
from openai import OpenAI

import setup
from utils import append_to_file, get_dict_from_file, get_images_missing_from_files

prompt_beginning = f"""
You are narrating over pictures in a picture book. Each picture will have specific elements provided: A: the filename, B: "Text on picture" (the text written on the picture), C: "Descriptive Text" (a description of what is happening in the picture). Your task is to generate two short, simple sentences per picture that are easy for children to understand.

**Instructions:**
1. Generate two very short sentences for each picture.
2. Generated sentences must be very short and simple.
3. Generated sentences must be in present tense.
4. Do not generate sentences that start with "In the".
5. Only generate names if they are mentioned in the "Text on picture" not otherwise.
6. Use pronouns like "he", "she", "they", "the main character", "the protagonist", or "the antagonist" if names are not mentioned in the "Text on picture".
7. Respond to each picture in the format: `<filename>;<sentence1>;<sentence2>`

**Format for each picture:**
- Picture: `<filename>` |
- Text on picture: `<text>` |
- Description of picture: `<description>` |  

**Example:**
Picture: 1.0.0.jpg | Text on picture: GOD- DAMMIT.. | Description of picture: In the heart of the electrified battlefield, Kai clenched his teeth, a mix of frustration and determination etched on his face as he muttered, "God-dammit.. |

**Example response:**
1.4.0.jpg;In the electrified battlefield, the main character clenched his teeth with frustration and determination.;Muttering, "God-dammit," his face etched with a mix of emotions.

**Response format:**
`<filename>;<sentence1>;<sentence2>`

**Pictures**
Below, all pictures are listed. You must generate sentences for each picture. I have given you 50 pictures, so generate 100 sentences!
Don't use names such as "Kai", "Alex", "Adam", "Hana"  if similar names do not appear in B: "Text on picture" texts. 

"""

propmt_ending = """
Remember not to include names in the sentences unless the name is within B: "Text on picture" texts.
You must iterate over each of the 50 above pictures and generate an answer for each.
"""


def get_openai_api_key():
    with open('hidden/openai_key.txt', 'r') as file:
        return file.read().replace('\n', '')


def get_prompt_from_image(image_name, text_on_picture, description_of_picture) -> str:
    return f"Picture: {image_name} | Text on picture: {text_on_picture} | Description of picture: {description_of_picture} |\n"


def openai_generate_text(prompt_overall_story: str = None):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=get_openai_api_key(),
    )

    prompt = prompt_beginning

    if prompt_overall_story is not None:
        prompt += prompt_overall_story

    generated_prompts = generate_prompts_for_images()

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


def generate_prompts_for_images():
    image_names = get_images_missing_from_files(setup.PATHS.OUT_IMAGE_DIR, setup.PATHS.SENTENCES)
    if len(image_names) == 0:
        print("No images missing generated sentences.")
        return []

    file_containing_text_on_pictures = setup.PATHS.TEXT_ON_PICTURES
    file_containing_generated_text = setup.PATHS.DESCRIPTIONS

    text_on_pictures_dict = get_dict_from_file(file_containing_text_on_pictures)
    generated_text_dict = get_dict_from_file(file_containing_generated_text)

    # Only keep first 100 images
    image_names = image_names[:50]

    prompts = []
    for image_name in image_names:
        text_on_picture = text_on_pictures_dict[image_name]
        description_of_picture = generated_text_dict[image_name]
        prompt = get_prompt_from_image(image_name, text_on_picture, description_of_picture)
        prompts.append(prompt)

    return prompts


def get_amount_of_tokens(prompt: str) -> float:
    amount_of_words = len(prompt.split(' '))
    return int(amount_of_words * 1.2)
