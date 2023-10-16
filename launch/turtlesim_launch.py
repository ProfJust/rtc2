# turtlesim_launch.py
#---------------------------------------------------------------------
# 16.10.23 by OJ 
# Westfälische Hochschule, Campus Bocholt, Ruhr TurtleBot Competition
#---------------------------------------------------------------------
# launches turtlesim and our move_node at the same time
# usage:
# $ ros2 launch rtc2 turtlesim_launch.py
# --------------------------------------------------------------------

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
 
    move = Node(
        package="rtc2",
        executable="move_turtlesim",
        name='move_node'
    )
 
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=turtlesim1,
                on_start=[move],
            )
        ),
        turtlesim1
    ])

# for more information on launch files see
# https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/
# https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/#launch-event-handler-list