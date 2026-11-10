# Week 2 — Obstacle Avoidance

## Assignment objective

The 2025 handout states:

> You will learn to implement basic obstacle avoidance behaviour on turtlebot.

## Implementation plan

Build a ROS 2 node for the simulated TurtleBot that uses its laser scan data to make a basic obstacle-avoidance decision.

A minimal behaviour to implement and test:

1. Subscribe to the TurtleBot `/scan` topic (`sensor_msgs/msg/LaserScan`).
2. Read valid range measurements in the robot's forward field of view.
3. Move forward while the path ahead is clear.
4. When an obstacle is closer than a configurable safety threshold, stop forward motion and turn right.
5. Resume forward motion when the forward path is clear.
6. Publish velocity commands to `/cmd_vel` using `geometry_msgs/msg/Twist`.

The scan topic, message type, threshold-based rule, and right-turn response are the concrete implementation plan for this repository. They are not additional quoted requirements from the short 2025 handout.

## Suggested package contents

- ROS 2 Python package and obstacle-avoidance node
- Configurable minimum obstacle distance and forward scan sector
- Launch/run instructions
- Test notes describing obstacle placement and observed robot response

## Verification checklist

- [ ] Confirm `/scan` message rate and frame.
- [ ] Validate handling of `inf`, `nan`, and out-of-range scan values.
- [ ] Verify forward motion when the path is clear.
- [ ] Verify stopping and right-turn response when an obstacle is detected.
- [ ] Verify that the robot does not continue publishing stale motion commands after shutdown.
- [ ] Record simulation evidence and known limitations.

## Status

Not implemented yet. Do not mark this assignment complete until the behaviour is observed in Webots.
