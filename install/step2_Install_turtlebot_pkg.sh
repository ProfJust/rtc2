mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
source ~/.bashrc


sudo apt install ros-humble-gazebo-* -y
sudo apt install ros-humble-cartographer -y
sudo apt install ros-humble-cartographer-ros -y
sudo apt install ros-humble-navigation2 -y
sudo apt install ros-humble-nav2-bringup -y
sudo apt install ros-humble-dynamixel-sdk -y
sudo apt install ros-humble-turtlebot3-msgs -y
sudo apt install ros-humble-turtlebot3 -y

cd ~/turtlebot3_ws/src/
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
cd ~/turtlebot3_ws && colcon build --symlink-install

echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc

# echo "export PYTHONPATH=${PYTHONPATH}:~/turtlebot3_ws/src/rtc2/rtc2_dist_packages" >> ~/.bashrc
source ~/.bashrc


