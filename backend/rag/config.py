from pydantic_settings import BaseSettings
class Settings(BaseSettings):
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
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
