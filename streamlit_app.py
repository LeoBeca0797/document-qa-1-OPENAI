import os
import streamlit as st
import pandas as pd
import pdfplumber
import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ---- PART 1: TEACHER-GUIDED STUDENT INPUT ----
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

    # Step 1: Guiding the teacher with questions
    question_prompt = "How many hours did the student spend studying this week?"
    st.write(f"1. {question_prompt}")
    study_hours = st.number_input("Enter the number of hours", min_value=0, max_value=100, value=0, key="study_hours")

    # Step 2: Mock formula calculation
    # Example formula: result = study_hours * 2 (e.g., for converting hours into points)
    formula_result = study_hours * 2

    # Step 3: Show the result and feedback based on the formula
    st.write("### Formula Calculation and Feedback")
    st.write(f"Formula: `study_hours * 2`")
    st.write(f"Result: `{formula_result}`")

    if formula_result < 50:
        st.success("The student is on track! Great job!")
    elif 50 <= formula_result < 100:
        st.warning("The student is doing okay but could improve.")
    else:
        st.error("The student needs significant improvement.")

    # Save student data to session state
    st.session_state.student_data[student_name] = {
        "Study Hours": study_hours,
        "Result": formula_result
    }

    # Step 4: Mock data upload
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

# ---- PART 2: CALCULATION SIDE ----
st.header("📊 Calculation Side")

# Persistent storage for calculation variables
if "calculation_data" not in st.session_state:
    st.session_state.calculation_data = {}

# Input variables for calculation
st.write("### Input Variables")
option1 = st.number_input("Enter Option 1 (e.g., Exam Score)", min_value=10, max_value=50, value=10, key="option1")
option2 = st.number_input("Enter Option 2 (e.g., Homework Score)", min_value=5, max_value=45, value=5, key="option2")
option3 = st.number_input("Enter Option 3 (e.g., Participation Score)", min_value=1, max_value=5, value=1, key="option3")

# Calculate the formula
calculation_result = (option1 + option2) * option3

# Save calculation data
st.session_state.calculation_data = {
    "Option 1": option1,
    "Option 2": option2,
    "Option 3": option3,
    "Result": calculation_result
}

# Show the result
st.write("### Formula Calculation")
st.write(f"Formula: `(Option 1 + Option 2) * Option 3`")
st.write(f"Result: `{calculation_result}`")

# Provide feedback based on the result
if calculation_result < 100:
    st.success("The result is less than 100. Everything looks good!")
elif 100 <= calculation_result < 200:
    st.warning("The result is between 100 and 200. Be cautious!")
else:
    st.error("The result is greater than 200. Immediate action is needed!")

# Debugging and detailed view
with st.expander("Detailed Calculation Data"):
    st.write("### Variables and Results")
    st.json(st.session_state.calculation_data)
