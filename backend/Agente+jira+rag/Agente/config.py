from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    # App
    APP_TITLE: str = "Jira AI Card Creator"
    APP_VERSION: str = "1.0.0"
    APP_DEBUG: bool = False

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX: str = "rag_documents"
    ELASTICSEARCH_USER: str = ""
    ELASTICSEARCH_PASSWORD: str = ""
    
    # Embeddings - Modelo optimizado para español
    # EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" 
    EMBEDDING_DIMENSION: int = 384
    
    # Chunking - Reducido para mejor precisión
    CHUNK_SIZE: int = 250
    CHUNK_OVERLAP: int = 100
    
    # RAG Parameters
    K_INITIAL: int = 15
    K_FINAL: int = 3
    
    # Documentos
    DOCS_PATH: str = "./docs"
    
    # LLM Configuration (opcional)
    LLM_MODEL: str = "ollama/llama2"
    # LLM_MODEL: str = "ollama/mistral"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    # Jira
    JIRA_URL: str = "https://pruebareeskiling.atlassian.net"
    JIRA_USER_EMAIL: str = "pruebareeskiling@gmail.com"
    JIRA_API_TOKEN: str = ""
    JIRA_PROJECT_KEY: str = "KAN"
    JIRA_DEFAULT_ISSUE_TYPE: str = "Task"
    JIRA_DEFAULT_PRIORITY: str = "Medium"

    # LLM - GPT (OpenAI o compatible)
    LLM_PROVIDER: str = "GPT"
    OPENAI_BASE_URL: str = "https://ia-backend-fastapi.dev-codingbuddy-4282826dce7d155229a320302e775459-0000.eu-de.containers.appdomain.cloud/aigen"  # o tu endpoint compatible
    OPENAI_API_KEY: str  = ""
    OPENAI_MODEL: str = "gpt-5-chat-nextai"  # o el modelo que quieras usar
    OPENAI_MAX_TOKENS: int = 250
    OPENAI_TEMPERATURE: float = 0.3

    # Prompt del sistema
    OPENAI_SYSTEM_PROMPT: str = (
        "Eres un asistente experto en gestión de proyectos. "
        "A partir del texto que recibas, debes extraer y estructurar "
        "una o varias tarjetas de Jira en formato JSON. "
        "Devuelve ÚNICAMENTE un JSON válido con la siguiente estructura:\n"
        "{\n"
        '  "issues": [\n'
        "    {\n"
        '      "summary": "Título de la tarea",\n'
        '      "description": "Descripción detallada",\n'
        '      "issue_type": "Task|Bug|Story|Epic",\n'
        '      "priority": "Highest|High|Medium|Low|Lowest",\n'
        '      "labels": ["label1", "label2"]\n'
        "    }\n"
        "  ]\n"
        "}\n"
        "No incluyas texto adicional fuera del JSON."
    )

    




    class Config:
        env_file = None

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = Settings()