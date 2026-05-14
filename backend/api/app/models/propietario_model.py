from sqlite3 import Connection
from app.utils.row import row_to_dict, rows_to_list

SELECT_PROPIETARIO = """
SELECT puerta, propietario AS nombre_propietario, telefono, email, estado
FROM Apartamento
"""

class PropietarioModel:
    @staticmethod
    def listar(db: Connection):
        return rows_to_list(db.execute(SELECT_PROPIETARIO + " ORDER BY puerta, propietario").fetchall())

    @staticmethod
    def por_puerta(db: Connection, puerta: str):
        return row_to_dict(db.execute(SELECT_PROPIETARIO + " WHERE puerta = ?", (puerta,)).fetchone())

    @staticmethod
    def por_nombre(db: Connection, nombre: str):
        return rows_to_list(db.execute(SELECT_PROPIETARIO + " WHERE propietario LIKE ? ORDER BY propietario", (f"%{nombre}%",)).fetchall())

    @staticmethod
    def por_estado(db: Connection, estado: str):
        return rows_to_list(db.execute(SELECT_PROPIETARIO + " WHERE lower(estado) = lower(?) ORDER BY puerta", (estado,)).fetchall())

    @staticmethod
    def actualizar_por_puerta(db: Connection, puerta: str, campos: dict):
        mapa = {"nombre_propietario": "propietario", "telefono": "telefono", "email": "email", "estado": "estado", "puerta": "puerta"}
        limpio = {mapa[k]: v for k, v in campos.items() if k in mapa and v is not None}
        if limpio:
            asignaciones = ", ".join(f"{campo} = ?" for campo in limpio)
            db.execute(f"UPDATE Apartamento SET {asignaciones} WHERE puerta = ?", [*limpio.values(), puerta])
            db.commit()
        nueva_puerta = limpio.get("puerta", puerta)
        return PropietarioModel.por_puerta(db, nueva_puerta)
