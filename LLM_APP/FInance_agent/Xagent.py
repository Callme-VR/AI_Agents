
from dotenv import load_dotenv
load_dotenv()
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.os import AgentOS

agent = Agent(
    name="Groq Ai Financial Agent",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[DuckDuckGoTools(), YFinanceTools()],
    instructions=[
        "Always use the Tables to display Financial/numerical Data.",
        "For text data use bullet point and small paragraph"
    ],
    debug_mode=True,
    markdown=True
)

agent_os = AgentOS(agents=[agent])

if __name__ == "__main__":
    agent_os.serve(app="Xagent:agent_os.get_app", reload=True)