
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.rag_system import RAGSystem
from rag import config
router = APIRouter()
rag = RAGSystem()
from .rag_system import RAGSystem
from rag.config import settings

router = APIRouter(prefix="/rag", tags=["RAG"])
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class IndexRequest(BaseModel):
    text: str
    metadata: dict = {}

@router.post("/query")
async def query_rag(request: QueryRequest):
    try:
        results = rag.query(request.query, request.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/index")
async def index_document(request: IndexRequest):
    try:
        result = rag.index_document(request.text, request.metadata)
        return {"status": "indexed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def rag_status():
    return {"status": "ok", "module": "RAG"}
