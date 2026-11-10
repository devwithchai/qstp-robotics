# turtle_controller

A small beginner-friendly ROS 2 Python package for Week 1.

## What it does

The `move_in_circle` node publishes `geometry_msgs/msg/Twist` messages to `/cmd_vel` at 10 Hz.

- `linear.x = 0.08`: moves the robot forward.
- `angular.z = 0.5`: turns the robot while it moves.

Because both values are non-zero, the TurtleBot follows a circular/curved path. Press **Ctrl+C** in the node terminal to stop it.

## Build

From this workspace directory:

```bash
cd ~/Desktop/qstp-robotics/project-kratos-autonomous/2025/week-01/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select turtle_controller
source install/setup.bash
```

## Run

Start the Webots TurtleBot simulation first. In another terminal:

```bash
source /opt/ros/humble/setup.bash
cd ~/Desktop/qstp-robotics/project-kratos-autonomous/2025/week-01/ros2_ws
source install/setup.bash
ros2 run turtle_controller move_in_circle
```

## Observe the commands

In a third terminal:

```bash
ros2 topic echo /cmd_vel
```

To stop the robot, press **Ctrl+C** in the controller terminal. The node also publishes a zero-velocity command during shutdown.
