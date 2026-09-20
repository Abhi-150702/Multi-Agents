from langchain.agents import create_agent

from models.llm import get_research_llm
from agents.research.prompt import RESEARCH_AGENT_SYSTEM_PROMPT

from tools.research.web.duckduckgo_search import duckduckgo_search
from tools.research.web.google_search import google_search
from tools.research.web.webpage import read_webpage
from tools.research.web.youtube import youtube_search
from tools.research.web.youtube_transcripts import youtube_transcript

from tools.research.code.github import github_search
from tools.research.academic.arxiv import arxiv_search

from config.settings import Settings
from config.logging_config import setup_logger
logger = setup_logger('research_agent')

tools = [
    duckduckgo_search,
    google_search,
    read_webpage,
    youtube_search,
    youtube_transcript,
    github_search,
    arxiv_search
]



def create_research_agent(config_settings: Settings = None) -> create_agent:
    logger.info("Initializing Research Agents!")
    logger.info(f"Registered {len(tools)} Tools with Research Agent")
    return create_agent(
        model=get_research_llm(config_settings),
        tools = tools,
        system_prompt=RESEARCH_AGENT_SYSTEM_PROMPT
    )
