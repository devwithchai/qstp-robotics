# Project Kratos 2024 — Week 3

This folder contains the ROS 2 Python package for the existing A* grid planner
and odometry-based path-following controller.

## Package

- ROS 2 package: `week3_assignment`
- Python modules: `week3_assignment/`
- Executable: `pid_controller`
- `path_planner.py` is a library module used by the controller, not a
  standalone ROS node.

## Build

Place this folder in a ROS 2 Humble workspace's `src/` directory, source the
Humble installation, then run:

```bash
colcon build --packages-select week3_assignment
source install/setup.bash
```

## Run

Start a simulation that publishes an occupancy grid on `/map` and odometry on
`/odom`, and accepts velocity commands on `/cmd_vel`. Then run:

```bash
ros2 run week3_assignment pid_controller
```

The controller currently uses a configurable world-frame goal at (2.0, 2.0).
It plans through cells marked free (occupancy value 0); occupied and unknown
cells are blocked. The path follower uses distance PID feedback and bounded
heading feedback.

This is a repaired version of the A*/PID code already present in the archive.
It is **not yet an implementation of the 2024 handout's multiple action-server
obstacle detection and handling task**. The handout does not specify the action
interfaces or server behaviour, so that part needs the original weekly
instructions before it can be implemented faithfully.

## Tests

The ROS-independent A* tests are in `test/test_path_planner.py`. Run them
with pytest in an environment with NumPy installed and this package on the
Python path:

```bash
python3 -m pytest test/test_path_planner.py
```

Runtime testing with a real occupancy grid, odometry stream, and simulator
remains necessary.
