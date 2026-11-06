# SPDX-License-Identifier: Apache-2.0
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    toolbox = Path(get_package_share_directory('slam_toolbox')) / 'launch' / 'online_async_launch.py'
    config = Path(get_package_share_directory('robotless_lab')) / 'config' / 'slam.yaml'
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(toolbox)),
            launch_arguments={'use_sim_time': 'true', 'slam_params_file': str(config)}.items()),
    ])
