
from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self._weight = weight
        self._height = height

    @property
    def weight(self):
        return self._weight

    @property
    def height(self):
        return self._height

    @abstractmethod
    def calculate_bmi(self):
        pass

    @abstractmethod
    def get_bmi_category(self):
        pass

    def print_info(self):
        bmi = self.calculate_bmi()
        category = self.get_bmi_category()
        print(f"{self.name} | Age: {self.age} | BMI: {bmi:.2f} | Category: {category}")


class Adult(Person):
    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "Nenpesh"
        elif bmi < 24.9:
            return "Pesha normale"
        elif bmi < 29.9:
            return "Mbipesh"
        else:
            return "Obez"



class Child(Person):
    def calculate_bmi(self):
        return (self.weight / (self.height ** 2)) * 1.3

    def get_bmi_category(self):
        bmi = self.calculate_bmi()

        if bmi < 14:
            return "Nenpesh"
        elif bmi < 18:
            return "Pesha Normale"
        elif bmi < 24:
            return "Mbipesh"
        else:
            return "Obez"


class BMIApp:
    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def collect_user_data(self):
        name = input("Emri: ")
        age = int(input("Mosha: "))
        weight = float(input("Pesha (kg): "))
        height = float(input("Gjatesia (m): "))

        if age >= 18:
            person = Adult(name, age, weight, height)
        else:
            person = Child(name, age, weight, height)

        self.add_person(person)

    def print_results(self):
        print("\n--- RESULTS ---")
        for person in self.people:
            person.print_info()

    def run(self):
        while True:
            self.collect_user_data()
            cont = input("Doni nje person tjeter? (y/n): ")
            if cont.lower() != 'y':
                break

        self.print_results()


if __name__ == "__main__":
    app = BMIApp()
    app.run()
