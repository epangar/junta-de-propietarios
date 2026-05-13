from fastapi import HTTPException
from sqlite3 import Connection
from app.models.balance_model import BalanceModel

class BalanceService:
    listar = staticmethod(BalanceModel.listar)
    listar_rango = staticmethod(BalanceModel.listar_rango)
    resumen_anio = staticmethod(BalanceModel.resumen_anio)
    resumen_categoria = staticmethod(BalanceModel.resumen_categoria)

    @staticmethod
    def crear(db: Connection, data):
        payload = data.model_dump()
        if payload.get("resultado") is None:
            payload["resultado"] = (payload.get("ingresos") or 0) - (payload.get("gastos") or 0)
        id_balance = BalanceModel.crear(db, payload)
        return BalanceModel.obtener(db, id_balance)

    @staticmethod
    def actualizar(db: Connection, id_balance: int, data):
        if not BalanceModel.obtener(db, id_balance):
            raise HTTPException(status_code=404, detail="Balance no encontrado")
        campos = data.model_dump(exclude_unset=True)
        actualizado = BalanceModel.actualizar(db, id_balance, campos)
        return actualizado
