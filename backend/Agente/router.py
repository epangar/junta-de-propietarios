
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class AgentRequest(BaseModel):
    mensaje: str
    contexto: Optional[str] = None
    historial: Optional[list] = []

@router.post("/chat")
async def chat_agent(request: AgentRequest):
    try:
        from Agente.agent.agent import run_agent
        result = run_agent(
            mensaje=request.mensaje,
            contexto=request.contexto,
            historial=request.historial
        )
        return {"status": "ok", "respuesta": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def agent_status():
    return {"status": "ok", "module": "Agente IA"}
