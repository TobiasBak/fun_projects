from Events.EventManager import EventManager


class SystemInterface:
    """ Interface for all systems. All system has access to the event manager."""
    def update(self, dt: float):
        pass

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

