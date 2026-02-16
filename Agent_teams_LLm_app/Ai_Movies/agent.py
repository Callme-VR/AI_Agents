# Import the required libraries
import streamlit as st
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.team import Team
from agno.models.groq import Groq
from agno.models.google import Gemini
from textwrap import dedent

st.title("Movies Script Production Agent")
st.caption("Bring your movie ideas to life with a production team")

# get API keys from user
google_api_key = st.text_input("Enter Google API key", type="password")
groq_api_key = st.text_input("Enter Groq API key", type="password")

if google_api_key and groq_api_key:

    script_writer = Agent(
        name="ScriptWriter",
        model=Gemini(
            id="gemini-3-pro-preview",
            api_key=google_api_key
        ),
        description=dedent("""
            You are an expert screenplay writer. Given a movie idea and genre,
            develop a compelling script outline with character descriptions and key plot points.
        """),
        instructions=[
            "Write a script outline with 3-5 main characters and key plot points.",
            "Outline the three-act structure and suggest 2-3 twists.",
            "Ensure the script aligns with the specified genre and target audience.",
        ],
    )

    casting_director = Agent(
        name="CastingDirector",
        model=Groq(
            id="openai/gpt-oss-120b",
            api_key=groq_api_key
        ),
        description=dedent("""
            You are a talented casting director. Given a script outline and character descriptions,
            suggest suitable actors for the main roles based on their past performances.
        """),
        instructions=[
            "Suggest 2-3 actors for each main role.",
            "Provide a brief explanation for each casting suggestion.",
            "Match actors based on role personality and past performances.",
            "Consider diversity and representation in your casting choices.",
        ],
    )

    movies_producers = Team(
        name="MoviesProducers",
        model=Gemini(id="gemini-3-pro-preview", api_key=google_api_key),
        members=[script_writer, casting_director],
        description="Experienced movie producer overseeing script and casting",
        instructions=[
            "Ask ScriptWriter for a script outline based on the movie idea.",
            "Pass the outline to CastingDirector for casting suggestions.",
            "Summarize the script outline and casting suggestions.",
            "Provide a concise movie concept overview."
        ],
        markdown=True,
    )

    # input field for the request query
    movie_idea = st.text_area("Describe the movie idea.")
    genre = st.selectbox(
        "Select movie genre:",
        ["Action", "Comedy", "Drama", "Sci-Fi", "Horror", "Romance", "Thriller"]
    )
    target_audience = st.selectbox(
        "Select target audience:",
        ["General", "Children", "Teenagers", "Adults", "Mature"]
    )
    estimated_runtime = st.slider("Estimated Runtime (in Minutes)", 60, 180, 120)

    # process the movie concept
    if st.button("Develop Movie Concept"):
        with st.spinner("Developing movie concept..."):

            input_text = (
                f"Movie idea: {movie_idea}, "
                f"Genre: {genre}, "
                f"Target audience: {target_audience}, "
                f"Runtime: {estimated_runtime} minutes"
            )

            response: RunOutput = movies_producers.run(input_text, stream=False)
            st.write(response.content)
