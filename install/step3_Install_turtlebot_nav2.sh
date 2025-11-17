# Version für das WS25
 printf " Installation der TurtleBot-Navigations-Pakete,  Version ab WS25 " 


sudo apt install ros-jazzy-cartographer -y
sudo apt install ros-jazzy-cartographer-ros -y
sudo apt install ros-jazzy-nav2-map-server -y


# cyclone DDS installieren (workaround not needed anymore)
# sudo apt install ros-jazzy-rmw-cyclonedds-cpp -y
# ---> bashrc Eintrag
# echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc

sudo apt install python3-transforms3d 
sudo apt install ros-jazzy-tf-transformations

#sudo apt install ros-jazzy-navigation2 -y
# Besser: die aktuellen Sources aus dem GitHub
cd ~/turtlebot3_ws/src
git clone -b jazzy https://github.com/ros-planning/navigation2.git -y

# sudo apt install ros-jazzy-nav2-bringup -y
# more recent from sourc
cd ~/turtlebot3_ws/src/
git clone -b jazzy https://github.com/ros-planning/navigation2.git -y

# sudo apt install ros-jazzy-dynamixel-sdk -y#
# more recent from sourc

cd ~/turtlebot3_ws/src/
git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/DynamixelSDK.git -y

# sudo apt install ros-jazzy-turtlebot3-msgs -y
# more recent from sourc
sudo apt remove ros-jazzy-turtlebot3-msgs -y
cd ~/turtlebot3_ws/src/
git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git -y

# sudo apt install ros-jazzy-turtlebot3 -y
# more recent from source
sudo apt remove ros-jazzy-turtlebot3 -y
cd ~/turtlebot3_ws/src/
# Robotis
git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3.git -y
git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git -y
sudo apt install ros-jazzy-turtlebot3-msgs -y


# ROS2 jazzy => https://index.ros.org/search/?term=rclcpp
# git clone -b jazzy https://github.com/ros-planning/navigation2.git
# git clone -b jazzy https://github.com/ros2/rcl_interfaces.git
# git clone -b jazzy https://github.com/ros2/test_interface_files.git
# git clone -b jazzy https://github.com/ament/ament_cmake.git
# git clone -b jazzy https://github.com/ament/ament_package.git
# git clone -b jazzy https://github.com/ros2/common_interfaces.git
# git clone -b jazzy https://github.com/ros2/rosidl_defaults.git
# git clone -b jazzy https://github.com/ros2/urdf.git
# git clone -b jazzy https://github.com/ros2/ament_cmake_ros
# git clone -b jazzy https://github.com/ros2/rclcpp.git
# git clone -b jazzy https://github.com/ament/ament_lint.git
# git clone -b jazzy https://github.com/ros2/rosidl.git

# schon in den packages enthalten sind:
# git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3_teleop.git
# git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3_naviagtion.git
# git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3_description.git
# git clone -b jazzy-devel https://github.com/ROBOTIS-GIT/turtlebot3_cartographer.git

echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc

 
 printf " Installation der Navigation fuer RTC2 WS24 ist fertig \n"
 printf "Kompilieren nicht vergessen \n  cd ~/turtlebot3_ws  &&  colcon build --symlink-install"
 printf " ...und sourcen   source ~/turtlebot3_ws/install/setup.bash \n"
 printf "$1 ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py "
 printf "$2 ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/turtlebot3_ws/src/rtc2/maps/map.yaml"
 printf "Als erstes in Gazebo ein Pose Estimate durchführen!"

 printf " Qt und PyQt installieren "
 # Fehlermeldungen in VSCode Terminal 
 sudo apt install qtwayland5
 unset GTK_PATH
 sudo apt install libcanberra-gtk-module






