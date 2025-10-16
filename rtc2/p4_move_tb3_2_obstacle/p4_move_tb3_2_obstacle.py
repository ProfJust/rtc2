#!/usr/bin/env python3
#
#   move_tb3_2_obstacle.py
# -------------------------------------------
#   for rtc2
#   by oj, 16.10.25
#   Westfälische Hochschule - Campus Bocholt
# -------------------------------------------
# Bewegt den TurtleBot3 zu einem vorgegebenen Zielpunkt
# Stoppt, wenn ein Hindernis im Weg ist
# Nutzt Odometry Daten für die aktuelle Position
# Nutzt cmd_vel (TwistStamped) um den Roboter zu bewegen
# TurtleBot3 Burger im Gazebo Haus Szenario
# -------------------------------------------
# usage
# $1 rros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
# $2 ros2 run rtc2 p4_move_tb3_2_obstacle
# -------------------------------------------

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from turtlesim.msg import Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from math import pow, atan2, sqrt, isnan


class clTurtleBot(Node):  # erbt von Node

    def __init__(self):
        super().__init__("move_tb3_node")
        self.pose = Pose()  # aktuelle pose vom CB update_pose
        self.goal = Pose()  # das gewünschte Ziel, hier auch als Pose
        self.vel_msg = TwistStamped() # Instanziiere Message mit cmd_vel
        self.ranges = [0.1, 0.2, 0.3 ] # 
        # self.cmd_vel_publisher_ = self.create_publisher(
        #                             Twist,
        #                             '/cmd_vel',
        #                             10)
        # TwistStamped für TurtleBot3 ab Jazzy
        self.cmd_vel_publisher_ = self.create_publisher(
                                    TwistStamped,  
                                    '/cmd_vel',
                                    10)
        
        
        timer_period = 0.2  # 200 msec
        self.cmd_timer_ = self.create_timer(
                            timer_period,
                            self.timer_cb_move_turtle)
        
        self.subscription = self.create_subscription(
                              Odometry,
                              'odom',
                              self.update_odom,
                              10)
        # HIER CODE EINFÜGEN

    def update_odom(self, msg):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        # self.get_logger().info(f"Current x={msg.pose.pose.position.x} current y={msg.pose.pose.position.y} and current angle = {self.pose.theta}")
        self.pose.x = round(msg.pose.pose.position.x, 4)
        self.pose.y = round(msg.pose.pose.position.y, 4)
        # orientation als Quaternion
        ox = msg.pose.pose.orientation.x
        oy = msg.pose.pose.orientation.y
        oz = msg.pose.pose.orientation.z
        ow = msg.pose.pose.orientation.w
        self.pose.theta = self.quaternion_to_euler(ox, oy, oz, ow)
        # print(self.pose)

    def get_scan(self, scan):       
        self.ranges = 0 # HIER CODE EINFÜGEN
          

    def euclidean_distance(self, goal):
        x = goal.x - self.pose.x
        y = goal.y - self.pose.y
        d = sqrt(pow(x,2) + pow(y,2))
        return d

    def linear_vel(self, goal, constant=1.5, max_vel=0.3):
        vel = constant * self.euclidean_distance(goal)
        if vel > max_vel:
            vel = max_vel
        return vel

    def steering_angle(self, goal):
        return atan2(goal.y - self.pose.y, goal.x - self.pose.x)

    def angular_vel(self, goal, constant=6, max_vel=1.0):
        vel = constant * (self.steering_angle(goal) - self.pose.theta)
        # kann auch negativ
        if vel > max_vel:
            vel = max_vel
        if vel < -max_vel:
            vel = -max_vel
        return vel

    def get_user_input(self):
        # Get the input from the user. Must be float!! do not use int
        self.goal.x = float(input("Set your x goal:  (e.g. 2.0) "))
        self.goal.y = float(input("Set your y goal:  (e.g. 0.0) "))

        # print("Please, insert a number slightly greater than 0 (e.g. 0.01)")
        self.distance_tolerance = 0.05 # float(input("Set your tolerance: "))

    def timer_cb_move_turtle(self):   # wird durch Timer regelmäßig aufgerufen
        end_programm_flag = False
        if not self.obstacle_detected():
            if self.euclidean_distance(self.goal) >= self.distance_tolerance:
                print(" move robot ")
                # HIER CODE EINFÜGEN
                self.vel_msg.header.stamp = self.get_clock().now().to_msg()
                self.vel_msg.header.frame_id = "odom"
                self.vel_msg.twist.linear.x = self.linear_vel(self.goal)
                self.vel_msg.twist.angular.z = self.angular_vel(self.goal)
                # print(self.vel_msg)        
               # ########################
                self.get_logger().info(f"Current lin_vel_x= {self.vel_msg.twist.linear.x} ang_vel_z ={self.vel_msg.twist.angular.z}")
               
            else: 
                # Stopping our robot after the movement is over.
                print(" stop robot - end programm ")
                # HIER CODE EINFÜGEN
                self.vel_msg.header.stamp = self.get_clock().now().to_msg()
                self.vel_msg.header.frame_id = "odom"
                self.vel_msg.twist.linear.x = 0.0
                self.vel_msg.twist.angular.z = 0.0 

                # ########################
              
                end_programm_flag = True
        else:
            # Stopping our robot because an obstacle is in the way
            print(" stop robot - obstacle detected ") 
            # HIER CODE EINFÜGEN

            # ########################
                
            # end_programm_flag = True               

        self.cmd_vel_publisher_.publish(self.vel_msg)  # ..senden

        if end_programm_flag :
            print(" exit now ")
            exit()

    def quaternion_to_euler(self, x, y, z, w):
        # https://computergraphics.stackexchange.com/questions/8195/how-to-convert-euler-angles-to-quaternions-and-get-the-same-euler-angles-back-fr
        """t0 = 2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = atan2(t0, t1) # Drehung um X-Achse

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = asin(t2))  # Drehung um Y-Achse"""

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = atan2(t3, t4)  # Drehung um Z-Achse in rad

        return yaw

    def obstacle_detected(self):
        STOP_DISTANCE = 0.3
        LIDAR_ERROR = 0.05
        SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR
        
        numbOfScans = len(self.ranges)
        #print("numbofscans")
        #print(numbOfScans)
        # Laserscan empfangen?
        if numbOfScans <= 3:  # 3 aus __Init__
            return False
        
        min_distance = min(self.ranges)
        if min_distance < SAFE_STOP_DISTANCE:
            self.get_logger().info(" Obstacle detected ")
            return True
        else:
            self.get_logger().info(" No Obstacle detected ")
            return False
        

def main(args=None):
    rclpy.init(args=args)    
    node = clTurtleBot()
    print("Gazebo starten")
    node.get_user_input() 
    
    while True:
        try:
            rclpy.spin(node)
        except:
            break
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()