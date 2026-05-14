from sqlite3 import Connection
from app.utils.row import row_to_dict, rows_to_list

SELECT_BALANCE = """
SELECT b.id_balance, b.fecha, b.ingresos, b.gastos, b.resultado, b.id_categoria,
       c.nombre AS categoria
FROM Balance_general b
LEFT JOIN Categoria c ON c.id_categoria = b.id_categoria
"""

class BalanceModel:
    @staticmethod
    def listar(db: Connection) -> list[dict]:
        return rows_to_list(db.execute(SELECT_BALANCE + " ORDER BY date(b.fecha) DESC, b.id_balance DESC").fetchall())

    @staticmethod
    def listar_rango(db: Connection, fecha_inicio: str, fecha_fin: str) -> list[dict]:
        return rows_to_list(db.execute(
            SELECT_BALANCE + " WHERE date(b.fecha) BETWEEN date(?) AND date(?) ORDER BY date(b.fecha) DESC, b.id_balance DESC",
            (fecha_inicio, fecha_fin),
        ).fetchall())

    @staticmethod
    def obtener(db: Connection, id_balance: int) -> dict | None:
        return row_to_dict(db.execute(SELECT_BALANCE + " WHERE b.id_balance = ?", (id_balance,)).fetchone())

    @staticmethod
    def crear(db: Connection, data: dict) -> dict:
        ingresos = data.get("ingresos") or 0
        gastos = data.get("gastos") or 0
        resultado = ingresos - gastos
        cur = db.execute(
            """
            INSERT INTO Balance_general(fecha, ingresos, gastos, resultado, id_categoria)
            VALUES (?, ?, ?, ?, ?)
            """,
            (str(data.get("fecha")) if data.get("fecha") else None, ingresos, gastos, resultado, data.get("id_categoria")),
        )
        db.commit()
        return BalanceModel.obtener(db, cur.lastrowid)

    @staticmethod
    def actualizar(db: Connection, id_balance: int, campos: dict) -> dict | None:
        actual = BalanceModel.obtener(db, id_balance)
        if actual is None:
            return None
        limpio = {k: v for k, v in campos.items() if v is not None}
        if "ingresos" in limpio or "gastos" in limpio:
            ingresos = limpio.get("ingresos", actual.get("ingresos") or 0)
            gastos = limpio.get("gastos", actual.get("gastos") or 0)
            limpio["resultado"] = ingresos - gastos
        if "fecha" in limpio:
            limpio["fecha"] = str(limpio["fecha"])
        if limpio:
            asignaciones = ", ".join(f"{campo} = ?" for campo in limpio)
            db.execute(f"UPDATE Balance_general SET {asignaciones} WHERE id_balance = ?", [*limpio.values(), id_balance])
            db.commit()
        return BalanceModel.obtener(db, id_balance)

    @staticmethod
    def resumen_anio(db: Connection, anio: int) -> dict:
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
    def resumen_categoria(db: Connection, anio: int) -> list[dict]:
        rows = db.execute(
            """
            SELECT c.id_categoria, COALESCE(c.nombre, 'Sin categoría') AS categoria,
                   COALESCE(SUM(b.ingresos),0) AS ingresos,
                   COALESCE(SUM(b.gastos),0) AS gastos
            FROM Balance_general b
            LEFT JOIN Categoria c ON c.id_categoria = b.id_categoria
            WHERE strftime('%Y', b.fecha) = ?
            GROUP BY c.id_categoria, c.nombre
            ORDER BY c.nombre
            """,
            (str(anio),),
        ).fetchall()
        resumen = []
        for r in rows_to_list(rows):
            ingresos = r["ingresos"] or 0
            gastos = r["gastos"] or 0
            resumen.append({
                "anio": anio,
                "id_categoria": r["id_categoria"],
                "categoria": r["categoria"],
                "ingresos": ingresos,
                "gastos": gastos,
                "saldo_cierre": ingresos - gastos,
                "porcentaje_gastos": round((gastos / ingresos) * 100, 2) if ingresos else 0,
            })
        return resumen
