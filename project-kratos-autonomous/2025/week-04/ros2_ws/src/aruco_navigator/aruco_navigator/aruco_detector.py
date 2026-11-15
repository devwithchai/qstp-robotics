import math

import cv2
import numpy as np
import rclpy

from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import PointStamped
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import Bool, Int32


class ArucoDetector(Node):

    MARKER_SIZE = 0.0625
    CAMERA_FORWARD_OFFSET = 0.03
    CAMERA_HEIGHT = 0.028

    def __init__(self):
        super().__init__('aruco_detector')

        self.declare_parameter('image_topic', '/camera/image_color')
        self.declare_parameter('camera_info_topic', '/camera/camera_info')
        self.declare_parameter('marker_topic', '/aruco/detected_id')
        self.declare_parameter(
            'marker_position_topic',
            '/aruco/marker_position',
        )
        self.declare_parameter(
            'detection_enabled_topic',
            '/aruco/detection_enabled',
        )
        self.declare_parameter('confirmation_frames', 3)
        self.declare_parameter('lost_frames_to_reset', 5)

        image_topic = self.get_parameter('image_topic').value
        camera_info_topic = self.get_parameter('camera_info_topic').value
        marker_topic = self.get_parameter('marker_topic').value
        marker_position_topic = self.get_parameter(
            'marker_position_topic'
        ).value
        detection_enabled_topic = self.get_parameter(
            'detection_enabled_topic'
        ).value

        self.confirmation_frames = max(
            1, int(self.get_parameter('confirmation_frames').value)
        )
        self.lost_frames_to_reset = max(
            1, int(self.get_parameter('lost_frames_to_reset').value)
        )

        self.bridge = CvBridge()
        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_ARUCO_ORIGINAL
        )
        self.detector_parameters = cv2.aruco.DetectorParameters_create()
        self.camera_matrix = None
        self.distortion_coefficients = None
        self.camera_info_width = 0
        self.camera_info_height = 0
        self.camera_info_warning_reported = False
        self.image_size_warning_reported = False

        self.candidate_id = None
        self.candidate_count = 0
        self.active_marker_id = None
        self.missing_frames = 0
        self.last_published_id = None
        self.detection_enabled = False

        self.marker_publisher = self.create_publisher(
            Int32,
            marker_topic,
            10
        )
        self.marker_position_publisher = self.create_publisher(
            PointStamped,
            marker_position_topic,
            10,
        )
        self.detection_enabled_subscription = self.create_subscription(
            Bool,
            detection_enabled_topic,
            self.detection_enabled_callback,
            10,
        )
        self.camera_info_subscription = self.create_subscription(
            CameraInfo,
            camera_info_topic,
            self.camera_info_callback,
            10,
        )
        self.image_subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )

        self.get_logger().info('ArUco detector started.')
        self.get_logger().info(f'Subscribing to: {image_topic}')
        self.get_logger().info(
            f'Subscribing to camera calibration: {camera_info_topic}'
        )
        self.get_logger().info(f'Publishing marker IDs to: {marker_topic}')
        self.get_logger().info(
            f'Publishing marker positions to: {marker_position_topic}'
        )
        self.get_logger().info(
            f'Waiting for detection enable state on: {detection_enabled_topic}'
        )

    def camera_info_callback(self, message):
        if message.width <= 0 or message.height <= 0 or len(message.k) != 9:
            self.camera_matrix = None
            self.distortion_coefficients = None
            self.get_logger().error(
                'CameraInfo has invalid image dimensions or intrinsic matrix.'
            )
            return

        matrix = np.asarray(message.k, dtype=np.float64).reshape(3, 3)
        if (
            not np.isfinite(matrix).all()
            or matrix[0, 0] <= 0.0
            or matrix[1, 1] <= 0.0
        ):
            self.camera_matrix = None
            self.distortion_coefficients = None
            self.get_logger().error(
                'CameraInfo contains invalid focal lengths or intrinsics.'
            )
            return

        distortion = np.asarray(message.d, dtype=np.float64)
        if distortion.size == 0:
            distortion = np.zeros(5, dtype=np.float64)
        if not np.isfinite(distortion).all():
            self.camera_matrix = None
            self.distortion_coefficients = None
            self.get_logger().error(
                'CameraInfo contains non-finite distortion coefficients.'
            )
            return

        self.camera_matrix = matrix
        self.distortion_coefficients = distortion
        self.camera_info_width = int(message.width)
        self.camera_info_height = int(message.height)
        self.camera_info_warning_reported = False

    def detection_enabled_callback(self, message):
        enabled = bool(message.data)
        if enabled != self.detection_enabled:
            self.detection_enabled = enabled
            self.candidate_id = None
            self.candidate_count = 0
            self.get_logger().info(
                f'Marker event publishing '
                f'{"enabled" if enabled else "disabled"}.'
            )

    def image_callback(self, msg):

        try:
            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )
        except CvBridgeError as error:
            self.get_logger().error(f'Image conversion failed: {error}')
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = cv2.aruco.detectMarkers(
            gray,
            self.dictionary,
            parameters=self.detector_parameters
        )

        detected_ids = [] if ids is None else ids.flatten().tolist()

        self._track_active_marker(detected_ids)
        if self.active_marker_id is not None:
            if self.active_marker_id in detected_ids:
                marker_index = detected_ids.index(self.active_marker_id)
                self._publish_marker_position(
                    corners[marker_index],
                    msg.header,
                    frame.shape[1],
                    frame.shape[0],
                )
            return

        if not self.detection_enabled:
            self.candidate_id = None
            self.candidate_count = 0
            return

        if len(detected_ids) != 1:
            self.candidate_id = None
            self.candidate_count = 0
            if detected_ids:
                self.get_logger().warning(
                    f'Expected one marker, but detected {len(detected_ids)}.'
                )
            return

        marker_id = int(detected_ids[0])
        self.missing_frames = 0

        if marker_id == self.candidate_id:
            self.candidate_count += 1
        else:
            self.candidate_id = marker_id
            self.candidate_count = 1

        if self.candidate_count >= self.confirmation_frames:
            self.active_marker_id = marker_id
            self.missing_frames = 0
            self._publish_marker_position(
                corners[0],
                msg.header,
                frame.shape[1],
                frame.shape[0],
            )

            if marker_id == self.last_published_id:
                self.get_logger().warning(
                    'Suppressing consecutive repeat of marker ID '
                    f'{marker_id}; '
                    'a different marker ID must be confirmed first.'
                )
                return

            marker_msg = Int32()
            marker_msg.data = marker_id
            self.marker_publisher.publish(marker_msg)
            self.last_published_id = marker_id
            self.get_logger().info(
                f'Marker detected and published: ID {marker_id}'
            )

    def _publish_marker_position(
        self,
        corners,
        image_header,
        image_width,
        image_height,
    ):
        if self.camera_matrix is None:
            if not self.camera_info_warning_reported:
                self.get_logger().warning(
                    'Waiting for valid /camera/camera_info before '
                    'publishing marker positions.'
                )
                self.camera_info_warning_reported = True
            return
        if (
            image_width != self.camera_info_width
            or image_height != self.camera_info_height
        ):
            if not self.image_size_warning_reported:
                self.get_logger().error(
                    'Image dimensions do not match CameraInfo; cannot '
                    f'estimate marker pose ({image_width}x{image_height} vs '
                    f'{self.camera_info_width}x{self.camera_info_height}).'
                )
                self.image_size_warning_reported = True
            return
        self.image_size_warning_reported = False

        try:
            _, translation_vectors, _ = (
                cv2.aruco.estimatePoseSingleMarkers(
                    [corners],
                    self.MARKER_SIZE,
                    self.camera_matrix,
                    self.distortion_coefficients,
                )
            )
        except cv2.error as error:
            self.get_logger().error(
                f'ArUco pose estimation failed: {error}'
            )
            return

        camera_x, camera_y, camera_z = map(
            float,
            translation_vectors[0][0],
        )
        if not all(
            math.isfinite(value)
            for value in (camera_x, camera_y, camera_z)
        ) or camera_z <= 0.0:
            self.get_logger().warning(
                'Ignoring invalid ArUco pose estimate.'
            )
            return

        marker_position = PointStamped()
        marker_position.header.stamp = image_header.stamp
        marker_position.header.frame_id = 'base_link'
        # Camera optical x-right/y-down/z-forward map to base -y/-z/+x.
        marker_position.point.x = self.CAMERA_FORWARD_OFFSET + camera_z
        marker_position.point.y = -camera_x
        marker_position.point.z = self.CAMERA_HEIGHT - camera_y
        self.marker_position_publisher.publish(marker_position)

    def _track_active_marker(self, detected_ids):
        if self.active_marker_id is None:
            return

        if self.active_marker_id in detected_ids:
            self.missing_frames = 0
            self.candidate_id = None
            self.candidate_count = 0
            return

        self.missing_frames += 1
        if self.missing_frames < self.lost_frames_to_reset:
            self.candidate_id = None
            self.candidate_count = 0
            return

        self.get_logger().info(
            f'Marker ID {self.active_marker_id} cleared. '
            'Detector ready for the next marker.'
        )
        self.active_marker_id = None
        self.missing_frames = 0
        self.candidate_id = None
        self.candidate_count = 0


def main(args=None):

    rclpy.init(args=args)

    node = ArucoDetector()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
