import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

from .laser_utils import get_front_sector_min_distance


class TurtlebotController(Node):
    """Drive forward, stopping at the distance goal or for front obstacles."""

    def __init__(self):
        super().__init__('turtlebot_controller')
        self.declare_parameter('linear_velocity', 0.2)
        self.declare_parameter('goal_distance', 2.0)
        self.declare_parameter('obstacle_threshold', 0.5)
        self.declare_parameter('front_sector_half_angle', 0.35)
        self.declare_parameter('scan_timeout_sec', 0.5)

        self.linear_velocity = float(self.get_parameter('linear_velocity').value)
        self.goal_distance = float(self.get_parameter('goal_distance').value)
        self.obstacle_threshold = float(
            self.get_parameter('obstacle_threshold').value
        )
        self.front_sector_half_angle = float(
            self.get_parameter('front_sector_half_angle').value
        )
        self.scan_timeout_sec = float(
            self.get_parameter('scan_timeout_sec').value
        )

        if self.linear_velocity < 0.0:
            raise ValueError('linear_velocity must be non-negative')
        if self.goal_distance <= 0.0 or self.obstacle_threshold <= 0.0:
            raise ValueError('goal_distance and obstacle_threshold must be positive')
        if not 0.0 <= self.front_sector_half_angle <= math.pi:
            raise ValueError('front_sector_half_angle must be between 0 and pi')
        if self.scan_timeout_sec <= 0.0:
            raise ValueError('scan_timeout_sec must be positive')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_subscription = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10
        )
        self.odom_subscription = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10
        )
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.current_x = 0.0
        self.start_x = None
        self.obstacle_distance = math.inf
        self.scan_received = False
        self.last_scan_time = None
        self.goal_reached = False
        self._state = None

    def _stop(self, state, message):
        self.publisher_.publish(Twist())
        if self._state != state:
            self.get_logger().info(message)
        self._state = state

    def scan_callback(self, msg):
        distance = get_front_sector_min_distance(
            msg.ranges,
            msg.angle_min,
            msg.angle_increment,
            self.front_sector_half_angle,
            msg.range_min,
            msg.range_max,
        )
        self.last_scan_time = self.get_clock().now()
        self.scan_received = distance is not None
        self.obstacle_distance = math.inf if distance is None else distance

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        if self.start_x is None:
            self.start_x = self.current_x
            self.get_logger().info(f'Starting x position: {self.start_x:.2f} m')

    def timer_callback(self):
        if self.start_x is None:
            self._stop('waiting_for_odometry', 'Waiting for odometry; robot stopped.')
            return
        if not self.scan_received or self.last_scan_time is None:
            self._stop('waiting_for_scan', 'No valid front LiDAR data; robot stopped.')
            return

        scan_age = (self.get_clock().now() - self.last_scan_time).nanoseconds / 1e9
        if scan_age > self.scan_timeout_sec:
            self._stop('stale_scan', 'LiDAR data is stale; robot stopped.')
            return

        distance_traveled = abs(self.current_x - self.start_x)
        if distance_traveled >= self.goal_distance:
            self.goal_reached = True
        if self.goal_reached:
            self._stop(
                'goal_reached',
                f'Goal reached after {distance_traveled:.2f} m; robot stopped.',
            )
            return
        if self.obstacle_distance <= self.obstacle_threshold:
            self._stop(
                'obstacle_detected',
                f'Front obstacle at {self.obstacle_distance:.2f} m; robot stopped.',
            )
            return

        if self._state != 'moving':
            self.get_logger().info('Front sector clear; moving forward.')
        self._state = 'moving'
        command = Twist()
        command.linear.x = self.linear_velocity
        self.publisher_.publish(command)

    def destroy_node(self):
        self.publisher_.publish(Twist())
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = TurtlebotController()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
