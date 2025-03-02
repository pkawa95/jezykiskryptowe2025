students = ["Jan Kowalski", "Monika Wiśniewska"]
imie = input ("Podaj imię: ")
nazwisko = input ("Podaj nazwisko:")
wiek = input("Podaj wiek:")
wiek = int(wiek)
newstudent = imie + ' ' + nazwisko
students.append(newstudent)
students
print("Twoje imie to: {} {}".format(imie,nazwisko))
print("Nowa lista studentów to", students)
if wiek <=20:
    print("Jesteś Młody")
elif(wiek >= 21 and wiek <=30):
    print("No już nie taki młody")
else:
    print("No już masz trochę lat")