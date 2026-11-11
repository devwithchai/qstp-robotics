# Week 2 — Obstacle Avoidance using LaserScan

**Source:** [QSTP Assignment 2: Obstacle Avoidance using LaserScan](assignment.pdf)

## Objective

Use TurtleBot3 LaserScan data to implement basic obstacle avoidance. The robot should move in a straight line until it detects an obstacle in front. When an obstacle is detected, it should rotate right until the path is clear, then continue moving forward.

## Topics covered

- Subscribing to sensor data (`LaserScan`)
- Writing ROS 2 subscribers and publishers
- Obstacle-avoidance logic
- Publishing velocity commands based on sensor input

## Assignment tasks

### 1. Create a ROS 2 package

- Package name: `obstacle_avoider`.

### 2. Subscribe to LaserScan data

- Subscribe to `/scan`.
- Use the LaserScan data to monitor the area in front of the robot.

### 3. Implement the obstacle-avoidance logic

- If the minimum front distance is greater than a threshold (the handout gives **0.5 metres** as an example), move forward.
- If an obstacle is detected, stop and turn right.
- Publish velocity commands on `/cmd_vel`.

The objective section describes the expected behaviour as turning right until the path is clear, then continuing forward.

## Submission requirements

- Submit a short video to Google Classroom showing TurtleBot moving straight, reaching an obstacle, and turning right.
- The video must also show a terminal displaying what is being published on the `cmd_vel` topic.
- Original deadline in the handout: **2 August 2025**.

## Demonstration video

[Watch the Week 2 obstacle-avoidance demonstration](https://drive.google.com/file/d/1UVp_tx9D8MLQvGscKsgjaxQzSTiSzj58/view?usp=sharing)

## References in the handout

- [ROS 2 LaserScan message](https://docs.ros2.org/latest/api/sensor_msgs/msg/LaserScan.html)
- [ROS 2 Humble publisher/subscriber tutorial](https://docs.ros.org/en/humble/Tutorials/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [TurtleBot3 simulation guide](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/)

## Our implementation environment and progress

The implementation uses Ubuntu 22.04, ROS 2 Humble, and Webots with `webots_ros2_turtlebot`. The handout refers to TurtleBot3 but does not mandate Webots; Webots is our simulator choice.

Verified:

- [x] Webots TurtleBot launches.
- [x] `/scan` is available and publishes continuously (observed at approximately 4.45 Hz).
- [x] `/cmd_vel` and `/odom` are available.
- [x] Create the `obstacle_avoider` ROS 2 package/node.
- [x] Implement front-sector distance checking and the 0.5 m obstacle threshold.
- [x] Verify forward motion with a clear path.
- [x] Verify stop-and-turn-right behaviour until the path is clear.
- [x] Verify that forward motion resumes after the obstacle is cleared.
- [x] Capture the demonstration video.

The controller uses hysteresis: it starts turning when the minimum front distance is **0.5 m or less** and resumes forward motion once the distance reaches **0.65 m**. This helps prevent rapid switching when readings fluctuate near the obstacle threshold.

**Status:** Week 2 implementation, simulation testing, and demonstration video are complete.
