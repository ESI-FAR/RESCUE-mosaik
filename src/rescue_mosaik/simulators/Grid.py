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

from rescue_mosaik.models.Event import Event
from rescue_mosaik.models.Grid import Grid

META: Meta = {
    "api_version": "3.0",
    "type": "hybrid",
    "models": {
        "Grid": {
            "public": True,
            "params": [],
            "attrs": ["grid_state", "events"],
            "trigger": ["events"],
        }
    },
}

logger = logging.getLogger(__name__)


class GridSimulator(Simulator):
    model: Grid

    def __init__(self):
        super().__init__(META)

    def create(self, num: int, model: str, **model_params: Any) -> list[CreateResult]:
        if model != "Grid" or num != 1:
            raise ValueError("Only one Grid instance is allowed")

        self.model = Grid()

        result: CreateResult = {
            "eid": "Grid_0",
            "type": "Grid",
        }
        return [result]

    def step(self, time: int, inputs: InputData, max_advance: int) -> int:
        # TODO Convert inputs to the format that the model expects
        # GridSimulator.step(time=5, inputs={'Grid_0': {'events': {'HackerSimulator-0.Hacker_0': [PortScanEvent(switch=1)]}}}, max_advance=4)
        logger.error(f"GridSimulator.step({time=}, {inputs=}, {max_advance=})")
        # TODO step is run for guard and hacker, should only run once per time step
        # GridSimulator.step(time=7, inputs={'Grid_0': {'events': {'HackerSimulator-0.Hacker_0': []}}}, max_advance=6)
        # GridSimulator.step(time=7, inputs={'Grid_0': {'events': {'GuardSimulator-0.Guard_0': []}}}, max_advance=7)

        events: list[Event] = []
        if "Grid_0" in inputs:
            other_events = cast(dict[str, list[Event]], inputs["Grid_0"]["events"])
            for event in other_events.values():
                events.extend(event)

        self.model.step(time, events)
        return time + 1

    def get_data(self, outputs: OutputRequest) -> OutputData:
        # TODO only return what is requested in outputs
        # logger.error(f"GridSimulator.get_data({self.model.state=})")
        return {
            "Grid_0": {
                "grid_state": self.model.state,
            }
        }
