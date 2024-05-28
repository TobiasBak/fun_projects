from ScreenReader.ScreenConverter import read_string_from_game


class ObjectInterface:
    def update(self):
        pass


class Energy(ObjectInterface):
    def __init__(self):
        self.energy = 0
        self.capacity = 0
        self.region = (50, 135, 480, 240)

    def update(self):
        energy_text = read_string_from_game(self.region)
        energy_text = energy_text.replace('\n', ' ')
        text_parts = energy_text.split(' ')
        self.energy = text_parts[1]
        self.capacity = text_parts[3]
        print(f'Energy: {self.energy}/{self.capacity}')
