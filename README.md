# Autonomous Ground Robot — QSTP Learning Archive

This repository documents my work from multiple **Project Kratos / Quark Summer Technical Project (QSTP)** programs focused on autonomous mobile robotics.

Instead of treating this as one finished robot project, the repository is being organized as a **multi-year learning archive** showing how my work progressed across different QSTP editions.

## Program Status

| Year | Program | Status | Notes |
|---|---|---|---|
| 2024 | Autonomous Ground Robot | Partial archive | Only the assignments I still have are included; the full Week 1–4 set is not available anymore. |
| 2025 | Project Kratos Autonomous QSTP | Planned / in development | I have the complete weekly task set and will rebuild and document the work properly. |
| 2026 | Project Kratos: The Art of Autonomous Navigation | Planned / in development | I have the complete weekly task set and will complete it with a cleaner development workflow and Git history. |

> The 2024 section is kept as an honest archive of my earlier learning work. I do not plan to recreate missing tasks just to make it look complete.

---

## What this repository covers

Across the three programs, the overall learning direction includes:

- Python for robotics
- ROS 2 nodes, topics, publishers and subscribers
- Mobile robot velocity control
- TurtleBot simulation
- Odometry and sensor data
- Obstacle handling
- Occupancy-grid maps
- Path planning
- PID-based motion control
- Autonomous navigation concepts

The 2025 and 2026 work will be added gradually as I complete the original assignments again with better understanding, cleaner code, and proper Git development.

---

## Current Repository Content

At present, the repository mainly contains my **2024 QSTP work**.

### 2024 — Autonomous Ground Robot

This was my introduction to ROS 2 and autonomous mobile robotics.

The available work shows a progression from basic ROS 2 communication to simple robot control and path-planning concepts.

#### Week 1 — ROS 2 Communication

The first task focuses on the ROS 2 publisher-subscriber model.

A publisher generates random integers, while another node receives them and classifies each value as odd or even.

Main concepts:

- ROS 2 nodes
- Publishers and subscribers
- Topics
- Message types
- Python with `rclpy`

```text
week1/odd_even_ros.py
```

#### Week 2 — Mobile Robot Control

This stage introduced TurtleBot motion and basic sensor-based behaviour.

The available work includes:

- keyboard-based velocity control through `/cmd_vel`
- odometry tracking using `/odom`
- obstacle-distance checking using `/scan`
- stopping after reaching a target distance
- stopping when an obstacle is too close

```text
week2/week2_assignments/
├── keyboard_control.py
└── turtlebot_controller.py
```

#### Week 3 — Path Planning and Control

This stage moves toward basic autonomous navigation.

The available work includes:

- A* path planning on an occupancy grid
- world-to-map and map-to-world conversion
- PID-based motion control
- use of `/map`, `/odom`, and `/cmd_vel`

```text
week3/week3_assignment/
├── path_planner.py
└── pid_controller.py
```

### 2024 Limitation

The original 2024 program continued further, but I no longer have the complete assignment set up to Week 4.

Because of that, the 2024 section will remain a **partial archive** rather than being presented as a completed QSTP program.

---

## Planned Repository Structure

As the 2025 and 2026 work is developed, I plan to reorganize the repository into a clearer year-wise structure similar to:

```text
Autonomous-Ground-Robot/
│
├── README.md
│
├── 2024/
│   ├── week1/
│   ├── week2/
│   └── week3/
│
├── 2025/
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   └── week4/
│
└── 2026/
    ├── week1/
    ├── week2/
    ├── week3/
    └── week4/
```

The existing 2024 folders have not been moved yet so that the current repository history stays intact while the new structure is planned carefully.

---

## Development Approach for 2025 and 2026

For the next two programs, I want the repository to show the development process properly rather than only the final assignment files.

The workflow will be:

1. understand the task before coding
2. create a focused development branch
3. implement the task in small steps
4. test the behaviour
5. commit meaningful changes
6. document what was learned and what changed
7. merge completed work into the main branch

This should make the repository useful not only as an assignment archive, but also as a record of my progress in autonomous mobile robotics.

---

## Tech Stack

The current and planned work mainly uses:

- ROS 2
- Python
- `rclpy`
- Gazebo
- TurtleBot
- NumPy
- Git and GitHub

ROS interfaces already used in the 2024 work include:

```text
geometry_msgs/Twist
sensor_msgs/LaserScan
nav_msgs/Odometry
nav_msgs/OccupancyGrid
```

---

## Overall Learning Path

```text
ROS 2 Fundamentals
        ↓
Publisher / Subscriber
        ↓
Mobile Robot Control
        ↓
Odometry + Sensor Data
        ↓
Obstacle Handling
        ↓
Occupancy Grid Mapping
        ↓
Path Planning
        ↓
Motion Control
        ↓
Autonomous Navigation
```

---

## Author

**Chaitanya Belekar**  
Robotics and Automation Engineering  
K.K. Wagh Institute of Engineering Education & Research, Nashik
