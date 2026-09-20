from langchain_groq import ChatGroq
from config.settings import Settings
from config.logging_config import setup_logger

logger = setup_logger("llm")
config_settings = Settings()

def get_supervisor_llm() -> ChatGroq:
    logger.info(f"Initialising Supervisor Model using: {config_settings.supervisor_model}")
    return ChatGroq(
        model=config_settings.supervisor_model,
        temperature=0,
        api_key=config_settings.groq_api_key
    )

def get_general_llm() -> ChatGroq:
    logger.info(f"Initialising General Model using: {config_settings.general_model}")
    return ChatGroq(
        model=config_settings.general_model,
        temperature=0,
        api_key=config_settings.groq_api_key
    )

def get_research_llm() -> ChatGroq:
    logger.info(f"Initialising Research Model using: {config_settings.research_model}")
    return ChatGroq(
        model=config_settings.research_model,
        temperature=0,
        api_key=config_settings.groq_api_key
    )

def get_coding_llm() -> ChatGroq:
    logger.info(f"Initialising Coding Model using: {config_settings.coding_model}")
    return ChatGroq(
        model=config_settings.coding_model,
        temperature=0,
        api_key=config_settings.groq_api_key
    )
