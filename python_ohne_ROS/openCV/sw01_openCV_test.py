import cv2
#https://blog.codecentric.de/2017/06/einfuehrung-in-computer-vision-mit-opencv-und-python/
# === usage ===
# sudo apt install libopencv-dev python3-opencv
# cd ~/turtlebot3_ws/src/rtc2/python_ohne_ROS/openC
# Ausführbar machen
# python3 sw01_openCV_test.py 

 
# lese Bild von Festplatte
image = cv2.imread("test.png")
 
# lese Farbwerte an Position y, x
y = 100
x = 50
(b, g, r) = image[y, x]
 
# gib Farbwerte auf Bildschirm aus
print(b,g,r)
print(" Das Bild per Maus aktivieren, dann Taste drücken => Weiter")
 
# setze Farbwerte auf Rot (im BGR-Farbraum)
image[y, x] = (0, 0, 255)
 
# waehle ein Region auf Interest an Punkt: (y, x) mit Dimension 50x50 Pixel
region_of_interest = image[y:y+50, x:x+50]
 
# zeige Bild in Fenster an
cv2.imshow("Bild", image)
 
# zeige Region of Interest an
cv2.imshow("ROI", region_of_interest)
 
# setze ROI auf Gruen
region_of_interest[:, :] = (0, 255, 0)
 
# die ROI ist ein "Zeiger" auf das urspruenglich geladene Image. Es enthaelt nun eine gruene Box!
cv2.imshow("Bild modifiziert", image)
 
# warte auf Tastendruck (wichtig, sonst sieht man das Fenster nicht)
print(" Das Bild per Maus aktivieren, dann Taste drücken => Weiter")
cv2.waitKey(0)
