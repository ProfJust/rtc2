#!/usr/bin/env  python3
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration

# for euler => quaternions install
# sudo apt install python3-transforms3d 
# sudo apt install ros-humble-tf-transformations

# Example from
# https://github.com/ros-planning/navigation2/blob/main/nav2_simple_commander/nav2_simple_commander/example_nav_to_pose.py
import tf_transformations

def main():
    rclpy.init()
    
    # Instanzieren 
    nav = BasicNavigator()
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = nav.get_clock().now().to_msg()
    # get a quaternion from euler-angles
    qx, qy, qz, qw = tf_transformations.quaternion_from_euler(0.0, 0.0, 0.0)
    initial_pose.pose.orientation.x = qx
    initial_pose.pose.orientation.y = qy
    initial_pose.pose.orientation.z = qy
    initial_pose.pose.orientation.w = qw
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.position.z = 0.0
    nav.setInitialPose(initial_pose)

    nav.waitUntilNav2Active()

    goal_pose = PoseStamped()   #  GOAL -----------------
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    # goal for turtlebot_world
    goal_pose.pose.position.x = 2.5
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0

    path = nav.getPath(initial_pose, goal_pose)
    # smoothed_path = nav.smoothPath(path)

    nav.goToPose(goal_pose)

    i=0
    while not nav.isTaskComplete():
        i = i+1
        feedback = nav.getFeedback()
        # if feedback.navigation_time > 600:
        #    nav.cancelTask()
        if feedback and i % 5 == 0:
           print(
               'Estimated time of arrival: '
               + '{0:.0f}'.format(
                   Duration.from_msg(feedback.estimated_time_remaining).nanoseconds
                   / 1e9
               )
               + ' seconds.'
           )

    result = nav.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')

    rclpy.shutdown()

if __name__ == '__main__':
    main()
