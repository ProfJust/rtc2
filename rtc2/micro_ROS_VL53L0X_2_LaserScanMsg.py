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
from rclpy.qos import ReliabilityPolicy, QoSProfile
qos_profile = QoSProfile(depth=10)
qos_profile.reliability = ReliabilityPolicy.BEST_EFFORT

class micro_ROS_Node(Node):
    def __init__(self):
        super().__init__("move_turtlesim_node")
        self.cmd_vel_publisher_ = self.create_publisher(
                                    LaserScan,
                                    "Lrange",
                                    qos_profile)  
        # the number `10` you are trying to pass seems to represent the depth, but since you are already specifying it in the `qos_profile`, it's unnecessary and will result in a syntax error.

        self.cmd_timer_ = self.create_timer(
                            0.5,
                            self.publish_cmd)
        
        self.sub1 = self.create_subscription(
                              Int32,
                              'range1',
                              self.listener_callback1,
                              qos_profile)
        self.sub2 = self.create_subscription(
                              Int32,
                              'range2',
                              self.listener_callback2,
                              qos_profile)
        self.sub1  # prevent unused variable warning
        self.sub2  # prevent unused variable warning
        self.my_range1 = 0.0
        self.my_range2 = 0.0

    def listener_callback1(self, msg):
        self.my_range1 = msg.data/1000 # msg in mm, range in m
        self.get_logger().info(' Sensor1 gives Position in m "%f"' % self.my_range1)

    def listener_callback2(self, msg):
        self.my_range2 = msg.data/1000 # msg in mm, range in m
        self.get_logger().info(' Sensor2 gives Position in m "%f"' % self.my_range2)

    def publish_cmd(self):        
        msg = LaserScan()  # Leer msg instanzieren
        # ... und füllen
        # https://github.com/mikeferguson/ros2_cookbook/blob/main/rclpy/time.md
        t = self.get_clock().now()
        msg.header.stamp = t.to_msg()
        msg.header.frame_id = "base_link"
        msg.angle_min = -0.02 # start angle of the scan [rad] 
        msg.angle_max =  0.02 # start angle of the scan [rad]  
        msg.angle_increment = 0.01 # angular distance between measurements [rad]
        msg.time_increment = 0.001 # time between measurements [seconds] - if your scanner
                           # # is moving, this will be used in interpolating position
                           # # of 3d points
        msg.scan_time = 0.0 # time between scans [seconds]
        msg.range_min = 0.02 # minimum range value [m]
        msg.range_max = 2.0   # maximum range value [m]
        msg.ranges = [self.my_range1, self.my_range1, self.my_range1, self.my_range2, self.my_range2  ] # range data [m]
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
