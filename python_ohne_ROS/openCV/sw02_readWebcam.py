import cv2
#https://blog.codecentric.de/2017/06/einfuehrung-in-computer-vision-mit-opencv-und-python/
 
# initialisiere WebCam
cam = cv2.VideoCapture(0)
 
# lese ein Bild von der WebCam
# mehrfach da WebCam Zeit zum starten braucht und das erste Bild oft 
# Fehler aufweist
ret, image = cam.read()
ret, image = cam.read()
ret, image = cam.read()

# zeige das Bild an
cv2.imshow("Bild von Webcam,", image)
 
# konvertiere das Bild in Graustufen
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# zeige das Bild an
cv2.imshow("Bild modifiziert", image)
 
# warte auf Tastendruck (Fesnter aktivieren!!) (wichtig, sonst sieht man das Fenster nicht)
cv2.waitKey(0)
