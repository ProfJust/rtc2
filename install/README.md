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
