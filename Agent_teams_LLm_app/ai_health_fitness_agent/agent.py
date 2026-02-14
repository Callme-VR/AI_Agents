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
     with st.expander("Diet Plan",expanded=True):
         col1,col2=st.columns([2,1])
         
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
    with st.expander("Workout Plan",expanded=True):
        col1,col2=st.columns([2,1])
        
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
          gemini_api_key = st.text_input("Gemini API Key", type="password",help="Enter your Gemini API key to enable the agent")
          
          if not gemini_api_key:
               st.warning("Please enter your Gemini API key to enable the agent")
               return
          
          st.success("API key configured successfully!")