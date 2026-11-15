# Week 4 – ArUco Tag Navigation

**Project Kratos – Autonomous Subsystem**

[QSTP Assignment 4 – ArUco Tag Navigation](https://drive.google.com/file/d/13qbvr3P7O4u1aHY4MxyT1vLNsylzPLqn/view?usp=sharing)

## Objective

The objective of this assignment is to use a robot-mounted camera and OpenCV to detect ArUco markers and navigate based on their IDs.

According to the assignment:
- ArUco ID `0` commands a 90° right turn.
- ArUco ID `1` commands a 90° left turn.
- The robot moves forward after completing each turn until it detects the next marker.
- The process repeats for five marker encounters, after which the robot stops.

This implementation uses ROS 2, OpenCV ArUco detection, camera-based marker pose estimation, and odometry feedback to complete a five-marker navigation sequence.

## Topics Covered

- Subscribing to camera data using `sensor_msgs/Image`
- Converting ROS 2 image messages to OpenCV images using `cv_bridge`
- Detecting ArUco markers using OpenCV
- Working with the `DICT_ARUCO_ORIGINAL` dictionary
- Estimating marker position using camera calibration
- Transforming camera measurements into the robot's base frame
- Controlling robot motion using visual input and odometry
- Implementing a state-based navigation controller

## Implementation Environment

| Component | Configuration |
|---|---|
| Operating System | Ubuntu 22.04 |
| ROS 2 | Humble |
| Simulator | Webots R2025a |
| Robot Model | e-puck |
| Programming Language | Python |
| Computer Vision | OpenCV ArUco |
| ROS Image Conversion | cv_bridge |
| Navigation Feedback | Wheel odometry |

**Robot model note:** The assignment specifies a TurtleBot3 Waffle. This implementation uses the e-puck model available through `webots_ros2_epuck` as a functional substitute in Webots.

## Assignment Tasks

The implementation addresses the following tasks:

1. Create a ROS 2 Python package named `aruco_navigator`.
2. Subscribe to the robot camera topic and convert incoming image messages using `cv_bridge`.
3. Detect marker IDs 0 and 1 using the `DICT_ARUCO_ORIGINAL` dictionary.
4. Interpret detected marker IDs and execute the corresponding navigation behaviour.
5. Repeat the process for five marker encounters and stop the robot after the fifth.

## Workspace Structure

```text
week-04/
├── README.md
├── worlds/
│   ├── aruco_epuck_world.wbt
│   └── textures/
│       ├── aruco_0.png
│       └── aruco_1.png
│
└── ros2_ws/
    └── src/
        └── aruco_navigator/
            ├── aruco_navigator/
            │   ├── __init__.py
            │   ├── aruco_detector.py
            │   └── navigation_controller.py
            │
            ├── launch/
            │   └── aruco_epuck_launch.launch.py
            │
            ├── resource/
            │   └── aruco_navigator
            ├── package.xml
            ├── setup.cfg
            └── setup.py
```


## Implementation

### 1. ArUco Marker Detection

The `aruco_detector` node subscribes to the e-puck camera:

- `/camera/image_color`
- `/camera/camera_info`

Camera images are converted into OpenCV format using `cv_bridge`. The detector uses OpenCV's `DICT_ARUCO_ORIGINAL` dictionary to identify markers.

A marker must be detected consistently across multiple frames before its ID is published. This helps avoid reacting to occasional false detections.

The node also uses camera calibration information to estimate the marker's position relative to the camera. This position is transformed into the robot's `base_link` frame.

Published topics:

- `/aruco/detected_id`
- `/aruco/marker_position`

### 2. Navigation Controller

The `navigation_controller` node processes marker detections and odometry feedback.

It uses a state-based approach with the following states:

- `WAITING_FOR_ODOM`
- `MOVING_FORWARD`
- `APPROACHING_MARKER`
- `ROTATING`
- `MISSION_COMPLETE`
- `ERROR`

When a valid marker is detected, the controller:

1. Stops forward motion.
2. Approaches the marker until the configured 0.22 m standoff distance is reached.
3. Calculates the target heading using the current odometry orientation.
4. Rotates in the required direction.
5. Resumes forward movement to search for the next marker.

The controller uses odometry yaw to determine when a turn is complete instead of relying on a fixed rotation duration. It also checks sensor-data freshness and stops the robot if required data becomes stale.

### 3. Marker Sequence

The custom Webots world contains five marker panels arranged to present one marker at a time along the intended route.

| Encounter | Marker ID | Direction | Target Turn |
|---|---:|---|---:|
| 1 | 0 | Right | 56.0° |
| 2 | 1 | Left | 107.6° |
| 3 | 0 | Right | 73.6° |
| 4 | 1 | Left | 154.4° |
| 5 | 0 | Stop | No turn |

The expected marker sequence is:

`[0, 1, 0, 1, 0]`

The controller rejects unexpected marker IDs and enters an error state rather than continuing with an invalid sequence. After accepting the fifth marker, it transitions to `MISSION_COMPLETE` and stops the robot.

### 4. ROS 2 Communication

| Node | Subscriptions | Publications |
|---|---|---|
| `aruco_detector` | `/camera/image_color`, `/camera/camera_info`, `/aruco/detection_enabled` | `/aruco/detected_id`, `/aruco/marker_position` |
| `navigation_controller` | `/aruco/detected_id`, `/aruco/marker_position`, `/odom` | `/cmd_vel`, `/aruco/detection_enabled` |

## Build and Run

### 1. Build the package

Open a terminal:

```bash
cd ~/Desktop/qstp-robotics/project-kratos-autonomous/2025/week-04/ros2_ws

source /opt/ros/humble/setup.zsh

colcon build --symlink-install --packages-select aruco_navigator

source install/setup.zsh
```

### 2. Start the Webots simulation

Open a separate terminal:

```bash
cd ~/Desktop/qstp-robotics/project-kratos-autonomous/2025/week-04/ros2_ws

source /opt/ros/humble/setup.zsh
source install/setup.zsh

export WEBOTS_HOME=/usr/local/webots

ros2 launch aruco_navigator aruco_epuck_launch.launch.py
```

Wait for Webots to start and the e-puck robot to become available.

### 3. Start the ArUco detector

Open another terminal:

```bash
cd ~/Desktop/qstp-robotics/project-kratos-autonomous/2025/week-04/ros2_ws

source /opt/ros/humble/setup.zsh
source install/setup.zsh

ros2 run aruco_navigator aruco_detector
```

### 4. Start the navigation controller

Open a third terminal:

```bash
cd ~/Desktop/qstp-robotics/project-kratos-autonomous/2025/week-04/ros2_ws

source /opt/ros/humble/setup.zsh
source install/setup.zsh

ros2 run aruco_navigator navigation_controller --ros-args -p use_sim_time:=true
```

The navigation controller uses the Webots simulation clock for rotation timeout calculations. Start Webots before starting the controller.

## Verification Checklist

- [x] ROS 2 package builds successfully.
- [x] Camera images are received and processed.
- [x] ArUco IDs 0 and 1 are detected.
- [x] Marker position is estimated using camera calibration.
- [x] Marker position is transformed into `base_link`.
- [x] Robot approaches detected markers before rotating.
- [x] Turn completion is determined using odometry.
- [x] Unexpected marker IDs trigger a safe stop.
- [x] Five-marker sequence completes successfully.
- [x] Robot stops after the fifth marker.
- [x] Full simulation successfully completed while screen recording was active.

## Demonstration Video

[Watch the Week 4 ArUco Navigation Demonstration](https://drive.google.com/file/d/1pD5qzE9ZSSELwP4hbwALXR4jTJbOIbEO/view?usp=sharing)

## Implementation Notes and Limitations

- **Robot model:** The assignment specifies TurtleBot3 Waffle, whereas this implementation uses the e-puck model in Webots.
- **Turn angles:** The assignment specifies fixed 90° turns. The custom marker layout uses route-specific turn angles of 56.0°, 107.6°, 73.6°, and 154.4° to align the robot with the next marker. This is a modification of the original fixed-turn requirement.
- **Marker pose estimation:** The detector uses the 62.5 mm coded marker size for pose estimation, rather than the full 75 mm panel size.
- **Navigation approach:** The implementation uses camera-based marker detection and wheel odometry. It does not use SLAM, map-based localization, or Nav2.
- **Simulation:** The marker panels are visual elements in the Webots world and are used for camera-based detection.

## Implementation Status

**Status:** Completed and successfully verified in Webots.

The five-marker navigation sequence was tested successfully, including a full run with screen recording enabled. The implementation and demonstration are ready for repository documentation and GitHub synchronization.