
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class JiraIssueRequest(BaseModel):
    titulo: str
    descripcion: str
    tipo: str = "Task"
    prioridad: str = "Medium"
    proyecto: Optional[str] = None

class AIGenerateRequest(BaseModel):
    prompt: str
    contexto: Optional[str] = None

@router.post("/create-issue")
async def create_issue(request: JiraIssueRequest):
    try:
        from jira_creator.services.jira_service import JiraService
        service = JiraService()
        result = service.create_issue(
            titulo=request.titulo,
            descripcion=request.descripcion,
            tipo=request.tipo,
            prioridad=request.prioridad
        )
        return {"status": "created", "issue": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_issue_ai(request: AIGenerateRequest):
    try:
        from jira_creator.services.openai_service import OpenAIService
        service = OpenAIService()
        result = service.generate_issue(request.prompt, request.contexto)
        return {"status": "generated", "issue": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def jira_status():
    return {"status": "ok", "module": "Jira Creator"}
