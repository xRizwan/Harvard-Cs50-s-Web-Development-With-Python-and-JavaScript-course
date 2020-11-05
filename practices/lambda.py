people = [
    {"name":"Harry" , "house": "Gryffindor"},
    {"name":"Cho" , "house": "Ravenclaw"},
    {"name":"Draco" , "house": "Slytherin"}
]

# lambda is used to give short functions to other functions
people.sort(key= lambda person: person["name"])

print(people)