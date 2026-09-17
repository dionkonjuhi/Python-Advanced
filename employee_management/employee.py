class Employee:

    def __init__(
        self,
        employee_id=None,
        first_name="",
        last_name="",
        email="",
        phone="",
        position="",
        salary=0
    ):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.position = position
        self.salary = salary

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return (
            f"{self.employee_id} - "
            f"{self.full_name()} - "
            f"{self.position}"
        )
