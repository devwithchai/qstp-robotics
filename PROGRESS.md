# QSTP work tracker

A lightweight snapshot of assignment status in this repository. It distinguishes code that is present from work that has actually been tested; it is not intended as a detailed study log.

**Last updated:** 15 November 2026  
**Repository status:** Project Kratos 2025 Weeks 1–4 source and documentation are in `main`. Week 3 was tested locally in Webots; a clean-clone reproduction check is still pending.

## Project Kratos — Autonomous Subsystem (2024)

| Week | Course-handout topic | What is currently in this repo | Status |
| --- | --- | --- | --- |
| 1 | Set up Ubuntu and ROS | `week-01/odd_even_ros.py` (a ROS 2 publisher/subscriber exercise) | The ROS 2 exercise is corrected and runtime-tested on ROS 2 Humble: publisher/subscriber operation and odd/even classification were verified, and Ctrl+C exits cleanly. See [PR #6](https://github.com/devwithchai/qstp-robotics/pull/6). This script alone does not establish that the broader setup task was completed. |
| 2 | ROS publisher/subscriber and TurtleBot obstacle avoidance | `week-02/week2_assignments/keyboard_control.py` and `turtlebot_controller.py` | Code present; package setup and runtime behavior need checking. |
| 3 | ROS Actionlib and action servers for obstacle handling | `week-03/week3_assignment/path_planner.py` and `pid_controller.py` | A* and PID code present, but these files do not establish that the handout's action-server task was done. |
| 4 | OpenCV with advanced navigation and color-based actions | No implementation on GitHub yet | Not documented |

**Code review notes to revisit:**
- Week 2: the `setup.py` package name and Python package folder do not match; the published tree also lacks some normal ROS package files. Verify `/scan`, `/odom`, and `/cmd_vel` in simulation.
- Week 3: check A* neighbor costs, priority-queue updates, map indexing, and how the robot stops at its final goal.
- Keep the original exercise goals separate from extra experiments. Record actual terminal/simulation results rather than marking code as tested in advance.

A repair proposal for 2024 Weeks 2–3 was submitted in [PR #9](https://github.com/devwithchai/qstp-robotics/pull/9), but the PR was closed without merging. Its proposed changes are not part of `main`, and the original Week 2–3 files remain unchanged. The unit tests added on that branch were not executed; ROS package builds and simulator runtime checks were not completed. Any future repair should start on a new branch.

## Project Kratos — Autonomous Subsystem (2025)

| Week | Course-handout task | Status |
| --- | --- | --- |
| 1 | ROS 2 setup and velocity publishing | Implemented and runtime-tested in Webots; demonstration recorded; merged into `main`. |
| 2 | TurtleBot obstacle avoidance | Implemented and tested in Webots; demonstration recorded; merged into `main`. |
| 3 | Coordinate follower using action servers | Implemented and tested in the local Webots simulation; action interface, server, and client packages are present under `week-03/ros2_ws/src/` in `main`. A clean-clone build/run check is still pending. |
| 4 | Marker detection, self-correcting navigation, and marker-based turns | Implemented and successfully verified in Webots; five-marker navigation sequence and screen-recorded run completed; merged into `main`. |

Week 4 implementation notes: it uses an e-puck instead of the handout's TurtleBot3 Waffle and route-specific turn angles instead of fixed 90-degree turns. See the [Week 4 README](project-kratos-autonomous/2025/week-04/README.md).

## Project Kratos — Autonomous Subsystem (2026)

| Week | Course-handout task | Status |
| --- | --- | --- |
| 0 | Ubuntu 22.04 and ROS 2 setup | Not documented |
| 1 | Keyboard teleoperation in TurtleBot simulation | Not uploaded |
| 2 | Obstacle-aware coordinate follower using Nav2 | Not uploaded |
| 3 | Mission Control GUI for ROS 2 data and node interaction | Not uploaded |
| 4 | Log waypoints, navigate around obstacles, and find an ArUco tag | Not uploaded |
| Bonus | Plan a fast maze-solving route | Not uploaded |

## Introduction to ROS2 (2026)

Only one edition of this program is included, so there is no extra year directory.

| Week | Course-handout topic | Status |
| --- | --- | --- |
| 0 | Ubuntu 22.04, ROS 2 Humble, Gazebo Ignition, Linux basics | Not documented |
| 1 | ROS 2 CLI, custom package, velocity topics, odometry | Not uploaded |
| 2 | Services and actions / server-client nodes | Not uploaded |
| 3 | URDF, sensors, plugins | Not uploaded |
| 4 | Robot camera and OpenCV processing | Not uploaded |

## Next steps

- [ ] Revisit 2024 Week 2 and Week 3 repairs on a new branch; run unit tests, ROS package builds, and simulator checks before marking the work verified.
- [ ] Build and run the 2025 Week 3 workspace from a fresh clone to confirm repository reproducibility.
- [ ] Add the 2026 Project Kratos work as assignments are implemented and tested.
- [ ] Organize and document the 2026 Introduction to ROS2 work as it progresses.

> This is a personal progress snapshot from QSTP participation, not official Project Kratos or BITS Pilani material. Update it when repository contents or verification status changes.
