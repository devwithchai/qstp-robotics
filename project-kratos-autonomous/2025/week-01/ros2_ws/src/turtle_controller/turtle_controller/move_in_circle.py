import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        # Publish velocity commands on the robot's command topic.
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Send a new command 10 times every second.
        self.timer = self.create_timer(0.1, self.publish_velocity)

        self.get_logger().info('TurtleBot is moving in a circle. Press Ctrl+C to stop.')

    def publish_velocity(self):
        command = Twist()

        # Forward speed (metres per second).
        command.linear.x = 0.08

        # Turning speed (radians per second).
        # Keeping both values non-zero makes the robot follow a curved path.
        command.angular.z = 0.5

        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)

    node = TurtleController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Send a zero-velocity command before shutting down.
        stop_command = Twist()
        node.publisher.publish(stop_command)
        node.get_logger().info('Stopping the TurtleBot.')

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
