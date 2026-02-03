📄 Resume & Job Matcher
🚀 Overview
This app allows you to upload a Resume and a Job Description, then uses an LLM to:

✅ Provide a Fit Score (0–100%)
💪 Highlight strengths in the resume
📝 Suggest improvements tailored to the job
A great tool for job seekers to optimize resumes for each application.

🛠️ Tech Stack
Python
Streamlit – for UI
Ollama + LLM (e.g., kimi-k2.5:cloud) – for analysis
PyMuPDF – for PDF parsing
⚡ Setup Instructions
Install dependencies:
pip install -r requirements.txt
Install Ollama and run a model (e.g. kimi-k2.5:cloud): ollama run kimi-k2.5:cloud
Start the app: streamlit run main.py