from mosaik import World
from mosaik.util import (
    plot_execution_graph,
    plot_execution_time,
    plot_execution_time_per_simulator,
)


def main() -> None:
    debug = True
    world = World(
        {
            "GridSimulator": {
                "python": "rescue_mosaik.simulators.Grid:GridSimulator",
            },
            "HackerSimulator": {
                "python": "rescue_mosaik.simulators.Hacker:HackerSimulator",
            },
            "GuardSimulator": {
                "python": "rescue_mosaik.simulators.Guard:GuardSimulator",
            },
        },
        debug=debug,
    )

    with world.group():
        grid_sim = world.start("GridSimulator", same_time_loop=True)
        guard_sim = world.start("GuardSimulator", same_time_loop=True)
        hacker_sim = world.start("HackerSimulator", same_time_loop=True)

    grid = grid_sim.Grid()
    guard = guard_sim.Guard()
    hacker = hacker_sim.Hacker()

    world.connect(grid, guard, "grid_state", "grid_state")
    world.connect_one
    world.connect(guard, grid, "events", "events", time_shifted=True)
    world.connect(hacker, grid, "events", "events", time_shifted=True)

    world.run(until=10)

    if debug:
        plot_execution_graph(world, folder=".")
        plot_execution_time(world, folder=".")
        plot_execution_time_per_simulator(world, folder=".")
