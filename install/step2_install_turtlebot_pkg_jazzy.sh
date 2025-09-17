source /opt/ros/jazzy/setup.bash
# mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src/
git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
sudo apt install python3-colcon-common-extensions
cd ~/turtlebot3_ws
colcon build --symlink-install
echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc

sudo apt install ros-jazzy-rqt-robot-steering
printf "wenn Plugin nicht zu in rqt zu sehen =>"
printf "ros2 run rqt_robot_steering rqt_robot_steering --force-discover"



printf " nur einmal: echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc "
printf "ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py