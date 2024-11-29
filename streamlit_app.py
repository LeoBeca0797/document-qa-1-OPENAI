import os
import streamlit as st
import pandas as pd
import pdfplumber
import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ---- TEACHER-GUIDED STUDENT INPUT ----
st.header("📐 Teacher-Guided Student Input Dashboard")

# Persistent storage for student data
if "student_data" not in st.session_state:
    st.session_state.student_data = {}

# Sidebar section for viewing added students
st.sidebar.header("Students List")
if st.session_state.student_data:
    student_list = list(st.session_state.student_data.keys())
    selected_student = st.sidebar.selectbox("Select a Student to View Details", student_list)
else:
    st.sidebar.write("No students added yet.")
    selected_student = None

# Display details of the selected student
if selected_student:
    st.sidebar.write(f"### {selected_student}'s Details")
    student_details = st.session_state.student_data[selected_student]
    for key, value in student_details.items():
        st.sidebar.write(f"- **{key}**: {value}")

# Teacher enters the student's name
student_name = st.text_input("Enter the Student's Name", placeholder="e.g., John Doe")

if student_name:
    st.write(f"### Guiding questions for **{student_name}**")

    # Step 1: Guiding the teacher with the first question
    question1_prompt = "How many hours did the student spend studying this week?"
    st.write(f"1. {question1_prompt}")
    study_hours = st.number_input("Enter the number of hours", min_value=0, max_value=100, value=0, key="study_hours")

    if study_hours > 0:
        # Step 2: Follow-up question 1
        question2_prompt = "How many assignments did the student complete this week?"
        st.write(f"2. {question2_prompt}")
        assignments_completed = st.number_input("Enter the number of assignments", min_value=0, max_value=50, value=0, key="assignments_completed")

        if assignments_completed > 0:
            # Step 3: Follow-up question 2
            question3_prompt = "How many classes did the student attend this week?"
            st.write(f"3. {question3_prompt}")
            classes_attended = st.number_input("Enter the number of classes", min_value=0, max_value=10, value=0, key="classes_attended")

            # Step 4: Mock formula calculation
            # Example formula: (study_hours * 2) + (assignments_completed * 1.5) + (classes_attended * 3)
            formula_result = (study_hours * 2) + (assignments_completed * 1.5) + (classes_attended * 3)

            # Step 5: Show the result and feedback based on the formula
            st.write("### Formula Calculation and Feedback")
            st.write(f"Formula: `(study_hours * 2) + (assignments_completed * 1.5) + (classes_attended * 3)`")
            st.write(f"Result: `{formula_result}`")

            if formula_result < 100:
                st.success("The student is on track! Great job!")
            elif 100 <= formula_result < 200:
                st.warning("The student is doing okay but could improve.")
            else:
                st.error("The student needs significant improvement.")

            # Save student data to session state
            st.session_state.student_data[student_name] = {
                "Study Hours": study_hours,
                "Assignments Completed": assignments_completed,
                "Classes Attended": classes_attended,
                "Result": formula_result
            }

            # Step 6: Mock data upload
            if st.button("Upload Data to Server"):
                # Simulate uploading the data (e.g., sending it to a backend API or database)
                mock_server_response = {
                    "status": "success",
                    "message": f"Data for {student_name} uploaded successfully.",
                    "data": st.session_state.student_data[student_name]
                }

                # Display a confirmation
                st.json(mock_server_response)
                st.success(f"Data for {student_name} has been uploaded successfully!")

# View all entered student data
if st.session_state.student_data:
    with st.expander("View All Student Data"):
        st.write("### Collected Student Data")
        st.json(st.session_state.student_data)
