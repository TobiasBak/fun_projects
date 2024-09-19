import re
import threading

import google.generativeai as genai

import setup
from FileInterfacce import FileInterface
from google.prompts import prompt_describe_image_1, prompt_describe_image_2, prompt_describe_image_3, \
    prompt_generate_sentence_1, prompt_generate_sentence_2, prompt_generate_sentence_3, prompt_generate_sentence_4
from old.open_ai import generate_prompts_for_images
from utils import get_lines_from_file, get_absolute_path, get_images_missing_from_files, \
    append_to_file, get_sentence_path
from PIL import Image

THREADS = 5
semaphore = threading.Semaphore(THREADS)  # Create a semaphore object


def get_api_key():
    with open(get_absolute_path('../Recap/hidden/gemini_key.txt'), 'r') as file:
        lines = file.readlines()
    return lines[0].strip()


genai.configure(api_key=get_api_key())


class Gemini:
    def __init__(self):
        self.out_sentences = get_sentence_path()
        self.out_descriptions = setup.PATHS.DESCRIPTIONS
        self.model_flash = genai.GenerativeModel('gemini-1.5-flash')
        self.model_pro = genai.GenerativeModel('gemini-1.5-pro')
        self.model_1 = genai.GenerativeModel('gemini-1.0-pro')
        self.generation_config = {"temperature": 1}
        self.safety_settings = [
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
            }
        ]

    def generate_description_for_images(self, images: list[str]):
        prompts = [prompt_describe_image_1, prompt_describe_image_2, prompt_describe_image_3]
        chat = self.model_flash.start_chat(history=[])

        for p in prompts:
            r = chat.send_message(p, generation_config=self.generation_config, safety_settings=self.safety_settings)
            print(r.text)

        for image in images:

            content = []
            img_data = Image.open(get_absolute_path(f"{setup.PATHS.IMAGE_DIR}/{image}"))
            content.append(img_data)
            content.append(f"You are describing {image} in detail. \n")

            print(f"Generating description for {image}...")

            response = chat.send_message(
                content,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            print(response.text)

            responses = response.text.split('\n')
            for r in responses:
                if r == '':
                    continue
                parts = r.split(';')
                if len(parts) > 3:
                    print(f"Invalid response: {r}")
                    continue

                append_to_file(self.out_descriptions, r)

    def _threaded_generate_description(self, thread_name, images):
        # Acquire a semaphore
        semaphore.acquire()
        try:
            print(f"Starting thread: {thread_name}")
            self.generate_description_for_images(images)
        finally:
            # Release the semaphore
            semaphore.release()

    def generate_descriptive_text(self):
        images = get_images_missing_from_files(setup.PATHS.IMAGE_DIR, setup.PATHS.DESCRIPTIONS)
        print(f"Starting generation of descriptions for {len(images)} images: ...")

        if len(images) == 0:
            print("No images missing descriptions. Exiting...")
            return

        threads = []
        for i in range(0, len(images), 10):
            thread_name = f"{i}/{len(images)}"
            thread = threading.Thread(target=self._threaded_generate_description, args=(thread_name, images[i:i + 10]))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        if len(get_images_missing_from_files(setup.PATHS.IMAGE_DIR, self.out_descriptions)) > 0:
            print("Some images are still missing descriptions. Will start generation again.")
            self.generate_descriptive_text()

    def generate_sentences_for_images_gemini(self, images: list[str]):
        file_interface = FileInterface()

        generated_prompts = generate_prompts_for_images(images)
        prompts = [prompt_generate_sentence_1, prompt_generate_sentence_2, prompt_generate_sentence_3,
                   prompt_generate_sentence_4]

        if len(generated_prompts) == 0:
            print("No sentences missing. Exiting...")
            return

        chat = self.model_pro.start_chat(history=[])

        for p in prompts:
            r = chat.send_message(p, generation_config=self.generation_config)
            print(r.text)

        g_prompt = ""

        images_per_prompt = 10
        for i in range(0, len(generated_prompts), images_per_prompt):
            for generated_prompt in generated_prompts[i:i + images_per_prompt]:
                g_prompt += generated_prompt
            tokens = self.model_pro.count_tokens(g_prompt)
            print(f"Amount of tokens: {tokens}")
            print(g_prompt)

            responses = None

            try :
                responses = chat.send_message(g_prompt, generation_config=self.generation_config,
                                              safety_settings=self.safety_settings)
            except Exception as e:
                responses = chat.send_message(g_prompt, generation_config=self.generation_config,
                                          safety_settings=self.safety_settings)
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

                #Todo: If it does not start with a number it probably needs to be appended to the previous image

                parts = x.split(';')
                description = parts[1]
                description = description.encode('ascii', 'ignore').decode('ascii')
                if description[:1] == '"' and description[-1:] == '"':
                    description = description[1:-1]

                file_interface.append_line(self.out_sentences, f"{parts[0]};{description}")

            g_prompt = ""

    def generate_sentences_gemini(self):
        images = get_images_missing_from_files(setup.PATHS.IMAGE_DIR, self.out_sentences)
        if len(images) == 0:
            print("No images missing generated sentences.")
            return []

        print(f"Starting generation of sentences for {len(images)} images: ...")

        # Run generate for images in batches batch_size
        batch_size = 100
        for i in range(0, len(images), batch_size):
            self.generate_sentences_for_images_gemini(images[i:i + batch_size])

        raise Exception("Please manually modify the first 50 sentences for a good experience")

    def remove_duplicate_sentences(self):
        lines = get_lines_from_file(self.out_sentences)
        sentences = {}
        for line in lines:
            parts = line.split(';')
            if parts[1] in sentences:
                print(f"Removing duplicate sentence: {parts[1]}")
                continue
            sentences[parts[1]] = parts[0]

        with open(self.out_sentences, 'w') as file:
            for key, value in sentences.items():
                file.write(f"{value};{key}\n")



