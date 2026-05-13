from fastapi import HTTPException
from sqlite3 import Connection, IntegrityError
from app.models.usuario_model import UsuarioModel
from app.utils.passwords import generar_password_inicial, hash_password

class UsuarioService:
    @staticmethod
    def insertar(db: Connection, data):
        password_inicial = generar_password_inicial(data.username)
        password_hash = hash_password(password_inicial)
        try:
            id_usuario = UsuarioModel.crear(db, data.username, data.email, password_hash, data.rol)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="El username o email ya existe")
        usuario = UsuarioModel.obtener_por_id(db, id_usuario)
        usuario["password_inicial"] = password_inicial
        return usuario

    @staticmethod
    def modificar(db: Connection, username: str, data):
        existente = UsuarioModel.buscar_por_username(db, username)
        if not existente:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        campos = data.model_dump(exclude_unset=True)
        actualizado = UsuarioModel.actualizar_por_username(db, username, campos)
        if "password" in actualizado:
            actualizado.pop("password", None)
        return actualizado
