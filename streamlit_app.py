import os
import streamlit as st
import pandas as pd
import pdfplumber
import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ---- GLOBAL CONFIGURATION ----\
st.title("📊 Interactive Dashboard")
st.write("This dashboard combines two functionalities:")
st.markdown(
    """
1. **Formula-Based Interactive Dashboard**: Select values to compute a formula and see the results dynamically.
2. **Document-Based RAG Question Answering**: Upload a document, and ask questions about its contents using OpenAI's ChatGPT API.
"""
)

# Sidebar for managing classes and students
st.sidebar.header("Class and Student Management")
class_name = st.sidebar.text_input("Enter Class Name", placeholder="e.g., Math 101")

# Persistent storage for classes and students
if "classes" not in st.session_state:
    st.session_state.classes = {}

# Create a new class
if class_name:
    if st.sidebar.button("Create Class"):
        if class_name not in st.session_state.classes:
            st.session_state.classes[class_name] = {}
            st.success(f"Class '{class_name}' created successfully!")
        else:
            st.warning(f"Class '{class_name}' already exists.")

# Select a class
if st.session_state.classes:
    selected_class = st.sidebar.selectbox("Select a Class", list(st.session_state.classes.keys()))
else:
    selected_class = None

# Add a student to the selected class
if selected_class:
    st.sidebar.subheader(f"Manage Students in {selected_class}")
    student_name = st.sidebar.text_input("Enter Student Name", placeholder="e.g., John Doe")

    if student_name and st.sidebar.button("Add Student"):
        if student_name not in st.session_state.classes[selected_class]:
            st.session_state.classes[selected_class][student_name] = {"Option 1": None, "Option 2": None, "Option 3": None}
            st.success(f"Student '{student_name}' added to class '{selected_class}'!")
        else:
            st.warning(f"Student '{student_name}' already exists in class '{selected_class}'.")

# Display students in the selected class
if selected_class:
    st.subheader(f"Students in {selected_class}")
    students = st.session_state.classes[selected_class]
    if students:
        for student, variables in students.items():
            st.write(f"**{student}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                option1 = st.number_input(f"{student} - Option 1", min_value=10, max_value=50, value=variables["Option 1"] or 10, key=f"{student}_Option1")
            with col2:
                option2 = st.number_input(f"{student} - Option 2", min_value=5, max_value=45, value=variables["Option 2"] or 5, key=f"{student}_Option2")
            with col3:
                option3 = st.number_input(f"{student} - Option 3", min_value=1, max_value=5, value=variables["Option 3"] or 1, key=f"{student}_Option3")

            # Save updated variables
            st.session_state.classes[selected_class][student] = {"Option 1": option1, "Option 2": option2, "Option 3": option3}

            # Calculate the formula for the student
            formula_result = (option1 + option2) * option3

            # Define ranges and messages
            ranges = {
                (0, 99): "The result is less than 100. Everything looks good!",
                (100, 199): "The result is between 100 and 200. Be cautious!",
                (200, float('inf')): "The result is greater than 200. Immediate action is needed!"
            }

            # Display result
            def get_message(value):
                for (low, high), message in ranges.items():
                    if low <= value <= high:
                        return message

            message = get_message(formula_result)
            if "less than 100" in message:
                st.success(message)
            elif "between 100" in message:
                st.warning(message)
            else:
                st.error(message)
    else:
        st.info("No students in this class yet.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
'''
