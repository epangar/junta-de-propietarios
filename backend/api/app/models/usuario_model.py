from datetime import datetime
from sqlite3 import Connection
from app.services.security_service import hash_password
from app.utils.row import row_to_dict

class UsuarioModel:
    @staticmethod
    def obtener_por_email(db: Connection, email: str) -> dict | None:
        return row_to_dict(db.execute("SELECT * FROM Usuario WHERE email = ?", (email,)).fetchone())

    @staticmethod
    def obtener_por_username(db: Connection, username: str) -> dict | None:
        return UsuarioModel.obtener_por_email(db, username)

    @staticmethod
    def crear(db: Connection, data: dict) -> dict:
        anio = datetime.now().year
        dominio = data["email"].split("@")[0]
        password_inicial = f"{dominio}{anio}"
        cur = db.execute(
            """
            INSERT INTO Usuario(email, password, rol, puerta_usuario, activo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data["email"], hash_password(password_inicial), data["rol"], data.get("puerta_usuario"), int(data.get("activo", True))),
        )
        db.commit()
        user = row_to_dict(db.execute("SELECT * FROM Usuario WHERE id_usuario = ?", (cur.lastrowid,)).fetchone())
        user["password_inicial"] = password_inicial
        return user

    @staticmethod
    def actualizar(db: Connection, username: str, campos: dict) -> dict | None:
        user = UsuarioModel.obtener_por_username(db, username)
        if user is None:
            return None
        limpio = {}
        if campos.get("email") is not None:
            limpio["email"] = campos["email"]
        if campos.get("usermail") is not None:
            limpio["email"] = campos["usermail"]
        for campo in ("rol", "puerta_usuario", "activo"):
            if campos.get(campo) is not None:
                limpio[campo] = int(campos[campo]) if campo == "activo" else campos[campo]
        limpio["fecha_modificacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        asignaciones = ", ".join(f"{campo} = ?" for campo in limpio)
        db.execute(f"UPDATE Usuario SET {asignaciones} WHERE id_usuario = ?", [*limpio.values(), user["id_usuario"]])
        db.commit()
        return row_to_dict(db.execute("SELECT * FROM Usuario WHERE id_usuario = ?", (user["id_usuario"],)).fetchone())
