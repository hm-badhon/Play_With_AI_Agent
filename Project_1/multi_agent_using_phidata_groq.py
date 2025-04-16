import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
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

finance_agent = Agent(
    name="Finance Agent",
    description= "Your task is to find the finance information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, 
                      company_info=True, company_news=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
    debug_mode= True
    )


bai_agent_team = Agent(
    team = [web_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instruction = ["Always include sources","Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
    debug_mode= True

)

bai_agent_team.print_response("Summarize analyst recommendations and share the latest news for NVDIA", stream =True)