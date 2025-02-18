from typing import Protocol


class Event(Protocol):
    type: str
    switch: int


def noop_dispatch(event: Event):
    pass


class Listener:
    def __init__(self):
        self.events = []

    def __call__(self, event: Event):
        self.events.append(event)

    def reset(self):
        self.events = []
