person =("Abhay", 21, "Asia")
name, age, native = person
print(name)
print(age)
print(native)


student = {
    "name": "Abhay",
    "age": 21,
    "native": "Asia"
}

print(student["name"])
print(student.get("age"))

student["grade"] = 91
student["age"]= 18
print(student)

student.pop("native")
del student["grade"]
print(student)