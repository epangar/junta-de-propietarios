from fastapi import HTTPException
from sqlite3 import Connection
from app.models.usuario_model import UsuarioModel
from app.services.jwt_service import crear_token
from app.utils.passwords import verificar_password

class AuthService:
    @staticmethod
    def login(db: Connection, email: str, password: str):
        usuario = UsuarioModel.buscar_por_email(db, email)
        if not usuario or usuario.get("activo") != 1:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        if not verificar_password(password, usuario["password"]):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        token = crear_token({
            "id_usuario": usuario["id_usuario"],
            "username": usuario["username"],
            "rol": usuario["rol"],
        })
        return {"access_token": token, "token_type": "bearer", "rol": usuario["rol"], "username": usuario["username"]}
