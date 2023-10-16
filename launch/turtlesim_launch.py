import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='rtc2',
            namespace='rtc2',
            executable='move_turtlesim',
            name='move_node'
        ),
        launch_ros.actions.Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='sim'
        ),        
    ])