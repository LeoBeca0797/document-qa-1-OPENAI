import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# ---- Set up cookies manager ----
cookies = EncryptedCookieManager(
    prefix="PISE_app_",  # Add a prefix to avoid conflicts
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

st.markdown('<div class="main-header">Benvenuta sul PISE</div>', unsafe_allow_html=True)
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
            "Prima elementare", "Seconda elementare", "Terza elementare", "Quarta elementare", "Quinta elementare",
            "Prima media", "Seconda media", "Terza media",
            "Prima superiore", "Seconda superiore", "Terza superiore", "Quarta superiore", "Quinta superiore"
        ],
    )

    styled_header(
        label="Domande di accompagnamento",
        description="Inserisci informazioni sul contesto socio-emotivo dello studente e sulla famiglia.",
        color="#2196F3",
    )

    # Additional Questions
    urbanization_level = st.selectbox(
        "🏙️ Livello di urbanizzazione del sito scolastico", 
        options=["Urbano", "Rurale"], 
                index=0,
        key="urbanization_level"
    )
    migration_background = st.radio(
        "🌍 Background migratorio", 
        options=["Sì", "No"], 
                index=0, key="migration_background"
    )
    parental_employment_status = st.selectbox(
        "👔 Status occupazionale dei genitori", 
        options=["Basso", "Medio", "Alto"], 
                index=0, 
        key="parental_employment_status"
    )
    parental_graduate = st.radio(
        "🎓 Almeno uno dei due genitori è laureato?", 
        options=["Sì", "No"], 
                index=0,
        key="parental_graduate"
    )
    max_parent_education = st.selectbox(
        "📘 Livello massimo di istruzione raggiunto da uno dei due genitori",
        options=[
            "Licenza elementare", 
            "Licenza media", 
            "Diploma superiore", 
            "Laurea triennale", 
            "Laurea magistrale", 
            "Dottorato"
        ],
                index=0,
        key="max_parent_education"
    )

    # Feedback Section
    styled_header(
        label="📊 Feedback",
        description="Valutazione basata sui dati forniti rispetto al livello socio-emozionale di riferimento.",
        color="#FF9800",
    )

    if parental_employment_status == "Basso" or urbanization_level == "Rurale":
        st.warning("🟡 Lo studente potrebbe trovarsi in un contesto a basso livello socio-emozionale.")
    else:
        st.success("🟢 Lo studente ha un contesto favorevole per il livello socio-emozionale.")

    # Save student data to session state
    st.session_state.student_data[student_name] = {
        "Età": age,
        "Genere": gender,
        "Livello Scolastico": grade_level,
        "Livello Urbanizzazione": urbanization_level,
        "Background Migratorio": migration_background,
        "Status Occupazionale Genitori": parental_employment_status,
        "Genitori Laureati": parental_graduate,
        "Livello Istruzione Massimo Genitori": max_parent_education,
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
st.markdown('<div class="footer">© 2024 PISE Support Tool</div>', unsafe_allow_html=True)
