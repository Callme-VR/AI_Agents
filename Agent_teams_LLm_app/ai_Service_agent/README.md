# AI Service Agent

A multi-agent AI system built with [agency-swarm](https://github.com/VRSEN/agency-swarm) and Streamlit for automated project analysis and technical specification generation.

## Overview

This application simulates a complete project evaluation team consisting of:
- **CEO (Project Director)** - Strategic project evaluation and requirements analysis
- **CTO (Technical Architect)** - Technical specification and architecture design
- **Product Manager** - Product roadmap and market fit analysis
- **Lead Developer** - Technical implementation planning and effort estimates
- **Client Success Manager** - Client satisfaction and expectation management

## Features

- Multi-agent AI collaboration for comprehensive project analysis
- Interactive Streamlit web interface
- Tab-based results display for each agent's analysis
- Session state management with chat history
- Project requirements analysis with customizable parameters
- Technical specification generation
- Product roadmap planning
- Client success strategy development

## Installation

1. Clone the repository or navigate to the project directory
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies:
  - `agency-swarm==1.7.0`
  - `streamlit`
  - `python-dotenv==1.1.1`

## Usage

1. Run the application:
   ```bash
   streamlit run agent.py
   ```

2. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Enter your OpenAI API key in the sidebar

4. Fill in the project details:
   - Project Name
   - Project Description
   - Project Type (Web/Mobile/Desktop/API/Data Analytics/AI-ML/Other)
   - Timeline (1-6 months)
   - Budget Range ($10k - $1M+)
   - Priority (High/Medium/Low)
   - Technical Requirements (optional)
   - Special Considerations (optional)

5. Click "Analyze Project" to run the multi-agent analysis

6. View results in the tabs:
   - CEO Strategic Analysis
   - CTO Technical Specifications
   - Product Manager's Plan
   - Lead Developer's Development Plan
   - Client Success Strategy

## How It Works

The system uses agency-swarm's multi-agent framework where:

1. **CEO Agent** first analyzes project requirements using the `AnalyzeProjectRequirements` tool, storing results in a shared context
2. **CTO Agent** retrieves the analysis and creates technical specifications using the `CreateTechnicalSpecification` tool
3. **Product Manager, Developer, and Client Manager** agents provide their specialized analyses based on the project information
4. All responses are displayed in organized tabs and saved to session history

## Project Structure

```
ai_Service_agent/
├── agent.py              # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── venv/                # Virtual environment (not tracked)
```

## Tools

### AnalyzeProjectRequirements
- Stores project analysis in shared context
- Captures: name, description, type, timeline, budget, priority, requirements
- Validates against duplicate analysis

### CreateTechnicalSpecification
- Creates technical specifications based on CEO's analysis
- Defines: architecture type, core technologies, scalability features
- Depends on project analysis being completed first

## Configuration

- API Key: Enter in the sidebar or set `OPENAI_API_KEY` environment variable
- Model Settings: Each agent uses temperature 0.3-0.7, max_tokens 2500

## Notes

- The application requires an active OpenAI API key with available credits
- Analysis results are stored in session state and can be viewed via the sidebar "Run Analysis" checkbox
- Use the "Clear" button in the sidebar to reset the session state

## License

MIT License

## Author

AI Agent Development Team
