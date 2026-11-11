import math
import threading
import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.duration import Duration
from rclpy.time import Time
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from tf2_ros import Buffer, TransformListener, TransformException

from coordinate_follower_interfaces.action import Coordinate


class CoordinateActionServer(Node):

    def __init__(self):
        super().__init__('coordinate_action_server')

        self.callback_group = ReentrantCallbackGroup()

        # Controller configuration
        self.goal_tolerance = 0.10
        self.heading_tolerance = 0.15

        self.linear_gain = 0.5
        self.angular_gain = 1.5

        self.max_linear_speed = 0.12
        self.max_angular_speed = 0.6

        self.control_period = 0.1
        self.goal_timeout = 120.0
        self.odom_timeout = 5.0

        # Odometry storage
        self.odom_lock = threading.Lock()
        self.latest_odom = None

        # Prevent simultaneous navigation goals
        self.goal_lock = threading.Lock()
        self.goal_active = False

        # Velocity publisher
        self.cmd_vel_publisher = self.create_publisher(
            Twist, '/cmd_vel', 10
        )

        # Odometry subscriber
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10,
            callback_group=self.callback_group
        )

        # TF2 buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(
            self.tf_buffer, self
        )

        # Action server
        self.action_server = ActionServer(
            self,
            Coordinate,
            'coordinate_follower',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.callback_group
        )

        self.get_logger().info(
            'Coordinate Action Server is ready.'
        )

    def odom_callback(self, msg):
        """Store the latest odometry message."""

        with self.odom_lock:
            self.latest_odom = msg

    @staticmethod
    def normalize_angle(angle):
        """Normalize an angle to [-pi, pi]."""

        return math.atan2(
            math.sin(angle),
            math.cos(angle)
        )

    @staticmethod
    def get_yaw(orientation):
        """Extract yaw from a quaternion."""

        return math.atan2(
            2.0 * (
                orientation.w * orientation.z
                + orientation.x * orientation.y
            ),
            1.0 - 2.0 * (
                orientation.y ** 2
                + orientation.z ** 2
            )
        )

    @staticmethod
    def transform_xy(x, y, transform):
        """Transform a planar point between coordinate frames."""

        translation = transform.transform.translation
        rotation = transform.transform.rotation

        yaw = CoordinateActionServer.get_yaw(rotation)

        transformed_x = (
            translation.x
            + math.cos(yaw) * x
            - math.sin(yaw) * y
        )

        transformed_y = (
            translation.y
            + math.sin(yaw) * x
            + math.cos(yaw) * y
        )

        return transformed_x, transformed_y

    @staticmethod
    def clamp(value, limit):
        return max(-limit, min(limit, value))

    def goal_callback(self, goal_request):
        """Validate incoming goals and prevent concurrent execution."""

        if not (
            math.isfinite(goal_request.x)
            and math.isfinite(goal_request.y)
        ):
            self.get_logger().warning(
                'Rejected invalid coordinate goal.'
            )
            return GoalResponse.REJECT

        with self.goal_lock:
            if self.goal_active:
                self.get_logger().warning(
                    'Rejected goal: another goal is active.'
                )
                return GoalResponse.REJECT

            self.goal_active = True

        self.get_logger().info(
            f'Accepted goal: x={goal_request.x:.2f}, '
            f'y={goal_request.y:.2f}'
        )

        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept cancellation requests."""

        self.get_logger().info('Cancellation requested.')

        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Execute the coordinate-following controller."""

        result = Coordinate.Result()
        start_time = time.monotonic()

        try:
            goal = goal_handle.request

            # Convert the requested map-frame goal into odom.
            odom_from_map = self.tf_buffer.lookup_transform(
                'odom',
                'map',
                Time(),
                timeout=Duration(seconds=1.0)
            )

            goal_x_odom, goal_y_odom = self.transform_xy(
                goal.x,
                goal.y,
                odom_from_map
            )

            self.get_logger().info(
                f'Goal in odom frame: '
                f'x={goal_x_odom:.2f}, y={goal_y_odom:.2f}'
            )

            while rclpy.ok():

                # Handle cancellation.
                if goal_handle.is_cancel_requested:
                    result.success = False
                    result.message = 'Goal canceled.'
                    goal_handle.canceled()
                    return result

                elapsed = time.monotonic() - start_time

                # Prevent indefinite execution.
                if elapsed > self.goal_timeout:
                    result.success = False
                    result.message = 'Goal execution timed out.'
                    goal_handle.abort()
                    return result

                # Get the latest odometry.
                with self.odom_lock:
                    odom = self.latest_odom

                if odom is None:
                    if elapsed > self.odom_timeout:
                        result.success = False
                        result.message = (
                            'No odometry received from /odom.'
                        )
                        goal_handle.abort()
                        return result

                    time.sleep(self.control_period)
                    continue

                position = odom.pose.pose.position
                orientation = odom.pose.pose.orientation

                robot_x = position.x
                robot_y = position.y
                robot_yaw = self.get_yaw(orientation)

                # Convert the current robot position into map frame.
                map_from_odom = self.tf_buffer.lookup_transform(
                    'map',
                    'odom',
                    Time(),
                    timeout=Duration(seconds=1.0)
                )

                current_map_x, current_map_y = self.transform_xy(
                    robot_x,
                    robot_y,
                    map_from_odom
                )

                # Calculate distance and heading error in odom.
                dx = goal_x_odom - robot_x
                dy = goal_y_odom - robot_y

                distance = math.hypot(dx, dy)

                desired_yaw = math.atan2(dy, dx)

                heading_error = self.normalize_angle(
                    desired_yaw - robot_yaw
                )

                # Publish continuous action feedback.
                feedback = Coordinate.Feedback()

                feedback.current_x = float(current_map_x)
                feedback.current_y = float(current_map_y)
                feedback.distance_remaining = float(distance)

                goal_handle.publish_feedback(feedback)

                # Check whether the target has been reached.
                if distance <= self.goal_tolerance:
                    result.success = True
                    result.message = 'Target reached successfully.'

                    goal_handle.succeed()

                    self.get_logger().info(
                        f'Reached target: '
                        f'x={goal.x:.2f}, y={goal.y:.2f}'
                    )

                    return result

                # Generate velocity commands.
                command = Twist()

                if abs(heading_error) > self.heading_tolerance:
                    # Rotate first when heading error is large.
                    command.angular.z = self.clamp(
                        self.angular_gain * heading_error,
                        self.max_angular_speed
                    )

                else:
                    # Move forward and correct small heading errors.
                    command.linear.x = min(
                        self.max_linear_speed,
                        self.linear_gain * distance
                    )

                    command.angular.z = self.clamp(
                        self.angular_gain * heading_error,
                        self.max_angular_speed
                    )

                self.cmd_vel_publisher.publish(command)

                time.sleep(self.control_period)

            result.success = False
            result.message = 'ROS shutdown before goal completion.'
            goal_handle.abort()

            return result

        except TransformException as error:
            result.success = False
            result.message = f'TF error: {error}'

            self.get_logger().error(result.message)

            goal_handle.abort()
            return result

        except Exception as error:
            result.success = False
            result.message = f'Execution error: {error}'

            self.get_logger().error(result.message)

            goal_handle.abort()
            return result

        finally:
            self.stop_robot()

            with self.goal_lock:
                self.goal_active = False

    def stop_robot(self):
        """Publish zero velocity."""

        self.cmd_vel_publisher.publish(Twist())


def main(args=None):

    rclpy.init(args=args)

    node = CoordinateActionServer()

    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)

    try:
        executor.spin()

    except KeyboardInterrupt:
        pass

    finally:
        node.stop_robot()

        if rclpy.ok():
            rclpy.shutdown()

        executor.shutdown()
        node.destroy_node()


if __name__ == '__main__':
    main()
