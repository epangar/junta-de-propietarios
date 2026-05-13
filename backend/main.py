from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from rag_system import initialize_rag_system
from config import settings
import uvicorn

app = FastAPI(
    title="RAG System with Elasticsearch",
    description="Sistema RAG usando Elasticsearch para búsqueda vectorial",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_system = None

class QueryRequest(BaseModel):
    question: str = Field(..., description="Pregunta del usuario")

class Source(BaseModel):
    content: str
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]

class HealthResponse(BaseModel):
    status: str
    message: str
    config: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    """Inicializa el sistema RAG al arrancar el servidor"""
    global rag_system
    try:
        print("=" * 50)
        print("Iniciando sistema RAG...")
        print("=" * 50)
        rag_system = initialize_rag_system()
        print("=" * 50)
        print("✓ Sistema RAG inicializado correctamente")
        print("=" * 50)
    except Exception as e:
        print(f"ERROR al inicializar el sistema RAG: {e}")
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de salud"""
    if rag_system is None:
        raise HTTPException(
            status_code=503,
            detail="Sistema RAG no inicializado"
        )
    
    return HealthResponse(
        status="healthy",
        message="Sistema RAG operativo",
        config={
            "embedding_model": settings.EMBEDDING_MODEL,
            "elasticsearch_url": settings.ELASTICSEARCH_URL,
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
            "k_documents": settings.K_FINAL
        }
    )

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Endpoint principal para consultas RAG"""
    if rag_system is None:
        raise HTTPException(
            status_code=503,
            detail="Sistema RAG no inicializado"
        )
    
    try:
        answer, sources = rag_system.query(request.question)
        
        return QueryResponse(
            answer=answer,
            sources=[
                Source(
                    content=source["content"],
                    metadata=source["metadata"]
                )
                for source in sources
            ]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando consulta: {str(e)}"
        )

@app.get("/stats")
async def get_stats():
    """Obtiene estadísticas del índice"""
    if rag_system is None:
        raise HTTPException(
            status_code=503,
            detail="Sistema RAG no inicializado"
        )
    
    return rag_system.get_index_stats()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
