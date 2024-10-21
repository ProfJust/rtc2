# Version für das WS24
 printf " Installation der TurtleBot- Pakete,  Version für das WS24 " 

mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
source ~/.bashrc

# Installation via apt
sudo apt install ros-humble-gazebo-* -y
sudo apt install ros-humble-cartographer -y
sudo apt install ros-humble-cartographer-ros -y
sudo apt install ros-humble-navigation2 -y
sudo apt install ros-humble-nav2-bringup -y
sudo apt install ros-humble-rmw-cyclonedds-cpp -y
echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc

sudo apt install python3-transforms3d 
sudo apt install ros-humble-tf-transformations
# git clone -b humble https://github.com/ros-planning/navigation2.git -y

# sudo apt install ros-humble-nav2-bringup -y
# more recent from sourc
#sudo apt remove ros-humble-nav2-bringup -y
#cd ~/turtlebot3_ws/src/
#git clone -b humble https://github.com/ros-planning/navigation2.git -y

# sudo apt install ros-humble-dynamixel-sdk -y#
# more recent from sourc
#sudo apt remove ros-humble-dynamixel-sdk -y
#cd ~/turtlebot3_ws/src/
#git clone -b humble-devel https://github.com/ROBOTIS-GIT/DynamixelSDK.git -y

# sudo apt install ros-humble-turtlebot3-msgs -y
# more recent from sourc
#sudo apt remove ros-humble-turtlebot3-msgs -y
#cd ~/turtlebot3_ws/src/
#git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git -y

# sudo apt install ros-humble-turtlebot3 -y
# more recent from source
# sudo apt remove ros-humble-turtlebot3 -y

# more recent from source
# already has  robot_model_type: "nav2_amcl::DifferentialMotionModel"
 sudo apt remove ros-humble-turtlebot3-teleop  -y
 sudo apt remove ros-humble-turtlebot3-navigation -y
 sudo apt remove ros-humble-turtlebot3-description -y
 sudo apt remove ros-humble-turtlebot3-cartographer -y

cd ~/turtlebot3_ws/src/
# Robotis
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3.git -y
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git -y
sudo apt install ros-humble-turtlebot3-msgs -y

# git clone -b humble-devel https://github.com/ROBOTIS-GIT/DynamixelSDK.git -y

# ROS2 Humble => https://index.ros.org/search/?term=rclcpp
# git clone -b humble https://github.com/ros-planning/navigation2.git
# git clone -b humble https://github.com/ros2/rcl_interfaces.git
# git clone -b humble https://github.com/ros2/test_interface_files.git
# git clone -b humble https://github.com/ament/ament_cmake.git
# git clone -b humble https://github.com/ament/ament_package.git
# git clone -b humble https://github.com/ros2/common_interfaces.git
# git clone -b humble https://github.com/ros2/rosidl_defaults.git
# git clone -b humble https://github.com/ros2/urdf.git
# git clone -b humble https://github.com/ros2/ament_cmake_ros
# git clone -b humble https://github.com/ros2/rclcpp.git
# git clone -b humble https://github.com/ament/ament_lint.git
# git clone -b humble https://github.com/ros2/rosidl.git

# schon in den packages enthalten sind:
# git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_teleop.git
# git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_naviagtion.git
# git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_description.git
# git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_cartographer.git

cd ~/turtlebot3_ws && colcon build --symlink-install

 echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc
 echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc

# ROS_LOCALHOST_ONLY environment variable allows you to limit ROS 2 communication to localhost only.
# This means your ROS 2 system, and its topics, services, and actions will not be visible to other computers
# on the local network. Using ROS_LOCALHOST_ONLY is helpful in certain settings, 
# such as classrooms, where multiple robots may publish to the same topic causing strange behaviors. 
 echo 'export ROS_LOCALHOST_ONLY=0' >> ~/.bashrc
 echo '# this environment variable allows you to limit ROS 2 communication to localhost only.' >> ~/.bashrc

# echo "export PYTHONPATH=${PYTHONPATH}:~/turtlebot3_ws/src/rtc2/rtc2_dist_packages" >> ~/.bashrc
 source ~/.bashrc

 
 printf " Installation fuer RTC2 WS24 ist fertig, nicht vergessen zu kompilieren " 


