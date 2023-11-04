#!/usr/bin/env python3
#
#   qt_robot_steering.py
# -------------------------------------------
#   for rtc2
#   by oj, 4.11.23
#   Westfälische Hochschule - Campus Bocholt
# -------------------------------------------
# usage
# $1 ros2 launch turtlebot3_gazebo empty_world.launch.py
#
# -------------------------------------------
#  GUI for robot-steering
# https://github.com/tasada038/pyqt_ros2_app/blob/master/main_pyqt_ros2.py
# -------------------------------------------
import sys
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
# from math import pow, atan2, sqrt

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
 QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QLabel)
from PyQt5.QtCore import Qt, QTimer


class clTurtleBot(Node):  # erbt von Node
    # vel_msg = Twist() # Instanziiere Message mit cmd_vel
    def __init__(self):
        rclpy.init(args=None) 
        super().__init__("robot_steering_node")
        
        self.pose = Pose()  # aktuelle pose vom CB update_pose
        self.goal = Pose()  # das gewünschte Ziel, hier auch als Pose
        self.vel_msg = Twist() # Instanziiere Message mit cmd_vel

        self.cmd_vel_publisher = self.create_publisher(
                                    Twist,
                                    "/cmd_vel",
                                    10)
        
        timer_period = 0.2  # 200 msec
        self.cmd_timer = self.create_timer(
                            timer_period,
                            self.timer_cb_move_turtle)
        
        self.subscription = self.create_subscription(
                              Odometry,
                              'odom',
                              self.update_odom,
                              10)
        self.subscription  # prevent unused variable warning

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

    def timer_cb_move_turtle(self):   # wird durch Timer regelmäßig aufgerufen
        # Linear velocity in the x-axis.
        # print("Timer Callback")
        self.cmd_vel_publisher.publish(self.vel_msg)

    def move_turtle(self,x,z):
        self.vel_msg.linear.x = float(x)/10.0
        self.vel_msg.linear.y = 0.0 # must be float, don't use only 0
        self.vel_msg.linear.z = 0.0 # must be float, don't use only 0    
        self.vel_msg.angular.z = float(z)
        self.vel_msg.angular.x = 0.0
        self.vel_msg.angular.y = 0.0
        # self.cmd_vel_publisher.publish(self.vel_msg)  # ..senden
        print("vel_msg published", x, z)
      

tb3 = clTurtleBot()  # globale Definition

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  
        MainWindow.resize(self, 800, 400)
        self.initUI()
        self.show()  
        # create Qt timer
        self.qtimer = QTimer(self)   
        self.qtimer.timeout.connect(tb3.timer_cb_move_turtle)  

    def initUI(self):
        #Instanziierung der Widgets
        self.lcd = QLCDNumber(self)
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setMinimum(-10)
        self.sld.setMaximum(10)
        self.sld.setValue(0)
        pbLess = QPushButton('<')
        pbMore = QPushButton('>')
        pbGo = QPushButton(' Go Turtle ')
        self.lblStatus = QLabel('Statuszeile')

        #BOX-Layout mit Widgets füllen
        vbox = QVBoxLayout()
        #1.Reihe
        vbox.addWidget(self.lcd)
        #2.Reihe
        vbox.addWidget(self.sld)
        #3.Reihe
        hbox = QHBoxLayout()
        hbox.addWidget(pbLess)
        hbox.addWidget(pbMore)
        vbox.addLayout(hbox)
        #4.Reihe
        vbox.addWidget(pbGo)
        #Alle Boxen ins Window setzen
        self.setLayout(vbox)

        #Signal und Slot verbinden
        self.sld.valueChanged.connect(self.lcd.display)
        self.sld.valueChanged.connect(self.lcd.display)

        pbLess.clicked.connect(self.SlotKlick)
        pbMore.clicked.connect(self.SlotKlick)
        pbGo.clicked.connect(self.SlotGo)

        #Fenster Konfigurieren
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('RTC - PyQt - TurtleBot3 - Steering')
        self.show()

    def SlotKlick(self):
        sender = self.sender()
        self.lblStatus.setText(sender.text() + ' was pressed')   
        if sender.text()=='<':
            wert = self.sld.value()
            wert = wert-1
            self.sld.setValue(wert)  
        else:
            wert = self.sld.value()
            wert = wert+1
            self.sld.setValue(wert)
            
    def SlotGo(self):
        # Hier geht die Turtle ab 
        print("slotGo")   
        tb3.move_turtle(self.sld.value(), 0.0)
        self.qtimer.start(100)
        

def main():
    
    
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
