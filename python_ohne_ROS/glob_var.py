def func():
    # global glob_var
    glob_var = 2
    print('glob_var in func =', glob_var)


glob_var = 1
print("glob_var =", glob_var)


func()
print("glob_var after func =", glob_var)

gewicht = input("Geben Sie Ihr Gewicht in kg an \n")
print("Ihr Gewicht ist", gewicht, "kg")

while True:
    eingabe = input("Bitte gib eine ganze Zahl ein: ")
    try:
        zahl = int(eingabe)
        print(f"Du hast die Zahl {zahl} eingegeben.")
        break
    except ValueError:
        print("Fehler: Bitte gib eine gültige ganze Zahl ein!")

