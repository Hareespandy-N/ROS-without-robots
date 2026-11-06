"""Compose installed simulation tools around our original warehouse world.

SPDX-License-Identifier: Apache-2.0
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    gazebo = Path(get_package_share_directory('gazebo_ros')) / 'launch'
    turtlebot = Path(get_package_share_directory('turtlebot3_gazebo')) / 'launch'
    world = Path(get_package_share_directory('robotless_lab')) / 'worlds' / 'learning_warehouse.world'
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true', description='Show Gazebo GUI'),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(gazebo / 'gzserver.launch.py')),
            launch_arguments={'world': str(world)}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(gazebo / 'gzclient.launch.py')),
            condition=IfCondition(LaunchConfiguration('gui'))),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(turtlebot / 'robot_state_publisher.launch.py')),
            launch_arguments={'use_sim_time': 'true'}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(turtlebot / 'spawn_turtlebot3.launch.py')),
            launch_arguments={'x_pose': '0.0', 'y_pose': '-3.0'}.items()),
    ])
