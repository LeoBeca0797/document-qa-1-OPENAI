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
styled_header(
    label="Inserisci i dati dello studente",
    description="Compila i campi sottostanti per raccogliere le informazioni necessarie.",
    color="#4CAF50",
)

student_name = st.text_input("👤 Nome dello studente", placeholder="Es: Mario Rossi")

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

    # Additional Questions
    urbanization_level = st.selectbox(
        "🏙️ Livello di urbanizzazione del sito scolastico", 
        options=["Urbano", "Rurale"], 
                index=0,
        key="urbanization_level"
    )
    school_type = st.selectbox(
        "🎓 Che tipo di scuola frequenta?", 
        options=["Liceo", "Istituto Tecnico", "Istituto Professionale"], 
                index=0, key="school_type"
    )
    migration_background = st.radio(
        "🌍 Background migratorio", 
        options=["Sì", "No"], 
                index=0, key="migration_background"
    )
    parental_employment_status = st.selectbox(
        "👔 Status Socio-Economico", 
        options=["Basso", "Medio", "Alto"], 
                index=0, 
        key="parental_employment_status"
    )

    # Feedback Section
    styled_header(
        label="📊 Feedback",
        description="Cosa ci dicono i dati OCSE:",
        color="#FF9800",
    )

    if parental_employment_status == "Basso" or urbanization_level == "Rurale":
        st.warning("🟡 Le caratteristiche che hai inserito solitamente si accompagnano a livelli di competenze socio-emotive basse! Le competenze socio-emotive in questione sono: **assertività**, **socialità**, **fiducia**, **resistenza allo stress**, **controllo delle emozioni**, **creatività**, **energia**, **ottimismo**, **curiosità**.")
        st.write("""
        ### Cosa implica questo?
        Solitamente, uno studente che presenta bassi livelli di queste skill, ha:
        - Una maggiore probabilità di avere **comportamenti a rischio** (poco sonno, alimentazione non corretta, abuso di alcol...)
        - Maggiori livelli di *ansia*
        - Minor *soddisfazione del proprio corpo*
        - Maggiori *rischi legati al benessere psicologico*

        - Minor probabilità di intraprendere una carriera in ambito informatico, scientifico e ingegneristico
    """)
        st.write("""
        ### Strumenti di supporto
        Il School Toolkit della Fondazione per la Scuola è uno strumento di autoformazione progettato per supportare gli insegnanti delle scuole secondarie nel creare lezioni altamente partecipative. Offre un catalogo di 16 attività di facilitazione che promuovono la partecipazione attiva degli studenti, favorendo lo scambio di idee e la collaborazione in classe.
        Queste attività mirano a potenziare le competenze trasversali degli studenti, tra cui quelle socio-emotive, attraverso metodi inclusivi ed esperienziali. Ad esempio, attività come il "Brainstorming" e il "Case Study" incoraggiano la riflessione collettiva e la risoluzione di problemi, sviluppando abilità come l'empatia, la comunicazione efficace e la collaborazione. 
        Implementando le attività proposte dal Toolkit, gli insegnanti possono creare un ambiente di apprendimento che facilita lo sviluppo delle competenze socio-emotive degli studenti, essenziali per il loro benessere e successo sia scolastico che personale. 
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
st.markdown('<div class="footer">© 2024 PISE Support Tool</div>', unsafe_allow_html=True)
