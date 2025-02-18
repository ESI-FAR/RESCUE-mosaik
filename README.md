# RESCUE mosaik

Simulator for RESCUE project using mosaik as co-simulation framework.

## World

Given a grid simulation with a power provider and consumer.
Between the provider and consumer there are 2 switches called switch1 and switch2.
The provider produces 1 unit of power and the consumer needs 1 unit of power.
Each switch will divide the power equally.

A switch can be in 3 modes:
- nominal, the switch passes power.
- bypass, the switch no longer passes power, other switches take up slack. Once in bypass mode the switch can no longer be changed.
- ddos, the switch no longer passes power, other switches do not take up slack. Once in ddos mode the switch can no longer be changed.
- bypass+ddos

Hacker simulation can fire 2 events
- portscan
- start_ddos, 
- stop_ddos, 

Guard simulation will get state (amount of power going through each switch and their modes) from the grid simulation.
The guard simulation can fire a bypass event.

The following events will happen:
- The hacker will fire a portscan event to switch1 on time step 5 and a ddos attack on time step 10.
- The guard will fire a bypass event for switch1 when it sees a portscan event being reported by the grid simulation.

## Scenarios

We will have the following scenarios
1. No hacker, consumer gets full power
2. Hacker and no guard, consumer gets half power
3. Hacker and guard, consumer gets full power

## Development

The simulator is using [uv](https://docs.astral.sh/uv/) as Python package and project manager.

To install 

```bash
pip install -e .
```

To run simulator use
```bash
rescue-mosaik
```

Run ruff check with
 
```bash
uv run ruff check
```

Run ruff format with

```bash
uv run ruff format
```

Run tests with

```bash
uv run pytest
```
