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
Each image should be described by one sentence narrating what is going on in the image.
Generated narrations should also include the text/conversations from the descriptions.

**Task Outline:**
1. You will be given descriptions of images. Each description includes specific details about context of the image and what is written in the image.
2. Based on these descriptions, generate a sentence for each image that collectively form a continuous story in present tense.
3. Ensure the sentences are in present tense flow logically from one to the next, maintaining a coherent and engaging narrative.

Return "Understood" when read
"""

prompt_generate_sentence_2 = f"""
You must uphold the following rules and guidelines

**Rules and Guidelines:**
1. Avoid Direct References to the Image: Do not use phrases like "In the picture" or "The image shows."
2. Sentence lengths: Each image should be described by a short and single sentence and the conversations from the image.
3. If the context and location changes drastically. It should be described as a new location or a flashback. 
4. Keep sentences simple by using at most 1 adverb and 1 adjective.
5. Use pronouns and character descriptions when referring to characters. Do not use character names.
6. Never mention the viewer, reader or speaker in the sentences.
7. Include all conversation from the text from the image

Return "Understood" when the rules and guidelines are understood.
"""

prompt_generate_sentence_3 = f"""
You must follow the process when generating sentences based on the descriptions

**Process:**
1. Read the Description: Carefully read and understand each image description.
2. Extract Key Elements: Identify key elements such as characters, settings, actions and information.
3. Generate Sentence: Formulate a short sentence in present tense that contributes to the overall narrative.
4. Following Rules and Guidelines: Ensure generated sentence follow rules and guidelines.

Return "Understood" when it is understood.
"""

prompt_generate_sentence_4 = f"""
**Output:**
For each of the inputted lines, generate a single return string in the following format:
`<image_name>`; `<story>`
`<story>` should include all the generated sentences about the image.
The return should be plaintext, not in JSON format.

Return "Understood" when read. 
"""


