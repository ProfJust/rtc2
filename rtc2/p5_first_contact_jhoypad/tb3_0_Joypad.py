#!/usr/bin/env python3
#
#   mtb3_0_Joypad.py.py
# -------------------------------------------
#   for rtc2
#   by oj, 13.11.23
#   Westfälische Hochschule - Campus Bocholt
#   see also http://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal
# -------------------------------------------

# install:
# $ sudo apt-get install ros-humble-teleop-twist-joy
# usage
# $1 ros2 launch teleop_twist_joy teleop-launch.py 
# $2 ros2 run tb3_0_Joypad.py
# ==> setup.py nicht vergessen
# -------------------------------------------
# Let TurtleBot be steered by Jopad
# 
# -------------------------------------------

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Joy
from math import pow, atan2, sqrt, isnan


class clTurtleJoy(Node):  # erbt von Node

    def __init__(self):
        super().__init__("move_tb3_by_Joypad_node")
        self.vel_msg = Twist() # Instanziiere Message mit cmd_vel
        self.cmd_vel_publisher_ = self.create_publisher(
                                    Twist,
                                    '/tb3_0/cmd_vel',
                                    10)
        
        self.subscription = self.create_subscription(
                              Joy,
                              'joy',
                              self.update_joy,
                              10)
        self.subscription  # prevent unused variable warning
        
    def update_joy(self, joy_msg):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        print ("callback Joy Node ")
        self.vel_msg.linear.x  = 0.5 * joy_msg.axes[1]
        self.vel_msg.angular.z = 1.0 * joy_msg.axes[0]
        self.cmd_vel_publisher_.publish(self.vel_msg)  # ..senden



def main(args=None):
    rclpy.init(args=args)    
    node = clTurtleJoy()
    
    while True:
        try:
            rclpy.spin(node)
        except:
            break
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()