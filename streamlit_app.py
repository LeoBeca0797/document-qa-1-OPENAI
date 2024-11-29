import streamlit as st

# ---- Add Logo on Left Border ----
logo_path = "logo/PISE.png"
st.sidebar.markdown(
    f"""
    <style>
        .sidebar .sidebar-content {{
            position: relative;
        }}
        .sidebar-content:before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 150px;
            background: url('{./logo/PISE.png}') no-repeat center center;
            background-size: contain;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- TEACHER-GUIDED STUDENT INPUT ----
st.header("Benvenuta sul PISE, il tuo aiuto nell'interpretazione e la raccolta delle capacità socio-emotive!")

# Persistent storage for student data
if "student_data" not in st.session_state:
    st.session_state.student_data = {}

# Sidebar section for viewing added students
st.sidebar.header("Students List")
if st.session_state.student_data:
    student_list = list(st.session_state.student_data.keys())
    selected_student = st.sidebar.selectbox("Seleziona una studentessa per vedere i dettagli", student_list)
else:
    st.sidebar.write("Non è stato aggiunto ancora uno studente!")
    selected_student = None

# Display details of the selected student
if selected_student:
    st.sidebar.write(f"### I dettagli di {selected_student}")
    student_details = st.session_state.student_data[selected_student]
    for key, value in student_details.items():
        st.sidebar.write(f"- **{key}**: {value}")

# Teacher enters the student's name
student_name = st.text_input("Inserisci il nome dello studente", placeholder="e.g., Mario Rossi")

if student_name:
    st.write(f"### Informazioni demografiche di **{student_name}**")

    # Collect demographic data
    age = st.number_input("Inserisci l'età dello studente", min_value=3, max_value=100, value=16, step=1, key="age")
    gender = st.selectbox("Seleziona il genere dello studente", options=["Maschio", "Femmina", "Non-Binario", "Altro"], key="gender")
    grade_level = st.selectbox(
    "Select the student's grade level",
    options=["Asilo", "Prima elementare", "Seconda elementare", "Terza elementare", "Quarta elementare", "Quinta elementare", "Scuola media", "Scuola superiore", "Università"]
)

    st.write(f"### Domande di accompagnamento di **{student_name}**")

    # Display all questions at once
    question1_prompt = "Quante ore ha dedicato lo studente allo studio questa settimana?"
    study_hours = st.number_input(
        f"1. {question1_prompt}", min_value=0, max_value=100, value=0, key="study_hours"
    )

    question2_prompt = "Quanti compiti ha completato lo studente questa settimana?"
    assignments_completed = st.number_input(
        f"2. {question2_prompt}", min_value=0, max_value=50, value=0, key="assignments_completed"
    )

    question3_prompt = "Quante lezioni ha frequentato lo studente questa settimana?"
    classes_attended = st.number_input(
        f"3. {question3_prompt}", min_value=0, max_value=10, value=0, key="classes_attended"
    )

    # Perform calculation (formula is hidden)
    formula_result = (study_hours * 2) + (assignments_completed * 1.5) + (classes_attended * 3)

    # Show feedback based on the result
    st.write("### Feedback")
    if formula_result < 100:
        st.success("Daje duro.")
    elif 100 <= formula_result < 200:
        st.warning("Occhio bro.")
    else:
        st.error("Vez sei fuori")

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
            "message": f"Dati di {student_name} caricati con successo.",
            "data": st.session_state.student_data[student_name],
        }

        # Display a confirmation
        st.success(f"Dati di {student_name} caricati con successo!")

# View all entered student data
if st.session_state.student_data:
    with st.expander("View All Student Data"):
        st.write("### Collected Student Data")
        st.json(st.session_state.student_data)
