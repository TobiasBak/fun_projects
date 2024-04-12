from Events.EventManager import EventManager


class SystemInterface:
    """ Interface for all systems. All system has access to the event manager."""
    def __init__(self):
        self.event_manager = EventManager.get_instance()

    def update(self, dt: float):
        pass

    def __str__(self):
        return "SystemInterface"

    def __repr__(self):
        return self.__str__()

