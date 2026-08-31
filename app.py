import streamlit as st

import pandas as pd

 

from database import (

    create_tables,

    add_student,

    get_students,

    update_student,

    delete_student,

    add_marks,

    get_marks,

    delete_marks

)

 

from calculations import (

    get_grade,

    calculate_sgpa

)

 

 

# --------------------------------------------------

# PAGE CONFIGURATION

# --------------------------------------------------

 

st.set_page_config(

    page_title="Student Management System",

    page_icon="",

    layout="wide"

)

 

 

# --------------------------------------------------

# CREATE DATABASE

# --------------------------------------------------

 

create_tables()

 

 

# --------------------------------------------------

# TITLE

# --------------------------------------------------

 

st.title(" Student Management & CGPA Dashboard")

 

st.write(

    "Manage students, subjects, marks and academic performance."

)

 

 

# --------------------------------------------------

# SIDEBAR

# --------------------------------------------------

 

st.sidebar.title("Navigation")

 

page = st.sidebar.radio(

    "Go to",

    [

        "Dashboard",

        "Students",

        "Marks & CGPA"

    ]

)

 

 

# ==================================================

# DASHBOARD

# ==================================================

 

if page == "Dashboard":

 

    st.header(" Dashboard")

 

    students = get_students()

 

    total_students = len(students)

 

    st.metric(

        "Total Students",

        total_students

    )

 

    if students:

 

        student_data = []

 

        for student in students:

 

            student_id = student[0]

            name = student[1]

            course = student[3]

            semester = student[4]

 

            marks = get_marks(student_id)

 

            sgpa = calculate_sgpa(marks)

 

            student_data.append({

                "Name": name,

                "Course": course,

                "Semester": semester,

                "SGPA": sgpa

            })

 

        df = pd.DataFrame(student_data)

 

        col1, col2, col3 = st.columns(3)

 

        col1.metric(

            "Class Average",

            round(df["SGPA"].mean(), 2)

        )

 

        col2.metric(

            "Highest SGPA",

            round(df["SGPA"].max(), 2)

        )

 

        col3.metric(

            "Lowest SGPA",

            round(df["SGPA"].min(), 2)

        )

 

        st.subheader(" Student Performance")

 

        st.dataframe(

            df,

            use_container_width=True

        )

 

        st.subheader(" SGPA Distribution")

 

        chart_data = df.set_index("Name")["SGPA"]

 

        st.bar_chart(chart_data)

 

    else:

 

        st.info(

            "No students available. Add students from the Students page."

        )

 

 

# ==================================================

# STUDENTS

# ==================================================

 

elif page == "Students":

 

    st.header(" Student Management")

 

    tab1, tab2, tab3 = st.tabs(

        [

            "Add Student",

            "View Students",

            "Delete Student"

        ]

    )

 

 

    # ----------------------------------------------

    # ADD STUDENT

    # ----------------------------------------------

 

    with tab1:

 

        st.subheader("Add New Student")

 

        with st.form("student_form"):

 

            name = st.text_input("Student Name")

 

            email = st.text_input("Email")

 

            course = st.selectbox(

                "Course",

                [

                    "BBA",

                    "BCA",

                    "B.Com",

                    "B.Sc",

                    "MBA",

                    "MCA"

                ]

            )

 

            semester = st.number_input(

                "Semester",

                min_value=1,

                max_value=8,

                step=1

            )

 

            submitted = st.form_submit_button(

                "Add Student"

            )

 

            if submitted:

 

                if name.strip() == "":

 

                    st.error(

                        "Please enter the student's name."

                    )

 

                else:

 

                    add_student(

                        name,

                        email,

                        course,

                        semester

                    )

 

                    st.success(

                        f"{name} added successfully!"

                    )

 

 

    # ----------------------------------------------

    # VIEW STUDENTS

    # ----------------------------------------------

 

    with tab2:

 

        students = get_students()

 

        if students:

 

            df = pd.DataFrame(

                students,

                columns=[

                    "ID",

                    "Name",

                    "Email",

                    "Course",

                    "Semester"

                ]

            )

 

            st.dataframe(

                df,

                use_container_width=True

            )

 

        else:

 

            st.info("No students found.")

 

 

    # ----------------------------------------------

    # DELETE STUDENT

    # ----------------------------------------------

 

    with tab3:

 

        students = get_students()

 

        if students:

 

            student_options = {

                f"{student[1]} (ID: {student[0]})":

                student[0]

                for student in students

            }

 

            selected_student = st.selectbox(

                "Select Student",

                list(student_options.keys())

            )

 

            student_id = student_options[selected_student]

 

            if st.button("Delete Student"):

 

                delete_student(student_id)

 

                st.success(

                    "Student deleted successfully."

                )

 

                st.rerun()

 

        else:

 

            st.info("No students available.")

 

 

# ==================================================

# MARKS & CGPA

# ==================================================

 

elif page == "Marks & CGPA":

 

    st.header(" Marks & CGPA")

 

    students = get_students()

 

    if not students:

 

        st.warning(

            "Please add students first."

        )

 

    else:

 

        student_options = {

            f"{student[1]} (ID: {student[0]})":

            student[0]

            for student in students

        }

 

        selected_student = st.selectbox(

            "Select Student",

            list(student_options.keys())

        )

 

        student_id = student_options[selected_student]

 

 

        # ------------------------------------------

        # ADD MARKS

        # ------------------------------------------

 

        st.subheader("Add Subject Marks")

 

        with st.form("marks_form"):

 

            subject = st.text_input(

                "Subject"

            )

 

            marks = st.number_input(

                "Marks",

                min_value=0.0,

                max_value=100.0,

                step=1.0

            )

 

            credits = st.number_input(

                "Credits",

                min_value=1,

                max_value=6,

                value=3

            )

 

            submitted = st.form_submit_button(

                "Add Marks"

            )

 

            if submitted:

 

                if subject.strip() == "":

 

                    st.error(

                        "Please enter a subject."

                    )

 

                else:

 

                    add_marks(

                        student_id,

                        subject,

                        marks,

                        credits

                    )

 

                    st.success(

                        "Marks added successfully!"

                    )

 

 

        # ------------------------------------------

        # DISPLAY MARKS

        # ------------------------------------------

 

        marks_data = get_marks(student_id)

 

        if marks_data:

 

            rows = []

 

            for mark in marks_data:

 

                mark_id = mark[0]

                subject_name = mark[1]

                mark_value = mark[2]

                credit_value = mark[3]

 

                rows.append({

                    "ID": mark_id,

                    "Subject": subject_name,

                    "Marks": mark_value,

                    "Credits": credit_value,

                    "Grade": get_grade(mark_value)

                })

 

            df = pd.DataFrame(rows)

 

            st.subheader(" Academic Performance")

 

            st.dataframe(

                df,

                use_container_width=True

            )

 

 

            # --------------------------------------

            # SGPA

            # --------------------------------------

 

            sgpa = calculate_sgpa(marks_data)

 

            st.success(

                f" Current SGPA: {sgpa}"

            )

 

 

            # --------------------------------------

            # DELETE MARKS

            # --------------------------------------

 

            st.subheader("Delete Subject")

 

            mark_options = {

                f"{mark[1]} - {mark[2]} marks":

                mark[0]

                for mark in marks_data

            }

 

            selected_mark = st.selectbox(

                "Select subject",

                list(mark_options.keys())

            )

 

            mark_id = mark_options[selected_mark]

 

            if st.button("Delete Subject"):

 

                delete_marks(mark_id)

 

                st.success(

                    "Subject deleted successfully."

                )

 

                st.rerun()

 

        else:

 

            st.info(

                "No marks added for this student."

            )