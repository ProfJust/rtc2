

# echo "$TURTLEBOT3_MODEL"
if [ "$TURTLEBOT3_MODEL" = "burger" ]; then
  echo "Das TURTLEBOT3_MODEL ist bereits als burger gesetzt. Pakete werden nicht erneut installiert."
else
  echo "TURTLEBOT3_MODEL ist nicht gesetzt oder nicht auf burger eingestellt. Pakete werden installiert."
  echo "$TURTLEBOT3_MODEL"
  #export TURTLEBOT3_MODEL="burger"
  export TURTLEBOT3_MODEL=burger 
  # kein Dauerhaftes setzen der Umgebungsvariable aus diesem Skript möglich 
  # => in die .bashrc schreiben und sourcen
  
  echo '# ------ ROS2 Jazzy Turtlebot3 Einstellungen -------' >> ~/.bashrc
  echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
  echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
  echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
  echo "TURTLEBOT3_MODEL wurde auf 'burger' gesetzt"
  echo 'export ROS_AUTOMATIC_DISCOVERY_RANGE=192.168.172.0/16' >> ~/.bashrc  
  echo '# Der Wert 192.168.0.0/16 ist eine CIDR-Notation und steht ' >> ~/.bashrc 
  echo '# für alle IP-Adressen von 192.168.0.0 bis 192.168.255.255. ' >> ~/.bashrc 
  echo "alias build='cd ~/turtlebot3_ws && colcon build --symlink-install  && source install/setup.bash'" >> ~/.bashrc 
  source /opt/ros/jazzy/setup.bash
    
  cd ~/turtlebot3_ws/src/
  git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
  git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
  git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
  git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
  sudo apt install python3-colcon-common-extensions -y
  sudo apt install ros-jazzy-ros-gz-bridge
  cd ~/turtlebot3_ws
  colcon build --symlink-install

  sudo apt install ros-jazzy-rqt-robot-steering -y
  ros2 run rqt_robot_steering rqt_robot_steering --force-discover
    
  printf "wenn Plugin nicht zu in rqt zu sehen =>"
  printf "\n ros2 run rqt_robot_steering rqt_robot_steering --force-discover "
  printf "\n Nach einem Neustart des Terminals bitte einmal ausführen: source ~/turtlebot3_ws/install/setup.bash "
  printf " nur einmal: echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc "
  printf "\n \n ####>>>>  source ~/.bashrc  in der Shell ausführen \n \n"
fi
