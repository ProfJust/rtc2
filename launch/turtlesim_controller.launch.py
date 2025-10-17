# Datei: turtlesim_praktikum.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Node 1: Turtlesim starten
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtle1'
        ),

        # Node 2: Eigene Klasse starten
        Node(
            package='rtc2',                     # dein ROS-Paketname
            executable='turtlesim_controller',  # der Name aus setup.py (entry_point)
            name='controller',
            output='screen'                     # Ausgabe in Terminal anzeigen
        )
    ])

