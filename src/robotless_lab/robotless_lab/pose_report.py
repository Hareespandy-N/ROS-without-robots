"""Read-only AMCL-versus-goal comparison for simulation learning.

SPDX-License-Identifier: Apache-2.0
"""

import math

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from robotless_lab.geometry import pose_error, quaternion_yaw


class PoseReporter(Node):
    def __init__(self):
        super().__init__('pose_report')
        self.declare_parameter('goal_x', 0.0)
        self.declare_parameter('goal_y', 0.0)
        self.declare_parameter('goal_yaw_deg', 0.0)
        self.goal = (
            float(self.get_parameter('goal_x').value),
            float(self.get_parameter('goal_y').value),
            math.radians(float(self.get_parameter('goal_yaw_deg').value)),
        )
        pose_error(self.goal, self.goal)  # Reject invalid parameters at startup.
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.report, qos_profile_sensor_data)
        self.get_logger().info('Read-only localization comparison; independent accuracy is not proven yet.')

    def report(self, message):
        if message.header.frame_id != 'map':
            self.get_logger().warning('Skipped pose: expected map frame.')
            return
        position = message.pose.pose.position
        rotation = message.pose.pose.orientation
        try:
            yaw = quaternion_yaw(rotation.x, rotation.y, rotation.z, rotation.w)
            error = pose_error(self.goal, (position.x, position.y, yaw))
        except ValueError as exc:
            self.get_logger().warning(f'Skipped invalid pose: {exc}')
            return
        stamp = message.header.stamp
        self.get_logger().info(
            f'frame=map stamp={stamp.sec}.{stamp.nanosec:09d} '
            f'goal_m=({self.goal[0]:.3f},{self.goal[1]:.3f}) '
            f'amcl_m=({position.x:.3f},{position.y:.3f}) '
            f'dx_mm={error["dx_mm"]:.3f} dy_mm={error["dy_mm"]:.3f} '
            f'xy_mm={error["xy_mm"]:.3f} yaw_deg={error["yaw_deg"]:.3f}'
        )


def main():
    rclpy.init()
    node = None
    try:
        node = PoseReporter()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
