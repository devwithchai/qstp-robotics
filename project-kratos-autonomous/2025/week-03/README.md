# Week 3 — Coordinate Follower using ROS 2 Actions

**Original assignment:** [QSTP Week 3 — Coordinate Follower (PDF)](https://drive.google.com/file/d/17LVHYQbUmyKpPwT65-eSkKDjtY6AKVYK/view?usp=sharing)

## Objective

Implement a coordinate follower for TurtleBot using a custom ROS 2 action interface. The robot receives target coordinates, moves towards each target, and reports its current position and remaining distance through action feedback.

## Topics covered

- Defining custom ROS 2 action interfaces
- Implementing ROS 2 action servers and clients
- Reading robot pose from odometry
- Transforming coordinates between the `map` and `odom` frames using TF2
- Publishing velocity commands to control a differential-drive robot
- Executing multiple coordinate goals sequentially

## Implementation environment

- Ubuntu 22.04
- ROS 2 Humble
- Webots with `webots_ros2_turtlebot`

The handout mentions Gazebo. This implementation uses **Webots** as the simulator.

## Assignment tasks

1. Create a ROS 2 package for the coordinate follower.
2. Define a custom action whose goal contains target `x` and `y` coordinates in metres.
3. Implement an action server that subscribes to `/odom` and publishes velocity commands to `/cmd_vel`.
4. Send continuous feedback containing the robot's current position and distance remaining to the target.
5. Return a successful result when the robot reaches the target within the configured tolerance.
6. Implement an action client that reads coordinates from a text file, sends goals one at a time, and waits for each result before sending the next goal.

## Workspace structure

```text
ros2_ws/
└── src/
    ├── coordinate_follower_interfaces/
    │   └── action/
    │       └── Coordinate.action
    └── coordinate_follower/
        ├── coordinate_follower/
        │   ├── coordinate_action_server.py
        │   └── coordinate_sequence_client.py
        └── config/
            └── coordinates.txt
```

### Custom action interface

The `Coordinate.action` interface contains:

- **Goal:** target `x` and `y` coordinates (metres, expressed in the `map` frame).
- **Result:** success flag and a status message.
- **Feedback:** current `x` and `y` position in the `map` frame, plus distance remaining to the target.

### Coordinate sequence

The client reads absolute target coordinates from `coordinate_follower/config/coordinates.txt`. The tested sequence was:

```text
0.30 0.00
0.60 0.00
```

The second coordinate is an absolute target in the `map` frame, not a relative displacement.

## Build and run

From the workspace directory:

```zsh
source /opt/ros/humble/setup.zsh
colcon build --packages-up-to coordinate_follower
source install/setup.zsh
```

Keep the Webots simulation running while testing. Start the following processes in separate terminals.

**Terminal 1 — Webots simulation**

```zsh
source /opt/ros/humble/setup.zsh
ros2 launch webots_ros2_turtlebot robot_launch.py
```

**Terminal 2 — Static `map → odom` transform**

```zsh
source /opt/ros/humble/setup.zsh
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
```

**Terminal 3 — Coordinate action server**

```zsh
source /opt/ros/humble/setup.zsh
source project-kratos-autonomous/2025/week-03/ros2_ws/install/setup.zsh
ros2 run coordinate_follower coordinate_action_server
```

**Terminal 4 — Sequential action client**

```zsh
source /opt/ros/humble/setup.zsh
source project-kratos-autonomous/2025/week-03/ros2_ws/install/setup.zsh
ros2 run coordinate_follower coordinate_sequence_client
```

## Verification checklist

- [x] Created the `coordinate_follower` Python package.
- [x] Created the `coordinate_follower_interfaces` package and custom `Coordinate.action`.
- [x] Built the custom action interface and verified it with `ros2 interface show`.
- [x] Implemented the action server with `/odom` subscription and `/cmd_vel` publishing.
- [x] Added TF2 transformations between the `map` and `odom` frames.
- [x] Implemented continuous action feedback with current position and distance remaining.
- [x] Implemented successful goal completion, cancellation handling, and robot stop commands.
- [x] Implemented a client that loads coordinate pairs from `coordinates.txt`.
- [x] Verified that the client waits for each action result before sending the next goal.
- [x] Tested two consecutive coordinate goals in the Webots TurtleBot simulation.
- [x] Verified that the robot stops after completing the sequence.
- [x] Recorded the demonstration video.

## Demonstration video

[Watch the Week 3 Coordinate Follower demonstration](https://drive.google.com/file/d/1V3TiowfxfRAGMz3e9aI_BBz0Iy27IpYD/view?usp=sharing)

## Implementation notes and limitations

- No SLAM or localization system is running in this simulation. An identity static transform from `map` to `odom` is used to make the assignment's map-frame goals available in the Webots test. A real robot would obtain this transform from its localization system.
- The controller does not implement obstacle avoidance. Run the demonstration only in a clear, controlled path.
- The configured goal tolerance is **0.10 m**, so the robot stops when it is within that distance of the target rather than needing to land exactly on the requested coordinate.

**Status:** Week 3 implementation, sequential-goal testing, and demonstration recording are complete.
