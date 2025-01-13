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

#ROS1 import tf
from tf2_ros import TransformBroadcaster, TransformStamped
import tf_transformations
#ROS1 br = tf.TransformBroadcaster()
import math
     

class micro_ROS_Node(Node):
    def __init__(self):
        super().__init__("move_turtlesim_node")
        self.cmd_vel_publisher_1 = self.create_publisher(
                                    LaserScan,
                                    "lrange",
                                    qos_profile)  
        # the number `10` you are trying to pass seems to represent the depth, but since you are already specifying it in the `qos_profile`, it's unnecessary and will result in a syntax error.
        self.cmd_vel_publisher_2 = self.create_publisher(
                                    LaserScan,
                                    "rrange",
                                    qos_profile)  


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

        self.br = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_transform_timer_cb)
    
    def broadcast_transform_timer_cb(self):
           t1 = TransformStamped()
           t1.header.stamp = self.get_clock().now().to_msg()
           t1.header.frame_id = 'base_link'
           t1.child_frame_id = 'sensor1_frame'
           
           t1.transform.translation.x = 0.065  # ca. 6,5cm
           t1.transform.translation.y = -0.065
           t1.transform.translation.z = 0.04   # ca. 4cm
           winkel_deg = 10 # Grad
           winkel_rad = winkel_deg /180.0 * math.pi
           q = tf_transformations.quaternion_from_euler(0, 0, winkel_rad)  # Roll, pitch, yaw
           t1.transform.rotation.x = q[0]
           t1.transform.rotation.y = q[1]
           t1.transform.rotation.z = q[2]
           t1.transform.rotation.w = q[3]
           self.br.sendTransform(t1)
           print("sending transform sensor1_frame => base_link")

           t2 = TransformStamped()
           t2.header.stamp = self.get_clock().now().to_msg()
           t2.header.frame_id = 'base_link'
           t2.child_frame_id = 'sensor2_frame'
           
           t2.transform.translation.x = 0.065  # ca. 6,5cm
           t2.transform.translation.y = 0.065
           t2.transform.translation.z = 0.04   # ca. 4cm
           winkel_deg = -10 # Grad
           winkel_rad = winkel_deg /180.0 * math.pi
           q = tf_transformations.quaternion_from_euler(0, 0, winkel_rad)  # Roll, pitch, yaw
           t2.transform.rotation.x = q[0]
           t2.transform.rotation.y = q[1]
           t2.transform.rotation.z = q[2]
           t2.transform.rotation.w = q[3]
           self.br.sendTransform(t2)
           print("sending transform sensor2_frame => base_link")


    def listener_callback1(self, msg1):
        self.my_range1 = msg1.data/1000 # msg in mm, range in m
        self.get_logger().info(' Sensor1 gives Position in m "%f"' % self.my_range1)

    def listener_callback2(self, msg2):
        self.my_range2 = msg2.data/1000 # msg in mm, range in m
        self.get_logger().info(' Sensor2 gives Position in m "%f"' % self.my_range2)

    def publish_cmd(self):        
        msg1 = LaserScan()  # Leer msg instanzieren
        # ... und füllen
        # https://github.com/mikeferguson/ros2_cookbook/blob/main/rclpy/time.md
        t1 = self.get_clock().now()
        msg1.header.stamp = t1.to_msg()
        msg1.header.frame_id = "sensor1_frame" #"base_link"
        msg1.angle_min = -0.04 # start angle of the scan [rad] 
        msg1.angle_max =  0.04 # start angle of the scan [rad]  
        msg1.angle_increment = 0.02 # angular distance between measurements [rad]
        msg1.time_increment = 0.001 # time between measurements [seconds] - if your scanner
                           # # is moving, this will be used in interpolating position
                           # # of 3d points
        msg1.scan_time = 0.0 # time between scans [seconds]
        msg1.range_min = 0.02 # minimum range value [m]
        msg1.range_max = 2.0   # maximum range value [m]
        msg1.ranges = [self.my_range1, self.my_range1, self.my_range1, self.my_range1, self.my_range1  ] # range data [m]
        # # (Note: values < range_min or > range_max should be discarded)
        msg1.intensities = [] # intensity data [device-specific units]. If your
        # # device does not provide intensities, please leave
        # # the array empty.
        self.cmd_vel_publisher_1.publish(msg1)  # ..senden

        t2 = self.get_clock().now()
        msg2 = LaserScan()  # Leer msg instanzieren
        msg2.header.stamp = t2.to_msg()
        msg2.header.frame_id = "sensor2_frame" #"base_link"
        msg2.angle_min = -0.04 # start angle of the scan [rad] 
        msg2.angle_max =  0.02 # start angle of the scan [rad]  
        msg2.angle_increment = 0.02 # angular distance between measurements [rad]
        msg2.time_increment = 0.001 # time between measurements [seconds] - if your scanner
                           # # is moving, this will be used in interpolating position
                           # # of 3d points
        msg2.scan_time = 0.0 # time between scans [seconds]
        msg2.range_min = 0.02 # minimum range value [m]
        msg2.range_max = 2.0   # maximum range value [m]
        msg2.ranges = [self.my_range2, self.my_range2, self.my_range2, self.my_range2, self.my_range2  ] # range data [m]
        # # (Note: values < range_min or > range_max should be discarded)
        msg2.intensities = [] # intensity data [device-specific units]. If your
        # # device does not provide intensities, please leave
        # # the array empty.
        self.cmd_vel_publisher_2.publish(msg2)  # ..senden
        
def main(args=None):
    rclpy.init(args=args)
    node = micro_ROS_Node()  # Instanzierung
    # node2 = Tf2Broadcaster()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
