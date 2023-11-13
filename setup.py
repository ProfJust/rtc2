import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'rtc2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files.
        # https://docs.ros.org/en/foxy/Tutorials/Intermediate/Launch/Launch-system.html
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='oj',
    maintainer_email='olaf.just@w-hs.de',
    description='Ruhr TurtleBot Competition using ROS2 and turtlebot3',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        # hier alle Pythons Scripte eintragen, die übersetzt werden sollen 
        #  Bezeichner zum starten mit ros2 run  =  
        #              Name des Files (ohne py) : Funktion die starten soll 
        'say_temp= rtc2.pub_temp:main',
        # 'min_pub= rtc2.publisher_member_function:main',
        'talk= rtc2.talker:main',
        'listen= rtc2.listener:main',
        'move_turtlesim= rtc2.move_turtle:main',
        'p2_turtlesim_move_distance= rtc2.move_turtle_distance:main',
        'p2_turtlesim_move_distance_import= rtc2.move_turtle_distance_import:main',
        'p3_turtlesim_move_2_goal= rtc2.move_turtle_2_goal:main',
        'ue4_qt_robot_steering= rtc2.qt_robot_steering:main',
        'tb3_joypad_steering= rtc2.tb3_0_Joypad:main',

        ],
    },
)
