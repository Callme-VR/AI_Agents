import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google import Gemini
from agno.run.agent import RunOutput
import streamlit as st
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage


if "GOOGLE_API_KEY" not in st.session_state:
    st.session_state.GOOGLE_API_KEY = None


with st.sidebar:
    st.title("ℹ️ Configuration")

    api_key = st.text_input(
        "Enter your Google API key:",
        type="password",
        value=st.session_state.GOOGLE_API_KEY or "",
    )
    st.caption(
        "Get your API key at: https://aistudio.google.com/apikey 🔑"
    )

    if api_key:
        st.session_state.GOOGLE_API_KEY = api_key
        st.success("API key saved!")
        st.rerun()
    elif st.session_state.GOOGLE_API_KEY:
        st.success("API key is set.")
        if st.button("Reset API key"):
            st.session_state.GOOGLE_API_KEY = None
            st.rerun()
        enable_search = st.checkbox("Enable web search (slower)", value=False)

st.info(
    "This tool provides AI-powered analysis of medical imaging data using "
    "advanced computer vision and radiological expertise."
)
st.warning(
    "⚠ DISCLAIMER: This tool is for educational and informational purposes only. "
    "All analyses should be reviewed by qualified healthcare professionals. "
    "Do not make medical decisions based solely on this analysis."
)

Medical_agent = None
if st.session_state.GOOGLE_API_KEY:
    tools = [DuckDuckGoTools()] if enable_search else []
    Medical_agent = Agent(
        model=Gemini(
            id="gemini-2.5-pro",
            api_key=st.session_state.GOOGLE_API_KEY,
        ),
        tools=tools,
        markdown=True,
    )

if not Medical_agent:
    st.warning("Please configure your API key.")


# prompt for the medical analysis query


query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the patient's medical image and structure your response as follows:


### 1. Image Type & Regions
-specify imaging modality (x-ray/MRI/CT/Ultrasound/etc.)
-identify the patient's anatomical Region and positioning
-comment on image quality and technical Adaquacy

### 2. Key Findings
- List primary observations systematically
- Note any abnormalities in the patient's imaging with precise descriptions
- Include measurements and densities where relevant
- Describe location, size, shape, and characteristics
- Rate severity: Normal/Mild/Moderate/Severe

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level
- List differential diagnoses in order of likelihood
- Support each diagnosis with observed evidence from the patient's imaging
- Note any critical or urgent findings

### 4. Patient-Friendly Explanation
- Explain the findings in simple, clear language that the patient can understand
- Avoid medical jargon or provide clear definitions
- Include visual analogies if helpful
- Address common patient concerns related to these findings

### 5. Research Context
IMPORTANT: Use the DuckDuckGo search tool to:
- Find recent medical literature about similar cases
- Search for standard treatment protocols
- Provide a list of relevant medical links of them too
- Research any relevant technological advances
- Include 2-3 key references to support your analysis

Format your response using clear markdown headers and bullet points. Be concise yet thorough.
"""


st.title("Medical Imaging Sensing for Professional Analysis")
st.write("Upload a medical image for professional analysis.")


# create containers for better organization
upload_container = st.container()
image_container = st.container()
analysis_container = st.container()


with upload_container:
    upload_file = st.file_uploader(
        "Upload medical image",
        type=["jpg", "jpeg", "png", "dicom"],
        help="Supported formats: JPG, JPEG, PNG, DICOM",
    )

resized_image = None
analyze_button = False

if upload_file is not None:
    with image_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = PILImage.open(upload_file)
            width, height = image.size
            aspect_ratio = width / height

            new_width = 450
            new_height = int(new_width / aspect_ratio)
            resized_image = image.resize((new_width, new_height))

            st.image(
                resized_image,
                caption="Uploaded medical image",
                width="stretch",
            )
            analyze_button = st.button(
                "🔍 Analyze Image",
                type="primary",
            )

with analysis_container:
    if analyze_button and resized_image is not None and Medical_agent is not None:
        with st.spinner("Analyzing the image... Please wait"):
            try:
                temp_path = "Temp_resized_image.png"
                resized_image.save(temp_path)
                agno_image = AgnoImage(filepath=temp_path)

                import traceback

                # run analysis
                response: RunOutput = Medical_agent.run(query, images=[agno_image])

                if response and response.content:
                    st.markdown("### 📋 Analysis Results")
                    st.markdown("---")
                    st.markdown(response.content)
                    st.markdown("---")
                    st.caption(
                        "Note: This analysis is generated by AI and should be reviewed by "
                        "a qualified healthcare professional."
                    )
                else:
                    st.error("Received empty response from the model. Please try again.")
            except Exception as e:
                st.error(f"Analysis error: {e}")
                with st.expander("Debug Details"):
                    st.code(traceback.format_exc())
    elif upload_file is None:
        st.info("👆 Please upload a medical image to begin analysis.")