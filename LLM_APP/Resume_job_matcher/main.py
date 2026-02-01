import streamlit as st
import requests
import fitz     # for pdf file reading  and pdf parsing 

st.Set_page_Config(page_title="Resume Job Matcher", page_icon=":briefcase:", layout="Centered")

st.title("Resume Job Matcher")

st.sidebar.info("""
This app uses a local LLM via **Ollama**.
1. Install Ollama: https://ollama.ai
2. Verify the ollama CLI works, by running the below commands in your terminal:
    2.1. Start the Ollama server: `ollama serve` on separate terminal.
    2.2. Run a model (e.g., `ollama pull llama3`).
    2.3. Verify local LLM llama is listed using `ollama list`.
    2.4. Run the streamlit run app.py command to start this app in another terminal.
3. Upload a Resume + Job Description to get a fit score and suggestions.
""")


# helper function to extract text from pdf file

def extract_text_from_pdf(file_path):
    text=""
    with fitz.open(stream=file_path, filetype="pdf") as doc:
        for page in doc:
            text+=page.get_text()
        return text
        