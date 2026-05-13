from sqlite3 import Connection
from app.models.propietario_model import PropietarioModel

class ApartamentoModel:
    @staticmethod
    def obtener_apartamento_usuario(db: Connection, id_usuario: int, puerta: str):
        return PropietarioModel.buscar_de_usuario(db, id_usuario, puerta)

    @staticmethod
    def obtener_apartamento_usuario_fecha(db: Connection, id_usuario: int, puerta: str, fecha_inicio: str, fecha_fin: str):
        return PropietarioModel.buscar_de_usuario_fecha(db, id_usuario, puerta, fecha_inicio, fecha_fin)
