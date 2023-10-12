#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
import random

class MoveTurtlesimNode(Node):
    def __init__(self):
        super().__init__("move_turtlesim_node")
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "turtle1/cmd_vel", 10)
        self.cmd_timer_ = self.create_timer(
            0.1, self.publish_cmd)

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