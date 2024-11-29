import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# ---- Set up cookies manager ----
cookies = EncryptedCookieManager(
    prefix="pisa_app_",  # Add a prefix to avoid conflicts
    password="a-very-secret-key"  # Replace with a strong secret key
)
if not cookies.ready():
    st.stop()

# ---- Check Login Status ----
if "logged_in" not in cookies:
    cookies["logged_in"] = "false"

if cookies["logged_in"] == "false":
    st.title("Accesso al PISA")
    username = st.text_input("Inserisci il tuo nome utente", placeholder="Es: insegnante1")
    password = st.text_input("Inserisci la tua password", type="password", placeholder="Es: password123")

    if st.button("Accedi"):
        if username == "insegnante1" and password == "password123":
            cookies["logged_in"] = "true"
            cookies.save()  # Save cookies

            # Use JavaScript to reload the page automatically
            st.write(
                """
                <script>
                setTimeout(function() {
                    window.location.reload();
                }, 2000);  // Reload after 2 second
                </script>
                """,
                unsafe_allow_html=True,
            )
            st.success("Accesso effettuato con successo! Ricaricamento automatico in corso...")
        else:
            st.error("Nome utente o password errati. Riprova.")
    st.stop()

# ---- Main Application ----
st.header("Benvenuta sul PISA, il tuo aiuto nell'interpretazione e la raccolta delle capacità socio-emotive!")

# Persistent storage for student data
if "student_data" not in st.session_state:
    st.session_state.student_data = {}

# Sidebar section for viewing added students
st.sidebar.header("Elenco Studenti")
if st.session_state.student_data:
    student_list = list(st.session_state.student_data.keys())
    selected_student = st.sidebar.selectbox("Seleziona uno studente per vedere i dettagli", student_list)
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
student_name = st.text_input("Inserisci il nome dello studente", placeholder="Es: Mario Rossi")

if student_name:
    st.write(f"### Informazioni demografiche di **{student_name}**")

    # Collect demographic data
    age = st.number_input("Inserisci l'età dello studente", min_value=3, max_value=100, value=16, step=1, key="age")
    gender = st.selectbox("Seleziona il genere dello studente", options=["Maschio", "Femmina", "Non-Binario", "Altro"], key="gender")
    grade_level = st.selectbox(
        "Seleziona il livello scolastico dello studente",
        options=["Asilo", "Prima elementare", "Seconda elementare",
