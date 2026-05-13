from sqlite3 import Connection
from app.utils.row import row_to_dict

class UsuarioModel:
    @staticmethod
    def buscar_por_email(db: Connection, email: str):
        row = db.execute("SELECT * FROM Usuario WHERE email = ?", (email,)).fetchone()
        return row_to_dict(row)

    @staticmethod
    def buscar_por_username(db: Connection, username: str):
        row = db.execute("SELECT * FROM Usuario WHERE username = ?", (username,)).fetchone()
        return row_to_dict(row)

    @staticmethod
    def crear(db: Connection, username: str, email: str, password_hash: str, rol: str) -> int:
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Usuario(username, email, password, rol, activo)
            VALUES (?, ?, ?, ?, 1)
            """,
            (username, email, password_hash, rol),
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def obtener_por_id(db: Connection, id_usuario: int):
        row = db.execute(
            """
            SELECT id_usuario, username, email, rol, fecha_creacion, fecha_modificacion, activo
            FROM Usuario WHERE id_usuario = ?
            """,
            (id_usuario,),
        ).fetchone()
        return row_to_dict(row)

    @staticmethod
    def actualizar_por_username(db: Connection, username: str, campos: dict):
        if not campos:
            return UsuarioModel.buscar_por_username(db, username)
        asignaciones = ", ".join(f"{campo} = ?" for campo in campos)
        valores = list(campos.values()) + [username]
        db.execute(
            f"""
            UPDATE Usuario
            SET {asignaciones}, fecha_modificacion = CURRENT_TIMESTAMP
            WHERE username = ?
            """,
            valores,
        )
        db.commit()
        nuevo_username = campos.get("username", username)
        return UsuarioModel.buscar_por_username(db, nuevo_username)
