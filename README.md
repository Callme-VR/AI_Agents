# 🤖 AI Agent Universe: Autonomous Intelligence

_Part of the [Master AI Repository](../README.md)_

Welcome to the **AI Agent** workspace. This project focuses on building autonomous and semi-autonomous systems where LLMs act as decision-makers and tool-users to solve complex, multi-step tasks.

---

## 🚀 Key Modules

### 👥 [Multi-Agent Teams](./Agent_teams_LLm_app)

Collaborative environments where multiple agents work together to achieve a common goal.

- **Movies Agent**: Expert in cinema and entertainment.
- **Startup Insight Agent**: Market analysis and startup evaluation.
- **Research Planner**: Orchestrates complex information gathering.
- **Financial & Health Agents**: Specialized advisors for personal management.

### 💼 [Single-Purpose LLM Apps](./LLM_APP)

Focused applications using individual agents for niche utility.

- **Finance Agent**: Real-time financial data tracking and analysis.
- **Resume Job Matcher**: Intelligent HR tool for matching talent to opportunities.
- **Web Scraping Agent**: AI-driven content extraction from dynamic websites.
- **Medical Screening**: Preliminary health analysis workflows.

---

## 🛠️ Technology Stack

- **Frameworks**: LangChain, PydanticAI, PhiData (implied by agent focus).
- **LLMs**: GPT-4, Claude 3.5, Gemini 1.5 Pro.
- **Tools**: Playwright (Scraping), yfinance (Finance), PDFPlumber (Resume Parsing).

---

## 📦 Installation & Usage

1. **Environment Setup**:

   ```bash
   cd Ai_agent
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   .\venv\Scripts\activate  # Windows
   ```

2. **Dependency Management**:
   Each sub-app has its own `requirements.txt`. Navigate to the specific app directory to install:

   ```bash
   cd LLM_APP/web_Scraping_agent
   pip install -r requirements.txt
   ```

3. **Playwright Initialization** (for scraping):
   ```bash
   playwright install
   ```

---

## 🐛 Troubleshooting

### Playwright Issues

If you see a `NotImplementedError`, ensure browser binaries are installed:

```bash
python -m playwright install
```

---

_Created with focus on Agentic Workflows._
