import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class clTurtleBot(Node):  # erbt von Node

    def __init__(self):
        super().__init__("move_turtlesim_node")
        self.pose = Pose()  # aktuelle pose vom CB update_pose
        self.goal = Pose()  # das gewünschte Ziel, hier auch als Pose
        self.vel_msg = Twist() # Instanziiere Message mit cmd_vel

        self.cmd_vel_publisher_ = self.create_publisher(
                                    Twist,
                                    "/turtle1/cmd_vel",
                                    10)
        
        timer_period = 0.2  # 200 msec
        self.cmd_timer_ = self.create_timer(
                            timer_period,
                            self.timer_cb_move_turtle)
        
        self.subscription = self.create_subscription(
                              Pose,
                              '/turtle1/pose',
                              self.update_pose,
                              10)
        self.subscription  # prevent unused variable warning

    def update_pose(self, msg):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        # self.get_logger().info(f"Current x={msg.x} current y={msg.y} and current angle = {msg.theta}")
        self.pose = msg
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal):
        x = goal.x - self.pose.x
        y = goal.y - self.pose.y
        d = sqrt(pow(x,2) + pow(y,2))
        return d

    def linear_vel(self, goal, constant=1.5):
        return constant * self.euclidean_distance(goal)

    def steering_angle(self, goal):
        return atan2(goal.y - self.pose.y, goal.x - self.pose.x)

    def angular_vel(self, goal, constant=6):
        return constant * (self.steering_angle(goal) - self.pose.theta)

    def get_user_input(self):
        # Get the input from the user. Must be float!! do not use int
        self.goal.x = float(input("Set your x goal: "))
        self.goal.y = float(input("Set your y goal: "))

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        print("Please, insert a number slightly greater than 0 (e.g. 0.01)")
        self.distance_tolerance = float(input("Set your tolerance: "))

    def timer_cb_move_turtle(self):   # wird durch Timer regelmäßig aufgerufen
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
            exit()
           
        self.cmd_vel_publisher_.publish(self.vel_msg)  # ..senden
