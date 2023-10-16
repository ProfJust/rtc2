https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/
https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/#launch-event-handler-list

from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch_ros.actions import Node
# from launch.event_handlers import OnExecutionComplete
from launch.event_handlers import OnProcessStart
  
def generate_launch_description():
     
    turtlesim1 = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name='turtlesim1'
    )
 
    turtlesim2 = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name='turtlesim2'
    )
 
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=turtlesim1,
                on_start=[turtlesim2],
            )
        ),
        turtlesim1
    ])