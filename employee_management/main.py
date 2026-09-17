import streamlit as st
import pandas as pd

import database



st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide"
)




database.create_table()



st.title("Employee Management System")

st.write(
    "Manage employees using Python, SQLite and Streamlit"
)




employees = database.get_all_employees()



col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Employees",
        len(employees)
    )

with col2:
    if employees:
        total_salary = sum(float(employee[6]) for employee in employees)
    else:
        total_salary = 0

    st.metric(
        "Total Salary",
        f"${total_salary:,.2f}"
    )

with col3:
    if employees:
        average_salary = total_salary / len(employees)
    else:
        average_salary = 0

    st.metric(
        "Average Salary",
        f"${average_salary:,.2f}"
    )


st.divider()



st.subheader("Employee Information")


with st.form("employee_form"):

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(
            "First Name"
        )

        email = st.text_input(
            "Email"
        )

        position = st.text_input(
            "Position"
        )

    with col2:
        last_name = st.text_input(
            "Last Name"
        )

        phone = st.text_input(
            "Phone"
        )

        salary = st.number_input(
            "Salary",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        add_employee_button = st.form_submit_button(
            " Add Employee",
            use_container_width=True
        )

    with col2:
        update_employee_button = st.form_submit_button(
            "✏ Update Employee",
            use_container_width=True
        )

    with col3:
        clear_button = st.form_submit_button(
            " Clear",
            use_container_width=True
        )




if add_employee_button:

    if not first_name.strip():
        st.error("Please enter the first name.")

    elif not last_name.strip():
        st.error("Please enter the last name.")

    elif not email.strip():
        st.error("Please enter the email.")

    elif not position.strip():
        st.error("Please enter the position.")

    elif salary < 0:
        st.error("Salary cannot be negative.")

    else:

        database.add_employee(
            first_name.strip(),
            last_name.strip(),
            email.strip(),
            phone.strip(),
            position.strip(),
            salary
        )

        st.success("Employee added successfully.")

        st.rerun()




if update_employee_button:

    selected_id = st.session_state.get("selected_employee_id")

    if selected_id is None:

        st.warning(
            "Please select an employee from the table first."
        )

    elif not first_name.strip():

        st.error("Please enter the first name.")

    elif not last_name.strip():

        st.error("Please enter the last name.")

    elif not email.strip():

        st.error("Please enter the email.")

    elif not position.strip():

        st.error("Please enter the position.")

    else:

        database.update_employee(
            selected_id,
            first_name.strip(),
            last_name.strip(),
            email.strip(),
            phone.strip(),
            position.strip(),
            salary
        )

        st.success("Employee updated successfully.")

        st.session_state.selected_employee_id = None

        st.rerun()




if clear_button:

    st.session_state.selected_employee_id = None

    st.rerun()




st.divider()

st.subheader("Search Employees")

col1, col2 = st.columns([4, 1])

with col1:

    search_text = st.text_input(
        "Search by name, email, phone or position",
        key="search_box"
    )

with col2:

    search_button = st.button(
        "🔎 Search",
        use_container_width=True
    )




if search_button and search_text.strip():

    employees = database.search_employees(
        search_text.strip()
    )

elif not search_text.strip():

    employees = database.get_all_employees()



st.subheader("Employee List")


if employees:

    table_data = []

    for employee in employees:

        table_data.append(
            {
                "ID": employee[0],
                "First Name": employee[1],
                "Last Name": employee[2],
                "Email": employee[3],
                "Phone": employee[4],
                "Position": employee[5],
                "Salary": f"${float(employee[6]):,.2f}"
            }
        )

    df = pd.DataFrame(table_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No employees found.")




st.divider()

st.subheader("Select Employee")


if employees:

    employee_options = {
        f"{employee[0]} - {employee[1]} {employee[2]}":
        employee[0]
        for employee in employees
    }

    selected_employee = st.selectbox(
        "Choose an employee",
        [""] + list(employee_options.keys())
    )

    if selected_employee:

        selected_id = employee_options[selected_employee]

        st.session_state.selected_employee_id = selected_id

        employee = database.get_employee(
            selected_id
        )

        if employee:

            st.write(
                f"**Selected:** {employee[1]} {employee[2]}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"📧 Email: {employee[3]}"
                )

                st.write(
                    f" Phone: {employee[4]}"
                )

            with col2:

                st.write(
                    f"💼 Position: {employee[5]}"
                )

                st.write(
                    f"💰 Salary: ${float(employee[6]):,.2f}"
                )




st.subheader("Delete Employee")


selected_id = st.session_state.get(
    "selected_employee_id"
)


if selected_id is not None:

    employee = database.get_employee(
        selected_id
    )

    if employee:

        st.warning(
            f"You are about to delete "
            f"{employee[1]} {employee[2]}."
        )

        if st.button(
            "🗑️ Delete Employee",
            type="primary"
        ):

            database.delete_employee(
                selected_id
            )

            st.session_state.selected_employee_id = None

            st.success(
                "Employee deleted successfully."
            )

            st.rerun()

else:

    st.info(
        "Select an employee above to enable deletion."
    )
