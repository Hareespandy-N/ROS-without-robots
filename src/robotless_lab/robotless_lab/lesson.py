"""A publisher/subscriber exercise with a visible sequence number.

SPDX-License-Identifier: Apache-2.0
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class LessonPublisher(Node):
    def __init__(self):
        super().__init__('lesson_publisher')
        self.sequence = 0
        self.publisher = self.create_publisher(String, '/robotless/lesson', 10)
        self.timer = self.create_timer(1.0, self.publish_lesson)

    def publish_lesson(self):
        message = String()
        message.data = f'Lesson message {self.sequence}: one topic connects two nodes.'
        self.publisher.publish(message)
        self.get_logger().info(message.data)
        self.sequence += 1


class LessonSubscriber(Node):
    def __init__(self):
        super().__init__('lesson_subscriber')
        self.received = 0
        self.subscription = self.create_subscription(
            String, '/robotless/lesson', self.receive_lesson, 10)

    def receive_lesson(self, message):
        self.received += 1
        self.get_logger().info(f'Received #{self.received}: {message.data}')


def _run(node_type):
    rclpy.init()
    node = node_type()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


def publisher_main():
    _run(LessonPublisher)


def subscriber_main():
    _run(LessonSubscriber)
