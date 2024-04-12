from Events.EventManager import EventManager


class SystemInterface:
    def __init__(self):
        self.event_mananger = EventManager.get_instance()

    def update(self, dt: float):
        pass

    def __str__(self):
        return "SystemInterface"

    def __repr__(self):
        return self.__str__()

