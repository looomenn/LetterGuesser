from typing import Callable, List


class Event:
    def __init__(self):
        self.listeners: List[Callable] = []

    def subscribe(self, listener: Callable):
        """ Add a listener function to be called when the event is triggered. """
        if listener not in self.listeners:
            self.listeners.append(listener)

    def unsubscribe(self, listener: Callable):
        """ Remove a listener function. """
        if listener in self.listeners:
            self.listeners.remove(listener)

    def notify(self, *args, **kwargs):
        """ Call all subscribed listeners with provided arguments. """
        for listener in self.listeners:
            listener(*args, **kwargs)
