import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

st.markdown(
    """
    <style>
    .question-label {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---- Set up cookies manager ----
cookies = EncryptedCookieManager(
    prefix="Primula_app_",  # Add a prefix to avoid conflicts
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

# Full-width logo as header
st.markdown(
    """
    <style>
    .full-width-header {
        display: block;
        width: 100%;
        margin: 0 auto;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Use st.image for full-width logo
st.image("Primula.png", use_column_width=True)


# Sidebar with Styled Header
st.sidebar.markdown("### 📝 Elenco Studenti")
st.sidebar.text_input("🔍 Cerca", placeholder="Inserisci un termine di ricerca")


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
st.markdown('<div class="question-label">👤 Nome dello studente</div>', unsafe_allow_html=True)

student_name = st.text_input("", placeholder="Es: Mario Rossi")

if student_name:
    st.write(f"### I dati di **{student_name}**")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("📅 Età", min_value=3, max_value=100, value=16, step=1, key="age")
    with col2:
        gender = st.selectbox("⚧️ Genere", options=["Maschio", "Femmina", "Non-Binario", "Altro"], key="gender")

    grade_level = st.selectbox(
        "📚 Livello scolastico",
        options=[
            "Prima superiore", "Seconda superiore", "Terza superiore", "Quarta superiore", "Quinta superiore"
        ],
    )

    styled_header(
        label="Domande di accompagnamento",
        description="Inserisci informazioni di contesto socio-demografico dello studente.",
        color="#2196F3",
    )
    st.divider()
    # Additional Questions
    st.markdown('<div class="question-label">🏙️ Livello di urbanizzazione del sito scolastico</div>', unsafe_allow_html=True)
    urbanization_level = st.selectbox(
        "", 
        options=["Urbano", "Rurale"], 
                index=0,
        key="urbanization_level"
    )
    st.divider()
    st.markdown('<div class="question-label">🎓 Che tipo di scuola frequenta?</div>', unsafe_allow_html=True)
    school_type = st.selectbox(
        "", 
        options=["Liceo", "Istituto Tecnico", "Istituto Professionale"], 
                index=0, key="school_type"
    )
    st.divider()
    st.markdown('<div class="question-label">🌍 Background migratorio</div>', unsafe_allow_html=True)
    migration_background = st.radio(
        "", 
        options=["Sì", "No"], 
                index=0, key="migration_background"
    )
    st.divider()
    st.markdown('<div class="question-label">👔 Status Socio-Economico</div>', unsafe_allow_html=True)
    parental_employment_status = st.selectbox(
        "", 
        options=["Basso", "Medio", "Alto"], 
                index=0, 
        key="parental_employment_status"
    )
    st.divider()

    st.warning("### **DISCLAIMER**: queste sono solo alcune delle domande estratte dal dataset OCSE. Ne verranno proposte molte altre in futuro per guidare il docente nel colloquio e navigare i dati.")
    st.divider()

    # Feedback Section
    styled_header(
        label="📊 Feedback",
        description="Cosa ci dicono i dati OCSE:",
        color="#FF9800",
    )

    if parental_employment_status == "Basso" or urbanization_level == "Rurale":
        st.warning("🟡 In questo caso bisogna porre particolare attenzione alle seguenti competenze socio-emotive: **assertività**, **socialità**, **fiducia**, **resistenza allo stress**, **controllo delle emozioni**, **creatività**, **energia**, **ottimismo**, **curiosità**.")
        st.write("""
        ### Cosa implica questo?
        I dati OCSE ci dicono che statisticamente uno studente che presenta bassi livelli di queste skill ha alte probabilità di avere:
        - Una maggiore probabilità di avere **comportamenti a rischio** (poco sonno, alimentazione non corretta, abuso di alcol...)
        - Maggiori livelli di *ansia*
        - Minor *soddisfazione del proprio corpo*
        - Maggiori *rischi legati al benessere psicologico*

        - Minor probabilità di essere orientata ad una **carriera in ambito STEM**.
    """)
        st.write("""
        ### Strumenti di supporto
        I dati OCSE ci dicono, per potenziare le competenze di **Maria**, potresti adottare delle *best practice*. Alcuni esempi li puoi trovare qua:"
        Lo **School Toolkit** della Fondazione per la Scuola è uno strumento di autoformazione per docenti delle scuole secondarie, progettato per promuovere lezioni partecipative e potenziare le competenze trasversali degli studenti, incluse quelle socio-emotive. Offre 16 attività pratiche, come brainstorming e case study, che favoriscono collaborazione, empatia e comunicazione efficace attraverso metodi esperienziali e inclusivi. Gli insegnanti, utilizzando queste attività, possono creare ambienti di apprendimento che sviluppano abilità fondamentali per il benessere e il successo scolastico e personale degli studenti.
    """)


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
st.markdown('<div class="footer">© 2024 Primula Support Tool - Powered by data OCSE®</div>', unsafe_allow_html=True)
