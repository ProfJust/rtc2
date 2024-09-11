# rtc2
Ruhr Turtlebot Competition, TurtleBot3 mit ROS2 Humble auf Ubuntu 22.04 - Jammy Jellyfish

## Voraussetzung
Ubuntu 22.04 ist installiert (als Dual Boot System, keine Virtual Box o.ä.) , 
Öffnen einer Shell mit STRG+ALT+T

# installation
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

# usage
build and run simple publisher "say_temp"

- $ cd turtlebot3_ws/
- $ colcon build --packages-select rtc2
- $ source install/setup.bash 
- $ ros2 run rtc2 say_temp 


Formatting: https://docs.github.com/de/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax


# usage important commands

nur das rtc2 - Paket übersetzen

`cd ~/turtlebot3_ws`
`colcon build --packages-select rtc2`
`source install/setup.bash`

ausführen

`ros2 run rtc2 talk`

