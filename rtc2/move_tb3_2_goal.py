#!/usr/bin/env python3
#
#   move_turtle_2_goal.py
# -------------------------------------------
#   for rtc2
#   by oj, 25.10.23
#   Westfälische Hochschule - Campus Bocholt
#   see also http://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal
# -------------------------------------------
# usage
# $1 ros2 run turtlesim turtlesim_node 
# $2 ros2 run rtc2 p4_tb3_move_2_goal
# ==> setup.py
# -------------------------------------------
# Let Turtle Move a given distance 
# (relative from start posotion)
# -------------------------------------------

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from math import pow, atan2, sqrt, isnan


class clTurtleBot(Node):  # erbt von Node

    def __init__(self):
        super().__init__("move_tb3_node")
        self.pose = Pose()  # aktuelle pose vom CB update_pose
        self.goal = Pose()  # das gewünschte Ziel, hier auch als Pose
        self.vel_msg = Twist() # Instanziiere Message mit cmd_vel
        self.ranges = [0.1, 0.2, 0.3 ] # 

        self.cmd_vel_publisher_ = self.create_publisher(
                                    Twist,
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
        self.subscription2 = self.create_subscription(
                              LaserScan,
                              'scan',
                              self.get_scan,
                              10)
        self.subscription  # prevent unused variable warning
        self.subscription2  # prevent unused variable warning

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
        # print("getscan")
        # https://github.com/ros2/rclpy/blob/rolling/rclpy/rclpy/wait_for_message.py
        # In ROS-Rolling gäbe es
        # scan = rclpy.wait_for_message('scan', LaserScan, 10)  # time_to_wait in sec
        #scan_filtered = [1.0, 1.0, 2.1, 1.3]
        # numbOfScans = len(scan.ranges) 
        # print("numbofscans")
        # print(numbOfScans)
        
        self.ranges = scan.ranges
        
        # nan (not a number) und inf (Infinity) durch Zahlen ersetzen
        #for i in range(self.ranges):
        #     if self.ranges[i] == float('Inf'):
        #         self.ranges[i] = 20
        #     elif isnan(self.ranges[i]):
        #         self.ranges[i] = 0

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
        self.goal.x = float(input("Set your x goal: "))
        self.goal.y = float(input("Set your y goal: "))

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        print("Please, insert a number slightly greater than 0 (e.g. 0.01)")
        self.distance_tolerance = float(input("Set your tolerance: "))

    def timer_cb_move_turtle(self):   # wird durch Timer regelmäßig aufgerufen
        end_programm_flag = False
        if not self.obstacle_detected():
            if self.euclidean_distance(self.goal) >= self.distance_tolerance:
                # Linear velocity in the x-axis.
                self.vel_msg.linear.x = self.linear_vel(self.goal)
                self.vel_msg.linear.y = 0.0 # must be float, don't use only 0
                self.vel_msg.linear.z = 0.0 # must be float, don't use only 0

                # Angular velocity in the z-axis.
                self.vel_msg.angular.x = 0.0 # must be float, don't use only 0
                self.vel_msg.angular.y = 0.0 # must be float, don't use only 0
                self.vel_msg.angular.z = self.angular_vel(self.goal)
                print(" move robot ")
                self.get_logger().info(f"Current lin_vel_x= {self.vel_msg.linear.x} ang_vel_z ={self.vel_msg.angular.z}")
            else: 
                # Stopping our robot after the movement is over.
                self.vel_msg.linear.x = 0.0 # must be float, don't use only 0
                self.vel_msg.angular.z = 0.0 # must be float, don't use only 0
                print(" stop robot - end programm ")
                end_programm_flag = True
        else:
            # Stopping our robot because an obstacle is in the way
                self.vel_msg.linear.x = 0.0 # must be float, don't use only 0
                self.vel_msg.linear.y = 0.0 # must be float, don't use only 0
                self.vel_msg.linear.z = 0.0 # must be float, don't use only 0
                self.vel_msg.angular.x = 0.0 # must be float, don't use only 0
                self.vel_msg.angular.y = 0.0 # must be float, don't use only 0
                self.vel_msg.angular.z = 0.0 # must be float, don't use only 0
                print(" stop robot - obstacle detected ") 
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
    node.get_user_input() # only at the beginning
    # this way => no statemachine needed
    
    while True:
        try:
            rclpy.spin(node)
        except:
            break
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()