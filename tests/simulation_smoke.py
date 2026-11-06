"""Read the running virtual robot; do not publish motion commands.

SPDX-License-Identifier: Apache-2.0
"""

import math
import time

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import LaserScan


def main():
    rclpy.init(args=[])
    node = Node('simulation_smoke')
    readings = {'clock': [], 'scan': None, 'odom': None}

    def clock_callback(message):
        readings['clock'].append(message.clock.sec + message.clock.nanosec * 1e-9)
        readings['clock'] = readings['clock'][-10:]

    def scan_callback(message):
        if message.ranges and any(math.isfinite(r) and r > 0 for r in message.ranges):
            readings['scan'] = message

    def odom_callback(message):
        pose = message.pose.pose
        if (message.header.frame_id == 'odom' and message.child_frame_id == 'base_footprint'
                and all(math.isfinite(v) for v in (
                    pose.position.x, pose.position.y, pose.orientation.z, pose.orientation.w))):
            readings['odom'] = message

    subscriptions = [
        node.create_subscription(Clock, '/clock', clock_callback, qos_profile_sensor_data),
        node.create_subscription(LaserScan, '/scan', scan_callback, qos_profile_sensor_data),
        node.create_subscription(Odometry, '/odom', odom_callback, qos_profile_sensor_data),
    ]
    started = time.monotonic()
    try:
        while time.monotonic() - started < 90:
            rclpy.spin_once(node, timeout_sec=0.2)
            clocks = readings['clock']
            if (len(clocks) >= 2 and clocks[-1] > clocks[0]
                    and readings['scan'] is not None and readings['odom'] is not None):
                print('Gazebo smoke passed: advancing /clock, finite /scan ranges, finite framed /odom.')
                return
        raise RuntimeError(
            'Simulation timed out: clock_samples=%d scan=%s odom=%s' % (
                len(readings['clock']), readings['scan'] is not None, readings['odom'] is not None))
    finally:
        for subscription in subscriptions:
            node.destroy_subscription(subscription)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
