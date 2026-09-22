from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key : str
    google_api_key : str
    google_cse_id : str

    # Groq models (fallback)
    general_model: str
    research_model: str
    coding_model: str
    supervisor_model: str

    # Ollama models (primary)
    general_ollama_model: str
    research_ollama_model: str
    coding_ollama_model: str
    supervisor_ollama_model: str

    # Ollama configuration
    ollama_base_url: str
    use_ollama: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

