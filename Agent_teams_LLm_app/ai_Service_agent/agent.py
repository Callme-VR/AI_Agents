import os
from typing import Literal
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
     