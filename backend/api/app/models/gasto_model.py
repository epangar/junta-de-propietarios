from sqlite3 import Connection
from app.utils.row import rows_to_list

class GastoModel:
    @staticmethod
    def numero_apartamentos(db: Connection) -> int:
        row = db.execute("SELECT COUNT(*) AS total FROM Apartamento").fetchone()
        return max(int(row["total"] or 1), 1)

    @staticmethod
    def calcular_cuota_mes(db: Connection, anio_mes: str | None = None) -> float:
        filtro = ""
        params: tuple = ()
        if anio_mes:
            filtro = " AND strftime('%Y-%m', b.fecha) = ?"
            params = (anio_mes,)
        row = db.execute(
            f"""
            SELECT COALESCE(SUM(b.gastos),0) AS gastos_comunes
            FROM Balance_general b
            LEFT JOIN Categoria c ON c.id_categoria = b.id_categoria
            WHERE lower(COALESCE(c.nombre,'')) NOT LIKE '%derrama%'
            {filtro}
            """,
            params,
        ).fetchone()
        return round((row["gastos_comunes"] or 0) / GastoModel.numero_apartamentos(db), 2)

    @staticmethod
    def calcular_derrama(db: Connection, anio_mes: str | None = None) -> float:
        filtro = ""
        params: tuple = ()
        if anio_mes:
            filtro = " AND strftime('%Y-%m', b.fecha) = ?"
            params = (anio_mes,)
        row = db.execute(
            f"""
            SELECT COALESCE(SUM(b.ingresos),0) AS total_derrama
            FROM Balance_general b
            LEFT JOIN Categoria c ON c.id_categoria = b.id_categoria
            WHERE lower(COALESCE(c.nombre,'')) LIKE '%derrama%'
            {filtro}
            """,
            params,
        ).fetchone()
        return round((row["total_derrama"] or 0) / GastoModel.numero_apartamentos(db), 2)

    @staticmethod
    def listar_por_puerta(db: Connection, puerta: str) -> list[dict]:
        rows = db.execute(
            """
            SELECT g.id_gasto_apto, a.puerta, g.fecha, g.pago, g.deuda
            FROM Apartamento a
            LEFT JOIN Gasto_apartamento g ON g.id_gasto_apto = a.id_gasto_apto
            WHERE a.puerta = ?
            ORDER BY date(g.fecha) DESC
            """,
            (puerta,),
        ).fetchall()
        salida = []
        for r in rows_to_list(rows):
            anio_mes = r["fecha"][:7] if r.get("fecha") else None
            cuota = GastoModel.calcular_cuota_mes(db, anio_mes)
            derrama = GastoModel.calcular_derrama(db, anio_mes)
            pago = r.get("pago")
            deuda = r.get("deuda")
            if deuda is None:
                deuda = max((cuota + derrama) - (pago or 0), 0)
            salida.append({**r, "cuota_mes": cuota, "derrama": derrama, "deuda": round(deuda, 2)})
        return salida

    @staticmethod
    def listar_por_puerta_fecha(db: Connection, puerta: str, fecha_inicio: str, fecha_fin: str) -> list[dict]:
        datos = GastoModel.listar_por_puerta(db, puerta)
        return [d for d in datos if d["fecha"] and fecha_inicio <= d["fecha"] <= fecha_fin]
