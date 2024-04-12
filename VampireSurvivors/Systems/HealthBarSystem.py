from Systems.SystemInterface import SystemInterface


class HealthBarSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        pass

    def __str__(self):
        return "HealthBarSystem"