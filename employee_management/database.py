import sqlite3

DATABASE_NAME = "employees.db"


def connect():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            position TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_employee(first_name, last_name, email, phone, position, salary):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO employees
        (first_name, last_name, email, phone, position, salary)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, email, phone, position, salary))

    connection.commit()
    connection.close()


def get_all_employees():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM employees
        ORDER BY id DESC
    """)

    employees = cursor.fetchall()

    connection.close()

    return employees


def get_employee(employee_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM employees
        WHERE id = ?
    """, (employee_id,))

    employee = cursor.fetchone()

    connection.close()

    return employee


def update_employee(employee_id, first_name, last_name, email,
                    phone, position, salary):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE employees
        SET first_name = ?,
            last_name = ?,
            email = ?,
            phone = ?,
            position = ?,
            salary = ?
        WHERE id = ?
    """, (
        first_name,
        last_name,
        email,
        phone,
        position,
        salary,
        employee_id
    ))

    connection.commit()
    connection.close()


def delete_employee(employee_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (employee_id,))

    connection.commit()
    connection.close()


def search_employees(search_text):
    connection = connect()
    cursor = connection.cursor()

    search = f"%{search_text}%"

    cursor.execute("""
        SELECT * FROM employees
        WHERE first_name LIKE ?
           OR last_name LIKE ?
           OR email LIKE ?
           OR phone LIKE ?
           OR position LIKE ?
        ORDER BY id DESC
    """, (
        search,
        search,
        search,
        search,
        search
    ))

    employees = cursor.fetchall()

    connection.close()

    return employees

