# =>
# 19.11.23 von OJ
# Enthält die Schritte aus
# https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup
# 

# Version für das WS24
printf " Installation von ROS2 unb der Treiber dem TurtleBot3, Version WS24 \n"

printf " Change Values  Update-Package-Lists to 0 and Unattended-Upgrade to 0"
sudo nano /etc/apt/apt.conf.d/20auto-upgrades

Input("Weiter?")

systemctl mask systemd-networkd-wait-online.service

