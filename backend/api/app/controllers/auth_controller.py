from fastapi import APIRouter, Depends
from sqlite3 import Connection
from app.database import get_db
from app.schemas.auth_schema import LoginRequest, TokenResponse, MessageResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Connection = Depends(get_db)):
    return AuthService.login(db, data.email, data.password)

@router.post("/logout", response_model=MessageResponse)
def logout():
    return {"message": "Sesión cerrada correctamente"}
