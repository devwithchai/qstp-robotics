import random
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import Int32, String

class IntegerPublisher(Node):
    def __init__(self):
        super().__init__('integer_publisher')
        self.pub = self.create_publisher(Int32, 'integers', 10)
        self.create_timer(1.0, self.publish_integer)

    def publish_integer(self):
        msg = Int32()
        msg.data = random.randint(1, 100)
        self.pub.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')

class OddEvenClassifier(Node):
    def __init__(self):
        super().__init__('odd_even_classifier')
        self.sub = self.create_subscription(
            Int32, 'integers', self.classify, 10)
        self.pub = self.create_publisher(String, 'oddeven', 10)

    def classify(self, msg):
        result = 'even' if msg.data % 2 == 0 else 'odd'
        output = String()
        output.data = result
        self.pub.publish(output)
        self.get_logger().info(f'{msg.data} is {result}')

def main():
    rclpy.init()
    publisher = IntegerPublisher()
    classifier = OddEvenClassifier()

    executor = SingleThreadedExecutor()
    executor.add_node(publisher)
    executor.add_node(classifier)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        publisher.destroy_node()
        classifier.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
