# Week 3 — Coordinate Follower

## Assignment objective

The 2025 handout states:

> You will learn about action servers and implement it in building a coordinate follower for the turtlebot.

## Implementation plan

Create an action-based coordinate follower that accepts a sequence of target coordinates and drives the TurtleBot toward them using odometry feedback.

Planned components:

1. A ROS 2 action definition for a coordinate goal, including target (x) and (y) coordinates.
2. An action server that accepts a goal, tracks execution, reports feedback, and returns a result.
3. A controller that subscribes to `/odom` and estimates the robot's current planar pose.
4. A velocity controller that publishes to `/cmd_vel), first aligning the robot with the target and then driving toward it.
5. A configurable position tolerance and safe stop when a goal is reached or cancelled.
6. A coordinate list stored in a text file and a client that submits the goals in sequence.

The action interface, odometry-based controller, coordinate file, and goal sequencing are implementation choices to realise the handout's coordinate-follower objective.

## Simulator choice

The Week 3 handout asks for Gazebo visualization. This repository uses Webots for all four weeks to keep the practical environment consistent with the available ROS 2 Humble setup. Webots is a deliberate substitution; it is not what the handout specifies.

## Verification checklist

- [ ] Define and build the action interface.
- [ ] Start the action server and send one coordinate goal.
- [ ] Verify feedback and successful result reporting.
- [ ] Verify that the robot reaches a goal within tolerance.
- [ ] Test multiple coordinates from the text file.
- [ ] Test cancellation and safe stopping.
- [ ] Record the Webots substitution and any differences from the Gazebo-based handout.

## Status

Not implemented yet. The coordinate follower must be tested in simulation before it is marked complete.
