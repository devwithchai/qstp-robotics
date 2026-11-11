import math

import numpy as np

from week3_assignment.path_planner import AStarPlanner


def test_astar_returns_path_on_free_grid():
    planner = AStarPlanner(np.zeros((5, 5), dtype=int), 1.0, (0.0, 0.0))
    path = planner.plan((0, 0), (4, 4))
    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)


def test_astar_uses_row_column_order_for_occupancy_grid():
    grid = np.zeros((3, 4), dtype=int)
    grid[1, 2] = 100
    planner = AStarPlanner(grid, 1.0, (0.0, 0.0))
    assert not planner.is_valid((2, 1))
    assert planner.is_valid((1, 2))


def test_astar_treats_unknown_cells_as_blocked():
    grid = np.zeros((3, 3), dtype=int)
    grid[1, 1] = -1
    planner = AStarPlanner(grid, 1.0, (0.0, 0.0))
    assert not planner.is_valid((1, 1))


def test_astar_does_not_cut_diagonal_obstacle_corners():
    grid = np.zeros((2, 2), dtype=int)
    grid[0, 1] = 100
    grid[1, 0] = 100
    planner = AStarPlanner(grid, 1.0, (0.0, 0.0))
    assert planner.plan((0, 0), (1, 1)) is None


def test_world_map_conversion_uses_cell_centers():
    planner = AStarPlanner(np.zeros((3, 3), dtype=int), 0.5, (1.0, 2.0))
    cell = planner.world_to_map((1.1, 2.1))
    assert cell == (0, 0)
    assert planner.map_to_world(cell) == (1.25, 2.25)


def test_world_map_conversion_respects_origin_yaw():
    planner = AStarPlanner(
        np.zeros((3, 3), dtype=int), 1.0, (1.0, 2.0, math.pi / 2.0)
    )
    assert planner.world_to_map((0.5, 2.5)) == (0, 0)
