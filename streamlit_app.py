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

# Ask the user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    # ---- PART 1: FORMULA-BASED INTERACTIVE DASHBOARD ----
    st.header("📐 Part 1: Formula-Based Interactive Dashboard")

    # Dropdown options
    option1_values = [10, 20, 30, 40, 50]
    option2_values = [5, 15, 25, 35, 45]
    option3_values = [1, 2, 3, 4, 5]

    # Sidebar for inputs
    st.sidebar.header("Input Parameters")
    option1 = st.sidebar.selectbox("Select Value for Option 1", option1_values)
    option2 = st.sidebar.selectbox("Select Value for Option 2", option2_values)
    option3 = st.sidebar.selectbox("Select Value for Option 3", option3_values)

    # Formula calculation
    formula_result = (option1 + option2) * option3

    # Define ranges and messages
    ranges = {
        (0, 99): "The result is less than 100. Everything looks good!",
        (100, 199): "The result is between 100 and 200. Be cautious!",
        (200, float('inf')): "The result is greater than 200. Immediate action is needed!"
    }

    # Function to get the message
    def get_message(value):
        for (low, high), message in ranges.items():
            if low <= value <= high:
                return message

    # Display the message
    st.write("### Formula Calculation")
    st.write(f"Formula: `(Option 1 + Option 2) * Option 3`")
    st.write(f"Result: `{formula_result}`")

    message = get_message(formula_result)
    if "less than 100" in message:
        st.success(message)
    elif "between 100" in message:
        st.warning(message)
    else:
        st.error(message)

    # Debug information
    with st.expander("Debug Information"):
        st.write(f"Option 1 Selected: `{option1}`")
        st.write(f"Option 2 Selected: `{option2}`")
        st.write(f"Option 3 Selected: `{option3}`")
        st.write(f"Formula Result: `{formula_result}`")

import os
import pdfplumber
import pandas as pd

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
