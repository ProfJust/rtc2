# ROS2 Jazzy - TurtleSim mit Tastatursteuerung
#---------------------------------------------------------------------
# launches turtlesim and our teleop_key at the same time
# usage:
# $ ros2 launch rtc2 turtlesim_teleop_key_launch.py
# --------------------------------------------------------------------
# um die Tastatursteuerung starten zu können
# muessen Sie ggf. xterm installieren:
# $ sudo apt install xterm 

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        # TurtleSim starten
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),

        # Zufallsbewegung starten
        Node(
            package='rtc2',
            executable='sw02_TurtleSim_publish_cmd_vel',
            name='rtc2',
            output='screen',
            prefix='xterm -e'
        )

    ])