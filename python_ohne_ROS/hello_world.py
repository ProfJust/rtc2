def my_main():
    print("Hello, world!")
    mystring =" mein erster String"
    print(mystring)

    mystring = 5.0
    mystring = mystring + 3.0
    print(mystring)

# Dies ist ein Zeilenkommentar
def bewertung(b):
    if (b > 25):
        print(" => Uebergewicht")
    elif (b < 18.5):
        print(" => Untergewicht")
    else:
        print(" => Normalgewicht")   

def add( a, b):
    return a+b

my_main()
bewertung(23)
print(add(4, 5))
print(add("Hello ", str(5)))