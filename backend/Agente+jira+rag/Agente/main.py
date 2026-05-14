from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile

from agent.agent import run_agent

app = FastAPI(title="Excel → SQLite Agent")
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from config import get_settings, Settings
from models import (
    AIGenerateRequest,
    AIGenerateResponse,
    ManualIssueRequest,
    ManualIssueResponse,
)
from services.jira_service import JiraService
from services.openai_service import OpenAIService

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from rag_system import initialize_rag_system

import uvicorn
from config import Settings
settings = Settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = await run_agent(tmp_path)

    return JSONResponse(result)


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación...")
    yield
    logger.info("Cerrando aplicación...")


# ── App ───────────────────────────────────────────────────────────────────────

# def create_app() -> FastAPI:
#     settings = get_settings()
#     app = FastAPI(
#         title=settings.APP_TITLE,
#         version=settings.APP_VERSION,
#         debug=settings.APP_DEBUG,
#         lifespan=lifespan,
#         description=(
#             "API para crear tarjetas en Jira de forma manual "
#             "o mediante generación automática con IA."
#         ),
#     )
#     return app


# app = create_app()


# ── Dependencias ──────────────────────────────────────────────────────────────

def get_jira_service(settings: Settings = Depends(get_settings)) -> JiraService:
    return JiraService(settings)


def get_openai_service(settings: Settings = Depends(get_settings)) -> OpenAIService:
    return OpenAIService(settings)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post(
    "/issues/ai-generate",
    response_model=AIGenerateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generar tarjetas Jira mediante IA",
    description=(
        "Recibe un texto libre, lo procesa con la IA configurada "
        "y crea automáticamente las tarjetas correspondientes en Jira."
    ),
    tags=["AI"],
)
async def ai_generate_issues(
    request: AIGenerateRequest,
    jira_svc: JiraService = Depends(get_jira_service),
    openai_svc: OpenAIService = Depends(get_openai_service),
) -> AIGenerateResponse:
    # 1. Enviar texto a la IA y obtener estructura de tarjetas
    try:
        issues_data, raw_response = await openai_svc.generate_jira_issues(request.text)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )
    except Exception as exc:
        logger.exception("Error al comunicarse con la IA")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al comunicarse con el servicio de IA: {exc}",
        )

    if not issues_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La IA no generó ninguna tarjeta a partir del texto proporcionado.",
        )

    # 2. Crear las tarjetas en Jira
    try:
        created_issues = jira_svc.create_issues_bulk(
            issues_data=issues_data,
            project_key=request.project_key,
        )
    except Exception as exc:
        logger.exception("Error al crear issues en Jira")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al crear las tarjetas en Jira: {exc}",
        )

    return AIGenerateResponse(
        total_issues_created=len(created_issues),
        issues=created_issues,
        raw_ai_response=raw_response,
    )


@app.post(
    "/issues/manual",
    response_model=ManualIssueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear tarjeta Jira manualmente",
    description=(
        "Crea una tarjeta en Jira directamente con los datos proporcionados, "
        "sin intervención de la IA."
    ),
    tags=["Manual"],
)
def create_manual_issue(
    request: ManualIssueRequest,
    jira_svc: JiraService = Depends(get_jira_service),
) -> ManualIssueResponse:
    try:
        created_issue = jira_svc.create_issue(
            summary=request.summary,
            description=request.description or "",
            issue_type=request.issue_type,
            priority=request.priority,
            labels=request.labels,
            story_points=request.story_points,
            project_key=request.project_key,
        )
    except Exception as exc:
        logger.exception("Error al crear issue manual en Jira")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al crear la tarjeta en Jira: {exc}",
        )

    return ManualIssueResponse(issue=created_issue)


# ── Health check ──────────────────────────────────────────────────────────────

# @app.get("/health", tags=["System"], summary="Health check")
# def health_check():
#     return JSONResponse(content={"status": "ok"})


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