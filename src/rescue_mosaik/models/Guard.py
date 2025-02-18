from dataclasses import dataclass
import logging

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


logger = logging.getLogger(__name__)


class Guard:
    def __init__(self, dispatcher=noop_dispatch):
        self.dispatcher = dispatcher
        # to disable bypass model needs to know when ddos is turned off
        # TODO scale to number of switches in grid state
        self.previous_state = [False, False]

    def step(self, time: int, inputs: GridState):
        for switch_id, switch in enumerate(inputs.switches):
            if switch.portscan:
                self.dispatcher(StartByPassEvent(switch_id))
            prev = self.previous_state[switch_id]
            ddos_switched_off = not switch.ddos and prev
            if switch.bypassed and ddos_switched_off:
                self.dispatcher(StopByPassEvent(switch_id))
            self.previous_state[switch_id] = switch.ddos
