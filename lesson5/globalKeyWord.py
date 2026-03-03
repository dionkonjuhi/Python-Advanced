from tkinter.font import names

from pyexpat.errors import messages

from lesson5.globalVariables import greets

greeting = "Hello"
name = "Renato"

def greet_2():
    global  greeting
    greeting = "Goodbye"

    name = "Liron"

    message = f"{greeting}, {name}!"

    print(message)
greet_2()

print(greeting)

print(name)