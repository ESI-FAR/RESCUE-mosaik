from dataclasses import dataclass

from rescue_mosaik.models.GridState import GridState
from .Event import noop_dispatch


@dataclass
class StartByPassEvent:
    type = "startbypass"
    switch: int


@dataclass
class StopByPassEvent:
    type = "stopbypass"
    switch: int


class Guard:
    def __init__(self, dispatcher=noop_dispatch):
        self.dispatcher = dispatcher

    def step(self, time: int, inputs: GridState):
        for switch_id, switch in enumerate(inputs.switches):
            if switch.portscan:
                self.dispatcher(StartByPassEvent(switch_id))
            if not switch.ddos and switch.bypassed:
                self.dispatcher(StopByPassEvent(switch_id))
