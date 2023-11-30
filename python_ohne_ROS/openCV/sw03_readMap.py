import cv2
#https://blog.codecentric.de/2017/06/einfuehrung-in-computer-vision-mit-opencv-und-python/
# === usage ===
# sudo apt install libopencv-dev python3-opencv
# cd ~/turtlebot3_ws/src/rtc2/python_ohne_ROS/openC
# Ausführbar machen
# chmod +x sw03_readMap.py 
# python3 sw01_openCV_test.py 
# pip install imutils
import imutils

 
# lese Bild von Festplatte
map = cv2.imread("map.pgm")
# zeige Bild in Fenster an
cv2.imshow("Bild", map)

print(" Das Bild per Maus aktivieren, dann Taste drücken => Weiter")
cv2.waitKey(0)

edgeMap = imutils.auto_canny(map)
cv2.imshow("Bild", edgeMap)

 
# warte auf Tastendruck (wichtig, sonst sieht man das Fenster nicht)
print(" Das Bild per Maus aktivieren, dann Taste drücken => Weiter")
cv2.waitKey(0)
