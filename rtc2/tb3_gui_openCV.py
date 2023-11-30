#!/usr/bin/env python3
# edited WHS, KK+KZ , 07.02.2023
# now with Tabs and more options
# usage
# $rosrun robocop_ros robocop_gui.py

from PyQt5.QtWidgets import (QWidget, QApplication,
                             QPushButton, QComboBox,
                             QGridLayout, QLabel,
                             QTabWidget, QLineEdit,
                             QSlider, QFileDialog,
                             QDialog)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import *
import sys
import os
import subprocess
import socket
import cv2 as cv
import shutil


class MainWindow(QTabWidget):
    myFilePath = os.path.dirname(os.path.abspath(__file__))
    basedir='/home/robotik-l2/catkin_ws/src/robocop_ros'
    filepath = ''

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # https://www.tutorialspoint.com/pyqt/pyqt_qtabwidget.htm
        self.tab0 = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.addTab(self.tab0, "Tab 1")
        self.addTab(self.tab1, "Tab 2")
        self.addTab(self.tab2, "Tab 3")
        self.addTab(self.tab3, "Tab 4")
        self.tab0UI()
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        # --- Window konfigurieren und starten
        self.setWindowTitle('RTC23 - Starthilfe ')
        pixPath = os.path.join(self.myFilePath, "Pic/rtc_logo_600px.png")
        self.setWindowIcon(QIcon(pixPath))

    def tab0UI(self):  # --- Logo ----
        # --- roscore ---
        self.myPb_roscore = QPushButton(self)
        self.myPb_roscore.setText(' starte ROS-Master ')
        self.myPb_roscore.clicked.connect(self.slot_roscore)
        # --- SSH ---
        self.Line_Edit_IP = QLineEdit("192.168.1.134")
        # --- Starte SSH Button ---
        self.myPb_ssh = QPushButton(self)
        self.myPb_ssh.setText('    SSH - Start    ')
        self.myPb_ssh.clicked.connect(self.slot_ssh)
        # --- IP-Adresse ---
        self.myPb_ip = QPushButton(self)
        self.myPb_ip.setText('get IP-Adress')
        self.myPb_ip.setMinimumWidth(200)
        self.myPb_ip.clicked.connect(self.get_ip_address)
        self.label_ip = QLineEdit("Deine IP-Adresse")
        # --- Edit Bashrc ---
        self.myPb_bash = QPushButton(self)
        self.myPb_bash.setText('  edit Bashrc  ')
        self.myPb_bash.clicked.connect(self.open_bashrc)
        # --- select-Wifi  ---
        self.wifi_combo = QComboBox()
        self.wifi_combo.addItems(self.get_wifiname())
        self.myPb_wifi = QPushButton(self)
        self.myPb_wifi.setText(' Connect ')
        self.myPb_wifi.clicked.connect(self.connect_wifi)

        # --- Grid Layout ---
        gbox = QGridLayout()
        # --- 1. Line ---
        gbox.addWidget(self.myPb_roscore, 0, 0, 1, 2)
        # --- 2. Line ---
        gbox.addWidget(self.Line_Edit_IP, 1, 0)
        gbox.addWidget(self.myPb_ssh, 1, 1)
        # --- 3. Line ---
        gbox.addWidget(self.label_ip, 2, 0)
        gbox.addWidget(self.myPb_ip, 2, 1)
        # --- 4. Line ---
        gbox.addWidget(self.myPb_bash, 3, 1)

        gbox.addWidget(self.wifi_combo, 5, 0)
        gbox.addWidget(self.myPb_wifi, 5, 1)
        # --- Tab Line ---
        self.setTabText(0, "Start")
        self.tab0.setLayout(gbox)

    def tab1UI(self):  # --- Karte erstellen --
        # --- Empty-Gazebo  ---
        self.gaz_options = ('Empty-Gazebo_World', 'Gazebo_House')
        self.gaz_combo = QComboBox()
        self.gaz_combo.addItems(self.gaz_options)
        self.myPb_gzb = QPushButton(self)
        self.myPb_gzb.setText(' Launch ')
        self.myPb_gzb.clicked.connect(self.launchGazebo)
        # --- Starte RViz ---
        self.myPb_rviz = QPushButton(self)
        self.myPb_rviz.setText(' RViz Gazebo ')
        self.myPb_rviz.clicked.connect(self.slot_rviz)
        # --- Starte Mapping ---
        self.myPb_gmap = QPushButton(self)
        self.myPb_gmap.setText(' Gmapping ')
        self.myPb_gmap.clicked.connect(self.slot_gmapping)
        # --- Teleop Start Button ---
        self.myPb_teleop = QPushButton(self)
        self.myPb_teleop.setText(' Teleop Controller ')
        self.myPb_teleop.clicked.connect(self.slot_teleop)
        # --- Name Map ---
        self.Line_Edit_Map = QLineEdit("myMap")
        self.label_Map = QLabel("Name der Map")
        self.label_Map.setFixedHeight(26)
        # --- Map Saver Button ---
        self.myPb_map_save = QPushButton(self)
        self.myPb_map_save.setText('Save Map')
        self.myPb_map_save.clicked.connect(self.slot_save_map)

        # --- Grid Layout ---
        gbox = QGridLayout()
        # --- 1. Line ---
        gbox.addWidget(self.gaz_combo, 0, 0)
        gbox.addWidget(self.myPb_gzb, 0, 1)
        # --- 2. Line ---
        gbox.addWidget(self.myPb_rviz, 1, 0, 1, 2)
        # --- 3. Line ---
        gbox.addWidget(self.myPb_gmap, 2, 0, 1, 2)
        # --- 4. Line ---
        gbox.addWidget(self.myPb_teleop, 3, 0, 1, 2)
        # --- 5. Line ---
        gbox.addWidget(self.Line_Edit_Map, 4, 0, 1, 2)
        # --- 6. Line ---
        gbox.addWidget(self.label_Map, 5, 0, 1, 2)
        # --- 7. Line ---
        gbox.addWidget(self.myPb_map_save, 6, 0, 1, 2)
        # --- Tab Line ---
        self.setTabText(1, "Karte")
        self.tab1.setLayout(gbox)

    def tab2UI(self):  # --- Opencv Karte Optimieren ----
        # ---- Kernel einstellen ----
        self.lKsCav = QLabel("Kernel Size for Cavitation", self)
        self.tKsCav = QSlider(Qt.Horizontal)
        self.tKsCav = QSlider(Qt.Horizontal)
        self.tKsCav.setMinimum(1)
        self.tKsCav.setMaximum(10)
        self.tKsCav.setValue(2)
        self.tKsCav.setTickPosition(QSlider.TicksBelow)
        self.tKsCav.setTickInterval(1)
        self.lKsCav2 = QLabel("1-10", self)
        # --- Dilation ---
        self.lKsDel = QLabel("Kernel Size for Dilation", self)
        self.tKsDel = QSlider(Qt.Horizontal)
        self.tKsDel = QSlider(Qt.Horizontal)
        self.tKsDel.setMinimum(1)
        self.tKsDel.setMaximum(10)
        self.tKsDel.setValue(2)
        self.tKsDel.setTickPosition(QSlider.TicksBelow)
        self.tKsDel.setTickInterval(1)
        self.lKsDel2 = QLabel("1-10", self)
        # --- Approximieren ---
        self.lAprox = QLabel("1/10 Prozent Aproximation", self)
        self.tAprox = QSlider(Qt.Horizontal)
        self.tAprox = QSlider(Qt.Horizontal)
        self.tAprox.setMinimum(1)
        self.tAprox.setMaximum(20)
        self.tAprox.setValue(3)
        self.tAprox.setTickPosition(QSlider.TicksBelow)
        self.tAprox.setTickInterval(1)
        self.lAprox2 = QLabel("1-20", self)
        # --- Map name ---
        self.l_Mapname = QLabel("MyMap", self)
        self.myPb_Mapname = QPushButton("Get Map File", self)
        self.myPb_Mapname.clicked.connect(
            lambda: self.FileDialog(self.basedir, True, 'pgm', False))
        self.myPb_Mapname.clicked.connect(
            lambda: self.l_Mapname.setText(QFileInfo(self.filepath).baseName()))
        # --- Enhance ---
        self.bEnhance = QPushButton("Enhance", self)
        self.bEnhance.clicked.connect(lambda: self.enhance(self.filepath))
        # --- Save Map ---
        self.myPb_savemap = QPushButton("Save New Map", self)
        self.myPb_savemap.clicked.connect(lambda: self.saveMap((self.filepath)))

        gridL = QGridLayout()
        # --- 1. Line ---
        gridL.addWidget(self.lKsCav, 0, 0)
        gridL.addWidget(self.tKsCav, 0, 1)
        gridL.addWidget(self.lKsCav2, 0, 2)
        # --- 2. Line ---
        gridL.addWidget(self.lKsDel, 1, 0)
        gridL.addWidget(self.tKsDel, 1, 1)
        gridL.addWidget(self.lKsDel2, 1, 2)
        # --- 3. Line ---
        gridL.addWidget(self.lAprox, 2, 0)
        gridL.addWidget(self.tAprox, 2, 1)
        gridL.addWidget(self.lAprox2, 2, 2)
        # --- 4. Line ---
        gridL.addWidget(self.l_Mapname, 3, 0)
        gridL.addWidget(self.myPb_Mapname, 3, 1)
        # --- 5. Line ---
        gridL.addWidget(self.bEnhance, 4, 0)
        gridL.addWidget(self.myPb_savemap, 4, 1)
        # --- Tab Line ---
        self.setTabText(2, "Optimieren")
        self.tab2.setLayout(gridL)

    def tab3UI(self):
        # --- Map name ---
        self.l_mapnav = QLabel("MyMap", self)
        self.myPb_getfile = QPushButton("Get Map File", self)
        self.myPb_getfile.clicked.connect(
            lambda: self.FileDialog(self.basedir, True, 'yaml', False))
        self.myPb_getfile.clicked.connect(
            lambda: self.l_mapnav.setText(QFileInfo(self.filepath).baseName()))
        # --- Navigation Start Button ---
        self.myPb_navigate = QPushButton(self)
        self.myPb_navigate.setText('Navigate to RViz Goal')
        self.myPb_navigate.clicked.connect(lambda: self.slot_navigate_to_goal(self.filepath))
        # --- TOF laser links rechts  ---
        self.myPb_laser = QPushButton(self)
        self.myPb_laser.setText(' Launch VL53 scan ')
        self.myPb_laser.clicked.connect(self.slot_laser)
        # --- Clear Costmao  ---
        self.myPb_clear = QPushButton(self)
        self.myPb_clear.setText(' Clear Costmap ')
        self.myPb_clear.clicked.connect(self.slot_clear)
        # --- Client ---
        self.myPb_client = QPushButton(self)
        self.myPb_client.setText(' Publish Pose 2 file')
        self.myPb_client.clicked.connect(self.slot_action_client)
        # --- Start Action Server Script ---
        self.myPb_action = QPushButton(self)
        self.myPb_action.setText('Move 2 Multigoal')
        self.myPb_action.clicked.connect(self.slot_action_server)
        # --- RTC Logo ---
        self.label_pic = QLabel('RTCLogo')
        pixPath = os.path.join(self.myFilePath, "Pic/rtc_logo_600px.png")
        self.pixmap = QPixmap(pixPath)
        self.label_pic.setPixmap(self.pixmap)

        # --- Grid Layout ---
        gbox = QGridLayout()
        # --- 1. Line ---
        gbox.addWidget(self.l_mapnav, 1, 0)
        gbox.addWidget(self.myPb_getfile, 1, 1)
        # --- 2. Line ---
        gbox.addWidget(self.myPb_navigate, 2, 0, 1, 2)
        # --- 3. Line ---
        gbox.addWidget(self.myPb_laser, 3, 0)
        gbox.addWidget(self.myPb_clear, 3, 1)
        # --- 4. Line ---
        gbox.addWidget(self.myPb_client, 4, 0)
        gbox.addWidget(self.myPb_action, 4, 1)
        # --- 5. Line ---
        gbox.addWidget(self.label_pic, 5, 0, 1, 2)
        # --- Tab Line ---
        self.setTabText(3, "Navigieren")
        self.tab3.setLayout(gbox)

    # --- Die  Slot-Methoden ---

    def slot_roscore(self):
        os.system('gnome-terminal --tab -- /bin/bash -c\
                  "roscore; exec bash"')

    def launchGazebo(self):
        option = self.gaz_options.index(self.gaz_combo.currentText())
        newPath = os.path.join(self.myFilePath, "Bash/gazebo.sh")
        if option == 0:
            subprocess.call([newPath, '-e'])
        elif option == 1:
            subprocess.call([newPath, '-h'])
        else:
            print('Got Nothing')

    def slot_rviz(self):
         os.system('gnome-terminal --tab -- /bin/bash -c\
                  "roslaunch --wait turtlebot3_gazebo \
                  turtlebot3_gazebo_rviz.launch;\
                  exec bash"')

    def slot_gmapping(self):
        os.system('gnome-terminal --tab -- /bin/bash -c\
                  "roslaunch --wait robocop_ros\
                  turtlebot3_slam.launch slam_methods:=gmapping;\
                  exec bash"')

    def slot_action_server(self):
        os.system('gnome-terminal --tab -- /bin/bash -c\
                  "rosrun robocop_ros\
                  multiple_goal.py;\
                  exec bash"')

    def slot_action_client(self):
        os.system('gnome-terminal --tab -- /bin/bash -c\
                  "rosrun robocop_ros\
                  publish_point_2_file.py;\
                  exec bash"')

    def slot_ssh(self):
        ip_str = str(self.Line_Edit_IP.text())
        newPath = os.path.join(self.myFilePath, "Bash/ssh.sh")
        subprocess.call([newPath, ip_str])

    def slot_save_map(self):
        map_str = str(self.Line_Edit_Map.text())
        newPath = os.path.join(self.myFilePath, "Bash/map_save.sh")
        subprocess.call([newPath, map_str])

    def slot_navigate_to_goal(self, map_str=''):
        if map_str == '':
            return
        newPath = os.path.join(self.myFilePath, "Bash/navigate.sh")
        subprocess.call([newPath, map_str])

    def slot_teleop(self):
        os.system('gnome-terminal --tab -- /bin/bash -c\
                  "roslaunch robocop_ros turtle_joy.launch;\
                  exec bash"')

    def slot_laser(self):
        os.system('gnome-terminal --tab -- /bin/bash -c\
                  "rosrun robocop_ros VL53_to_costmap.py;\
                  exec bash"')

    def get_ip_address(self):
        # eigene IP Adresse finden
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        r = s.getsockname()[0]
        self.label_ip.setText(r)

    def open_bashrc(self):
        # Direktes editiern der Bashrc
        os.system('gnome-terminal --tab -- /bin/bash -c\
                  "gedit ~/.bashrc; exit; exec bash"')

    def slot_clear(self):
        os.system('gnome-terminal --tab -- /bin/bash -c\
                   "rosservice call /move_base/clear_costmaps;\
                    exit; exec bash"')

    def get_wifiname(self):
        # Bekannte Netzwerke finden
        result = os.popen("nmcli -t -f NAME c show").read().splitlines(True)
        list_wifi = []
        for element in result:
            list_wifi.append(element.strip())
        return (list_wifi)

    def connect_wifi(self):
        # Wechseln der bekannten Internetverbindungen
        option = self.wifi_combo.currentText()
        option2 = os.popen(
            'nmcli -t -f NAME c show --active').read().replace('\n', '')
        newPath = os.path.join(self.myFilePath, "Bash/connect_wifi.sh")
        subprocess.call([newPath, option, option2])

    def enhance(self, map_str=''):
        # Function inspired by image processing found in:
        # Howes, J., Minichino, J. (2020). Learning OpenCV 4 Computer Vision with Python 3.
        # Third Edition, Packt Publishing Ltd., Birmingham.
        if map_str == '':
            return
        image = cv.imread(map_str, cv.IMREAD_GRAYSCALE)
        img = image.copy()
        # Displaying the result
        cv.namedWindow("Original")
        cv.imshow("Original", img)
        # Coversion to grayscale, inversion, edge detection
        gray = cv.bitwise_not(img)
        edges = cv.Canny(gray, 50, 200)
        # Find the contours. The first two largest contours are for the outer contour
        # So, taking the rest of the contours for inner contours
        cnts = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[2:]
        # Filling the inner contours with black color
        for c in cnts:
            epsilon = self.tAprox.value()/1000 * cv.arcLength(c, False)
            approx = cv.approxPolyDP(c, epsilon, False)
            cv.drawContours(img, [approx], -1, (0, 0, 0), -1)
        # Displaying the result
        cv.namedWindow("Contour", cv.WINDOW_NORMAL)
        cv.imshow("Contour", img)

        kernelCav = cv.getStructuringElement(
            cv.MORPH_RECT, (int(self.tKsCav.value()), int(self.tKsCav.value())))
        cavPic = cv.erode(img, kernelCav)

        kernelDel = cv.getStructuringElement(
            cv.MORPH_RECT, (int(self.tKsDel.value()), int(self.tKsDel.value())))
        delPic = cv.dilate(cavPic, kernelDel)
        self.image = delPic.copy()
        # Displaying the result
        cv.namedWindow("After Dilate", cv.WINDOW_NORMAL)
        cv.imshow("After Dilate", delPic)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def saveMap(self, map_str=''):
        #basedir=os.path.commonpath([self.myFilePath,map_str])
        basedir=os.path.join(self.basedir,'maps')
        # /home/robotik-l2/catkin_ws/src/robocop_ros/maps
        old_name = map_str
        # Separate base from extension
        base, extension = os.path.splitext(old_name)
        # Initial new name
        new_name = os.path.join(basedir, base)
        ii = 1
        while True:
            new_name = os.path.join(basedir,base, base + "_" + str(ii) + extension)
            if not os.path.exists(new_name):
                shutil.copy(old_name, new_name)
                print("Copied", old_name, "as", new_name)
                break 
            ii += 1
        #os.remove(map_str) 
        # Saving the image
        print(str(map_str))
        cv.imwrite(str(map_str), self.image)

    def FileDialog(self, directory='', forOpen=True, fmt='', isFolder=False):
        options = QFileDialog.Options()
        # setzt andere Explorer
        # options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        dialog = QFileDialog(self)
        dialog.setOptions(options)
        dialog.setFilter(dialog.filter() | QDir.Hidden)

        # ARE WE TALKING ABOUT FILES OR FOLDERS
        if isFolder:
            dialog.setFileMode(QFileDialog.DirectoryOnly)
        else:
            dialog.setFileMode(QFileDialog.AnyFile)
        # OPENING OR SAVING
        dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(
            QFileDialog.AcceptSave)

        # SET FORMAT, IF SPECIFIED
        if fmt != '' and isFolder is False:
            dialog.setDefaultSuffix(fmt)
            dialog.setNameFilters([f'{fmt} (*.{fmt})'])

        # SET THE STARTING DIRECTORY
        if directory != '':
            dialog.setDirectory(str(directory))
        else:
            dialog.setDirectory('/home')

        if dialog.exec_() == QDialog.Accepted:
           self.filepath = dialog.selectedFiles()[0]  # returns a list
        else:
            self.filepath = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
