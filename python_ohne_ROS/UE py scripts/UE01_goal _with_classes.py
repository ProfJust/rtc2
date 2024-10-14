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
    def __init__(self, x, y, t): # Konstruktor
        self.x = x
        self.y = y
        self.theta = t

pose = clPose(5.5, 5.5, 0.0) # Instanzierung
pose2 = clPose(5.5, 7.5, 0.0) # Instanzierung

# Goal als Klasse
class clGoal:
    def __init__(self, x, y): # Konstruktor mit Parametern
        self.x = x
        self.y = y
    
goal = clGoal(7.5, 7.5)
    
# Vector als Klasse
class clVector:
    def __init__(self): # Konstruktor
        self.x = 0
        self.y = 0        

    def getVect(self, g, p):
        self.x = g.x - p.x
        self.y = g.y - p.y

    # https://www.programiz.com/python-programming/operator-overloading
    #def __lshift__(self, g, p):
    #    self.x = g.x - p.x
    #    self.y = g.y - p.y
    #   return self
    # ==> TypeError: clVector.__lshift__() missing 1 required positional argument: 'p'
    # AI.w-hs.de: Die Methode `lshift` ist so definiert, dass sie drei Argumente erwartet (einschließlich `self`),
    # aber in der Tat sollte sie nur zwei Argumente akzeptieren: `self` und ein anderes Objekt, 
    # mit dem der Operator verwendet wird. In Python wird bei der Überladung von Operatoren im Allgemeinen immer
    # nur ein zusätzliches Argument übergeben, weil das erste `self` das linke Operand des Operators ist. 
    # Die Lösung besteht darin, die Methode `lshift` so zu ändern, dass sie nur das zweite Objekt erwartet, 
    # etwa als Tupel. Hier ist, wie Sie den Code umschreiben können, um das Problem zu beheben:

    def __lshift__(self, other):
        g, p = other  # Erwarte ein Tupel von goal und pose
        self.x = g.x - p.x
        self.y = g.y - p.y
        return self

s = clVector() # Instanzierung

theta2goal = math.atan2(goal.y - pose.y, goal.x - pose.x)
print("Winkel zum Ziel: ", theta2goal," ",round(rad2deg(theta2goal), 3)) 

s.getVect( goal, pose)  # Vektor zum Ziel

print("Vektor: ", s.x," ", s.y) #, end="")  # kein Zeilenumbruch

s2 = clVector() # Instanzierung
# s2.x = goal.x
# s2.y = goal.y

s2 << (goal, pose)  # Überladener Operator LSHIFT
# TypeError: clVector.__lshift__() missing 1 required positional argument: 'p'
# # https://www.programiz.com/python-programming/operator-overloading

print("Vektor2: ", s2.x," ", s2.y) #, end="")  # kein Zeilenumbruch


