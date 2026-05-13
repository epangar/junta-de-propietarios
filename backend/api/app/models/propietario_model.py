from sqlite3 import Connection
from app.utils.row import row_to_dict, rows_to_list

class PropietarioModel:
    @staticmethod
    def _select_base(where: str = "", order: str = "ORDER BY a.id_apto") -> str:
        return f"""
        SELECT
            a.id_apto,
            CAST(a.id_apto AS TEXT) AS puerta,
            a.propietario,
            a.telefono,
            a.email,
            COALESCE(a.cuota_mes, 0) AS cuota_mes,
            COALESCE(SUM(g.monto), COALESCE(a.derrama, 0), 0) AS derrama,
            COALESCE(a.deuda, 0) AS deuda,
            CASE WHEN COALESCE(a.deuda, 0) > 0 THEN 'En mora' ELSE 'Al día' END AS estado
        FROM Apartamento a
        LEFT JOIN Gasto_apartamento g ON g.id_apto = a.id_apto
        {where}
        GROUP BY a.id_apto
        {order}
        """

    @staticmethod
    def listar(db: Connection):
        return rows_to_list(db.execute(PropietarioModel._select_base()).fetchall())

    @staticmethod
    def filtrar_fecha(db: Connection, fecha_inicio: str, fecha_fin: str):
        sql = PropietarioModel._select_base(
            "WHERE date(g.fecha) BETWEEN date(?) AND date(?)",
            "ORDER BY a.id_apto",
        )
        return rows_to_list(db.execute(sql, (fecha_inicio, fecha_fin)).fetchall())

    @staticmethod
    def buscar_por_puerta(db: Connection, puerta: str):
        sql = PropietarioModel._select_base("WHERE CAST(a.id_apto AS TEXT) = ?")
        return row_to_dict(db.execute(sql, (puerta,)).fetchone())

    @staticmethod
    def crear(db: Connection, data: dict) -> int:
        deuda = data.get("deuda") or 0
        estado = "En mora" if deuda > 0 else "Al día"
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Apartamento(id_edificio, cuota_mes, derrama, deuda, estado, propietario, telefono, email, id_usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("id_edificio"), data.get("cuota_mes"), data.get("derrama"), deuda,
                estado, data.get("propietario"), data.get("telefono"), data.get("email"), data.get("id_usuario"),
            ),
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def actualizar_por_puerta(db: Connection, puerta: str, campos: dict):
        if "deuda" in campos and "estado" not in campos:
            campos["estado"] = "En mora" if (campos["deuda"] or 0) > 0 else "Al día"
        if campos:
            asignaciones = ", ".join(f"{campo} = ?" for campo in campos)
            valores = list(campos.values()) + [puerta]
            db.execute(f"UPDATE Apartamento SET {asignaciones} WHERE CAST(id_apto AS TEXT) = ?", valores)
            db.commit()
        return PropietarioModel.buscar_por_puerta(db, puerta)

    @staticmethod
    def buscar_de_usuario(db: Connection, id_usuario: int, puerta: str):
        sql = PropietarioModel._select_base("WHERE a.id_usuario = ? AND CAST(a.id_apto AS TEXT) = ?")
        return row_to_dict(db.execute(sql, (id_usuario, puerta)).fetchone())

    @staticmethod
    def buscar_de_usuario_fecha(db: Connection, id_usuario: int, puerta: str, fecha_inicio: str, fecha_fin: str):
        sql = PropietarioModel._select_base(
            "WHERE a.id_usuario = ? AND CAST(a.id_apto AS TEXT) = ? AND date(g.fecha) BETWEEN date(?) AND date(?)"
        )
        return row_to_dict(db.execute(sql, (id_usuario, puerta, fecha_inicio, fecha_fin)).fetchone())
