import re
import setup
from FileInterfacce import FileInterface
from utils import get_sentence_path

"""This file contains functions to optimize strings in the dataset."""

strings_to_remove = [
    "reaperscans.com", "reaperscans", "luascans", "luascans.com", "lightscans", "lightscans.com", "mangadex",
    ">", "<", "&", ".fun", ".com", "Read at:", "read:", "read at:", "read at", "translation",
    "to read this series and chapters", "for the fastest releases",
    "To support us", "to support us", "To support the author", "to support the author",
    "To support the scanlation group",
    "to continue !", "Visit to read this series up to chapter 10"
]


def optimize_descriptions():
    file_interface = FileInterface()
    description_dict = file_interface.get_dict_from_file(setup.PATHS.DESCRIPTIONS)

    print(f"Removing specifict strings from descriptions")
    for key, value in description_dict.items():
        description = value

        if len(description) > 1500:
            print(f"Removing long description: {description}")
            description = description[:1500]

        description = _remove_specific_strings_from_text(description)
        description = description.replace('a speech bubble', 'text')
        description = description.replace('speech bubble', 'text')
        description = description.replace('~', '').replace('(', '').replace(')', '')
        description = description.replace(',"', '."')

        # Remove all non-ascii characters
        description = description.encode('ascii', 'ignore').decode('ascii')

        description_dict[key] = description

    file_interface.write_dict_to_file(setup.PATHS.DESCRIPTIONS, description_dict)


def should_remove_quote(quote: str):
    # If quote only contains dots or commas, remove it
    if quote.replace('.', '').replace(',', '').replace(' ', '') == '':
        return True


def optimize_description_quotes():
    file_interface = FileInterface()
    description_dict = file_interface.get_dict_from_file(setup.PATHS.DESCRIPTIONS)
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

    file_interface.write_dict_to_file(setup.PATHS.DESCRIPTIONS, description_dict)


def optimize_sentences_errors(language: setup.LanguageCodes):
    path = get_sentence_path(language)
    file_interface = FileInterface()
    sentence_dict = file_interface.get_dict_from_file(path)

    print(f"Optimizing errors in {len(sentence_dict)}...")
    for key, value in sentence_dict.items():
        description = value
        description = _remove_specific_strings_from_text(description)
        description = _remove_descriptions_about_voices(description)
        description = description.replace('"', '').replace('""', '')
        description = _capitalize_letters(description)
        sentence_dict[key] = description

    file_interface.write_dict_to_file(path, sentence_dict)


def _remove_descriptions_about_voices(description: str):
    out = re.sub(r',\s*his voice[^,.]*[.,]', '.', description)
    out = re.sub(r',\s*her voice[^,.]*[.,]', '.', out)
    return out


def _remove_specific_strings_from_text(description: str):
    global strings_to_remove
    for string in strings_to_remove:
        description = description.replace(string, "")

    return description


def _capitalize_letters(description: str):
    # Capitalize first letter of each sentence
    sentences = description.split('.')
    for i, sentence in enumerate(sentences):
        if sentence == '':
            continue
        if sentence == ' ':
            sentences[i] = ''
            continue
        sentences[i] = ' ' + sentence.strip().capitalize()
    return '.'.join(sentences)
