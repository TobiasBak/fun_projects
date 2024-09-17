import re
import setup
from FileInterfacce import FileInterface
from utils import get_sentence_path

"""This file contains functions to optimize strings in the dataset."""


def optimize_descriptions():
    file_interface = FileInterface()
    description_dict = file_interface.get_dict_from_file(setup.PATHS.DESCRIPTIONS)

    for key, value in description_dict.items():
        description = value

        if len(description) > 1500:
            print(f"Removing long description: {description}")
            description = description[:1500]

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
        sentence_dict[key] = description

    file_interface.write_dict_to_file(path, sentence_dict)


def _remove_descriptions_about_voices(description: str):
    out = re.sub(r',\s*his voice[^,.]*[.,]', '.', description)
    out = re.sub(r',\s*her voice[^,.]*[.,]', '.', out)
    return out



def _remove_specific_strings_from_text(description: str):
    strings_to_remove = [
        "reaperscans.com", "reaperscans", "luascans", "luascans.com",
        ">", "<", "&"
    ]

    for string in strings_to_remove:
        description = description.replace(string, "")

    return description


