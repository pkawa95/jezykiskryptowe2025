#Lista [] - jest edytowalna/manipulowalna/mutowalna
#Indexy_listy 0,1,2,3,4
firt_list = [1,2,3,4,5]

print(firt_list)
#dodawanie do listy
firt_list.append(66)
print(firt_list[3])
print('aktualizacja')
firt_list[3] = 55
print(firt_list)
#odwracanie listy
print('odwracanie')
print(firt_list[::-1])
print('usuwanie')
del firt_list[2]
print(firt_list)
#nowa tablica
second_list = [1,'kasia',2,'gosia']
print(second_list)
second_list.remove['kasia']
print(second_list)