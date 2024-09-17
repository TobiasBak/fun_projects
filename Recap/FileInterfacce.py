import csv
import os
import setup

class FileInterface:
    def _clean_text(self, text: str):
        # Remove newlines and other unwanted characters
        out = text.replace('\n', '').replace('\r', '')
        out = out.replace('<', '').replace('>', '').replace('&', '')
        return out

    def append_line(self, file_path: str, line: str):
        clean_line = self._clean_text(line)
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            file.write(clean_line + '\n')

    def append_key_value(self, file_path: str, key: str, value: str):
        clean_key = self._clean_text(key)
        clean_value = self._clean_text(value)
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([clean_key, clean_value])

    def write_dict_to_file(self, file_path: str, data_dict: dict):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            for key, value in data_dict.items():
                clean_key = self._clean_text(key)
                clean_value = self._clean_text(value)
                writer.writerow([clean_key, clean_value])

    def get_dict_from_file(self, file_path: str) -> dict:
        data_dict = {}

        if not os.path.exists(file_path):
            return data_dict

        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 2:
                    data_dict[row[0]] = row[1]
        return data_dict

    def get_images_missing_from_file(self, file_path: str) -> list:
        keys = []

        # If the file does not exist, return all images
        if not os.path.exists(file_path):
            return self._get_images_as_list()

        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                keys.append(row[0])
        images = self._get_images_as_list()
        missing_images = [image for image in images if image not in keys]
        return missing_images

    def _get_images_as_list(self) -> list:
        directory = setup.PATHS.IMAGE_DIR
        images = []
        for file in os.listdir(directory):
            if file.endswith(".jpg"):
                images.append(file)
        return images