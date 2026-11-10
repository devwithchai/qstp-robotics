# Project Kratos — Autonomous Subsystem QSTP (2025)

This directory contains my learning and implementation work for the 2025 edition of the Project Kratos Autonomous Subsystem QSTP.

## Course outline

The 2025 handout lists four weekly assignments:

| Week | Topic | Core outcome |
|---|---|---|
| 1 | Setting up ROS 2 | Set up Ubuntu and ROS 2, and publish a velocity command to a node |
| 2 | Obstacle Avoidance | Implement basic obstacle avoidance behaviour on TurtleBot |
| 3 | Coordinate Follower | Learn action servers and build a coordinate follower for TurtleBot |
| 4 | Autonomous Navigation | Detect markers using computer vision and build a self-correcting marker-following and turning algorithm |

These topics are specific to the 2025 handout. They should not be confused with the 2024 or 2026 Kratos assignments or the separate Introduction to ROS 2 course.

## Simulator note

The practical work in this directory is being developed with **Webots** and `webots_ros2_turtlebot` on ROS 2 Humble. The Week 3 handout specifies Gazebo for visualization; using Webots there is a deliberate simulator substitution, not a requirement stated by the handout. Any resulting differences or limitations will be documented.

## Folder structure

- `week-01/` — ROS 2 setup and velocity publishing
- `week-02/` — TurtleBot obstacle avoidance
- `week-03/` — Action-based coordinate follower
- `week-04/` — Marker detection and self-correcting navigation

## Status policy

A task is marked **tested** only after its runtime behaviour has been observed. Code presence alone is not proof of completion. Each week will record implementation, run instructions, verification evidence, and known limitations.

> Personal learning work based on the 2025 QSTP handout. This is not an official Project Kratos or BITS Pilani repository.
