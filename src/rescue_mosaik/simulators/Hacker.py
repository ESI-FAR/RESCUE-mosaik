import logging
from typing import Any
from mosaik_api_v3 import (
    CreateResult,
    InputData,
    Simulator,
    Meta,
)

from rescue_mosaik.models.Hacker import Hacker
from rescue_mosaik.models.Event import Listener

logger = logging.getLogger(__name__)

META: Meta = {
    "api_version": "3.0",
    "type": "hybrid",
    "models": {
        "Hacker": {
            "public": True,
            "params": [],
            "attrs": ["events"],
            "non-persistent": ["events"],
            "trigger": ["events"],
        }
    },
}


class HackerSimulator(Simulator):
    model: Hacker

    def __init__(self):
        super().__init__(META)
        self.listener = Listener()
        self.time = 0

    def create(self, num: int, model: str, **model_params: Any) -> list[CreateResult]:
        if model != "Hacker" or num != 1:
            raise ValueError("Only one Hacker instance is allowed")

        self.model = Hacker(self.listener)

        result: CreateResult = {
            "eid": "Hacker_0",
            "type": "Hacker",
        }
        return [result]

    def step(self, time: int, inputs: InputData, max_advance: int) -> int:
        # logger.error(f"HackerSimulator.step({time=}, {inputs=})")
        self.listener.reset()
        self.model.step(time)
        self.time = time
        return time + 1

    def get_data(self, outputs):
        # if len(self.listener.events) > 0:
        #     logger.error(
        #         f"HackerSimulator.get_data({outputs=}, {self.listener.events=})"
        #     )
        return {
            "Hacker_0": {
                "events": self.listener.events,
            },
            "time": self.time,
        }
