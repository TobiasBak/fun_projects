import os

from openai import OpenAI

from consts import OUT_TEXT_DIR, OUT_IMAGE_DIR
from utils import append_to_file

prompt_beginning = """
You are narrating over pictures in a picture book. Each picture will have specific elements provided: A: the filename, B: "Text on picture" (the text written on the picture), C: "Descriptive Text" (a description of what is happening in the picture). Your task is to generate two short, simple sentences per picture that are easy for children to understand.

**Instructions:**
1. Generate two very short sentences for each picture.
2. Sentences must be very short and simple.
3. Sentences must be in present tense.
4. Do not start sentences with "In the".
5. Only use names if they are mentioned in the "Text on picture" not otherwise.
6. Use pronouns like "he", "she", "they", "the main character", "the protagonist", or "the antagonist" if names are not mentioned in the "Text on picture".

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
Below, all pictures are listed. You must generate sentences for each picture. If you are given 100 pictures, the string you return must contain 200 sentences.
Don't use names such as "Kai" if similar names do not appear in B: "Text on picture" texts. 
"""


def get_openai_api_key():
    with open('hidden/openai_key.txt', 'r') as file:
        return file.read().replace('\n', '')


def get_prompt_from_image(image_name, text_on_picture, description_of_picture) -> str:
    return f"Picture: {image_name} | Text on picture: {text_on_picture} | Description of picture: {description_of_picture} |\n"


def openai_generate_text(name: str, prompt_overall_story: str = None):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=get_openai_api_key(),
    )

    prompt = prompt_beginning

    if prompt_overall_story is not None:
        prompt += prompt_overall_story

    generated_prompts = generate_prompts_for_images(name)

    for generated_prompt in generated_prompts:
        prompt += generated_prompt

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
            append_to_file(f'{OUT_TEXT_DIR}/eng.{name}_openai_generated.csv', x + '\n')


def generate_prompts_for_images(name: str):
    image_names = []
    for file in os.listdir(OUT_IMAGE_DIR):
        if file.endswith(".jpg"):
            image_names.append(file)

    file_containing_text_on_pictures = f'{OUT_TEXT_DIR}/eng.{name}_text_on_pictures.csv'
    file_containing_generated_text = f'{OUT_TEXT_DIR}/eng.{name}_generated_text.csv'

    text_on_pictures_dict = {}
    with open(file_containing_text_on_pictures, 'r') as file:
        for line in file:
            parts = line.split(',')
            text_on_pictures_dict[parts[0]] = parts[1].replace('\n', '')

    generated_text_dict = {}
    with open(file_containing_generated_text, 'r') as file:
        for line in file:
            parts = line.split(';')
            generated_text_dict[parts[0]] = parts[1].replace('\n', '')

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
