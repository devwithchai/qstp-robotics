# QSTP work tracker

This is a working checklist for my robotics QSTP exercises. It tracks **files that exist**, **work that has been tested**, and **tasks still to attempt** separately. A file being present does not mean the assignment was completed or accepted.

The course outlines below come from the handouts for each edition. The file/status observations are based on the repository as of 26 October 2026.

## Project Kratos — Autonomous Subsystem (2024)

| Week | Course-handout topic | What is currently in this repo | Status |
| --- | --- | --- | --- |
| 1 | Set up Ubuntu and ROS | `week-01/odd_even_ros.py` (a ROS 2 publisher/subscriber exercise) | Code present; needs correction/testing. This file alone does not establish the setup task was completed. |
| 2 | ROS publisher/subscriber and TurtleBot obstacle avoidance | `week-02/week2_assignments/keyboard_control.py` and `turtlebot_controller.py` | Code present; package setup and runtime behavior need checking. |
| 3 | ROS Actionlib and action servers for obstacle handling | `week-03/week3_assignment/path_planner.py` and `pid_controller.py` | A* and PID code present, but these files do not establish that the handout's action-server task was done. |
| 4 | OpenCV with advanced navigation and color-based actions | No implementation on GitHub yet | Not documented |

**Code review notes to revisit:**
- Week 1: the two nodes are spun sequentially, so the classifier is never reached during normal operation.
- Week 2: the `setup.py` package name and Python package folder do not match; the published tree also lacks some normal ROS package files. Verify `/scan`, `/odom`, and `/cmd_vel` in simulation.
- Week 3: check A* neighbor costs, priority-queue updates, map indexing, and how the robot stops at its final goal.
- Keep the original exercise goals separate from extra experiments. Record actual terminal/simulation results rather than marking code as tested in advance.

## Project Kratos — Autonomous Subsystem (2025)

| Week | Course-handout task | Status |
| --- | --- | --- |
| 1 | ROS 2 setup and velocity publishing | Not uploaded |
| 2 | TurtleBot obstacle avoidance | Not uploaded |
| 3 | Coordinate follower using action servers | Not uploaded |
| 4 | Marker detection, self-correcting navigation, and marker-based turns | Not uploaded |

Some fundamentals overlap with 2024. Reuse what was learned, but keep the 2025 submission focused on its own assignment and demonstrate the differences.

## Project Kratos — Autonomous Subsystem (2026)

| Week | Course-handout task | Status |
| --- | --- | --- |
| 0 | Ubuntu 22.04 and ROS 2 setup | Not documented |
| 1 | Keyboard teleoperation in TurtleBot simulation | Not uploaded |
| 2 | Obstacle-aware coordinate follower using Nav2 | Not uploaded |
| 3 | Mission Control GUI for ROS 2 data and node interaction | Not uploaded |
| 4 | Log waypoints, navigate around obstacles, and find an ArUco tag | Not uploaded |
| Bonus | Plan a fast maze-solving route | Not uploaded |

The Mission Control GUI, Nav2-based follower, waypoint mission, and maze solver are distinct tasks worth documenting individually.

## Introduction to ROS2 (2026)

Only one edition of this program is included, so there is no extra year directory.

| Week | Course-handout topic | Status |
| --- | --- | --- |
| 0 | Ubuntu 22.04, ROS 2 Humble, Gazebo Ignition, Linux basics | Not documented |
| 1 | ROS 2 CLI, custom package, velocity topics, odometry | Not uploaded |
| 2 | Services and actions / server-client nodes | Not uploaded |
| 3 | URDF, sensors, plugins | Not uploaded |
| 4 | Robot camera and OpenCV processing | Not uploaded |

## How I want to work through it

1. **Preserve earlier submissions.** Fix clear problems in small commits, without presenting old code as freshly completed coursework.
2. **Test before checking off.** For each task, record how to run it, what I observed, and what still fails. Screenshots or short recordings are useful where they actually demonstrate behavior.
3. **Avoid repeating identical exercises.** Refer back to earlier fundamentals where appropriate, while implementing the new requirement for each edition.
4. **Document honestly.** Separate *implemented*, *tested*, *partially working*, and *not attempted*. Do not imply certification or official affiliation.

### Immediate next steps

- [ ] Repair and test the 2024 Week 1 publisher/subscriber example.
- [ ] Restore/verify the ROS package layout for 2024 Week 2; test teleoperation and obstacle stopping.
- [ ] Review 2024 Week 3 A* and PID code against the actual assignment brief, then test it.
- [ ] Gather the detailed weekly assignment instructions where the short handouts are insufficient.
- [ ] Begin the distinct 2025 and 2026 tasks, adding their work only after it exists.

> These are my personal learning notes from QSTP participation, not official Project Kratos or BITS Pilani material.
