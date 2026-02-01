from sys import exception
import streamlit as st
import requests
import fitz     # for pdf file reading  and pdf parsing 

st.set_page_config(page_title="Resume Job Matcher", page_icon=":briefcase:", layout="centered")

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


def get_text_from_file(file_name):
    if file_name.type == "application/pdf":
        file_text=extract_text_from_pdf(file_name)
    else:
        file_text=file_name.read().decode("utf-8")
    return file_text


    # upload the Resume with Pdf form of local file system and file Uploader function

resume_file=st.file_uploader("Upload your Resume (PDF)", type=["pdf","txt"])
job_file=st.file_uploader("upload the Job Description (PDF)", type=["pdf","txt"])

if st.button("Match Resume with Job Description"):
    if resume_file and job_file:
        # extract the Resume Text from the Resume File
        resume_text=get_text_from_file(resume_file)

        # extract from job description text from the job description file
        job_text=get_text_from_file(job_file)


        # prompt for the LLm

         # Prompt
        Prompt = f"""
        You are an AI career assistant.
        
        Resume:
        {resume_text}

        Job Description:
        {job_text}

        Please analyze and return:
        1. A **Fit Score** (0-100%) of how well this resume matches the job.
        2. Key strengths (resume areas that align well).
        3. Specific recommendations to improve the resume to better fit the job.
        Format neatly in Markdown.
        """

        try:
            with st.spinner("⏳ Analyzing The Resume vs Job Desciptions.. "):
               response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "gemma3:4b", "prompt": Prompt, "stream": False},
                )
            data=response.json()
            output=data.get("response","No response From model.")
                # show the Result 

            st.subheader("Match Analysis")
            st.markdown(output)

            st.session_state["resume_match"]=output


        except Exception as e:
                st.error(f"an Error Occured:{str(e)}")
                
    else:
        st.warning("please uplod the Resume again resume and job desciption")



# download the Report of this project
if "resume_match" in st.session_state:
    st.download_button(
        "Dowload Match Report",
        st.session_state['resume_match'],
        file_name="resume_match_report.md",
        mime="text/markdown"
    )