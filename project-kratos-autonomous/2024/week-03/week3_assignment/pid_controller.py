import math

import numpy as np
import rclpy
from geometry_msgs.msg import Pose, Twist
from nav_msgs.msg import OccupancyGrid, Odometry
from rclpy.node import Node

from .path_planner import AStarPlanner


def normalize_angle(angle):
    """Wrap an angle to [-pi, pi]."""
    return math.atan2(math.sin(angle), math.cos(angle))


class PIDController(Node):
    """Follow an A* grid path using distance PID and heading feedback."""

    def __init__(self):
        super().__init__('pid_controller')
        self.declare_parameter('goal_x', 2.0)
        self.declare_parameter('goal_y', 2.0)
        self.declare_parameter('kp', 0.5)
        self.declare_parameter('ki', 0.01)
        self.declare_parameter('kd', 0.1)
        self.declare_parameter('max_linear_speed', 0.2)
        self.declare_parameter('max_angular_speed', 0.8)
        self.declare_parameter('waypoint_tolerance', 0.12)
        self.declare_parameter('goal_tolerance', 0.12)
        self.declare_parameter('max_linear_heading_error', 0.6)
        self.declare_parameter('control_period', 0.1)

        self.goal = Pose()
        self.goal.position.x = float(self.get_parameter('goal_x').value)
        self.goal.position.y = float(self.get_parameter('goal_y').value)
        self.kp = float(self.get_parameter('kp').value)
        self.ki = float(self.get_parameter('ki').value)
        self.kd = float(self.get_parameter('kd').value)
        self.max_linear_speed = float(
            self.get_parameter('max_linear_speed').value
        )
        self.max_angular_speed = float(
            self.get_parameter('max_angular_speed').value
        )
        self.waypoint_tolerance = float(
            self.get_parameter('waypoint_tolerance').value
        )
        self.goal_tolerance = float(self.get_parameter('goal_tolerance').value)
        self.max_linear_heading_error = float(
            self.get_parameter('max_linear_heading_error').value
        )
        self.control_period = float(
            self.get_parameter('control_period').value
        )

        positive_values = (
            self.max_linear_speed,
            self.max_angular_speed,
            self.waypoint_tolerance,
            self.goal_tolerance,
            self.control_period,
        )
        if any(value <= 0.0 for value in positive_values):
            raise ValueError('speed, tolerance, and period parameters must be positive')
        if min(self.kp, self.ki, self.kd) < 0.0:
            raise ValueError('PID gains must be non-negative')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.odom_subscription = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10
        )
        self.map_subscription = self.create_subscription(
            OccupancyGrid, 'map', self.map_callback, 10
        )
        self.timer = self.create_timer(self.control_period, self.control_callback)

        self.planner = None
        self.path = []
        self.current_target = 0
        self.current_x = None
        self.current_y = None
        self.current_yaw = None
        self.integral = 0.0
        self.previous_error = None
        self.goal_reached = False
        self._last_state = None

    def map_callback(self, msg):
        if msg.info.width == 0 or msg.info.height == 0:
            self.get_logger().error('Received an empty occupancy grid.')
            self.path = []
            self.planner = None
            return
        expected_size = msg.info.width * msg.info.height
        if len(msg.data) != expected_size:
            self.get_logger().error('Occupancy grid data size does not match its dimensions.')
            self.path = []
            self.planner = None
            return

        quaternion = msg.info.origin.orientation
        origin_yaw = math.atan2(
            2.0 * (quaternion.w * quaternion.z + quaternion.x * quaternion.y),
            1.0 - 2.0 * (quaternion.y ** 2 + quaternion.z ** 2),
        )
        map_data = np.asarray(msg.data, dtype=np.int16).reshape(
            (msg.info.height, msg.info.width)
        )
        self.planner = AStarPlanner(
            map_data,
            msg.info.resolution,
            (msg.info.origin.position.x, msg.info.origin.position.y, origin_yaw),
        )
        self.path = []
        self.current_target = 0
        self.integral = 0.0
        self.previous_error = None
        self.goal_reached = False

    def odom_callback(self, msg):
        pose = msg.pose.pose
        self.current_x = pose.position.x
        self.current_y = pose.position.y
        q = pose.orientation
        self.current_yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y ** 2 + q.z ** 2),
        )

    def _publish_stop(self, state, message=None):
        self.publisher_.publish(Twist())
        if message and self._last_state != state:
            self.get_logger().info(message)
        self._last_state = state

    def _ensure_path(self):
        if self.planner is None or self.current_x is None:
            return False
        if self.path:
            return True

        start = self.planner.world_to_map((self.current_x, self.current_y))
        goal = self.planner.world_to_map(
            (self.goal.position.x, self.goal.position.y)
        )
        grid_path = self.planner.plan(start, goal)
        if not grid_path:
            self._publish_stop('no_path', 'No valid A* path found; robot stopped.')
            return False

        self.path = [self.planner.map_to_world(cell) for cell in grid_path]
        self.current_target = 0
        self.integral = 0.0
        self.previous_error = None
        self.get_logger().info(f'A* generated a path with {len(self.path)} cells.')
        return True

    def control_callback(self):
        if self.current_x is None or self.planner is None:
            self._publish_stop('waiting_for_data', 'Waiting for map and odometry; robot stopped.')
            return
        if not self._ensure_path():
            return
        if self.goal_reached:
            self._publish_stop('goal_reached')
            return

        target = self.path[self.current_target]
        dx = target[0] - self.current_x
        dy = target[1] - self.current_y
        distance_error = math.hypot(dx, dy)

        tolerance = (
            self.goal_tolerance
            if self.current_target == len(self.path) - 1
            else self.waypoint_tolerance
        )
        if distance_error <= tolerance:
            if self.current_target == len(self.path) - 1:
                self.goal_reached = True
                self._publish_stop('goal_reached', 'Goal reached; robot stopped.')
                return
            self.current_target += 1
            target = self.path[self.current_target]
            dx = target[0] - self.current_x
            dy = target[1] - self.current_y
            distance_error = math.hypot(dx, dy)

        desired_yaw = math.atan2(dy, dx)
        heading_error = normalize_angle(desired_yaw - self.current_yaw)
        dt = self.control_period
        self.integral = max(
            -1.0, min(1.0, self.integral + distance_error * dt)
        )
        derivative = 0.0
        if self.previous_error is not None:
            derivative = (distance_error - self.previous_error) / dt
        self.previous_error = distance_error

        linear = (
            self.kp * distance_error
            + self.ki * self.integral
            + self.kd * derivative
        )
        linear = max(0.0, min(linear, self.max_linear_speed))
        if abs(heading_error) > self.max_linear_heading_error:
            linear = 0.0
        else:
            linear *= max(0.0, math.cos(heading_error))

        angular = max(
            -self.max_angular_speed,
            min(1.5 * heading_error, self.max_angular_speed),
        )

        command = Twist()
        command.linear.x = linear
        command.angular.z = angular
        self.publisher_.publish(command)
        self._last_state = 'tracking'


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = PIDController()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.publisher_.publish(Twist())
            node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
