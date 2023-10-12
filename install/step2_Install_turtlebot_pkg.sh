mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
source ~/.bashrc
#c olcon build --symlink-install --parallel-workers 1

sudo apt install ros-humble-gazebo-* -y
sudo apt install ros-humble-cartographer -y
sudo apt install ros-humble-cartographer-ros -y
sudo apt install ros-humble-navigation2 -y
sudo apt install ros-humble-nav2-bringup -y

source ~/.bashrc

sudo apt install ros-humble-dynamixel-sdk -y
sudo apt install ros-humble-turtlebot3-msgs -y
sudo apt install ros-humble-turtlebot3 -y

echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc
source ~/.bashrc
