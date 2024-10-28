#!/usr/bin/env python3

# move_turtle.py
#   for rtc2
#   by oj, 15.10.23
#   Westfälische Hochschule - Campus Bocholt
# -------------------------------------------
# usage
# $1 ros2 run turtlesim turtlesim_node 
# $2 ros2 run rtc2 move_turtlesim
# -------------------------------------------
# First example to publish and subscribe
# messages form a Robot (Turtlesim)
# -------------------------------------------
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from turtlesim.msg import Pose

import random

class MoveTurtlesimNode(Node):
    def __init__(self):
        super().__init__("move_turtlesim_node")
        self.cmd_vel_publisher_ = self.create_publisher(
                                    Twist,
                                    "turtle1/cmd_vel",
                                    10)
        self.cmd_timer_ = self.create_timer(
                            0.1,
                            self.publish_cmd)
        
        self.subscription = self.create_subscription(
                              Pose,
                              'turtle1/pose',
                              self.listener_callback,
                              10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(' Turtle is at Position x "%f"' % msg.x)
        self.get_logger().info('                       y "%f"' % msg.y)
        self.get_logger().info('                   theta "%f"' % msg.theta)


    def publish_cmd(self):
        vel = random.randint(0, 100) / 100
        turn =  3.1415927 /8
        msg = Twist()  # Leer msg instanzieren
        msg.linear.x = vel  # ... und füllen
        msg.angular.z = turn

        self.cmd_vel_publisher_.publish(msg)  # ..senden
        
def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtlesimNode()  # Instanzierung
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()