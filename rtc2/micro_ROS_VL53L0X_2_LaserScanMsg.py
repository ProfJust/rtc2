#!/usr/bin/env python3
#
#   micro_ROS_VL53L0X_2_LaserScanMsg.py
# -------------------------------------------
#   for rtc2
#   by oj, 17.12.24
#   Westfälische Hochschule - Campus Bocholt
# -------------------------------------------
# usage
# # $2 ros2 run rtc2 micro_ROS_2_laserscan
# -------------------------------------------
# Empfängt die Messwerte vom micro_ros Sensor und 
# baut daraus eine LaserScan Message zum Import bei NAV2
# 
# -------------------------------------------
import rclpy
from rclpy.node import Node
#from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32
#from turtlesim.msg import Pose
#from math import pow, atan2, sqrt, pi

class micro_ROS_Node(Node):
    def __init__(self):
        super().__init__("move_turtlesim_node")
        self.cmd_vel_publisher_ = self.create_publisher(
                                    LaserScan,
                                    "Lrange",
                                    10)
        self.cmd_timer_ = self.create_timer(
                            0.5,
                            self.publish_cmd)
        
        self.subscription = self.create_subscription(
                              Int32,
                              'range',
                              self.listener_callback,
                              10)
        self.subscription  # prevent unused variable warning
        self.my_range = 0.0

    def listener_callback(self, msg):
        self.my_range = msg.data/1000 # msg in mm, range in m
        self.get_logger().info(' Sensor gives Position in m "%f"' % self.my_range)

    def publish_cmd(self):        
        msg = LaserScan()  # Leer msg instanzieren
        # ... und füllen
        # https://github.com/mikeferguson/ros2_cookbook/blob/main/rclpy/time.md
        t = self.get_clock().now()
        msg.header.stamp = t.to_msg()
        msg.header.frame_id = "base_link"
        msg.angle_min = -0.01 # start angle of the scan [rad] 
        msg.angle_max =  0.01 # start angle of the scan [rad]  
        msg.angle_increment = 0.01 # angular distance between measurements [rad]
        msg.time_increment = 0.001 # time between measurements [seconds] - if your scanner
                           # # is moving, this will be used in interpolating position
                           # # of 3d points
        msg.scan_time = 0.0 # time between scans [seconds]
        msg.range_min = 0.02 # minimum range value [m]
        msg.range_max = 9.0   # maximum range value [m]
        msg.ranges = [self.my_range, self.my_range, self.my_range ] # range data [m]
        # # (Note: values < range_min or > range_max should be discarded)
        msg.intensities = [] # intensity data [device-specific units]. If your
        # # device does not provide intensities, please leave
        # # the array empty.
        self.cmd_vel_publisher_.publish(msg)  # ..senden
        
def main(args=None):
    rclpy.init(args=args)
    node = micro_ROS_Node()  # Instanzierung
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
