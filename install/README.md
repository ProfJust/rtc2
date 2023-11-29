# rtc2
Ruhr Turtlebot Competition mit ROS2

# installation
erstelle den Ordner  ~/turtlebot3_ws/src
  $ cd ~
  $ mkdir turtlebot3_ws
  $ cd turtlebot3_ws
  $ mkdir src
  $ cd src

clone rtc2 dorthin
  $ git clone https://github.com/ProfJust/rtc2
  

mache step1....sh und step2....sh ausführbar
und führe sie aus

$ cd ~/turtlebot3_ws/src
$ ./step1...
$ ./step2...

# usage
to be done



# nano ~/.bashrc

In der .bashrc muss folgendes stehen (realBot)
 => Gazebo mit mehreren Tln in einem Netz:  export ROS_LOCALHOST_ONLY=1  

export ROS_DOMAIN_ID=30 #TURTLEBOT3
export TURTLEBOT3_MODEL=burger
export ROS_LOCALHOST_ONLY=0  # 0 = Communication allowed
# this environment variable allows you to limit ROS 2 communication to localhost only.
source /opt/ros/humble/setup.bash
source ~/turtlebot3_ws/install/setup.bash



# install Raspicam Driver for ROS2 on TB3
sudo apt-get install ros-${ROS_DISTRO}-v4l2-camera
sudo nano /boot/firmware/config.txt
   => Set   camera_autodetect=0
sudo apt install v4l-utils
v4l2-ctl -D


sudo apt install v4l2loopback-dkms
sudo modprobe v4l2loopback

#usage
ubuntu@ubuntu:~$ ros2 run v4l2_camera v4l2_camera_node

=> Wrong Pixel Format use Param.file
