# !/usr/bin/env python
# goal.py
# -----------------------------------
# 9.10.2023 by OJ
# -----------------------------------

import math
def rad2deg(winkel):
    return winkel/3.1415927*180.0


# Pose der Turtle
[x,y, theta] = [5.5, 5.5, 0.0]

# Goal 
[xg,yg] = [7.5, 7.5]

theta2goal = math.atan2(yg-y, xg-x)
print("Winkel zum Ziel: ", theta2goal," ",round(rad2deg(theta2goal), 3)) 

[sx, sy] = [xg-x, yg-y]  # Vektor zum Ziel
print("Vektor: ", sx," ", sy) #, end="")  # kein Zeilenumbruch

