import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoider(Node):

    def __init__(self):
        super().__init__('obstacle_avoider')

        # Subscribe to LiDAR data
        self.scan_subscriber = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        # Publisher for robot velocity commands
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.stop_threshold = 0.5
        self.resume_threshold = 0.65

        self.forward_speed = 0.08
        self.turn_speed = 0.5

        self.is_turning = False

        self.last_state = None

        self.get_logger().info('Obstacle avoider started. Waiting for /scan...')

    def scan_callback(self, msg):

        # Extract the front-facing 60-degree sector
        front_ranges = msg.ranges[150:211]

        # Filter invalid measurements
        valid_front_ranges = [
            distance for distance in front_ranges
            if math.isfinite(distance)
            and msg.range_min <= distance <= msg.range_max
        ]

        # Start with a zero-velocity command
        cmd = Twist()

        if not valid_front_ranges:

            # Stop if LiDAR data is unreliable
            current_state = 'no_valid_scan'

        else:

            min_front_distance = min(valid_front_ranges)

            # Hysteresis-based state transitions
            if self.is_turning:

                if min_front_distance >= self.resume_threshold:
                    self.is_turning = False

            else:

                if min_front_distance <= self.stop_threshold:
                    self.is_turning = True

            # Generate velocity based on current state
            if self.is_turning:
                cmd.angular.z = -self.turn_speed
                current_state = 'turning_right'

            else:
                cmd.linear.x = self.forward_speed
                current_state = 'moving_forward'

            # Log distance only when the state changes
            if current_state != self.last_state:
                self.get_logger().info(f'Minimum front distance: {min_front_distance:.3f} m')

        # Publish velocity command
        self.cmd_vel_publisher.publish(cmd)

        # Log state transitions
        if current_state != self.last_state:

            if current_state == 'moving_forward':
                self.get_logger().info('Path clear. Moving forward.')

            elif current_state == 'turning_right':
                self.get_logger().warning('Obstacle detected. Turning right.')

            else:
                self.get_logger().warning('No valid front LiDAR readings. Stopping.')

            self.last_state = current_state

def main(args=None):
    rclpy.init(args=args)

    node = ObstacleAvoider()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
