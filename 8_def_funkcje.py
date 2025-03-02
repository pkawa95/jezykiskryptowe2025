import random

array=[]

def addToArray(item):
    array.append(item)
    print(array, 'Ilosc pozycji w tablicy to: ', len(array))
    checkArray()

def checkArray():
    if len(array) == 10:
        print("Wpisano 10 pozycji")
    else:
        addToArray(random.randint(0,9))

checkArray()
print("Koniec programu")
