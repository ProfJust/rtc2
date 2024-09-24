Ziel:

USB-Tiefen-Camera am TurtleBot3 angeschlossen. Wegen der geringen Rechenleistung des RaspberryPis, soll das Bild auf dem Rmeote PC verabeitet werden (insbesondere eine Poincloud2 generieren für Nav2-Stack).

USBIP leitet die über USB herinkommenden Daten über das WLAN weiter an den Remote PC.


Dazu Server - Installation auf dem TB3 / Raspberry PI (getestet mit Astra Orbbec)

     1.) Richtige Version heruasfinden, abhängig vom installierten Image
        $ sudo apt-get update
        $ apt list 'linux-image-*' --installed 
        $ sudo apt-get install hwdata linux-tools-raspi linux-tools-5.15.0-1043-raspi
        $ sudo apt install linux-tools-*generic*
        $ sudo apt-get install usbip

    2.) Add/remove Module from Kernel
    Grundsätzlich besitzt der Linux-Kernel einen monolithischen Aufbau, allerdings bietet er auch die Möglichkeit, 
    Module mit dem Befehl modprobe zur Laufzeit zu laden und entladen.
    modprobe löst dabei automatisch Abhängigkeiten auf, d.h. wenn das zu ladende Modul andere Module voraussetzt, 
    werden diese automatisch in der richtigen Reihenfolge mit geladen bzw. werden Module automatisch mit entfernt, 
    welche nur aus Abhängigkeitsgründen geladen wurden.
 
        $ sudo modprobe usbip-host 

    3.) Server-Daemon starten
        $  sudo usbipd --daemon 

    4.) Auswahl des USB der angebunden werden soll
        $ usbip list --local
        $ sudo usbip bind --busid 1-1.2 
  





Abholen der Daten auf dem Remote PC (getestet mit Astra Orbbec)

    1.) Installation von https://github.com/orbbec/OrbbecSDK_ROS2
      ..
      Achtung! Astra Orbbec funktioniert nicht mit dem OrbbecSDK_ROS2
      Am besten die Kamera zunächt direkt am Remote PC testen (ohne usbIP) um die Funktion zu prüfen.

    2.) Installation von usbIP auf dem Remote PC (als Client)
        Richtige Version herausfinden, abhängig vom installierten Image
            $ apt list 'linux-image-*' --installed
        
            $ sudo apt-get install hwdata linux-tools-generic-hwe
            $ sudo apt-get install hwdata linux-tools-generic
            $ sudo apt-get install usbip
        
        Testen ob usbip funktioniert, Liste aller direkt angeschlossenen UBSs
            $ usb $ usbip list -l



    3.) Lesen der Camera Daten die über usbIP hereinkommen, Client starten

           $ sudo modprobe vhci-hcd

        Prüfen ob Daten hereinkommen

           $ usbip list --remote 192.168.178.33 
        
        Daten als virtuellen USB am Remote PC hinzufügen

           $ sudo usbip attach --remote 192.168.178.33 --busid 1-1.2 

        Kamera und ros2 starten, als ob direkt am Remote-PC angeschlossen

            $ ros2 launch astra_camera astra.launch.xml
            $ ...
            $ rqt
            $ rviz2

Quellen:
    Die Idee kommt von hier:
    https://www.mybotshop.de/Turtlebot3-3D-SLAM

    USBIP wird hier beschrieben
    https://wiki.ubuntuusers.de/USBIP/