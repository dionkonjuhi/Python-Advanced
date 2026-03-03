


def person(name, greeting="Hello"):
    message = f"{greeting}, {name}"
    return message

default_greeting = person("Festa")
custom_greeting = person("Melina", 'Hi')

print(default_greeting)
print(custom_greeting)