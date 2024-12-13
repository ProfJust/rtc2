Zu ändernde Files

/home/oju/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/urdf/turtlebot3_burger.urdf

und 
/home/oju/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf 


Gazebo-Spawnen nutzt model.sdf
[spawn_entity]: Loading entity XML from file /home/oju/turtlebot3_ws/install/turtlebot3_gazebo/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf

RViZ und ROS2 benötigt die Infos in turtlebot3_burger.urdf



Gazebo wortreich starten

ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py extra_gazebo_args:="--verbose"
