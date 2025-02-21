# RESCUE mosaik

> [!NOTE]
> This is a personal experiment by @sverhoeven to learn the [mosaik framework](https://mosaik.readthedocs.io/) by applying it to a scenario, made up by me, in the world of the [RESCUE project](https://research-software-directory.org/projects/rescue).

Simulator for [RESCUE project](https://research-software-directory.org/projects/rescue) using [mosaik](https://gitlab.com/mosaik/mosaik) as co-simulation framework.

## World

Given a grid simulation with a power provider and consumer.
Between the provider and consumer there are 2 switches called switch1 and switch2.
The provider produces 100 units of power and the consumer needs 100 units of power.
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

<details>
<summary>Click to see the output</summary>

```bash

        ____                              _ _
       /    \                            (_) |
  ____/      \  _ __ ___   ___  ___  __ _ _| | __
 /    \      / | '_ ` _ \ / _ \/ __|/ _` | | |/ /
/      \____/  | | | | | | (_) \__ \ (_| | |   <
\      /    \  |_| |_| |_|\___/|___/\__,_|_|_|\_\
 \____/      \____
 /    \      /    \     mosaik: 3.4.0
/      \____/      \       API: 3.0.13
\      /    \      /    Python: 3.12.3
 \____/      \____/         OS: Linux-6.8.0-52-generic-x86_64-with-glibc2.39
      \      /            Docs: https://mosaik.readthedocs.io/en/3.4.0/
       \____/     Get in touch: https://github.com/orgs/OFFIS-mosaik/discussions

2025-02-21 08:44:59.765 | WARNING  | mosaik.async_scenario:__init__:311 - You are running your simulation in debug mode. This can lead to significant slow-downs, as it will create a graph of the entire execution. Only use this mode if you intend to analyze the execution graph afterwards.
2025-02-21 08:44:59.765 | INFO     | mosaik.async_scenario:start:361 - Starting "GridSimulator" as "GridSimulator-0" ...
2025-02-21 08:44:59.767 | INFO     | mosaik.async_scenario:start:361 - Starting "GuardSimulator" as "GuardSimulator-0" ...
2025-02-21 08:44:59.768 | INFO     | mosaik.async_scenario:start:361 - Starting "HackerSimulator" as "HackerSimulator-0" ...
2025-02-21 08:44:59.770 | INFO     | mosaik.async_scenario:run:697 - Starting simulation.
  0%|                                                                                                                                                                                                                                           | 0/14 [00:00<?, ?steps/s]
GridSimulator.step(time=0 consumed_power=100 switch1=Switch(power=50, portscan=False, ddos=False, bypassed=False) events=[])
GridSimulator.step(time=1 consumed_power=100.0 switch1=Switch(power=50.0, portscan=False, ddos=False, bypassed=False) events=[])
GridSimulator.step(time=2 consumed_power=100.0 switch1=Switch(power=50.0, portscan=False, ddos=False, bypassed=False) events=[])
GridSimulator.step(time=3 consumed_power=100.0 switch1=Switch(power=50.0, portscan=False, ddos=False, bypassed=False) events=[PortScanEvent(switch=1)])
GridSimulator.step(time=4 consumed_power=100.0 switch1=Switch(power=50.0, portscan=True, ddos=False, bypassed=False) events=[StartByPassEvent(switch=1)])
GridSimulator.step(time=5 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=False, bypassed=True) events=[])
GridSimulator.step(time=6 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=False, bypassed=True) events=[])
GridSimulator.step(time=7 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=False, bypassed=True) events=[StartDDOSEvent(switch=1)])
GridSimulator.step(time=8 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=True, bypassed=True) events=[])
GridSimulator.step(time=9 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=True, bypassed=True) events=[])
GridSimulator.step(time=10 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=True, bypassed=True) events=[])
GridSimulator.step(time=11 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=True, bypassed=True) events=[StopDDOSEvent(switch=1)])
GridSimulator.step(time=12 consumed_power=100.0 switch1=Switch(power=0, portscan=False, ddos=False, bypassed=True) events=[StopByPassEvent(switch=1)])
GridSimulator.step(time=13 consumed_power=100.0 switch1=Switch(power=50.0, portscan=False, ddos=False, bypassed=False) events=[])
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 14/14 [00:00<00:00, 2057.40steps/s]
2025-02-21 08:44:59.778 | INFO     | mosaik.async_scenario:run:753 - Simulation finished successfully.
```

</details>

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

To type check with

```bash
uv run mypy src
```