import csv

class FileInterface:
    def _clean_text(self, text):
        # Remove newlines and other unwanted characters
        return text.replace('\n', '').replace('\r', '').replace(';', '')

    def append_line(self, file_path, line):
        clean_line = self._clean_text(line)
        with open(file_path, 'a', newline='') as file:
            file.write(clean_line + '\n')

    def write_dict_to_file(self, file_path, data_dict):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for key, value in data_dict.items():
                writer.writerow([key, value])

    def get_dict_from_file(self, file_path):
        data_dict = {}
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 2:
                    data_dict[row[0]] = row[1]
        return data_dict