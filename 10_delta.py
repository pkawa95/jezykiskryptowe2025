import math

print("Program do obliczania delty równania kwadratowego (ax² + bx + c = 0)")

# Pobieranie danych od użytkownika
try:
    a = float(input("Podaj współczynnik a: "))
    b = float(input("Podaj współczynnik b: "))
    c = float(input("Podaj współczynnik c: "))

    if a == 0:
        print("To nie jest równanie kwadratowe, ponieważ a = 0.")
    else:
        # Obliczanie delty
        delta = b**2 - 4*a*c
        print(f"Delta wynosi: {delta}")

        # Obliczanie pierwiastków jeśli delta >= 0
        if delta > 0:
            x1 = (-b - math.sqrt(delta)) / (2*a)
            x2 = (-b + math.sqrt(delta)) / (2*a)
            print(f"Równanie ma dwa pierwiastki rzeczywiste: x1 = {x1}, x2 = {x2}")
        elif delta == 0:
            x = -b / (2*a)
            print(f"Równanie ma jeden pierwiastek rzeczywisty: x = {x}")
        else:
            print("Równanie nie ma pierwiastków rzeczywistych.")

except ValueError:
    print("Błąd: Wprowadź poprawne wartości liczbowe.")
