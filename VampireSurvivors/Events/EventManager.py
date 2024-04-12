from typing import Callable


class EventManager:
    """Singleton class that manages events and listeners."""
    _instance = None

    def __init__(self):
        self.listeners: dict[Callable] = {}

    def add_listener(self, event_type, listener: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def remove_listener(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)

    def dispatch_event(self, event):
        event_type = type(event)
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(event)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EventManager()
        return cls._instance
