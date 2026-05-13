from sqlite3 import Connection
from app.utils.row import row_to_dict, rows_to_list

class BalanceModel:
    @staticmethod
    def listar(db: Connection):
        rows = db.execute("SELECT * FROM Balance_general ORDER BY fecha DESC, id_balance DESC").fetchall()
        return rows_to_list(rows)

    @staticmethod
    def listar_rango(db: Connection, fecha_inicio: str, fecha_fin: str):
        rows = db.execute(
            """
            SELECT * FROM Balance_general
            WHERE date(fecha) BETWEEN date(?) AND date(?)
            ORDER BY fecha DESC, id_balance DESC
            """,
            (fecha_inicio, fecha_fin),
        ).fetchall()
        return rows_to_list(rows)

    @staticmethod
    def obtener(db: Connection, id_balance: int):
        row = db.execute("SELECT * FROM Balance_general WHERE id_balance = ?", (id_balance,)).fetchone()
        return row_to_dict(row)

    @staticmethod
    def crear(db: Connection, data: dict) -> int:
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Balance_general(resultado, fecha, gastos, ingresos)
            VALUES (?, ?, ?, ?)
            """,
            (data.get("resultado"), str(data.get("fecha")), data.get("gastos"), data.get("ingresos")),
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def actualizar(db: Connection, id_balance: int, campos: dict):
        if not campos:
            return BalanceModel.obtener(db, id_balance)
        asignaciones = ", ".join(f"{campo} = ?" for campo in campos)
        valores = [str(v) if campo == "fecha" else v for campo, v in campos.items()] + [id_balance]
        db.execute(f"UPDATE Balance_general SET {asignaciones} WHERE id_balance = ?", valores)
        db.commit()
        return BalanceModel.obtener(db, id_balance)

    @staticmethod
    def resumen_anio(db: Connection, anio: int):
        row = db.execute(
            """
            SELECT COALESCE(SUM(ingresos),0) AS total_ingresos,
                   COALESCE(SUM(gastos),0) AS total_gastos
            FROM Balance_general
            WHERE strftime('%Y', fecha) = ?
            """,
            (str(anio),),
        ).fetchone()
        data = row_to_dict(row)
        data["anio"] = anio
        data["saldo_cierre"] = data["total_ingresos"] - data["total_gastos"]
        return data

    @staticmethod
    def resumen_categoria(db: Connection, anio: int):
        # La BD entregada no tiene columna categoria en Balance_general.
        # Se devuelve una categoría genérica para que el front tenga contrato estable.
        resumen = BalanceModel.resumen_anio(db, anio)
        gastos = resumen["total_gastos"]
        ingresos = resumen["total_ingresos"]
        return [{
            "anio": anio,
            "categoria": "General",
            "ingresos": ingresos,
            "gastos": gastos,
            "saldo_cierre": ingresos - gastos,
            "porcentaje_gastos": round((gastos / ingresos) * 100, 2) if ingresos else 0,
        }]
