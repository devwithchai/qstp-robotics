# QSTP work tracker

This is a working checklist for my robotics QSTP exercises. It tracks **files that exist**, **work that has been tested**, and **tasks still to attempt** separately. A file being present does not mean the assignment was completed or accepted.

The course outlines below come from the handouts for each edition. The file/status observations were reviewed on 9 November 2026.

## Project Kratos — Autonomous Subsystem (2024)

| Week | Course-handout topic | What is currently in this repo | Status |
| --- | --- | --- | --- |
| 1 | Set up Ubuntu and ROS | `week-01/odd_even_ros.py` (a ROS 2 publisher/subscriber exercise) | The ROS 2 exercise is corrected and runtime-tested on ROS 2 Humble: publisher/subscriber operation and odd/even classification were verified, and Ctrl+C exits cleanly. See [PR #6](https://github.com/devwithchai/qstp-robotics/pull/6). This script alone does not establish that the broader setup task was completed. |
| 2 | ROS publisher/subscriber and TurtleBot obstacle avoidance | `week-02/week2_assignments/` | Package metadata and entry points repaired; keyboard input is non-blocking with command timeout; obstacle controller filters the forward LiDAR sector and stops on missing/stale sensor data. LiDAR helper tests added; build and simulator runtime still need verification. |
| 3 | ROS Actionlib and action servers for obstacle handling | `week-03/week3_assignment/` | Package metadata repaired; A* grid indexing, diagonal costs, corner checks and map transforms corrected; PID path follower revised with bounded commands and goal stopping. A* tests added; build and simulator runtime still need verification. The handout's multiple action-server task remains unimplemented pending detailed requirements. |
| 4 | OpenCV with advanced navigation and color-based actions | No implementation on GitHub yet | Not documented |

**Code review notes to revisit:**
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

- [ ] Build and runtime-test the repaired 2024 Week 2 package in the intended TurtleBot simulation.
- [ ] Build and runtime-test the repaired 2024 Week 3 package with a known occupancy grid and odometry source.
- [ ] Obtain detailed 2024 Week 3 action-server instructions before implementing the remaining handout requirement.
- [ ] Gather the detailed weekly assignment instructions where the short handouts are insufficient.
- [ ] Begin the distinct 2025 and 2026 tasks, adding their work only after it exists.

> These are my personal learning notes from QSTP participation, not official Project Kratos or BITS Pilani material.
