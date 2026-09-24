import requests
import pandas as pd
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide"
)


# =========================
# API FUNCTIONS
# =========================

def get_employees():

    try:

        response = requests.get(
            f"{API_URL}/employees"
        )

        if response.status_code == 200:
            return response.json()

        st.error(
            f"Gabim nga API: {response.status_code}"
        )

        return []

    except requests.exceptions.ConnectionError:

        st.error(
            "FastAPI nuk është duke punuar."
        )

        return []


def create_employee(data):

    try:

        return requests.post(
            f"{API_URL}/employees",
            json=data
        )

    except requests.exceptions.ConnectionError:

        return None


def update_employee(employee_id, data):

    try:

        return requests.put(
            f"{API_URL}/employees/{employee_id}",
            json=data
        )

    except requests.exceptions.ConnectionError:

        return None


def delete_employee(employee_id):

    try:

        return requests.delete(
            f"{API_URL}/employees/{employee_id}"
        )

    except requests.exceptions.ConnectionError:

        return None


def search_employees(query):

    try:

        response = requests.get(
            f"{API_URL}/search",
            params={"q": query}
        )

        if response.status_code == 200:
            return response.json()

        return []

    except requests.exceptions.ConnectionError:

        st.error(
            "Nuk mund të lidhet me FastAPI."
        )

        return []


# =========================
# HEADER
# =========================

st.title(
    "👨‍💼 Employee Management System"
)

st.write(
    "Streamlit + FastAPI + SQLite"
)

st.divider()


# =========================
# GET EMPLOYEES
# =========================

employees = get_employees()


# =========================
# DASHBOARD
# =========================

st.header("📊 Dashboard")


total_employees = len(employees)


total_salary = sum(
    float(employee["salary"])
    for employee in employees
)


average_salary = (
    total_salary / total_employees
    if total_employees > 0
    else 0
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👥 Total Employees",
        total_employees
    )


with col2:

    st.metric(
        "💰 Total Salary",
        f"${total_salary:,.2f}"
    )


with col3:

    st.metric(
        "📈 Average Salary",
        f"${average_salary:,.2f}"
    )


st.divider()


# =========================
# ADD EMPLOYEE
# =========================

st.header("➕ Add Employee")


with st.form("add_employee_form"):

    col1, col2 = st.columns(2)


    with col1:

        first_name = st.text_input(
            "Emër",
            placeholder="Shkruaj emrin"
        )


        email = st.text_input(
            "Email",
            placeholder="example@gmail.com"
        )


        position = st.text_input(
            "Position",
            placeholder="Developer"
        )


    with col2:

        last_name = st.text_input(
            "Mbiemër",
            placeholder="Shkruaj mbiemrin"
        )


        phone = st.text_input(
            "Phone",
            placeholder="044123456"
        )


        salary = st.number_input(
            "Salary",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


    submitted = st.form_submit_button(
        "➕ Add Employee",
        use_container_width=True
    )


if submitted:

    if not first_name.strip():

        st.error(
            "Emri është i detyrueshëm."
        )

    elif not last_name.strip():

        st.error(
            "Mbiemri është i detyrueshëm."
        )

    elif not email.strip():

        st.error(
            "Email është i detyrueshëm."
        )

    elif not position.strip():

        st.error(
            "Position është i detyrueshëm."
        )

    else:

        response = create_employee({

            "first_name": first_name.strip(),

            "last_name": last_name.strip(),

            "email": email.strip(),

            "phone": phone.strip()
            if phone.strip()
            else None,

            "position": position.strip(),

            "salary": salary
        })


        if response is None:

            st.error(
                "Nuk mund të lidhet me FastAPI."
            )

        elif response.status_code == 201:

            st.success(
                "Employee u shtua me sukses!"
            )

            st.rerun()

        else:

            try:

                error = response.json()["detail"]

            except Exception:

                error = (
                    f"Gabim {response.status_code}"
                )

            st.error(error)


st.divider()


# =========================
# SEARCH
# =========================

st.header("🔎 Search Employee")


search_text = st.text_input(
    "Kërko employee",
    placeholder="Emër, mbiemër, email, phone ose position"
)


if search_text.strip():

    display_employees = search_employees(
        search_text.strip()
    )

else:

    display_employees = employees


# =========================
# EMPLOYEE LIST
# =========================

st.header("👥 Employee List")


if display_employees:

    table_data = []


    for employee in display_employees:

        table_data.append({

            "ID":
                employee["id"],

            "Emër":
                employee["first_name"],

            "Mbiemër":
                employee["last_name"],

            "Email":
                employee["email"],

            "Phone":
                employee["phone"] or "",

            "Position":
                employee["position"],

            "Salary":
                f"${float(employee['salary']):,.2f}"
        })


    df = pd.DataFrame(
        table_data
    )


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Nuk ka employees."
    )


st.divider()


# =========================
# MANAGE EMPLOYEE
# =========================

st.header("⚙️ Manage Employee")


if not employees:

    st.info(
        "Nuk ka employees për të menaxhuar."
    )

else:

    employee_options = {

        f"ID {employee['id']} - "
        f"{employee['first_name']} "
        f"{employee['last_name']}":

        employee["id"]

        for employee in employees
    }


    selected_employee = st.selectbox(
        "Zgjidh Employee",
        list(employee_options.keys())
    )


    selected_id = employee_options[
        selected_employee
    ]


    employee = next(

        (
            e for e in employees
            if e["id"] == selected_id
        ),

        None
    )


    if employee:

        # =========================
        # UPDATE
        # =========================

        st.subheader(
            f"✏️ Edit Employee "
            f"(ID: {employee['id']})"
        )


        with st.form("update_employee_form"):

            col1, col2 = st.columns(2)


            with col1:

                new_first_name = st.text_input(
                    "Emër",
                    value=employee["first_name"]
                )


                new_email = st.text_input(
                    "Email",
                    value=employee["email"]
                )


                new_position = st.text_input(
                    "Position",
                    value=employee["position"]
                )


            with col2:

                new_last_name = st.text_input(
                    "Mbiemër",
                    value=employee["last_name"]
                )


                new_phone = st.text_input(
                    "Phone",
                    value=employee["phone"] or ""
                )


                new_salary = st.number_input(
                    "Salary",
                    min_value=0.0,
                    value=float(employee["salary"]),
                    step=100.0,
                    format="%.2f"
                )


            update_button = st.form_submit_button(
                "💾 Update Employee",
                use_container_width=True
            )


        if update_button:

            if not new_first_name.strip():

                st.error(
                    "Emri është i detyrueshëm."
                )

            elif not new_last_name.strip():

                st.error(
                    "Mbiemri është i detyrueshëm."
                )

            elif not new_email.strip():

                st.error(
                    "Email është i detyrueshëm."
                )

            elif not new_position.strip():

                st.error(
                    "Position është i detyrueshëm."
                )

            else:

                response = update_employee(

                    selected_id,

                    {
                        "first_name":
                            new_first_name.strip(),

                        "last_name":
                            new_last_name.strip(),

                        "email":
                            new_email.strip(),

                        "phone":
                            new_phone.strip()
                            if new_phone.strip()
                            else None,

                        "position":
                            new_position.strip(),

                        "salary":
                            new_salary
                    }
                )


                if response is None:

                    st.error(
                        "Nuk mund të lidhet me FastAPI."
                    )

                elif response.status_code == 200:

                    st.success(
                        "Employee u përditësua me sukses!"
                    )

                    st.rerun()

                else:

                    try:

                        error = response.json()["detail"]

                    except Exception:

                        error = (
                            f"Gabim {response.status_code}"
                        )

                    st.error(error)


        st.divider()


        # =========================
        # DELETE
        # =========================

        st.subheader(
            "🗑️ Delete Employee"
        )


        st.warning(
            f"Po përgatiteni të fshini: "
            f"{employee['first_name']} "
            f"{employee['last_name']} "
            f"(ID: {employee['id']})"
        )


        delete_button = st.button(
            "🗑️ Delete Employee",
            type="primary",
            use_container_width=True
        )


        if delete_button:

            response = delete_employee(
                selected_id
            )


            if response is None:

                st.error(
                    "Nuk mund të lidhet me FastAPI."
                )

            elif response.status_code == 200:

                st.success(
                    "Employee u fshi me sukses!"
                )

                st.rerun()

            else:

                try:

                    error = response.json()["detail"]

                except Exception:

                    error = (
                        f"Gabim {response.status_code}"
                    )

                st.error(error)
