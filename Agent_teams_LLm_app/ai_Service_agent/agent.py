import os
from typing import Literal, List

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
    
    architecture_type: Literal[
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
       
        specification = {
            "project_name": project_analysis["name"],
            "architecture_type": self.architecture_type,
            "technologies": self.core_technologies,
            "scalability_features": self.scalability_features,
        }
        self.context.set("specification", specification)
        return f"Technical specification created successfully for {project_analysis['name']}"
   
   
   
def init_session_state()->None:
     """Initialize session state"""
     if "message" not in st.session_state:
         st.session_state.message=[]
     if "api_key" not in st.session_state:
         st.session_state.api_key=None
        
        
def main()->None:
     st.set_page_config(page_title="AI Service Agent", layout="wide", page_icon=":robot_face:")
     init_session_state()
     
     # api configuration
     
     with st.sidebar:
          st.header("API Service Agent")
          st.subheader("API Configuration")
          api_key=st.text_input("API Key", type="password", value=st.session_state.api_key)
          
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
          project_name=st.text_input("Project Name")
          project_description=st.text_area("project",help="Describe the Project,its goal,any specific environment,any specific features")
          
          col1,col2=st.columns(2)
          with col1:
               project_type=st.selectbox("Project Type", ["Web Application", "Mobile Application", "Desktop Application", "API Development", "Data Analytics", "AI/ML Solution", "Other"])
               timeline=st.selectbox("Timeline", ["1 month", "2 months", "3 months", "4 months", "5 months", "6 months"])
          with col2:
               project_budget=st.selectbox("Project Budget", ["$10k-50k", "$50k-100k", "$100k-200k", "$200k-500k", "$500k-1M", "$1M+"])
               
               priority=st.selectbox("Priority", ["High", "Medium", "Low"])
               
          tech_requirements=st.text_area("Technical Requirements", help="Enter any specific technical requirements")
          
          special_considerations=st.text_area("Special Considerations", help="Enter any special considerations")
          
          submit_button=st.form_submit_button("Analyze Project")
          
          if submit_button and project_name and project_description:
               try:
                    ceo = Agent(
                        name="Project Director",
                        description="You are a CEO of multiple companies in the past and have a lot of experience in evaluating projects and making strategic decisions.",
                        instructions="""You are an experienced CEO who evaluates projects. Follow these steps strictly:

1. FIRST, use the AnalyzeProjectRequirements tool with:
   - project_name: The name from the project details
   - project_description: The full project description
   - project_type: The type of project (Web Application, Mobile App, etc)
   - project_budget: The specified budget range

2. WAIT for the analysis to complete before proceeding.

3. Review the analysis results and provide strategic recommendations.
""",
                        tools=[AnalyzeProjectRequirements],
                        model_settings=ModelSettings(temperature=0.7, max_tokens=2500),
                    )
                    
                    cto = Agent(
                        name="Technical Architect",
                        description="Senior technical architect with experience in designing scalable and secure systems.",
                        instructions="""You are a technical architect. Follow these steps strictly:

1. WAIT for the project analysis to be completed by the CEO.

2. Use the CreateTechnicalSpecification tool with:
   - architecture_type: Choose from Monolithic/Microservices/Serverless/Event-driven/Other
   - core_technologies: List main technologies
   - scalability_features: Choose High/Medium/Low based on project needs

3. Review the technical specification and provide additional recommendations.
""",
                        tools=[CreateTechnicalSpecification],
                        model_settings=ModelSettings(temperature=0.7, max_tokens=2500),
                    )
                    
                    product_manager = Agent(
                         name="Product Manager",
                         description="Experienced product manager with a track record of delivering successful products.",
                         instructions="""You are a product manager. Follow these steps strictly:

- Manage project scope and timeline giving the roadmap of the project
- Define product requirements and you should give potential products and features that can be built for the startup
""",
                         model_settings=ModelSettings(temperature=0.7, max_tokens=2500),
                    )
                    
                    developer = Agent(
                         name="Lead Developer",
                         description="Senior developer with full stack expertise.",
                         instructions="""You are a lead developer. Follow these steps strictly:

- Plan technical implementation
- Provide effort estimates
- Review technical feasibility
""",
                         model_settings=ModelSettings(temperature=0.3, max_tokens=2500),
                    )
                    
                    client_manager = Agent(
                         name="Client Success Manager",
                         description="Experienced client manager focused on project delivery.",
                         instructions="""You are a client success manager. Follow these steps strictly:

- Ensure client satisfaction
- Manage expectations
- Handle feedback
""",
                         model_settings=ModelSettings(temperature=0.3, max_tokens=2500),
                    )
                    
                    agency = Agency(
                         agents=[
                              ceo,
                              cto,
                              product_manager,
                              developer,
                              client_manager,
                         ],
                         communication_flows=[
                              (ceo, cto),
                              (ceo, product_manager),
                              (ceo, developer),
                              (ceo, client_manager),
                              (cto, developer),
                              (product_manager, developer),
                              (product_manager, client_manager),
                         ],
                    )
                    
                    # prepare project informations
                    
                    project_info={
                         "name":project_name,
                    }
                    
                    
               except Exception as e:
                    st.error(f"Error creating agents: {str(e)}")