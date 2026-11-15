#!/usr/bin/env python3

import math
import time
from enum import Enum

import rclpy
from geometry_msgs.msg import PointStamped, Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Bool, Int32


class NavigationState(Enum):
    WAITING_FOR_ODOM = 'WAITING_FOR_ODOM'
    MOVING_FORWARD = 'MOVING_FORWARD'
    APPROACHING_MARKER = 'APPROACHING_MARKER'
    ROTATING = 'ROTATING'
    MISSION_COMPLETE = 'MISSION_COMPLETE'
    ERROR = 'ERROR'


class NavigationController(Node):

    EXPECTED_MARKER_IDS = (0, 1, 0, 1, 0)
    TURN_ANGLES = tuple(map(math.radians, (-56.0, 107.6, -73.6, 154.4)))

    def __init__(self):
        super().__init__('navigation_controller')

        self.declare_parameter('forward_speed', 0.05)
        self.declare_parameter('approach_speed', 0.03)
        self.declare_parameter('angular_speed', 0.35)
        self.declare_parameter('odom_timeout', 0.75)
        self.declare_parameter('marker_pose_timeout', 0.75)
        self.declare_parameter('standoff_distance', 0.22)
        self.declare_parameter('standoff_tolerance', 0.01)
        self.declare_parameter('yaw_tolerance', math.radians(2.0))

        self.forward_speed = float(self.get_parameter('forward_speed').value)
        self.approach_speed = float(self.get_parameter('approach_speed').value)
        self.angular_speed = float(self.get_parameter('angular_speed').value)
        if not math.isfinite(self.angular_speed) or self.angular_speed <= 0.0:
            raise ValueError('angular_speed must be finite and positive.')

        longest_turn = max(abs(angle) for angle in self.TURN_ANGLES)
        minimum_turn_timeout = 1.5 * longest_turn / self.angular_speed
        self.declare_parameter('turn_timeout', minimum_turn_timeout)
        self.turn_timeout = float(self.get_parameter('turn_timeout').value)
        self.odom_timeout = float(self.get_parameter('odom_timeout').value)
        self.marker_pose_timeout = float(
            self.get_parameter('marker_pose_timeout').value
        )
        self.standoff_distance = float(
            self.get_parameter('standoff_distance').value
        )
        self.standoff_tolerance = float(
            self.get_parameter('standoff_tolerance').value
        )
        self.yaw_tolerance = float(self.get_parameter('yaw_tolerance').value)
        self._validate_parameters(minimum_turn_timeout)

        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.detection_enabled_publisher = self.create_publisher(
            Bool,
            '/aruco/detection_enabled',
            10,
        )
        self.marker_subscription = self.create_subscription(
            Int32,
            '/aruco/detected_id',
            self.marker_callback,
            10,
        )
        self.marker_position_subscription = self.create_subscription(
            PointStamped,
            '/aruco/marker_position',
            self.marker_position_callback,
            10,
        )
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10,
        )

        self.state = NavigationState.WAITING_FOR_ODOM
        self.odom_received = False
        self.last_odom_received_at = None
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.encounter_count = 0
        self.current_marker_id = None
        self.marker_range = None
        self.last_marker_position_received_at = None
        self.last_approach_log_at = 0.0

        self.rotation_started_at = 0.0
        self.rotation_start_yaw = 0.0
        self.rotation_target_yaw = 0.0
        self.last_rotation_log_at = 0.0

        self.control_timer = self.create_timer(0.05, self.control_callback)
        self._publish_detection_enabled()
        self.get_logger().info(
            'Navigation controller ready; waiting for odometry. '
            f'Route={list(self.EXPECTED_MARKER_IDS)}, '
            f'turn_timeout={self.turn_timeout:.2f}s.'
        )

    def _validate_parameters(self, minimum_turn_timeout):
        numeric_parameters = (
            ('forward_speed', self.forward_speed),
            ('approach_speed', self.approach_speed),
            ('angular_speed', self.angular_speed),
            ('turn_timeout', self.turn_timeout),
            ('odom_timeout', self.odom_timeout),
            ('marker_pose_timeout', self.marker_pose_timeout),
            ('standoff_distance', self.standoff_distance),
            ('standoff_tolerance', self.standoff_tolerance),
            ('yaw_tolerance', self.yaw_tolerance),
        )
        for name, value in numeric_parameters:
            if not math.isfinite(value):
                raise ValueError(f'{name} must be finite.')
            if value <= 0.0:
                raise ValueError(f'{name} must be greater than zero.')
        if self.turn_timeout < minimum_turn_timeout:
            raise ValueError(
                'turn_timeout must accommodate the longest route turn '
                'with a 50% safety margin; expected at least '
                f'{minimum_turn_timeout:.2f} seconds.'
            )
        if self.standoff_tolerance >= self.standoff_distance:
            raise ValueError(
                'standoff_tolerance must be less than standoff_distance.'
            )
        if self.yaw_tolerance >= math.pi:
            raise ValueError('yaw_tolerance must be less than pi radians.')

    @staticmethod
    def _yaw_from_quaternion(quaternion):
        sin_yaw = 2.0 * (
            quaternion.w * quaternion.z + quaternion.x * quaternion.y
        )
        cos_yaw = 1.0 - 2.0 * (
            quaternion.y * quaternion.y + quaternion.z * quaternion.z
        )
        return math.atan2(sin_yaw, cos_yaw)

    @staticmethod
    def _normalize_angle(angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def _publish_stop(self):
        self.cmd_publisher.publish(Twist())

    def _publish_detection_enabled(self):
        message = Bool()
        message.data = self.state is NavigationState.MOVING_FORWARD
        self.detection_enabled_publisher.publish(message)

    def _transition_to(self, new_state, reason):
        if self.state is new_state:
            return

        self._publish_stop()
        old_state = self.state
        self.state = new_state
        self.get_logger().info(
            f'State transition: {old_state.value} -> {new_state.value} '
            f'({reason})'
        )
        self._publish_detection_enabled()

    def odom_callback(self, message):
        position = message.pose.pose.position
        self.x = position.x
        self.y = position.y
        self.yaw = self._yaw_from_quaternion(
            message.pose.pose.orientation
        )
        self.last_odom_received_at = time.monotonic()
        self.odom_received = True

    def marker_callback(self, message):
        if self.state is not NavigationState.MOVING_FORWARD:
            self.get_logger().debug(
                f'Ignoring marker ID {message.data} during {self.state.value}.'
            )
            return

        if not self._odometry_is_fresh():
            self._fail('Cannot process marker because odometry is stale.')
            return

        if self.encounter_count >= len(self.EXPECTED_MARKER_IDS):
            return

        marker_id = int(message.data)
        expected_id = self.EXPECTED_MARKER_IDS[self.encounter_count]
        if marker_id != expected_id:
            self._fail(
                f'Unexpected marker at encounter {self.encounter_count + 1}: '
                f'expected ID {expected_id}, received ID {marker_id}.'
            )
            return

        self.current_marker_id = marker_id
        self.encounter_count += 1
        self.marker_range = None
        self.last_marker_position_received_at = None
        self.last_approach_log_at = 0.0
        self.get_logger().info(
            f'Encounter {self.encounter_count}/'
            f'{len(self.EXPECTED_MARKER_IDS)}: expected ID {expected_id}, '
            f'received ID {marker_id}; target standoff '
            f'{self.standoff_distance:.3f} m.'
        )

        if self.encounter_count == len(self.EXPECTED_MARKER_IDS):
            self._complete_mission()
            return

        self._transition_to(
            NavigationState.APPROACHING_MARKER,
            f'confirmed expected marker ID {marker_id}',
        )

    def marker_position_callback(self, message):
        point = message.point
        values = (point.x, point.y, point.z)
        if not all(math.isfinite(value) for value in values):
            return
        if message.header.frame_id != 'base_link':
            self.get_logger().error(
                'Marker position must be expressed in base_link; received '
                f"'{message.header.frame_id}'."
            )
            if self.state is NavigationState.APPROACHING_MARKER:
                self._fail('Marker position frame is not base_link.')
            return
        if point.x <= 0.0:
            return

        self.marker_range = math.hypot(point.x, point.y)
        self.last_marker_position_received_at = time.monotonic()

    def _odometry_is_fresh(self):
        if self.last_odom_received_at is None:
            return False
        elapsed = time.monotonic() - self.last_odom_received_at
        return elapsed <= self.odom_timeout

    def _marker_position_is_fresh(self):
        if self.last_marker_position_received_at is None:
            return False
        return (
            time.monotonic() - self.last_marker_position_received_at
            <= self.marker_pose_timeout
        )

    def _begin_rotation(self):
        turn_angle = self.TURN_ANGLES[self.encounter_count - 1]
        self.rotation_start_yaw = self.yaw
        self.rotation_target_yaw = self._normalize_angle(
            self.rotation_start_yaw + turn_angle
        )
        self.rotation_started_at = self.get_clock().now().nanoseconds / 1e9
        self.last_rotation_log_at = 0.0
        direction = 'right' if turn_angle < 0.0 else 'left'
        self.get_logger().info(
            f'Rotation setup after encounter {self.encounter_count}: '
            f'direction={direction}, starting yaw='
            f'{math.degrees(self.rotation_start_yaw):.2f}°, target yaw='
            f'{math.degrees(self.rotation_target_yaw):.2f}°, '
            f'turn={math.degrees(turn_angle):+.2f}°.'
        )
        self._transition_to(
            NavigationState.ROTATING,
            f'{self.standoff_distance:.2f} m robot-centre standoff reached; '
            f'rotate {direction}',
        )

    def control_callback(self):
        self._publish_detection_enabled()

        active_states = (
            NavigationState.MOVING_FORWARD,
            NavigationState.APPROACHING_MARKER,
            NavigationState.ROTATING,
        )
        now = time.monotonic()
        if self.state in active_states and not self._odometry_is_fresh():
            elapsed = (
                math.inf
                if self.last_odom_received_at is None
                else now - self.last_odom_received_at
            )
            self._fail(
                f'Odometry became stale after {elapsed:.2f} seconds '
                f'(timeout {self.odom_timeout:.2f} seconds).'
            )
            return

        if self.state is NavigationState.WAITING_FOR_ODOM:
            self._publish_stop()
            if self.odom_received:
                self._transition_to(
                    NavigationState.MOVING_FORWARD,
                    'odometry received',
                )
            return

        if self.state is NavigationState.MOVING_FORWARD:
            command = Twist()
            command.linear.x = self.forward_speed
            self.cmd_publisher.publish(command)
            return

        if self.state is NavigationState.APPROACHING_MARKER:
            if not self._marker_position_is_fresh():
                elapsed = (
                    math.inf
                    if self.last_marker_position_received_at is None
                    else now - self.last_marker_position_received_at
                )
                self._fail(
                    'Marker position became stale while approaching '
                    f'(age {elapsed:.2f}s, timeout '
                    f'{self.marker_pose_timeout:.2f}s).'
                )
                return

            if self.marker_range is None:
                self._fail('No valid marker range is available.')
                return

            if now - self.last_approach_log_at >= 0.5:
                self.get_logger().info(
                    f'Encounter {self.encounter_count}: marker range '
                    f'{self.marker_range:.3f} m; target standoff '
                    f'{self.standoff_distance:.3f} m.'
                )
                self.last_approach_log_at = now

            if (
                self.marker_range
                <= self.standoff_distance + self.standoff_tolerance
            ):
                self._begin_rotation()
                return

            command = Twist()
            command.linear.x = self.approach_speed
            self.cmd_publisher.publish(command)
            return

        if self.state is NavigationState.ROTATING:
            yaw_error = self._normalize_angle(
                self.rotation_target_yaw - self.yaw
            )
            measured_change = self._normalize_angle(
                self.yaw - self.rotation_start_yaw
            )
            if abs(yaw_error) <= self.yaw_tolerance:
                self._transition_to(
                    NavigationState.MOVING_FORWARD,
                    'odometry yaw target reached',
                )
                self.get_logger().info(
                    f'Rotation complete: target yaw='
                    f'{math.degrees(self.rotation_target_yaw):.2f}°, '
                    f'measured yaw change='
                    f'{math.degrees(measured_change):+.2f}°.'
                )
                return

            elapsed = (
                self.get_clock().now().nanoseconds / 1e9
                - self.rotation_started_at
            )
            if elapsed >= self.turn_timeout:
                self._fail(
                    f'Rotation timed out after {elapsed:.2f}s: starting yaw='
                    f'{math.degrees(self.rotation_start_yaw):.2f}°, '
                    'target yaw='
                    f'{math.degrees(self.rotation_target_yaw):.2f}°, '
                    f'measured yaw change='
                    f'{math.degrees(measured_change):+.2f}°.'
                )
                return

            command = Twist()
            command.angular.z = math.copysign(self.angular_speed, yaw_error)
            self.cmd_publisher.publish(command)

            if now - self.last_rotation_log_at >= 1.0:
                direction = 'right' if command.angular.z < 0.0 else 'left'
                self.get_logger().info(
                    f'Rotating {direction}: start='
                    f'{math.degrees(self.rotation_start_yaw):.2f}°, target='
                    f'{math.degrees(self.rotation_target_yaw):.2f}°, current='
                    f'{math.degrees(self.yaw):.2f}°, measured change='
                    f'{math.degrees(measured_change):+.2f}°, error='
                    f'{math.degrees(yaw_error):+.2f}°.'
                )
                self.last_rotation_log_at = now
            return

        if self.state in (
            NavigationState.MISSION_COMPLETE,
            NavigationState.ERROR,
        ):
            self._publish_stop()

    def _complete_mission(self):
        self._transition_to(
            NavigationState.MISSION_COMPLETE,
            f'completed {self.encounter_count} expected marker encounters',
        )
        self.get_logger().info(
            'Navigation mission complete after the fifth marker encounter.'
        )

    def _fail(self, reason):
        self._transition_to(NavigationState.ERROR, reason)
        self.get_logger().error(reason)

    def destroy_node(self):
        self._publish_stop()
        disabled = Bool()
        disabled.data = False
        self.detection_enabled_publisher.publish(disabled)
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = NavigationController()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
