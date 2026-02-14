import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.run.agent import RunOutput



st.set_page_config(
     page_title="AI Health & Fitness Agent", 
     page_icon="🤖",
     layout="wide",
     initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)


def display_diet_plan(plane_context):
    with st.expander("Diet Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Why this plan works")
            st.write(plane_context.get("why_this_plan_works", ""))
            st.markdown("### Meal Plan")
            st.write(plane_context.get("meal_plan", "Plan not available"))
            
        with col2:
            st.markdown("### ⚠️ Important Considerations")
            considerations = plane_context.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)


def display_fitness_plan(plan_context):
    with st.expander("Workout Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Goals")
            st.write(plan_context.get("goals", "goal not specified"))
            st.markdown("### Exercise Routine")
            st.write(plan_context.get("exercise_routine", "Exercise routine not available"))
        
        with col2:
            st.markdown("### ⚠️ Important Considerations")
            tips = plan_context.get("important_considerations", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.warning(tip)


def main():
    if "dietry_plan" not in st.session_state:
        st.session_state.dietry_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = {}
        st.session_state.plan_generated = False
        
    st.title("AI Health & Fitness Agent")
    st.markdown("""
                <div style="background-color:#f0fff4;padding:1rem;border-radius:0.5rem;">
                    <h2>Welcome to your AI Health & Fitness Agent!</h2>
                    <p>This agent will help you create a personalized diet and workout plan based on your goals and preferences.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("api configurations")
        gemini_api_key = st.text_input("Gemini API Key", type="password", help="Enter your Gemini API key to enable the agent")
        
        if not gemini_api_key:
            st.warning("Please enter your Gemini API key to enable the agent")
            return
        
        st.success("API key configured successfully!")
        
        
    if gemini_api_key:
        try:
            Gemini_model = Gemini(id="gemini-2.0-flash-exp", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"Error initializing Gemini model: {e}")
            return
        st.header("Agent is ready to use!")
        
        
        col1, col2 = st.columns(2)
        
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, step=1, help="Enter your age")
            
            height = st.number_input("Height (cm)", min_value=100, max_value=250.0, step=0.1, help="Enter your height in cm")
            
            activity_level = st.selectbox(
                "Activity Level",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                help="Choose your typical activity level"
            )
            
            dietry_preferences = st.selectbox("Dietry Preferences", 
                                ["Vegan",
                                 "Keto",
                                 "Low Carb",
                                 "Dairy Free",
                                 "Vegetarian",
                                 "Non-Vegetarian",
                                 "Other"], 
                                help="Choose your typical dietry preference")
        with col2:
             weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, step=0.1, help="Enter your weight in kg")
             sex = st.selectbox("Sex", ["Male", "Female", "Other"], help="Choose your sex")
             
             fitness_goal = st.selectbox("Fitness Goal", 
                                        ["Weight Loss", "Muscle Gain", "Maintenance", "Endurance", "Strength"], 
                                        help="Choose your primary fitness goal")
        if st.button("Generate Plan"):
            with st.spinner("Generating your personalized plan..."):
                try:
                     dietry_plan=Agent(
                          name="Dietry Plan Agent",
                          model= Gemini_model,
                           instructions=[
                            "Consider the user's input, including dietary restrictions and preferences.",
                            "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                            "Provide a brief explanation of why the plan is suited to the user's goals.",
                            "Focus on clarity, coherence, and quality of the recommendations.",
                        ]
                           
                     )
                     
                     fitness_agent=Agent(
                          name="Fitness Plan Agent",
                          model= Gemini_model,
                          instructions=[
                            "Provide exercises tailored to the user's goals.",
                            "Include warm-up, main workout, and cool-down exercises.",
                            "Explain the benefits of each recommended exercise.",
                            "Ensure the plan is actionable and detailed.",
                        ]
                     )
                     
                     
                     
                     
                     
                     
                except Exception as e:
                     st.error(f"Error generating plan: {e}")
                     return