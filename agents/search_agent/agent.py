from google.adk.agents import Agent
from google.adk.tools import google_search

from dotenv import load_dotenv

load_dotenv()

search_agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    description="Agente especializado em buscar informações sobre investimentos usando busca na web.",
    instruction="""
    Você é um agente especializado em buscar informações sobre investimentos no mercado financeiro brasileiro usando ferramentas de busca na web.
    """,
    tools=[google_search],
)
