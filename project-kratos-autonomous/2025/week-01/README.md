# Week 1 — ROS 2 Basics

**Source:** [QSTP Assignment 1: ROS 2 Basics](https://drive.google.com/file/d/1GpiqTVfowTs_FQP9pMMJehuY8GAYUWUG/view?usp=drive_link)

## Objective

Get familiar with ROS 2 by interacting with topics, creating a simple ROS 2 package, and publishing velocity commands to control a simulated TurtleBot.

## Topics covered

- ROS 2 topic communication
- ROS 2 package creation
- Publishing velocity commands to a TurtleBot

## Setup requirements from the handout

1. Ubuntu 22.04 LTS
2. ROS 2 Humble Hawksbill
3. TurtleBot3 packages

## Assignment tasks

### 1. Set up a ROS 2 workspace

- Create a ROS 2 workspace (the handout gives `ros2_ws` as an example).
- Source the ROS 2 setup file in `.bashrc`.

### 2. Create a ROS 2 package

- Package name: `turtle_controller`.
- Write a Python script in the `turtle_controller` node that publishes velocity commands.

### 3. Launch TurtleBot and publish velocities

- Run TurtleBot.
- Use the custom node to publish velocity commands to TurtleBot.
- Try linear and angular velocity commands to make TurtleBot move in a circle.

### 4. Monitor topics

Use the ROS 2 CLI tools:

- `ros2 topic list`
- `ros2 topic echo`
- `ros2 topic pub`

The purpose is to understand ROS 2 topic communication.

## Submission requirements

- Submit a short video showing TurtleBot moving, with a terminal visible showing what is being published on the `cmd_vel` topic.
- Demonstrate velocity publishing using **both** the custom script and terminal commands.
- Original deadline in the handout: **26 July 2025**.

## References in the handout

- [ROS 2 Humble documentation](https://docs.ros.org/en/humble/index.html)
- [ROS 2 Humble tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 tutorial video](https://www.youtube.com/watch?v=Gg25GfA456o)
- [TurtleBot3 simulation guide](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/)

## Our implementation environment and progress

The current implementation environment is Ubuntu 22.04, ROS 2 Humble, and Webots using `webots_ros2_turtlebot`. Webots is our chosen simulator; the Week 1 handout itself does not prescribe a simulator.

Verified so far:

- [x] Webots TurtleBot launches.
- [x] ROS 2 topics are visible.
- [x] `/scan` publishes continuously.
- [x] A velocity command published to `/cmd_vel` visibly moved the TurtleBot.
- [x] `/odom` reports the robot pose; one observed sample showed (x = 0.6559\,m), (y = 0.0\\,m), after the movement test.
- [x] Create and run the custom `turtle_controller` Python package/node.
- [x] Verify circular motion using the custom node.
- [x] Capture the required video showing both script-based and terminal-based velocity publishing.

## Demonstration video

[Watch the Week 1 ROS 2 velocity-control demonstration](https://drive.google.com/file/d/1PKEezS342-OfKXQR2kHGu1EnCZKZumIf/view?usp=sharing)

> Google Drive may ask viewers to sign in. If access is restricted, the file owner must grant viewing permission to their Google account.

**Status:** Week 1 implementation and testing are complete. The custom controller node successfully publishes velocity commands, the TurtleBot moves in a circle in Webots, and the required demonstration video has been recorded.
