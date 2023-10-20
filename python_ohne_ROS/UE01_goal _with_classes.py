# !/usr/bin/env python3
# UE01_goal_with_classes.py
# -----------------------------------
# 20.10.2023 by OJ
# -----------------------------------

import math
def rad2deg(winkel):
    return winkel/3.1415927*180.0

#### Bisheriger Code ######
# Pose der Turtle
[x,y, theta] = [5.5, 5.5, 0.0]
#
[xg,yg] = [7.5, 7.5]

theta2goal = math.atan2(yg-y, xg-x)
print("Winkel zum Ziel: ", theta2goal," ",round(rad2deg(theta2goal), 3)) 

[sx, sy] = [xg-x, yg-y]  # Vektor zum Ziel
print("Vektor: ", sx," ", sy) #, end="")  # kein Zeilenumbruch


#### OOP Code ######
# Pose der Turtle als Klasse
class clPose:
    def __init__(self): # Konstruktor
        self.x = 5.5
        self.y = 5.5
        self.theta = 0.0

pose = clPose() # Instanzierung

# Goal als Klasse
class clGoal:
    def __init__(self, _x, _y): # Konstruktor mit Parametern
        self.x = _x
        self.y = _y
    
goal = clGoal(7.5, 7.5)
    
# Vector als Klasse
class clVector:
    def __init__(self): # Konstruktor
        self.x = 0
        self.y = 0

    def getVect(self, g, p):
        self.x = g.x - p.x
        self.y = g.y - p.y

s = clVector() # Instanzierung

theta2goal = math.atan2(goal.y - pose.y, goal.y - pose.x)
print("Winkel zum Ziel: ", theta2goal," ",round(rad2deg(theta2goal), 3)) 

s.getVect( goal, pose)  # Vektor zum Ziel
print("Vektor: ", s.x," ", s.y) #, end="")  # kein Zeilenumbruch


