from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from config.settings import Settings
from config.logging_config import setup_logger
from typing import Union
import requests

logger = setup_logger("llm")
# config_settings = Settings()

# Cache to track if Ollama is available
_ollama_available = None


def check_ollama_availability(config_settings: Settings = None) -> bool:
    """
    Check if Ollama service is available and responding.
    Caches the result to avoid repeated checks.
    """
    global _ollama_available

    # Return cached result if already checked
    if _ollama_available is not None:
        return _ollama_available

    try:
        logger.info(f"Checking Ollama availability at {config_settings.ollama_base_url}...")
        response = requests.get(
            f"{config_settings.ollama_base_url}/api/tags",
            timeout=3
        )
        _ollama_available = response.status_code == 200

        if _ollama_available:
            logger.info("✓ Ollama service is available and responding")
        else:
            logger.warning(f"✗ Ollama service returned status code: {response.status_code}")

        return _ollama_available
    except requests.exceptions.RequestException as e:
        logger.warning(f"✗ Ollama service is not available: {str(e)}")
        logger.info("Will use Groq models as fallback")
        _ollama_available = False
        return False


def get_llm_with_fallback(
    ollama_model: str,
    groq_model: str,
    model_type: str,
    temperature: float = 0,
    config_settings: Settings = None
) -> Union[ChatOllama, ChatGroq]:
    """
    Try to initialize Ollama model first, fall back to Groq if unavailable.

    Args:
        ollama_model: Name of the Ollama model
        groq_model: Name of the Groq model (fallback)
        model_type: Type of model (for logging)
        temperature: Temperature setting for the model

    Returns:
        Either ChatOllama or ChatGroq instance
    """
    # Check if Ollama is available
    if config_settings and config_settings.use_ollama and check_ollama_availability(config_settings=config_settings):
        try:
            logger.info(f"Initializing {model_type} with Ollama model: {ollama_model}")

            # Try to initialize Ollama model
            llm = ChatOllama(
                model=ollama_model,
                base_url=config_settings.ollama_base_url,
                temperature=temperature
            )

            # Test the model with a simple query to ensure it works
            try:
                test_response = llm.invoke("test")
                logger.info(f"✓ {model_type} successfully initialized with Ollama ({ollama_model})")
                return llm
            except Exception as test_error:
                logger.warning(f"✗ Ollama model {ollama_model} failed test: {str(test_error)}")
                raise test_error

        except Exception as e:
            logger.warning(f"Failed to initialize Ollama model {ollama_model}: {str(e)}")
            logger.info(f"Falling back to Groq model: {groq_model}")

    # Fallback to Groq
    logger.info(f"Initializing {model_type} with Groq model: {groq_model}")
    llm = ChatGroq(
        model=groq_model,
        temperature=temperature,
        api_key=config_settings.groq_api_key
    )
    logger.info(f"✓ {model_type} successfully initialized with Groq ({groq_model})")
    return llm

def get_supervisor_llm(config_settings: Settings) -> Union[ChatOllama, ChatGroq]:
    """Get supervisor LLM with Ollama primary and Groq fallback."""
    return get_llm_with_fallback(
        ollama_model=config_settings.supervisor_ollama_model,
        groq_model=config_settings.supervisor_model,
        model_type="Supervisor Model",
        temperature=0,
        config_settings=config_settings
    )

def get_general_llm(config_settings) -> Union[ChatOllama, ChatGroq]:
    """Get general LLM with Ollama primary and Groq fallback."""
    return get_llm_with_fallback(
        ollama_model=config_settings.general_ollama_model,
        groq_model=config_settings.general_model,
        model_type="General Model",
        temperature=0,
        config_settings=config_settings
    )

def get_research_llm(config_settings) -> Union[ChatOllama, ChatGroq]:
    """Get research LLM with Ollama primary and Groq fallback."""
    return get_llm_with_fallback(
        ollama_model=config_settings.research_ollama_model,
        groq_model=config_settings.research_model,
        model_type="Research Model",
        temperature=0,
        config_settings=config_settings
    )

def get_coding_llm(config_settings) -> Union[ChatOllama, ChatGroq]:
    """Get coding LLM with Ollama primary and Groq fallback."""
    return get_llm_with_fallback(
        ollama_model=config_settings.coding_ollama_model,
        groq_model=config_settings.coding_model,
        model_type="Coding Model",
        temperature=0,
        config_settings=config_settings
    )
