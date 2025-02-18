from .GridState import GridState, Switch
from .Event import Event


class Grid:
    state: GridState

    def __init__(self):
        # TODO make configurable
        self.state = GridState(
            100,
            100,
            [
                Switch(50, False, False, False),
                Switch(50, False, False, False),
            ],
        )

    def step(self, time: int, inputs: list[Event]):
        # process events
        for switch in self.state.switches:
            switch.portscan = False
        for event in inputs:
            # Hacker events
            if event.type == "portscan":
                self.state.switches[event.switch].portscan = True
            elif event.type == "startddos":
                self.state.switches[event.switch].ddos = True
            elif event.type == "stopddos":
                self.state.switches[event.switch].ddos = False
            # Guard events
            elif event.type == "startbypass":
                self.state.switches[event.switch].bypassed = True
            elif event.type == "stopbypass":
                self.state.switches[event.switch].bypassed = False
            else:
                raise ValueError(f"Unknown event type: {event.type}")

        # calculate power throughput
        nr_passing_switches = len([s for s in self.state.switches if not s.bypassed])
        power_per_switch = self.state.provided_power / nr_passing_switches
        for switch in self.state.switches:
            if switch.bypassed:
                switch.power = 0
            elif switch.ddos:
                switch.power = 0
            else:
                switch.power = power_per_switch

        # calculate consumed power
        self.state.consumed_power = sum(s.power for s in self.state.switches)
