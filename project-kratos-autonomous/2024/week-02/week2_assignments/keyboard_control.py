import select
import sys
import termios
import time
import tty

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class KeyboardControl(Node):
    """Publish short-lived velocity commands from terminal key presses."""

    def __init__(self):
        super().__init__('keyboard_control')
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('angular_speed', 0.2)
        self.declare_parameter('command_timeout_sec', 0.25)

        self.linear_speed = float(self.get_parameter('linear_speed').value)
        self.angular_speed = float(self.get_parameter('angular_speed').value)
        self.command_timeout_sec = float(
            self.get_parameter('command_timeout_sec').value
        )
        if self.linear_speed < 0.0 or self.angular_speed < 0.0:
            raise ValueError('speeds must be non-negative')
        if self.command_timeout_sec <= 0.0:
            raise ValueError('command_timeout_sec must be positive')
        if not sys.stdin.isatty():
            raise RuntimeError('Keyboard control requires an interactive terminal.')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self._last_key = None
        self._last_key_time = 0.0
        self._stdin_fd = sys.stdin.fileno()
        self._terminal_settings = termios.tcgetattr(self._stdin_fd)
        tty.setcbreak(self._stdin_fd)
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.get_logger().info(
            'Use W/S to move, A/D to turn, Space to stop, and Q to quit.'
        )

    def timer_callback(self):
        while select.select([sys.stdin], [], [], 0.0)[0]:
            key = sys.stdin.read(1)
            if not key:
                break
            key = key.lower()
            if key == 'q':
                self.publish_stop()
                rclpy.try_shutdown()
                return
            if key == ' ':
                self._last_key = None
                continue
            if key in ('w', 's', 'a', 'd'):
                self._last_key = key
                self._last_key_time = time.monotonic()
            else:
                self._last_key = None

        twist = Twist()
        fresh = (
            self._last_key is not None
            and time.monotonic() - self._last_key_time <= self.command_timeout_sec
        )
        if fresh:
            if self._last_key == 'w':
                twist.linear.x = self.linear_speed
            elif self._last_key == 's':
                twist.linear.x = -self.linear_speed
            elif self._last_key == 'a':
                twist.angular.z = self.angular_speed
            elif self._last_key == 'd':
                twist.angular.z = -self.angular_speed
        else:
            self._last_key = None
        self.publisher_.publish(twist)

    def publish_stop(self):
        self._last_key = None
        self.publisher_.publish(Twist())

    def destroy_node(self):
        try:
            self.publish_stop()
        finally:
            termios.tcsetattr(
                self._stdin_fd, termios.TCSADRAIN, self._terminal_settings
            )
            super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = KeyboardControl()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
