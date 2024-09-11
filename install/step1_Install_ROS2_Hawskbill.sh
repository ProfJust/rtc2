# bisher from http://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Development-Setup.html
# doppelte Packete im turtlebot3_ws/src Ordner
# =>
# am 25.10.23 geändert
# https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings

# ensure that the Ubuntu Universe repository is enabled
sudo apt install software-properties-common
sudo add-apt-repository universe

# add the ROS 2 GPG key with apt.
sudo apt update 
sudo apt upgrade
sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

#add the repository to your sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 packages
sudo apt update 
sudo apt upgrade
sudo apt install ros-humble-desktop
sudo apt install ros-humble-ros-base
sudo apt install ros-dev-tools
# für die Praktika
sudo apt install ros-humble-turtlesim

# Environment setup
# Replace ".bash" with your shell if you're not using bash
# Possible values are: setup.bash, setup.sh, setup.zsh

mkdir -p ~/turtlebot3_ws/src
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
echo 'source ~/turtlebot3_ws/install/local_setup.bash' >> ~/.bashrc
echo 'alias build="cd ~/turtlebot3_ws; colcon build --mixin release;  source ~/turtlebot3_ws/install/local_setup.bash"' >> ~/.bashrc


# Install development tools and ROS tools
sudo apt update && sudo apt install -y \
  python3-flake8-docstrings \
  python3-pip \
  python3-pytest-cov
  
sudo apt install -y \
   python3-flake8-blind-except \
   python3-flake8-builtins \
   python3-flake8-class-newline \
   python3-flake8-comprehensions \
   python3-flake8-deprecated \
   python3-flake8-import-order \
   python3-flake8-quotes \
   python3-pytest-repeat \
   python3-pytest-rerunfailures

  pip install -U setuptools
   
# mkdir -p ~/turtlebot3_ws/src
# cd ~/turtlebot3_ws

#  ?????????????????? wo kommt das her?
# vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos src

sudo apt upgrade
sudo rosdep init
rosdep update

# rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers"

source ~/.bashrc
cd ~/turtlebot3_ws/
colcon build --symlink-install
# wenn schwacher PC nur mit 1 Kern kompilieren =>
# colcon build --symlink-install --parallel-workers 1
# source ~/turtlebot3_ws/install/local_setup.bash
source ~/turtlebot3_ws/install/setup.bash
