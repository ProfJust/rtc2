# rtc2
Ruhr Turtlebot Competition, TurtleBot3 mit ROS2 Humble auf Ubuntu 22.04 - Jammy Jellyfish

![RTC-Logo klein](https://github.com/user-attachments/assets/d6a17f16-8c45-4dc8-b8c4-b778b112c7e3)

## Installation RTC2-Turtlebot3 - Paket
### Voraussetzung
Ubuntu 22.04 ist installiert (als Dual Boot System, keine Virtual Box o.ä.) , 

### Öffnen einer Shell mit STRG+ALT+T
erstelle den Ordner `~/turtlebot3_ws/src` mit folgende Shell-Befehlen => $
* ` $ cd ~ ` 
* ` $ mkdir turtlebot3_ws `
* ` $ cd turtlebot3_ws`
* ` $ mkdir src`
* ` $ cd src`

clone rtc2 dorthin
  ` $ git clone https://github.com/ProfJust/rtc2.git`
  
  Falls das git-Software-Paket noch nicht installiert ist, installieren Sie es mit
  ` $ sudo apt install git`
  

mache step1....sh und step2....sh ausführbar
und führe sie aus

* $ cd ~/turtlebot3_ws/src/rtc2/install
* $ ./step1...
* $ ./step2... 

### usage
build and run simple publisher "say_temp"

Mit Alias "build", definiert in der .bashrc
- $ build 
- $ ros2 run rtc2 say_temp

oder
- $ ros2 launch rtc2 turtlesim_launch.py

Unsere Gazebo-Umgebung starteb wir mit
- $ ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
  
  ![Screenshot from 2024-09-11 12-43-56](https://github.com/user-attachments/assets/207e0f12-7db6-4db3-9078-2dc2b160b19c)


Ohne Alias
- $ cd turtlebot3_ws/
- $ colcon build --packages-select rtc2
- $ source install/setup.bash 
- $ ros2 run rtc2 say_temp 


Formatting: https://docs.github.com/de/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
