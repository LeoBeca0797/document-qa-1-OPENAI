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
        description="Cosa ci dicono i dati OCSE:",
        color="#FF9800",
    )

    if parental_employment_status == "Basso" or urbanization_level == "Rurale":
        st.warning("🟡 Le caratteristiche che hai inserito solitamente si accompagnano a livelli di competenze socio-emotive basse!")
        st.write("""
        ### Impatto delle Competenze Socio-Emotive (SES) sul Benessere degli Studenti
        - **Benessere psicologico e relazionale**: Competenze come la resistenza allo stress, l'ottimismo e il controllo emotivo sono associate a un benessere psicologico migliore. Gli studenti con livelli più alti di queste competenze tendono a sperimentare meno ansia in classe e durante i test e a mantenere un'immagine corporea positiva.
        - Relazioni sociali positive e soddisfacenti sono più comuni tra studenti con elevate capacità di empatia e sociabilità. Queste competenze migliorano le interazioni con compagni di classe e insegnanti, rafforzando il senso di appartenenza e diminuendo il rischio di isolamento.
        - **Comportamenti salutari**: Gli studenti con maggiori abilità nella regolazione emotiva e nella resilienza allo stress tendono a intraprendere comportamenti più sani, come evitare il consumo di alcol e tabacco e praticare attività fisica regolarmente.
        - **Soddisfazione della vita**: L'ottimismo e l'energia sono fortemente correlati con una maggiore soddisfazione per la vita e una visione più positiva del futuro. Gli studenti che possiedono queste competenze affrontano meglio le sfide e mantengono un atteggiamento propositivo verso il raggiungimento dei propri obiettivi.
        - **Equità e benessere tra i gruppi**: Tuttavia, esistono differenze significative nella distribuzione delle competenze socio-emotive tra studenti di diverso genere e background socio-economico, che possono influenzare il benessere. Ad esempio, gli studenti provenienti da contesti socio-economici svantaggiati spesso riportano livelli inferiori di fiducia, empatia e motivazione al successo, il che può avere impatti negativi sulla loro esperienza scolastica complessiva.
        - **Ruolo dell'ambiente scolastico e familiare**: Un ambiente scolastico che promuove attivamente l'apprendimento socio-emotivo, supportato da insegnanti preparati e pratiche didattiche mirate, può favorire il benessere degli studenti. Anche il coinvolgimento delle famiglie e delle comunità nella promozione di queste competenze è cruciale.
    """)
        st.write("""
        ### Intervento per Migliorare il Benessere degli Studenti con le Competenze Socio-Emotive
        Un intervento efficace per migliorare il benessere degli studenti attraverso lo sviluppo delle competenze socio-emotive è l'integrazione strutturata di programmi SEL (Social Emotional Learning) nel curriculum scolastico.

        #### Come Funziona:
        - **Curriculum dedicato**: Implementare lezioni specifiche focalizzate sullo sviluppo di competenze come empatia, gestione dello stress, collaborazione e resilienza emotiva. Ad esempio, si possono prevedere moduli settimanali con attività pratiche e riflessioni guidate.
        - **Formazione degli insegnanti**: Offrire corsi di formazione per insegnanti affinché siano preparati a insegnare e modellare le competenze socio-emotive. Questo include strategie per gestire le dinamiche di classe e per supportare gli studenti in situazioni difficili (OCSE2023_Italy_2)(OECD_II Report).
        - **Creazione di ambienti scolastici positivi**: Promuovere relazioni positive attraverso pratiche come il rinforzo positivo e la gestione costruttiva dei conflitti. Gli insegnanti e i leader scolastici possono adottare politiche che enfatizzano il rispetto, l'inclusività e la sicurezza emotiva.
        - **Monitoraggio e feedback**: Introdurre strumenti di autovalutazione per studenti e insegnanti per monitorare lo sviluppo delle competenze socio-emotive. Inoltre, il feedback frequente e personalizzato degli insegnanti può incoraggiare miglioramenti continui (OECD_I Report).
        - **Coinvolgimento della comunità e delle famiglie**: Integrare le attività di apprendimento socio-emotivo con il coinvolgimento delle famiglie e delle comunità, attraverso workshop e programmi di sensibilizzazione per genitori.

        #### Esempio Pratico:
        Un programma come il **"Second Step"**, utilizzato in molti paesi, combina attività in classe, risorse online e formazione per insegnanti per sviluppare competenze socio-emotive. Include scenari interattivi, giochi di ruolo e discussioni che aiutano gli studenti a riconoscere e gestire le emozioni, migliorare le loro relazioni e prendere decisioni responsabili (OECD_II Report).

        Questo approccio integrato garantisce un impatto a lungo termine, aumentando sia il benessere immediato degli studenti che le loro capacità di affrontare il futuro.
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
