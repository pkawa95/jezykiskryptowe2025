# Krotkli - tuples
values = (1,2,3,4,5)
print(values)
print(values[0])

#values[0] = 10
#print(values)

#del values[0]

values.remove(1)
print(values)

data_db = (1,[2],3,4,5,6)
data_db[1][0] = 22222
print(data_db)