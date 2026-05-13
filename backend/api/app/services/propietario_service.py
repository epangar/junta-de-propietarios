from fastapi import HTTPException
from sqlite3 import Connection
from app.models.propietario_model import PropietarioModel

class PropietarioService:
    listar = staticmethod(PropietarioModel.listar)
    filtrar_fecha = staticmethod(PropietarioModel.filtrar_fecha)

    @staticmethod
    def buscar_por_puerta(db: Connection, puerta: str):
        propietario = PropietarioModel.buscar_por_puerta(db, puerta)
        if not propietario:
            raise HTTPException(status_code=404, detail="Propietario/apartamento no encontrado")
        return propietario

    @staticmethod
    def crear(db: Connection, data):
        id_apto = PropietarioModel.crear(db, data.model_dump())
        return PropietarioModel.buscar_por_puerta(db, str(id_apto))

    @staticmethod
    def actualizar(db: Connection, puerta: str, data):
        if not PropietarioModel.buscar_por_puerta(db, puerta):
            raise HTTPException(status_code=404, detail="Propietario/apartamento no encontrado")
        return PropietarioModel.actualizar_por_puerta(db, puerta, data.model_dump(exclude_unset=True))
