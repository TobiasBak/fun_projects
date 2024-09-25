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

combined_prompt_descriptions = f"""
You are tasked with describing a picture in detail.
The picture is taken from a Manhwa. 
You must never mention the viewer or reader in the descriptions.


**Instructions:**
1. Generate a detailed description for each of the sub-pictures in the jpg.
2. If the image have multiple areas, describe each area in detail. However, combine all descriptions into a single string.
3. Do not describe Speech Bubbles.
4. Combine all the descriptions into a single description for the jpg.


**How to describe jpgs in detail:**
You must generate an in depth description for each jpg that include the following elements combined in a single string:
1. Characters: Visible characters must be described in detail. Never describe where they are looking. 
2. Setting: The setting and area in the picture must be described. 
3. Actions: The actions happening in the picture must be described.
4. Text: You must extract all English text from speech bubbles should be extracted from the image in lowercase.
5. Exclude text that is ads such as "Read at:" or "Visit us at:". or .com sites in general.
6. Exclude all text describing actions such as "vroom", "bang" "Gurgle" and non-english characters.


**Return Format:**
The combined description must be returned in the following format. This means remove all newlines and replace them with a space.:
`<file_name>`; `<combined descriptions>`
You must only return 1 string containing all the details from the descriptions.

**Format of combined descriptions:**
The combined descriptions should be in the following format:
`<file_name>`; *Text*: "<text>", *Characters*: "<characters>", *Setting*: "<setting>", *Actions*: "<actions>"


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

combined_prompt_sentences = f"""
**AI Mission Brief:** Turning Image Descriptions into a Narrative
**Mission Objective:**
You are tasked with transforming a series of detailed image descriptions into a coherent, flowing story in english. 
Each sentence generated should contribute to the overall narrative and provide seamless transitions between images. 


**Task Outline:**
1. You will be given a description of images. Each description includes specific details about the text in the image, the characters, the setting and the actions.
2. You will also be given prior sentences that have been generated from previous images.
3. Based on the context of the prior sentences and the image descriptions, generate simple short sentence continuing the story. 
4. If the description contains text, prioritize the text in the sentence.


**Rules and Guidelines:**
1. If the description includes text, prioritize incorporating entirety of the text into the sentences.
2. Avoid Direct References to the Image: Do not use phrases like "In the picture" or "The image shows."
3. Use pronouns when mentioning characters and never mention character names. 
4. Never mention the viewer, reader or speaker in the sentences.
5. Do not describe the character and their actions in detail. Instead focus on the story the image is telling.
6. Limit yourself to one adjective and adverb.
7. Never include dialog attributions in the sentences such as "he said" or "she asked", "they replied", "he shouts" etc.
8. Never include sound effects in the sentences.
9. Never include who is saying the text in the generated sentence.
10. Never include what direction the character is looking in the generated sentence.



**Process:**
1. Read the Description: Carefully read and understand the description.
2. Extract Key Elements: Identify key elements such as returning characters, settings, actions and information.
3. Look at the prior sentences: Carefully read the prior sentences to understand the context.
4. Generate Sentences: Formulate sentences in present tense that continues the story. If no prior sentences are available, start the story.
5. Following Rules and Guidelines: Ensure generated sentence follow rules and guidelines.

Run the process for each image description and generate a short narrative that flows smoothly from one image to the next.

**Output:**
For the output, generate strings in the following format, for each of the given descriptions:
`<image_name>`; `<story>`
`<story>` should include the generated sentence continuing the story.
The return should be plaintext, not in JSON format.
"""

