from fastapi import HTTPException
from sqlite3 import Connection
from app.models.apartamento_model import ApartamentoModel

class ApartamentoService:
    @staticmethod
    def ver_apartamento(db: Connection, user: dict, puerta: str):
        apto = ApartamentoModel.obtener_apartamento_usuario(db, user["id_usuario"], puerta)
        if not apto:
            raise HTTPException(status_code=404, detail="No tienes acceso a esta puerta o no existe")
        return apto

    @staticmethod
    def ver_apartamento_fecha(db: Connection, user: dict, puerta: str, fecha_inicio: str, fecha_fin: str):
        apto = ApartamentoModel.obtener_apartamento_usuario_fecha(db, user["id_usuario"], puerta, fecha_inicio, fecha_fin)
        if not apto:
            raise HTTPException(status_code=404, detail="No hay datos para esa puerta y rango de fecha")
        return apto
