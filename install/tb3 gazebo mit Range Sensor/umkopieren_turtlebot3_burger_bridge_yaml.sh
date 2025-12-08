#!/bin/bash
set -e

# Pfade definieren
HOME_DIR="$HOME"
# Originales File das wir ändern wollen
SRC_FILE="$HOME_DIR/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/params/turtlebot3_burger_bridge.yaml"
# Backup File des Originals
BACKUP_FILE="$HOME_DIR/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/params/turtlebot3_burger_bridge.yaml.bak"
# Neue Datei die wir anstelle des Originals einfügen wollen
NEW_FILE="$HOME_DIR/turtlebot3_ws/src/rtc2/install/tb3 gazebo mit Range Sensor/Jazzy Version with Gazebo Harmonic/turtlebot3_burger_bridge.yaml"
# Zielort der neuen Datei
TARGET_FILE="$HOME_DIR/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/params/turtlebot3_burger_bridge.yaml"

# 1. Existierende test.urdf umbenennen
if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$BACKUP_FILE"
    echo "Backup erstellt: $BACKUP_FILE"
else
    echo "WARNUNG: $SRC_FILE wurde nicht gefunden. Es wird kein Backup erstellt."
fi

# 2. Neue Datei kopieren und umbenennen
if [ -f "$NEW_FILE" ]; then
    cp "$NEW_FILE" "$TARGET_FILE"
    echo "Neue Datei kopiert nach: $TARGET_FILE"
else
    echo "FEHLER: $NEW_FILE wurde nicht gefunden!"
    exit 1
fi

echo "Vorgang abgeschlossen."

