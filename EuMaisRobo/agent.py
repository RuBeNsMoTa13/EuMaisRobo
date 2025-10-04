# EuMaisRobo/agent.py
from google.adk.agents import Agent

from EuMaisRobo.prompt import ROOT_AGENT_INSTRUCTION
from EuMaisRobo.tools import search_news

root_agent = Agent(
    name="EuMaisRobo",
    model="gemini-2.0-flash",
    description="a bot can search news about ai",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[search_news],
)