import sqlite3


DATABASE_NAME = "employees.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            position TEXT NOT NULL,
            salary REAL NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def get_all_employees():
    connection = get_connection()

    employees = connection.execute("""
        SELECT *
        FROM employees
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return employees


def get_employee(employee_id):
    connection = get_connection()

    employee = connection.execute("""
        SELECT *
        FROM employees
        WHERE id = ?
    """, (employee_id,)).fetchone()

    connection.close()

    return employee


def add_employee(
    first_name,
    last_name,
    email,
    phone,
    position,
    salary
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO employees
        (
            first_name,
            last_name,
            email,
            phone,
            position,
            salary
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        first_name,
        last_name,
        email,
        phone,
        position,
        salary
    ))

    connection.commit()

    employee_id = cursor.lastrowid

    connection.close()

    return employee_id


def update_employee(
    employee_id,
    first_name,
    last_name,
    email,
    phone,
    position,
    salary
):
    connection = get_connection()

    connection.execute("""
        UPDATE employees
        SET
            first_name = ?,
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
    connection = get_connection()

    connection.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (employee_id,))

    connection.commit()
    connection.close()


def search_employees(search_text):
    connection = get_connection()

    search = f"%{search_text}%"

    employees = connection.execute("""
        SELECT *
        FROM employees
        WHERE
            first_name LIKE ?
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
    )).fetchall()

    connection.close()

    return employees
