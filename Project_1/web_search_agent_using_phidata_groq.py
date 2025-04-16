import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

load_dotenv()
web_agent = Agent(
    name = "Web agent for B-Ai",
    role="Search the web for the information",
    model = Groq(id='llama-3.3-70b-versatile'),
    tools = [DuckDuckGo()],
    instruction = ["Always include sources"],
    show_tool_calls = True,
    markdown = True,
    debug_mode= True
)


web_agent.print_response("What is the Capital of Bangladesh ?", stream =True)
