from fastapi import APIRouter, Depends
from sqlite3 import Connection
from app.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioCreateResponse
from app.services.usuario_service import UsuarioService
from app.services.security_service import roles_required

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("", response_model=UsuarioCreateResponse, dependencies=[Depends(roles_required(["admin", "junta"]))])
def insertar_usuario(data: UsuarioCreate, db: Connection = Depends(get_db)):
    return UsuarioService.insertar(db, data)

@router.patch("/{username}", response_model=UsuarioResponse, dependencies=[Depends(roles_required(["admin", "junta"]))])
def modificar_usuario(username: str, data: UsuarioUpdate, db: Connection = Depends(get_db)):
    return UsuarioService.modificar(db, username, data)
