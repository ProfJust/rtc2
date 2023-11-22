#!/usr/bin/env  python3
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

# for euler => quaternions install
# sudo apt install python3-transforms3d 
# sudo apt install ros-humble-tf-transformations
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

    rclpy.shutdown()

if __name__ == '__main__':
    main()
