import streamlit as st

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
    st.write(f"### Demographic Information for **{student_name}**")

    # Collect demographic data
    age = st.number_input("Enter the student's age", min_value=3, max_value=100, value=16, step=1, key="age")
    gender = st.selectbox("Select the student's gender", options=["Male", "Female", "Non-binary", "Other"], key="gender")
    grade_level = st.selectbox(
        "Select the student's grade level",
        options=["Kindergarten", "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade", "Middle School", "High School", "College"],
        key="grade_level"
    )

    st.write(f"### Guiding questions for **{student_name}**")

    # Display all questions at once
    question1_prompt = "How many hours did the student spend studying this week?"
    study_hours = st.number_input(
        f"1. {question1_prompt}", min_value=0, max_value=100, value=0, key="study_hours"
    )

    question2_prompt = "How many assignments did the student complete this week?"
    assignments_completed = st.number_input(
        f"2. {question2_prompt}", min_value=0, max_value=50, value=0, key="assignments_completed"
    )

    question3_prompt = "How many classes did the student attend this week?"
    classes_attended = st.number_input(
        f"3. {question3_prompt}", min_value=0, max_value=10, value=0, key="classes_attended"
    )

    # Perform calculation (formula is hidden)
    formula_result = (study_hours * 2) + (assignments_completed * 1.5) + (classes_attended * 3)

    # Show feedback based on the result
    st.write("### Feedback")
    if formula_result < 100:
        st.success("The student is on track! Great job!")
    elif 100 <= formula_result < 200:
        st.warning("The student is doing okay but could improve.")
    else:
        st.error("The student needs significant improvement.")

    # Save student data to session state
    st.session_state.student_data[student_name] = {
        "Age": age,
        "Gender": gender,
        "Grade Level": grade_level,
        "Study Hours": study_hours,
        "Assignments Completed": assignments_completed,
        "Classes Attended": classes_attended,
        "Result": formula_result,
    }

    # Mock data upload
    if st.button("Upload Data to Server"):
        # Simulate uploading the data (e.g., sending it to a backend API or database)
        mock_server_response = {
            "status": "success",
            "message": f"Data for {student_name} uploaded successfully.",
            "data": st.session_state.student_data[student_name],
        }

        # Display a confirmation
        st.success(f"Data for {student_name} has been uploaded successfully!")

# View all entered student data
if st.session_state.student_data:
    with st.expander("View All Student Data"):
        st.write("### Collected Student Data")
        st.json(st.session_state.student_data)
