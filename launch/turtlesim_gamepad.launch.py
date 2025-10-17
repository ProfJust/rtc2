from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),
        Node(
            package='joy_linux',
            executable='joy_linux_node',
            name='joy',
            output='screen'
        ),
        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_twist_joy',
            parameters=[{
                'enable_button': 5,          # RB als Deadman
                'axis_linear.x': 1,          # linker Stick vor/zurück
                'scale_linear.x': 2.0,
                'axis_angular.z': 0,         # rechter Stick links/rechts
                'scale_angular.z': 2.0,
            }],
            remappings=[('cmd_vel', '/turtle1/cmd_vel')]
        ),
    ])
