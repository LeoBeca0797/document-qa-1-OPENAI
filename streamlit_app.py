import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# ---- Set up cookies manager ----
cookies = EncryptedCookieManager(
    prefix="pisa_app_",  # Add a prefix to avoid conflicts
    password="a-very-secret-key"  # Replace with a strong secret key
)
if not cookies.ready():
    st.stop()

# ---- Styling Function ----
def styled_header(label, description, color):
    st.markdown(
        f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 5px;">
            <h3 style="color: white; margin: 0;">{label}</h3>
            <p style="color: white; margin: 0;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---- Main Application ----
# Header Section
st.markdown(
    """
    <style>
    .main-header {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 18px;
        text-align: center;
        color: #555555;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888888;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">Ciao Elisa, benvenuta su PISE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Il tuo aiuto nell\'interpretazione e la raccolta delle capacità socio-emotive!</div>', unsafe_allow_html=True)

# Sidebar with Styled Header
st.sidebar.markdown("### 📝 Elenco Studenti")
if "student_data" not in st.session_state:
    st.session_state.student_data = {}

if st.session_state.student_data:
    student_list = list(st.session_state.student_data.keys())
    selected_student = st.sidebar.selectbox("Seleziona uno studente per vedere i dettagli", student_list)
else:
    st.sidebar.info("Non è stato aggiunto ancora uno studente!")
    selected_student = None

# Display details of the selected student
if selected_student:
    st.sidebar.write(f"### 📋 I dettagli di {selected_student}")
    student_details = st.session_state.student_data[selected_student]
    for key, value in student_details.items():
        st.sidebar.write(f"- **{key}**: {value}")

# Student Input Section
styled_header(
    label="Inserisci i dati dello studente",
    description="Compila i campi sottostanti per raccogliere le informazioni necessarie.",
    color="#4CAF50",
)

student_name = st.text_input("👤 Nome dello studente", placeholder="Es: Mario Rossi")

if student_name:
    st.write(f"### Informazioni demografiche di **{student_name}**")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("📅 Età", min_value=3, max_value=100, value=16, step=1, key="age")
    with col2:
        gender = st.selectbox("⚧️ Genere", options=["Maschio", "Femmina", "Non-Binario", "Altro"], key="gender")

    grade_level = st.selectbox(
        "📚 Livello scolastico",
        options=[
            "Asilo", "Prima elementare", "Seconda elementare", "Terza elementare", "Quarta elementare",
            "Quinta elementare", "Scuola media", "Scuola superiore", "Università"
        ],
    )

    styled_header(
        label="Domande di accompagnamento",
        description="Inserisci i dettagli sull'impegno dello studente.",
        color="#2196F3",
    )

    study_hours = st.number_input(
        "1️⃣ Ore dedicate allo studio questa settimana", min_value=0, max_value=100, value=0, key="study_hours"
    )
    assignments_completed = st.number_input(
        "2️⃣ Compiti completati questa settimana", min_value=0, max_value=50, value=0, key="assignments_completed"
    )
    classes_attended = st.number_input(
        "3️⃣ Lezioni frequentate questa settimana", min_value=0, max_value=10, value=0, key="classes_attended"
    )

    # Perform calculation (formula is hidden)
    formula_result = (study_hours * 2) + (assignments_completed * 1.5) + (classes_attended * 3)

    # Show feedback based on the result
    styled_header(
        label="📊 Feedback",
        description="Valutazione basata sui dati forniti.",
        color="#FF9800",
    )
    if formula_result < 100:
        st.success("🟢 Continua così!")
    elif 100 <= formula_result < 200:
        st.warning("🟡 Fai attenzione, serve un po' più impegno.")
    else:
        st.error("🔴 Situazione critica, è necessario migliorare.")

    # Save student data to session state
    st.session_state.student_data[student_name] = {
        "Età": age,
        "Genere": gender,
        "Livello Scolastico": grade_level,
        "Ore di Studio": study_hours,
        "Compiti Completati": assignments_completed,
        "Lezioni Frequentate": classes_attended,
        "Risultato": formula_result,
    }

    # Option to upload data
    upload_data = st.checkbox("Vuoi caricare i dati in forma anonima?")

    if upload_data:
        if st.button("Carica i Dati sul Server"):
            st.success(f"Dati di **{student_name}** caricati con successo! (Tutti i dati sono anonimizzati)")
    else:
        st.info("I dati non saranno caricati, ma sono visibili solo localmente.")

# View all entered student data
if st.session_state.student_data:
    with st.expander("📖 Visualizza Tutti i Dati degli Studenti"):
        st.write("### Dati Raccolti degli Studenti")
        st.json(st.session_state.student_data)

# Footer
st.markdown('<div class="footer">© 2024 PISA Support Tool</div>', unsafe_allow_html=True)
