 source /opt/ros/humble/setup.bash
   99  git clone https://github.com/ProfJust/rtc2.git
  100  cd rtc2/
  101  ./step1_Install_ROS2_Hawskbill.sh 
  102  source /opt/ros/humble/setup.bash
  103  gedit ~/.bashrc
  104  ros2 pkg create --build-type ament python rtc2
  105  ros2 pkg create --build-type ament_python rtc2
  106  ls
  107  ros2 run turtlesim turtlesim_node 
  108  git clone https://github.com/ProfJust/rtc2.git
  109  cd ..
  110  source install/setup.bash 
  111  ros2 run rtc2 say_hello 
  112  ros2 topic list
  113  ros2 topic echo /temperature 



101  ./step1_Install_ROS2_Hawskbill.sh 
  102  source /opt/ros/humble/setup.bash
  103  gedit ~/.bashrc
  104  ros2 pkg create --build-type ament python rtc2
  105  ros2 pkg create --build-type ament_python rtc2
  106  ls
  107  ros2 run turtlesim turtlesim_node 
  108  git clone https://github.com/ProfJust/rtc2.git
  109  cd ..
  110  source install/setup.bash 
  111  ros2 run rtc2 say_hello 
  112  ros2 topic list
  113  ros2 topic echo /temperature 
  114  colcon build --packages-select rtc2
  115  cd turtlebot3_ws/
  116  colcon build --packages-select rtc2
  117  source install/setup.bash 
  118  ros2 run rtc2 say_temp 
