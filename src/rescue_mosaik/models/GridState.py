from dataclasses import dataclass


@dataclass
class Switch:
    power: float
    portscan: bool
    ddos: bool
    bypassed: bool


@dataclass
class GridState:
    provided_power: float
    consumed_power: float
    switches: list[Switch]
