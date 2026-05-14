
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Junta de Propietarios - API Unificada")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── RAG ──────────────────────────────────────

try:
    from rag.router import router as rag_router
    app.include_router(rag_router, prefix="/rag", tags=["RAG"])
    print("✅ Módulo RAG cargado correctamente")
except Exception as e:
    print(f"❌ ERROR cargando módulo RAG: {e}")

# ── JIRA ─────────────────────────────────────
try:
    from jira_creator.router import router as jira_router
    app.include_router(jira_router, prefix="/jira", tags=["Jira Creator"])
    print("✅ Módulo Jira Creator cargado correctamente")
except Exception as e:
    print(f"❌ ERROR cargando módulo Jira Creator: {e}")

# ── AGENTE ───────────────────────────────────
try:
    from Agente.router import router as agent_router
    app.include_router(agent_router, prefix="/agente", tags=["Agente IA"])
    print("✅ Módulo Agente IA cargado correctamente")
except Exception as e:
    print(f"❌ ERROR cargando módulo Agente: {e}")

# ── HEALTH CHECK ─────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "API Junta de Propietarios funcionando"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

# ── ARRANQUE ─────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
