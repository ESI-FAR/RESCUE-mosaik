from typing import Protocol


class Event(Protocol):
    type: str
    switch: int


def noop_dispatch(event: Event):
    pass
