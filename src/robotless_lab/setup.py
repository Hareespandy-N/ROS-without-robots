# SPDX-License-Identifier: Apache-2.0
from glob import glob

from setuptools import find_packages, setup

package_name = 'robotless_lab'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/worlds', glob('worlds/*.world')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hareespandy-N',
    maintainer_email='266934573+Hareespandy-N@users.noreply.github.com',
    description='ROS 2 lessons and original warehouse simulation composition',
    license='Apache-2.0',
    entry_points={'console_scripts': [
        'lesson_publisher = robotless_lab.lesson:publisher_main',
        'lesson_subscriber = robotless_lab.lesson:subscriber_main',
        'pose_report = robotless_lab.pose_report:main',
    ]},
)
