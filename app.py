import streamlit as st
import pandas as pd

# In-memory databases (simulated)
if 'employees' not in st.session_state:
    st.session_state.employees = pd.DataFrame(columns=["ID", "Name", "Role", "Task"])
if 'leave_requests' not in st.session_state:
    st.session_state.leave_requests = pd.DataFrame(columns=["Employee ID", "Reason", "Status"])

# Sidebar login
st.sidebar.title("Login")
user_role = st.sidebar.selectbox("Role", ["Admin", "Employee"])
user_id = st.sidebar.text_input("Enter your ID")
logged_in = st.sidebar.button("Login")

def add_employee():
    st.subheader("Add Employee")
    emp_id = st.text_input("Employee ID")
    name = st.text_input("Name")
    role = st.selectbox("Role", ["Employee", "Admin"])
    if st.button("Add"):
        if emp_id and name:
            st.session_state.employees = pd.concat([st.session_state.employees, pd.DataFrame([[emp_id, name, role, ""]], columns=st.session_state.employees.columns)], ignore_index=True)
            st.success("Employee added")

def delete_employee():
    st.subheader("Delete Employee")
    emp_id = st.text_input("Enter Employee ID to delete")
    if st.button("Delete"):
        st.session_state.employees = st.session_state.employees[st.session_state.employees["ID"] != emp_id]
        st.success("Employee deleted")

def view_edit_employees():
    st.subheader("View/Edit Employees")
    df = st.session_state.employees.copy()
    st.dataframe(df)
    edit_id = st.text_input("Enter Employee ID to edit task")
    new_task = st.text_input("New Task")
    if st.button("Update Task"):
        st.session_state.employees.loc[st.session_state.employees["ID"] == edit_id, "Task"] = new_task
        st.success("Task updated")

def leave_request(emp_id):
    st.subheader("Leave Request")
    reason = st.text_input("Leave Reason")
    if st.button("Submit Leave Request"):
        st.session_state.leave_requests = pd.concat([st.session_state.leave_requests, pd.DataFrame([[emp_id, reason, "Pending"]], columns=st.session_state.leave_requests.columns)], ignore_index=True)
        st.success("Request submitted")

def process_leave_requests():
    st.subheader("Leave Requests")
    df = st.session_state.leave_requests.copy()
    st.dataframe(df)
    req_index = st.number_input("Enter Request Index to update", min_value=0, max_value=len(df)-1, step=1)
    status = st.selectbox("Set Status", ["Accepted", "Rejected"])
    if st.button("Update Request"):
        st.session_state.leave_requests.at[req_index, "Status"] = status
        st.success("Leave request updated")

def assign_tasks():
    st.subheader("Assign Tasks")
    emp_id = st.text_input("Enter Employee ID to assign task")
    task = st.text_input("Enter Task")
    if st.button("Assign Task"):
        st.session_state.employees.loc[st.session_state.employees["ID"] == emp_id, "Task"] = task
        st.success("Task assigned")

if logged_in:
    st.title("Employee Management System")
    if user_role == "Admin":
        add_employee()
        delete_employee()
        view_edit_employees()
        assign_tasks()
        process_leave_requests()
    elif user_role == "Employee":
        if user_id in st.session_state.employees["ID"].values:
            view_edit_employees()
            leave_request(user_id)
        else:
            st.error("Invalid Employee ID")