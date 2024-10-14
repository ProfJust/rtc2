summe = 0  # globale Variable


def add(su):
    # nur mit Keyword global kann eine globale Variable
    # verändert werden
    global summe 
    summe = summe + 1

my_range = range(1, 10, 2 )   # [ 1, 3, 5, 7]
print(my_range)
for i in my_range:
    print(i)

print("\n")
my_list = [1 ,2, 3, 5.3, "sieben" ,9, "ü"]   #ü
ü=2
print(ü)

my_list[0] = 77
for i in my_list:
    print(i)

my_tupel = ("Heinz", 77, 6.7)
for i in my_tupel:
    print(i)
