from rescue_mosaik.models.Grid import Grid
from rescue_mosaik.models.GridState import GridState, Switch
from rescue_mosaik.models.Guard import StartByPassEvent
from rescue_mosaik.models.Hacker import PortScanEvent, StartDDOSEvent, StopDDOSEvent


def test_zero_events():
    grid = Grid()
    grid.step(0, [])
    expected = GridState(
        provided_power=100,
        consumed_power=100,
        switches=[
            Switch(50, portscan=False, ddos=False, bypassed=False),
            Switch(50, portscan=False, ddos=False, bypassed=False),
        ],
    )
    assert grid.state == expected

def test_portscan_on_first_switch():
    grid = Grid()
    grid.step(0, [PortScanEvent(0)])
    expected = GridState(
        provided_power=100,
        consumed_power=100,
        switches=[
            Switch(50, portscan=True, ddos=False, bypassed=False),
            Switch(50, portscan=False, ddos=False, bypassed=False),
        ],
    )
    assert grid.state == expected

def test_ddos_on_first_switch():
    grid = Grid()
    grid.step(0, [StartDDOSEvent(0)])
    expected = GridState(
        provided_power=100,
        consumed_power=50,
        switches=[
            Switch(0, portscan=False, ddos=True, bypassed=False),
            Switch(50, portscan=False, ddos=False, bypassed=False),
        ],
    )
    assert grid.state == expected


def test_bypass_on_first_switch():
    grid = Grid()
    grid.step(0, [StartByPassEvent(0)])
    expected = GridState(
        provided_power=100,
        consumed_power=100,
        switches=[
            Switch(0, portscan=False, ddos=False, bypassed=True),
            Switch(100, portscan=False, ddos=False, bypassed=False),
        ],
    )
    assert grid.state == expected

def test_bypass_and_ddos_on_first_switch():
    grid = Grid()
    grid.step(0, [StartByPassEvent(0), StartDDOSEvent(0)])
    expected = GridState(
        provided_power=100,
        consumed_power=100,
        switches=[
            Switch(0, portscan=False, ddos=True, bypassed=True),
            Switch(100, portscan=False, ddos=False, bypassed=False),
        ],
    )
    assert grid.state == expected

def test_given_bypass_and_toggle_ddos_on_first_switch():
    grid = Grid()
    grid.step(0, [StartByPassEvent(0)])
    grid.step(1, [StartDDOSEvent(0)])
    grid.step(2, [StopDDOSEvent(0)])
    expected = GridState(
        provided_power=100,
        consumed_power=100,
        switches=[
            Switch(0, portscan=False, ddos=False, bypassed=True),
            Switch(100, portscan=False, ddos=False, bypassed=False),
        ],
    )
    assert grid.state == expected
