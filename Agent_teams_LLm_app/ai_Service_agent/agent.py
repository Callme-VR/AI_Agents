import os
from typing import Literal

from plotly.graph_objs import layout
from agency_swarm import Agent, Agency, BaseTool, ModelSettings
from pydantic import Field
import streamlit as st


class AnalyzeProjectRequirements(BaseTool):
    """Analyze Project Requirements and Feasibility"""

    project_name: str = Field(..., description="Name of the Project")

    project_description: str = Field(..., description="Description of the Project")

    project_type: Literal[
        "Web Application",
        "Mobile Application",
        "Desktop Application",
        "API Development",
        "Data Analytics",
        "AI/ML Solution",
        "Other"
    ] = Field(..., description="Type of the Project")

    project_budget: Literal[
        "$10k-50k",
        "$50k-100k",
        "$100k-200k",
        "$200k-500k",
        "$500k-1M",
        "$1M+"
    ] = Field(..., description="Budget of the Project")

    class ToolConfig:
        name = "Analyze Project Requirements"
        description = "Analyze Project Requirements and Feasibility"
        on_call_at_a_time = True

    def run(self) -> str:
        """Analyzing Project Requirements"""

        if self.context.get("project_analysis", None) is not None:
            raise ValueError("Project analysis is already stored in state")

        analysis = {
            "name": self.project_name,
            "type": self.project_type,
            "complexity": "high",
            "timeline": "3 months",
            "budget_feasibility": "within range",
            "requirements": [
                "Scalable architecture",
                "Security",
                "API integration"
            ]
        }

        self.context.set("project_analysis", analysis)

        return "Project analysis completed. Please proceed with technical specification."



class CreateTechnicalSpecification(BaseTool):
    """Create Technical Specification"""
    
    artectecture_type=Literal[
         "Monolithic",
         "Microservices",
         "Serverless",
         "Event-driven",
         "Other"
    ] = Field(..., description="Type of the Architecture")
    
    core_technologies: List[str] = Field(..., description="Core Technologies")
    
    scalability_features: Literal[
        "Low",
        "Medium",
        "High"
    ] = Field(..., description="Scalability")
    
    class ToolConfig:
        name = "Create Technical Specification"
        description = "Create Technical Specification"
        on_call_at_a_time = True
        
    def run(self) -> str:
        """Creating Technical Specification"""
        
        project_analysis=self.context.get("project_analysis", None)
        
        
        if project_analysis is None:
            raise ValueError("Project analysis is not stored in state")
       
        specification={
            project_name:project_analysis["name"],
            architecture_type:self.artectecture_type,
            technologies:self.core_technologies.spli(","),
            scalability_features:self.scalability_features,
       }
        self.context.set("specification", specification)
        return "Technical specification created successfully{project_analysis['name']}"
   
   
   
def init_session_state()->None:
     """Initialize session state"""
     if "message" not in st.session_state:
         st.session_state.message=[]
     if "api_key" not in st.session_state:
         st.session_state.api_key=None
        
        
def main()->None:
     st.page_config(page_title="AI Service Agent", layout="wide", page_icon=":robot_face:")
     init_session_state()
     
     # api configuration
     
     with st.sidebar:
          st.header("API Service Agent")
          st.subheader("API Configuration")
          api_key=st.text_input("API Key", type="password", value=st.session_state.api_key, on_change=init_session_state)
          
          if api_key:
               st.session_state.api_key=api_key
               st.success("API Key configured successfully")
               
          else:
               st.warning("API Key is required")
               st.markdown("[Get your API key here](https://platform.openai.com/api-keys)")
               return
          
     # agent configuration using swarn v1
     os.environ["OPENAI_API_KEY"] = st.session_state.api_key
     
     # with project input Form
     
     with st.form(key="project_form"):
          st.subheader("Project Input")
     
     