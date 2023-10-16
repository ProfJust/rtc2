# talker_listener_launch.py
#---------------------------------------------------------------------
# 16.10.23 by OJ 
# Westfälische Hochschule, Campus Bocholt, Ruhr TurtleBot Competition
#---------------------------------------------------------------------
# launches talker and listener at the same time
# usage:
# $ ros2 launch rtc2 talker_listener_launch.py
# --------------------------------------------------------------------

from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch_ros.actions import Node
# from launch.event_handlers import OnExecutionComplete
from launch.event_handlers import OnProcessStart
  
def generate_launch_description():
     
    turtlesim1 = Node(
        package="rtc2",
        executable="talk",
        name='talker'
    )
 
    turtlesim2 = Node(
        package="rtc2",
        executable="listen",
        name='listener'
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

# for more information on launch files see
# https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/
# https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/#launch-event-handler-list
