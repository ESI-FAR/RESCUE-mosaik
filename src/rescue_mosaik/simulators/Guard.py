import logging
from typing import Any, cast
from mosaik_api_v3 import (
    CreateResult,
    InputData,
    OutputData,
    OutputRequest,
    Simulator,
    Meta,
)

from rescue_mosaik.models.GridState import GridState
from rescue_mosaik.models.Guard import Guard
from rescue_mosaik.models.Event import Listener

logger = logging.getLogger(__name__)

META: Meta = {
    "api_version": "3.0",
    "type": "hybrid",
    "models": {
        "Guard": {
            "public": True,
            "params": [],
            "attrs": ["events", "grid_state"],
            "non-persistent": ["events"],
            "trigger": ["events"],
        }
    },
}


class GuardSimulator(Simulator):
    model: Guard

    def __init__(self):
        super().__init__(META)
        self.listener = Listener()
        self.time = 0

    def create(self, num: int, model: str, **model_params: Any) -> list[CreateResult]:
        if model != "Guard" or num != 1:
            raise ValueError("Only one Guard instance is allowed")

        self.model = Guard(self.listener)

        result: CreateResult = {
            "eid": "Guard_0",
            "type": "Guard",
        }
        return [result]

    def step(self, time: int, inputs: InputData, max_advance: int) -> int:
        # logger.error(f"GuardSimulator.step({time=}, {inputs=}, {max_advance=})")
        self.listener.reset()
        self.time = time

        # map inputs to GridState
        states = cast(dict[str, GridState], inputs["Guard_0"]["grid_state"])
        state = list(states.values())[0]

        self.model.step(time, state)
        return time + 1

    def get_data(self, outputs: OutputRequest) -> OutputData:
        if len(self.listener.events) > 0:
            logger.error(
                f"GuardSimulator.get_data({outputs=}, {self.listener.events=})"
            )
        return {
            "Guard_0": {
                "events": self.listener.events,
            },
            "time": self.time,
        }
