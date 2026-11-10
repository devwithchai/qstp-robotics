# Week 1 — Setting up ROS 2

## Assignment objective

The 2025 handout states:

> You will learn to set up Ubuntu and ROS2, as well as publish a velocity to a node.

## Learning and implementation tasks

1. Use the Ubuntu 22.04 and ROS 2 Humble environment.
2. Become familiar with the ROS 2 command-line interface and inspect the active ROS graph.
3. Run the TurtleBot simulation and identify the velocity command and odometry topics.
4. Publish a `geometry_msgs/msg/Twist` command to the robot velocity topic.
5. Create a small ROS 2 package and a node that publishes velocity commands.
6. Implement a circular-motion demonstration by publishing a constant forward velocity and a non-zero angular velocity.
7. Inspect odometry to observe the robot's position and orientation while it moves.

The command-line publishing and circular-motion exercise are implementation steps used to demonstrate the handout's velocity-publishing objective; the handout itself does not prescribe a specific topic name, velocity, or circular trajectory.

## Current environment and observed checks

- OS: Ubuntu 22.04
- ROS 2: Humble
- Simulator: Webots with `webots_ros2_turtlebot`
- Velocity topic observed: `/cmd_vel`
- Odometry topic observed: `/odom`
- Laser scan topic observed: `/scan`
- A velocity command was published to `/cmd_vel`.
- The TurtleBot was observed moving in Webots.
- An odometry sample reported (x = 0.6559\,m), (y = 0.0\,m), with near-zero velocity at the time of capture.

This verifies basic simulated movement and odometry publication. The custom circular-motion node and its runtime verification are still to be added.

## Verification checklist

- [x] Webots TurtleBot launches.
- [x] ROS 2 topics are visible.
- [x] `/scan` publishes continuously.
- [x] Velocity command causes visible robot movement.
- [x] Odometry reports robot pose.
- [ ] Create the `turtle_controller` ROS 2 Python package.
- [ ] Run and verify the circular-motion node.
- [ ] Record the final run command and evidence.

## Notes

Do not treat the initial manual `ros2 topic pub` check as completion of the custom-node exercise. Update this file after the package and circular-motion node have been implemented and tested.
