import re
import threading
import time

import google.generativeai as genai

import setup
from FileInterfacce import FileInterface
from google.prompts import combined_prompt_sentences, combined_prompt_descriptions
from old.open_ai import generate_prompts_for_images
from utils import get_lines_from_file, get_absolute_path, get_images_missing_from_files, \
    append_to_file, get_sentence_path, sort_images_by_order, remove_image
from PIL import Image
from google.generativeai.types import HarmCategory, HarmBlockThreshold

THREADS = 5
semaphore = threading.Semaphore(THREADS)  # Create a semaphore object


def get_api_key():
    with open(get_absolute_path('../Recap/hidden/gemini_key.txt'), 'r') as file:
        lines = file.readlines()
    return lines[0].strip()


genai.configure(api_key=get_api_key())


class Gemini:
    def __init__(self):
        self.model_descriptions = genai.GenerativeModel('gemini-1.5-flash',
                                                        system_instruction=combined_prompt_descriptions)
        self.model_sentences = genai.GenerativeModel(model_name='gemini-1.5-flash-exp-0827',
                                                     system_instruction=combined_prompt_sentences)
        self.generation_config = {"temperature": 1, "response_mime_type": "text/plain"}
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

    def generate_description_for_images(self, images: list[str], thread_name: str):
        # chat = self.model_descriptions.start_chat(history=[])
        for image in images:
            content = []
            img_data = Image.open(get_absolute_path(f"{setup.PATHS.IMAGE_DIR}/{image}"))
            content.append(img_data)
            content.append(f"You are describing {image} in detail. \n")

            print(f"Generating description for {image}...")


            response = self.model_descriptions.generate_content(
                content,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )

            if response._error:
                # remove image from folder
                print(f"Error for image {image}: {response._error}")
                remove_image(image)
                continue

            responses = response.text.split('\n')
            for r in responses:
                if r == '':
                    continue
                parts = r.split(';')
                if len(parts) > 3:
                    print(f"Invalid response: {r}")
                    continue
                if len(parts) == 3:
                    r = f"{parts[0]};{parts[1]} {parts[2]}"

                append_to_file(setup.PATHS.DESCRIPTIONS, r)

    def _threaded_generate_description(self, thread_name, images):
        # Acquire a semaphore
        semaphore.acquire()
        try:
            print(f"Starting thread: {thread_name}")
            self.generate_description_for_images(images, thread_name)
        finally:
            # Release the semaphore
            semaphore.release()

    def generate_descriptive_text(self):
        images = get_images_missing_from_files(setup.PATHS.IMAGE_DIR, setup.PATHS.DESCRIPTIONS)
        print(f"Starting generation of descriptions for {len(images)} images: ...")

        if len(images) == 0:
            print("No images missing descriptions. Exiting...")
            return

        batch_size = 10
        threads = []
        for i in range(0, len(images), batch_size):
            thread_name = f"{i}/{len(images)}"
            thread = threading.Thread(target=self._threaded_generate_description, args=(thread_name, images[i:i + batch_size]))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Todo make it actually check the images instead of len(images)
        if len(get_images_missing_from_files(setup.PATHS.IMAGE_DIR, setup.PATHS.DESCRIPTIONS)) > 0:
            print("Some images are still missing descriptions. Will start generation again.")
            self.generate_descriptive_text()

    # def generate_sentences_for_images_gemini(self, images: list[str]):
    #     file_interface = FileInterface()
    #
    #     generated_prompts = generate_prompts_for_images(images)
    #
    #     if len(generated_prompts) == 0:
    #         print("No sentences missing. Exiting...")
    #         return
    #
    #     chat = self.model_sentences.start_chat(history=[])
    #
    #     g_prompt = ""
    #
    #     images_per_prompt = 10
    #     for i in range(0, len(generated_prompts), images_per_prompt):
    #         for generated_prompt in generated_prompts[i:i + images_per_prompt]:
    #             g_prompt += generated_prompt
    #         tokens = self.model_sentences.count_tokens(g_prompt)
    #         print(f"Amount of tokens: {tokens}")
    #         print(g_prompt)
    #
    #         responses = None
    #
    #         try:
    #             responses = chat.send_message(g_prompt, generation_config=self.generation_config,
    #                                           safety_settings=self.safety_settings)
    #         except Exception as e:
    #             responses = chat.send_message(g_prompt, generation_config=self.generation_config,
    #                                           safety_settings=self.safety_settings)
    #         print(f"RAW RESPONSE=================")
    #         print(responses.text)
    #
    #         if not responses.text:
    #             print("No sentences generated.")
    #             return
    #
    #         replies = responses.text.split('\n')
    #
    #         refactored_data = {}
    #         last_key = None
    #         for i in range(len(replies)):
    #             if self._check_if_text_is_key(replies[i]):
    #                 last_key = replies[i]
    #                 if last_key not in refactored_data:
    #                     refactored_data[last_key] = ""
    #             elif last_key is not None:
    #                 refactored_data[last_key] += ' ' + replies[i].replace('\n', ' ')
    #
    #         for key, value in refactored_data.items():
    #             file_interface.append_line(setup.PATHS.SENTENCES, f"{key};{value}")
    #
    #         g_prompt = ""

    def generate_sentences_for_images_gemini_using_prior_sentences(self, images: list[str]):
        file_interface = FileInterface()
        description_dict = file_interface.get_dict_from_file(setup.PATHS.DESCRIPTIONS)
        sentence_path = get_sentence_path(setup.LanguageCodes.English)

        sentence_dict = file_interface.get_dict_from_file(sentence_path)

        chat = self.model_sentences.start_chat(history=[])

        g_prompt = ""

        sorted_images = sort_images_by_order(images)

        images_per_prompt = 5
        prior_sentences = 10
        sleep_between_requests = 10
        for i in range(0, len(sorted_images), images_per_prompt):
            for im in sorted_images[i:i + images_per_prompt]:
                g_prompt += f"{im};{description_dict[im]}\n"

            last_10_sentences = list(sentence_dict.values())[-prior_sentences:]

            g_prompt += "**Prior sentences:**\n"
            g_prompt += "\n".join(last_10_sentences)

            print(f"Sending Prompt: {g_prompt}")

            response = chat.send_message(g_prompt, generation_config=self.generation_config,
                                         safety_settings=self.safety_settings)

            print(f"RAW RESPONSE=================\n{response.text}")

            if not response.text:
                print("No sentences generated.")
                return

            replies = response.text.split('\n')

            for reply in replies:
                if not reply:
                    continue
                parts = reply.split(';')
                if len(parts) != 2:
                    print(f"Invalid response: {reply}")
                    continue
                sentence_dict[parts[0]] = parts[1]
                file_interface.append_line(sentence_path, reply)

            g_prompt = ""
            time.sleep(sleep_between_requests)

    def generate_sentences_gemini(self):
        sentence_path = get_sentence_path(setup.LanguageCodes.English)
        images = get_images_missing_from_files(setup.PATHS.IMAGE_DIR, sentence_path)
        if len(images) == 0:
            print("No images missing generated sentences.")
            return []

        print(f"Starting generation of sentences for {len(images)} images: ...")

        # Run generate for images in batches batch_size
        batch_size = 100
        for i in range(0, len(images), batch_size):
            self.generate_sentences_for_images_gemini_using_prior_sentences(images[i:i + batch_size])
        # self.generate_sentences_for_images_gemini_using_prior_sentences(images)

        raise Exception("Please manually modify the first 50 sentences for a good experience")

    def remove_duplicate_sentences(self, language: setup.LanguageCodes):
        file_interface = FileInterface()
        sentences_path = get_sentence_path(language)
        print(sentences_path)
        lines = file_interface.get_lines_from_file(sentences_path)
        print(lines)
        line_dict = {}
        for line in lines:
            parts = line.split(';')
            if len(parts) != 2:
                print(f"Invalid line: {line}")
                continue
            if parts[0] not in line_dict.keys():
                line_dict[parts[0]] = parts[1]

        file_interface.write_dict_to_file(sentences_path, line_dict)

    def _check_if_text_is_key(self, text: str) -> bool:
        # If text is key it will start with a number followed by a dot followed by a number
        return bool(re.match(r'^\d+\.\d+', text))
