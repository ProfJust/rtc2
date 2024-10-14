# !/usr/bin/env python
# BMI.py
# -----------------------------------
# 9.11.2020 by OJ
# -----------------------------------
def bmi(m, le):
    bmi = m/(le*le)
    return bmi

def bewertung(bmi, alter):
    bmi_ug = 18.5
    bmi_og = 25.0

    if 19<=alter<=24:
        bmi_ug = 19.0
        bmi_og = 24.0 
    if 25<=alter<=34:
        bmi_ug = 20.0
        bmi_og = 25.0
    if 35<=alter<=44:
        bmi_ug = 21.0
        bmi_og = 26.0
    if 45<=alter<=54:
        bmi_ug = 22.0
        bmi_og = 27.0
    if 55<=alter<=64:
        bmi_ug = 23.0
        bmi_og = 28.0
    if 64 < alter:
        bmi_ug = 24.0
        bmi_og = 29.0

    if bmi< bmi_ug: 
        print("Untergewicht")
    elif bmi > bmi_og:
        print("Übergewicht")
    else:
        print("Normalgewicht")

def main():
    eingabe = input("Geben Sie Ihr Gewicht in kg an \n")
    gewicht = eval(eingabe)
    eingabe = input("Geben Sie Ihre Koerpergroesse in m an \n")
    laenge = eval(eingabe)
    eingabe = input("Geben Sie Ihr Alter in Jahren an \n")
    alter = eval(eingabe)
    # globale Variable werden oft durch "_" gekenzeichnet
    _bmi = bmi(gewicht, laenge)
    print("BMI: %f " % _bmi)
    bewertung(_bmi, alter)

# ------------------------------------------------------
main()