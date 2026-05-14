from sqlite3 import Connection
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.auth_schema import LoginRequest, TokenResponse, MessageResponse
from app.services.auth_service import login as login_service
from app.services.jwt_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Connection = Depends(get_db)):
    return login_service(db, payload.email, payload.password)

@router.post("/logout", response_model=MessageResponse)
def logout(_: dict = Depends(get_current_user)):
    return {"message": "Sesión cerrada. El frontend debe eliminar el token JWT."}
