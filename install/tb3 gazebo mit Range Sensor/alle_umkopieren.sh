#!/bin/bash

echo "Kopiert die URDF und SDF Dateien für den TurtleBot3 - Burger mit Range Sensor an die richtigen Stellen"

echo " Gazebo - Model "
./umkopieren_model_sdf.sh

echo " URDF - Model "
./umkopieren_turtlebot3_burger_urdf.sh

echo " Gazebo - Bridge "
./umkopieren_turtlebot3_burger_bridge_yaml.sh

echo "Vorgang Alle Kopieren abgeschlossen."

