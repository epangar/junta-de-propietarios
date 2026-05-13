from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.auth_controller import router as auth_router
from app.controllers.resumen_controller import router as resumen_router
from app.controllers.balance_controller import router as balance_router
from app.controllers.propietario_controller import router as propietario_router
from app.controllers.apartamento_controller import router as apartamento_router
from app.controllers.usuario_controller import router as usuario_router
from app.database import run_startup_checks
from app.config import settings

app = FastAPI(
    title="API Junta de Condominios",
    version="2.0.0",
    description="API MVC con FastAPI, SQLite y Pydantic para Angular y servidor MCP.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.angular_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup() -> None:
    run_startup_checks()

@app.get("/", tags=["Health"])
def healthcheck():
    return {"status": "ok", "message": "API Junta de Condominios activa"}

app.include_router(auth_router)
app.include_router(resumen_router)
app.include_router(balance_router)
app.include_router(propietario_router)
app.include_router(apartamento_router)
app.include_router(usuario_router)
