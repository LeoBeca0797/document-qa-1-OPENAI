import os
import streamlit as st
import pandas as pd
import pdfplumber
import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ---- GLOBAL CONFIGURATION ----
st.title("📊 Interactive Dashboard")
st.write("This dashboard combines two functionalities:")
st.markdown(
    """
1. **Formula-Based Interactive Dashboard**: Select values to compute a formula and see the results dynamically.
2. **Document-Based RAG Question Answering**: Upload a document, and ask questions about its contents using OpenAI's ChatGPT API.
"""
)

'''# Ask the user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.", icon="🗝️")
else:
    openai.api_key = openai_api_key
'''
# ---- PART 1: FORMULA-BASED INTERACTIVE DASHBOARD WITH STUDENT MANAGEMENT ----
st.header("📐 Part 1: Formula-Based Interactive Dashboard with Student Management")

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

import os
import pdfplumber
import pandas as pd
'''
# ---- PART 2: DOCUMENT-BASED RAG QUESTION ANSWERING ----
st.header("📄 Part 2: Document-Based RAG Question Answering")

# Function to preload frequently used documents
@st.cache_data
def load_preloaded_documents():
    """Load frequently used documents."""
    preloaded_documents = {
        "Document 1": "./preloaded_docs/doc1.txt",
        "Document 2": "./preloaded_docs/doc2.pdf",
        "Document 3": "./preloaded_docs/doc3.xlsx"
    }
    documents = {}
    for name, path in preloaded_documents.items():
        if not os.path.exists(path):
            st.warning(f"File not found: {path}")
            continue

        file_type = path.split(".")[-1].lower()
        try:
            if file_type == "pdf":
                with pdfplumber.open(path) as pdf:
                    text = "".join([page.extract_text() for page in pdf.pages])
            elif file_type == "txt":
                with open(path, "r") as file:
                    text = file.read()
            elif file_type == "xlsx":
                df = pd.read_excel(path)
                text = "\n".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))
            else:
                text = None
                st.warning(f"Unsupported file format: {path}")
            documents[name] = text
        except Exception as e:
            st.error(f"Error processing {path}: {e}")
    return documents

# Allow users to upload a document or choose from preloaded ones
st.write("Upload a document or select from preloaded options.")
uploaded_file = st.file_uploader("Upload a document (.txt, .md, .pdf, .xlsx)", type=("txt", "md", "pdf", "xlsx"))
preloaded_documents = load_preloaded_documents()
selected_doc = st.selectbox("Choose a preloaded document (Optional)", options=["None"] + list(preloaded_documents.keys()))

# Determine the document text to use
if uploaded_file:
    document_text = extract_text_from_file(uploaded_file)
    st.write("Using the uploaded document.")
elif selected_doc != "None":
    document_text = preloaded_documents[selected_doc]
    st.write(f"Using preloaded document: {selected_doc}")
else:
    document_text = None
    st.warning("Please upload a document or select a preloaded document to continue.")

# Ask the user for a question
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="e.g., Summarize this document.",
    disabled=document_text is None,
)

if document_text and question:
    with st.spinner("Processing your request..."):
        try:
            # Step 2: Generate embeddings for the document chunks
            st.info("Step 2: Generating embeddings for the document...")
            chunk_size = 500
            document_chunks = [
                document_text[i:i + chunk_size]
                for i in range(0, len(document_text), chunk_size)
            ]

            embeddings = []
            for chunk in document_chunks:
                response = openai.Embedding.create(
                    model="text-embedding-ada-002",
                    input=chunk
                )
                embeddings.append(response["data"][0]["embedding"])

            # Step 3: Generate embeddings for the question
            st.info("Step 3: Generating embeddings for the question...")
            question_embedding_response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=question
            )
            question_embedding = question_embedding_response["data"][0]["embedding"]

            # Step 4: Find the most relevant chunk using cosine similarity
            st.info("Step 4: Finding the most relevant chunk...")
            similarities = cosine_similarity([question_embedding], embeddings)
            most_relevant_chunk_index = np.argmax(similarities)
            most_relevant_chunk = document_chunks[most_relevant_chunk_index]

            # Step 5: Use ChatGPT API to answer the question
            st.info("Step 5: Generating the answer using ChatGPT API...")
            completion_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Replace with "gpt-4" if needed
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Based on the following context, answer the question:\n\nContext: {most_relevant_chunk}\n\nQuestion: {question}"}
                ]
            )
            answer = completion_response["choices"][0]["message"]["content"]

            # Display the result
            st.success("Here is the answer:")
            st.write(f"**Answer:** {answer}")

            # Debug Information
            with st.expander("Debug Information"):
                st.write(f"**Most Relevant Chunk:**\n{most_relevant_chunk}")
                st.json({"similarities": similarities.tolist()})

        except Exception as e:
            st.error(f"An error occurred: {e}")
'''
