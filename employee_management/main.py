from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

from database import (
    create_table,
    get_all_employees,
    get_employee,
    add_employee,
    update_employee,
    delete_employee,
    search_employees
)


app = FastAPI(
    title="Employee Management System API"
)


# =========================
# DATABASE
# =========================

create_table()


# =========================
# EMPLOYEE MODEL
# =========================

class Employee(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    position: str
    salary: float


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "Employee Management API is running"
    }


# =========================
# GET ALL EMPLOYEES
# =========================

@app.get("/employees")
def get_employees():

    employees = get_all_employees()

    return [
        dict(employee)
        for employee in employees
    ]


# =========================
# GET ONE EMPLOYEE
# =========================

@app.get("/employees/{employee_id}")
def get_one_employee(employee_id: int):

    employee = get_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee nuk u gjet."
        )

    return dict(employee)


# =========================
# CREATE EMPLOYEE
# =========================

@app.post("/employees", status_code=201)
def create_employee(employee: Employee):

    if not employee.first_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Emri është i detyrueshëm."
        )

    if not employee.last_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Mbiemri është i detyrueshëm."
        )

    if not employee.email.strip():
        raise HTTPException(
            status_code=400,
            detail="Email është i detyrueshëm."
        )

    if not employee.position.strip():
        raise HTTPException(
            status_code=400,
            detail="Pozita është e detyrueshme."
        )

    if employee.salary < 0:
        raise HTTPException(
            status_code=400,
            detail="Salary nuk mund të jetë negativ."
        )

    try:

        employee_id = add_employee(
            employee.first_name.strip(),
            employee.last_name.strip(),
            employee.email.strip(),
            employee.phone.strip()
            if employee.phone
            else None,
            employee.position.strip(),
            employee.salary
        )

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=400,
            detail="Ky email ekziston tashmë."
        )

    return {
        "id": employee_id,
        "message": "Employee u shtua me sukses."
    }


# =========================
# UPDATE EMPLOYEE
# =========================

@app.put("/employees/{employee_id}")
def edit_employee(
    employee_id: int,
    employee: Employee
):

    existing = get_employee(employee_id)

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Employee nuk u gjet."
        )

    if not employee.first_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Emri është i detyrueshëm."
        )

    if not employee.last_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Mbiemri është i detyrueshëm."
        )

    if not employee.email.strip():
        raise HTTPException(
            status_code=400,
            detail="Email është i detyrueshëm."
        )

    if not employee.position.strip():
        raise HTTPException(
            status_code=400,
            detail="Pozita është e detyrueshme."
        )

    if employee.salary < 0:
        raise HTTPException(
            status_code=400,
            detail="Salary nuk mund të jetë negativ."
        )

    try:

        update_employee(
            employee_id,
            employee.first_name.strip(),
            employee.last_name.strip(),
            employee.email.strip(),
            employee.phone.strip()
            if employee.phone
            else None,
            employee.position.strip(),
            employee.salary
        )

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=400,
            detail="Ky email ekziston tashmë."
        )

    return {
        "message": "Employee u përditësua me sukses."
    }


# =========================
# DELETE EMPLOYEE
# =========================

@app.delete("/employees/{employee_id}")
def remove_employee(employee_id: int):

    existing = get_employee(employee_id)

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Employee nuk u gjet."
        )

    delete_employee(employee_id)

    return {
        "message": "Employee u fshi me sukses."
    }


# =========================
# SEARCH
# =========================

@app.get("/search")
def search(q: str):

    employees = search_employees(q)

    return [
        dict(employee)
        for employee in employees
    ]