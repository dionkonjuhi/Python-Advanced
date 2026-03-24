class Student:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    # getter për name

    def name(self):
        return self.__name

    # setter për name

    def name(self, value):
        self.__name = value

    # getter për age

    def age(self):
        return self.__age

    # setter për age

    def age(self, value):
        self.__age = value


student12 = Student("Dion", 17)

print("Name:", student12.name)
student12.name = "Egzon"
print("Updated Name:", student12.name)

print("Age:", student12.age)
student12.age = 18
print("Updated Age:", student12.age)