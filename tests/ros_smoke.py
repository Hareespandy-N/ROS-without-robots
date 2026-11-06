"""Exercise the actual lesson nodes and read-only reporter using ROS middleware.

Run after colcon build and sourcing install/setup.bash; no Gazebo required.
SPDX-License-Identifier: Apache-2.0
"""

import time

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rcl_interfaces.msg import Log
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

from robotless_lab.lesson import LessonPublisher, LessonSubscriber
from robotless_lab.pose_report import PoseReporter


def main():
    rclpy.init(args=[])
    nodes = [LessonPublisher(), LessonSubscriber(), PoseReporter(), Node('smoke_observer')]
    executor = SingleThreadedExecutor()
    for node in nodes:
        executor.add_node(node)
    observer = nodes[-1]
    messages, logs = [], []
    lesson_subscription = observer.create_subscription(
        String, '/robotless/lesson', lambda msg: messages.append(msg.data), 10)
    log_subscription = observer.create_subscription(
        Log, '/rosout', lambda msg: logs.append(msg.msg) if msg.name == 'pose_report' else None, 100)
    publisher = observer.create_publisher(PoseWithCovarianceStamped, '/amcl_pose', 10)
    started = time.monotonic()

    def publish_sample():
        pose = PoseWithCovarianceStamped()
        pose.header.frame_id = 'odom' if time.monotonic() - started < 3.0 else 'map'
        pose.header.stamp = observer.get_clock().now().to_msg()
        pose.pose.pose.position.x = 0.003
        pose.pose.pose.position.y = -0.004
        pose.pose.pose.orientation.w = 1.0
        publisher.publish(pose)

    sample_timer = observer.create_timer(0.1, publish_sample)
    try:
        while time.monotonic() - started < 8.0:
            executor.spin_once(timeout_sec=0.1)
            if (nodes[1].received >= 2 and len(messages) >= 2
                    and any('expected map frame' in line for line in logs)
                    and any('dx_mm=3.000 dy_mm=-4.000 xy_mm=5.000' in line for line in logs)):
                break
        assert nodes[1].received >= 2, 'Lesson subscriber did not receive repeated messages.'
        assert len(set(messages)) >= 2, 'Publisher sequence did not change.'
        assert any('expected map frame' in line for line in logs), 'Wrong-frame pose was not rejected.'
        assert any('dx_mm=3.000 dy_mm=-4.000 xy_mm=5.000' in line for line in logs), logs
        print('ROS smoke passed: actual topic delivery, sequence, frame rejection, and pose report.')
    finally:
        observer.destroy_timer(sample_timer)
        observer.destroy_subscription(lesson_subscription)
        observer.destroy_subscription(log_subscription)
        executor.shutdown()
        for node in nodes:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
