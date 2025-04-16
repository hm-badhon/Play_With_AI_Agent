
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.playground import Playground, serve_playground_app

load_dotenv()
web_search_agent = Agent(
    name = "Web Search agent for B-Ai",
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

app = Playground(agents=[finance_agent, web_search_agent]).get_app()

if __name__ =="__main__":
    serve_playground_app("playground:app", reload=True)