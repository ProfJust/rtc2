# rtc2
Ruhr Turtlebot Competition, TurtleBot3 mit ROS2 Humble

# installation
erstelle den Ordner `~/turtlebot3_ws/src`
* ` $ cd ~ ` 
* ` $ mkdir turtlebot3_ws `
* ` $ cd turtlebot3_ws`
* ` $ mkdir src`
* ` $ cd src`

clone rtc2 dorthin
  ` $ git clone https://github.com/ProfJust/rtc2`
  

mache step1....sh und step2....sh ausführbar
und führe sie aus

* $ cd ~/turtlebot3_ws/src
* $ ./step1...
* $ ./step2... 

# usage
build and run simple publisher "say_temp"

* cd turtlebot3_ws/
* colcon build --packages-select rtc2
* source install/setup.bash 
* ros2 run rtc2 say_temp 
