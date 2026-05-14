from sqlite3 import Connection, IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioCreadoOut
from app.services.jwt_service import require_roles

router = APIRouter(prefix="/usuarios", tags=["Usuario"], dependencies=[Depends(require_roles("admin", "junta"))])

@router.post("/insertar_usuario", response_model=UsuarioCreadoOut, status_code=status.HTTP_201_CREATED)
def insertar_usuario(payload: UsuarioCreate, db: Connection = Depends(get_db)):
    try:
        return UsuarioModel.crear(db, payload.model_dump())
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese email")

@router.patch("/modificar_usuario/{username}", response_model=UsuarioOut)
def modificar_usuario(username: str, payload: UsuarioUpdate, db: Connection = Depends(get_db)):
    user = UsuarioModel.actualizar(db, username, payload.model_dump(exclude_unset=True))
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
