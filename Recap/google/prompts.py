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
5. Text: English text should be extracted from the image in lowercase. The text should be followed by where it is positioned relative to the characters.

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

prompt_generate_sentence_1 = f"""
**AI Mission Brief:** Turning Image Descriptions into a Narrative
**Mission Objective:**
You are tasked with transforming a series of detailed image descriptions into a coherent, flowing story in english. 
Each sentence generated should contribute to the overall narrative and provide seamless transitions. 
Each image should be described by two sentences that contribute to the overall narrative.

**Task Outline:**
1. You will be given descriptions of 100 images. Each description includes specific details about the visual elements and context of the image.
2. Based on these descriptions, generate two sentences for each image that collectively form a continuous story in present tense.
3. Ensure the sentences flow logically from one to the next, maintaining a coherent and engaging narrative.

Return "Understood" when read
"""

prompt_generate_sentence_2 = f"""
You must uphold the following rules and guidelines

**Rules and Guidelines:**
1. Avoid Direct References to the Image: Do not use phrases like "In the picture" or "The image shows."
2. Use conversation from the image as part of the story.
3. Natural Transitions: Create smooth transitions between sentences and scenes. Ensure each sentence logically follows the previous one, building a continuous and engaging narrative.
4. Vary Sentence Structure: Use a variety of words to start sentences to keep the narrative engaging and dynamic.
5. Sentence lengths: Each image should be described by two simple sentences focusing on setting and actions.
6. If the context and location changes drastically. It should be described as a new location or a flashback. 
7. Reduce the amount of commas in the sentences by using more periods.
8. Use pronouns and character descriptions when referring to characters. Do not use character names.
9. Never mention the viewer, reader or speaker in the sentences.

Return "Understood" when the rules and guidelines are understood.
"""

prompt_generate_sentence_3 = f"""
You must follow the process when generating sentences based on the descriptions

**Process:**
1. Read the Description: Carefully read and understand each image description.
2. Extract Key Elements: Identify key elements such as characters, settings, and actions.
3. Generate Sentence: Formulate a sentence in present tense that incorporates these elements and contributes to the overall narrative.
4. Ensure Continuity: Ensure each generated sentence logically follows the previous one, maintaining narrative coherence.
5. Following Rules and Guidelines: Ensure generated sentence follow rules and guidelines.
By adhering to these guidelines, you will create a compelling and seamless story that effectively translates the visual and emotional content to a fluent story.

Return "Understood" when it is understood.
"""

prompt_generate_sentence_4 = f"""
Following is examples on input and output and the expected output format.

**Example Input Description:**
1.0.B.jpg; There is text above him that says 'E-Rank Hunter.' There is more text below him that says 'The Hunter Guild's' and 'Haa.' The image conveys a feeling of despair and determination. A young man is lying on the ground, bleeding profusely from multiple wounds. He is wearing a blue hoodie with the hood up. His hair is short and dark. His face is contorted in pain, but he has a determined look in his eyes. The background is dark, and it appears he is in some sort of abandoned building.


**Example Output Sentence:**
1.0.B.jpg; Clutching his bleeding wounds, the young man struggled to rise from the cold floor. Despite the pain etched across his face, Sung Jin-Woo's eyes burned with determination.


**Output:**
For each of the inputted lines, generate a single return string in the following format:
`<image_name>`; `<story>`
`<story>` should include all the generated sentences about the image.
The return should be plaintext, not in JSON format.

Return "Understood" when read. 
"""



# def get_files_that_gemini_deem_unnecessary():
#     _prompt = prompt_unnecessary_lines
#     lines_from_file = get_lines_from_file(setup.PATHS.DESCRIPTIONS)
#     for line in lines_from_file:
#         _prompt += line + '\n'
#
#     print(f"Gemini is finding unnecessary lines in the descriptions...")
#
#     _prompt += prompt_unnecessary_lines_end
#
#     tokens = model.count_tokens(_prompt)
#     print(f"Amount of tokens: {tokens}")
#
#     responses = model.generate_content(_prompt)
#
#     print(responses)
#
#     if not responses.candidates:
#         print("No sentences generated.")
#         return
#
#     # If there are candidates, get the first one (usually the best)
#     first_candidate = responses.candidates[0]
#     print(first_candidate.content)  # Print the generated text
#     if first_candidate is None:
#         print("No unnecessary lines found.")
#         return
#
#     print(responses.text)