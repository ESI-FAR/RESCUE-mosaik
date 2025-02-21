from dataclasses import dataclass

from .Event import noop_dispatch


@dataclass
class PortScanEvent:
    type = "portscan"
    switch: int


@dataclass
class StartDDOSEvent:
    type = "startddos"
    switch: int


@dataclass
class StopDDOSEvent:
    type = "stopddos"
    switch: int


class Hacker:
    def __init__(self, dispatcher=noop_dispatch):
        self.dispatcher = dispatcher

    def step(self, time: int):
        if time == 2:
            self.dispatcher(PortScanEvent(1))
        if time == 6:
            self.dispatcher(StartDDOSEvent(1))
        if time == 10:
            self.dispatcher(StopDDOSEvent(1))
