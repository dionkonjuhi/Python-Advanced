from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

import database


app = FastAPI(
    title="Employee Management API",
    description="CRUD API for Employee Management System",
    version="1.0.0"
)


database.create_table()


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = ""
    position: str
    salary: float


class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = ""
    position: str
    salary: float


def employee_to_dict(employee):
    return {
        "id": employee["id"],
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "email": employee["email"],
        "phone": employee["phone"],
        "position": employee["position"],
        "salary": employee["salary"]
    }


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "Employee Management API",
        "status": "running"
    }


# =========================
# CREATE
# =========================

@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate):

    if employee.salary < 0:
        raise HTTPException(
            status_code=400,
            detail="Salary cannot be negative"
        )

    try:

        employee_id = database.add_employee(
            employee.first_name.strip(),
            employee.last_name.strip(),
            employee.email.strip(),
            employee.phone.strip(),
            employee.position.strip(),
            employee.salary
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "message": "Employee created successfully",
        "id": employee_id
    }


# =========================
# READ ALL
# =========================

@app.get("/employees")
def get_employees():

    employees = database.get_all_employees()

    return [
        employee_to_dict(employee)
        for employee in employees
    ]


# =========================
# READ ONE
# =========================

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    employee = database.get_employee(employee_id)

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee_to_dict(employee)


# =========================
# UPDATE
# =========================

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate
):

    existing_employee = database.get_employee(
        employee_id
    )

    if not existing_employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if employee.salary < 0:

        raise HTTPException(
            status_code=400,
            detail="Salary cannot be negative"
        )

    try:

        database.update_employee(
            employee_id,
            employee.first_name.strip(),
            employee.last_name.strip(),
            employee.email.strip(),
            employee.phone.strip(),
            employee.position.strip(),
            employee.salary
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "message": "Employee updated successfully"
    }


# =========================
# DELETE
# =========================

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    employee = database.get_employee(
        employee_id
    )

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    database.delete_employee(employee_id)

    return {
        "message": "Employee deleted successfully"
    }


# =========================
# SEARCH
# =========================

@app.get("/search")
def search_employees(q: str):

    employees = database.search_employees(q)

    return [
        employee_to_dict(employee)
        for employee in employees
    ]
