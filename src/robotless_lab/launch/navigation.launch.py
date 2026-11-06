"""Start installed Nav2 with a learner-created map; never send a goal.

SPDX-License-Identifier: Apache-2.0
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    bringup = Path(get_package_share_directory('nav2_bringup')) / 'launch' / 'bringup_launch.py'
    turtlebot = Path(get_package_share_directory('turtlebot3_navigation2'))
    return LaunchDescription([
        DeclareLaunchArgument('map', description='Absolute path to your saved map YAML'),
        DeclareLaunchArgument('gui', default_value='true', description='Show RViz'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(bringup)),
            launch_arguments={
                'map': LaunchConfiguration('map'),
                'use_sim_time': 'true',
                'params_file': str(turtlebot / 'param' / 'humble' / 'burger.yaml'),
            }.items()),
        Node(package='rviz2', executable='rviz2', output='screen',
             condition=IfCondition(LaunchConfiguration('gui')),
             arguments=['-d', str(turtlebot / 'rviz' / 'tb3_navigation2.rviz')],
             parameters=[{'use_sim_time': True}]),
    ])
