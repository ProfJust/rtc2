#!/usr/bin/env python3
#
#   move_turtle_distance.py
# -------------------------------------------
#   for rtc2
#   by oj, 20.10.23
#   Westfälische Hochschule - Campus Bocholt
# -------------------------------------------
# usage
# $1 ros2 run turtlesim turtlesim_node 
# $2 ros2 run rtc2 p2_turtlesim_move_distance
# -------------------------------------------
# Let Turtle Move a given distance 
# (relative from start posotion)
# -------------------------------------------
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
#from std_msgs.msg import String
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, pi

from .my_class_files.turtlesim_class_file import MoveTurtlesimNode
# Wichtig, den "." nicht vergessen !!!!
        
def main(args=None):
    rclpy.init(args=args)    
    node = MoveTurtlesimNode()  # Instanzierung
    while True:
        try:
            rclpy.spin(node)
        except:
            break
    rclpy.shutdown()

if __name__ == "__main__":
    main()