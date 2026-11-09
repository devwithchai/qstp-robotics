# Project Kratos 2024 — Week 2

This folder contains the ROS 2 Python package for the keyboard teleoperation and
straight-line obstacle-stop exercises.

## Package

- ROS 2 package: `week2_assignments`
- Python modules: `week2_assignments/`
- Executables:
  - `keyboard_control`
  - `turtlebot_controller`

## Build

Place this folder in a ROS 2 Humble workspace's `src/` directory, source the
Humble installation, then run:

```bash
colcon build --packages-select week2_assignments
source install/setup.bash
```

## Run

Start the TurtleBot simulation first, then use one controller at a time:

```bash
ros2 run week2_assignments keyboard_control
```

Or run the forward obstacle-stop controller:

```bash
ros2 run week2_assignments turtlebot_controller
```

The keyboard controller uses W/S to move, A/D to turn, Space to stop, and Q
to quit. It publishes a zero command when input becomes stale. It requires an
interactive terminal.

The obstacle-stop controller subscribes to `scan` and `odom`, and publishes
to `cmd_vel`. It stops until valid front-sector LiDAR and odometry data are
available, stops when the scan becomes stale, and stops at its configured
travel distance or obstacle threshold. Parameters can be inspected and changed
with standard ROS 2 parameter tools.

**Do not run both controllers at the same time:** both publish velocity
commands to `cmd_vel`, so they would compete for control of the robot.

This controller preserves the original straight-line stop behaviour. It does
not implement a turning or replanning obstacle-avoidance strategy because the
2024 handout does not specify one.

## Tests

The ROS-independent LiDAR helper tests are in `test/test_laser_utils.py`.
Run them in an environment with pytest and the package on the Python path:

```bash
python3 -m pytest test/test_laser_utils.py
```

Runtime testing against the intended TurtleBot simulation is still required.
