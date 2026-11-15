
import math
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from ament_index_python.packages import get_package_share_directory
from action_msgs.msg import GoalStatus

from coordinate_follower_interfaces.action import Coordinate


class CoordinateSequenceClient(Node):

    def __init__(self):
        super().__init__('coordinate_sequence_client')

        self.action_client = ActionClient(
            self,
            Coordinate,
            '/coordinate_follower'
        )

        # Locate the installed coordinate file.
        package_share = get_package_share_directory(
            'coordinate_follower'
        )

        self.coordinate_file = (
            Path(package_share) / 'config' / 'coordinates.txt'
        )

    def load_coordinates(self):
        """Read and validate coordinate pairs from the text file."""

        coordinates = []

        with open(self.coordinate_file, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):

                # Remove comments and ignore empty lines.
                line = line.split('#', 1)[0].strip()

                if not line:
                    continue

                values = line.split()

                if len(values) != 2:
                    raise ValueError(
                        f'Invalid coordinate at line {line_number}. '
                        'Expected exactly two values: x y'
                    )

                try:
                    x, y = map(float, values)
                except ValueError:
                    raise ValueError(
                        f'Invalid numbers at line {line_number}: {line}'
                    )

                if not math.isfinite(x) or not math.isfinite(y):
                    raise ValueError(
                        f'Non-finite coordinate at line {line_number}'
                    )

                coordinates.append((x, y))

        if not coordinates:
            raise ValueError('No valid coordinates found in coordinates.txt')

        return coordinates

    def feedback_callback(self, feedback_msg):
        """Display feedback received while a goal is executing."""

        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Position: ({feedback.current_x:.3f}, '
            f'{feedback.current_y:.3f}) | '
            f'Distance remaining: '
            f'{feedback.distance_remaining:.3f} m'
        )

    def send_goal(self, x, y):
        """Send one goal and wait until its result is received."""

        goal = Coordinate.Goal()
        goal.x = x
        goal.y = y

        self.get_logger().info(
            f'Sending goal: x={x:.2f}, y={y:.2f}'
        )

        # Send the goal asynchronously.
        send_goal_future = self.action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        rclpy.spin_until_future_complete(
            self,
            send_goal_future
        )

        goal_handle = send_goal_future.result()

        if goal_handle is None:
            self.get_logger().error('Failed to receive goal response.')
            return False

        if not goal_handle.accepted:
            self.get_logger().error('Goal was rejected by the server.')
            return False

        self.get_logger().info('Goal accepted. Waiting for result...')

        # Request the result and wait for completion.
        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        response = result_future.result()

        if response is None:
            self.get_logger().error('Failed to receive action result.')
            return False

        if response.status != GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().error(
                f'Goal did not succeed. Status: {response.status}'
            )
            return False

        result = response.result

        if not result.success:
            self.get_logger().error(
                f'Goal failed: {result.message}'
            )
            return False

        self.get_logger().info(
            f'Goal completed successfully: {result.message}'
        )

        return True


def main(args=None):

    rclpy.init(args=args)

    client = CoordinateSequenceClient()

    try:
        # Load all target coordinates.
        coordinates = client.load_coordinates()

        client.get_logger().info(
            f'Loaded {len(coordinates)} coordinate goals.'
        )

        # Wait until the action server becomes available.
        while rclpy.ok():
            if client.action_client.wait_for_server(timeout_sec=2.0):
                break

            client.get_logger().info(
                'Waiting for coordinate action server...'
            )

        if not rclpy.ok():
            return

        # Execute goals sequentially.
        for index, (x, y) in enumerate(coordinates, start=1):

            client.get_logger().info(
                f'========== GOAL {index}/{len(coordinates)} =========='
            )

            success = client.send_goal(x, y)

            if not success:
                client.get_logger().error(
                    'Sequence stopped because a goal failed.'
                )
                break

        else:
            client.get_logger().info(
                'All coordinate goals completed successfully!'
            )

    except (OSError, ValueError) as error:
        client.get_logger().error(str(error))

    finally:
        client.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
