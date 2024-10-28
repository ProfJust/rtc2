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


class MoveTurtlesimNode(Node):
    def __init__(self):
        super().__init__("move_turtlesim_dist_node")
        self.numbofmsg = 0
        self.pose = Pose() 
        self.state = 0
        self.cmd_vel_publisher_ = self.create_publisher(
                                    Twist,
                                    "turtle1/cmd_vel",
                                    10)
        timer_period = 0.2  # sec
        self.cmd_timer_ = self.create_timer(
                            timer_period,
                            self.timer_cb_move_distance)
        
        self.subscription = self.create_subscription(
                              Pose,
                              'turtle1/pose',
                              self.update_pose,
                              10)
        self.subscription  # prevent unused variable warning
        
    def update_pose(self, msg):  # called when msg is received
        self.numbofmsg +=1
        # Debug Ausgabe
        # self.get_logger().info(' Turtle is at Position x "%f"' % msg.x)
        # self.get_logger().info('                       y "%f"' % msg.y)
        # self.get_logger().info('                   theta "%f"' % msg.theta)
        
        # Pose global speichern
        self.pose.x = round(msg.x, 4)
        self.pose.y = round(msg.y, 4)
        self.pose.theta = round(msg.theta,  4)
    
    def get_user_input(self):
        #---- Get the input from the user ----
        print("\nGet user input")
        self.dist_x = eval(input("Set your x dist: "))
        self.dist_y = eval(input("Set your y dist: "))
        self.dist = sqrt(pow(self.dist_x, 2) + pow(self.dist_y, 2))
        self.sollTheta = atan2(self.dist_y, self.dist_x)
        self.get_logger().info(' OK, distance to go is "%f"' % self.dist)

    def get_start_pose(self):
        #---- Get start Position of Turtle - meanwhile received?
        print("\nGet start pose")
        self.start_x = self.pose.x
        self.start_y = self.pose.y
        self.get_logger().info(' Start Pose is x = "%s"' % self.start_x)
        self.get_logger().info('               y = "%s"' % self.start_y)
        self.get_logger().info(' Angle to turn to "%s" ' % self.sollTheta)
        self.get_logger().info(' Still to turn    "%s"\n'% abs(self.pose.theta - self.sollTheta))
        # input("press any key")

    def timer_cb_move_distance(self):  # wird durch Timer regelmäßig aufgerufen
        # self.get_logger().info('Timer CB:  state is "%s"' % self.state)
        vel_msg = Twist() # Instanziiere Message mit cmd_vel
        # ====== State Machine =======
        if self.state == 0:
            self.get_user_input()
            self.state = 1

        elif self.state == 1:
            self.get_start_pose()
            self.state = 2

        elif self.state == 2: 
            # --- Turtle zuerst drehen ---
            tolerance = 0.015     
            if (abs(self.pose.theta - self.sollTheta) > tolerance):
                # erlaubter theta Bereich [-pi...pi]
                if self.pose.theta > pi:
                    self.pose.theta = self.pose.theta - 2*pi
                elif self.pose.theta < -pi:
                    self.pose.theta = self.pose.theta +2 * pi
            
                # Angular velocity in the z-axis.
                if self.pose.theta - self.sollTheta > 0:
                    vel_msg.angular.z = -0.2
                else:
                    vel_msg.angular.z = 0.2
                
                self.get_logger().info(' Pose theta is "%s"' % self.pose.theta)
                self.get_logger().info(' Goal angle is "%s"' % self.sollTheta)
                self.get_logger().info(' Still to turn "%s"\n' % abs(self.pose.theta - self.sollTheta))       
            else:
                vel_msg.angular.z = 0.0  # stop turning  
                self.state = 3   

        elif self.state == 3:
            # --- Dann die Strecke fahren ---
            self.get_logger().info('Pose is x: "%s"' % self.pose.x)
            self.get_logger().info('        y: "%s"' % self.pose.y)

            dist_already = sqrt(pow((self.start_x - self.pose.x),2) + pow((self.start_y - self.pose.y),2))
            dist_to_go = abs(self.dist)
            still_togo = dist_to_go - dist_already
            self.get_logger().info('Still to Go "%s"\n' % still_togo)   
                
            if dist_already < dist_to_go:                
                vel_msg.linear.x = 0.2  # Linear velocity in the x-axis.         
            else:          
                #--- Stopping our robot after the movement is over.
                self.get_logger().info("Reached aim - now stopping ")
                vel_msg.linear.x = 0.0
                vel_msg.angular.z = 0.0
                self.cmd_vel_publisher_.publish(vel_msg)  # ..senden        
                exit() #Programm beenden     

        # Publishing our vel_msg
        self.cmd_vel_publisher_.publish(vel_msg)  # ..senden

        
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