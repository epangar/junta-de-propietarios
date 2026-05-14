from sqlite3 import Connection
from fastapi import HTTPException, status
from app.services.security_service import verify_password
from app.services.jwt_service import create_access_token
from app.utils.row import row_to_dict


def login(db: Connection, email: str, password: str) -> dict:
    row = db.execute("SELECT * FROM Usuario WHERE email = ? AND activo = 1", (email,)).fetchone()
    user = row_to_dict(row)
    if user is None or not verify_password(password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos")
    token = create_access_token({"sub": str(user["id_usuario"]), "email": user["email"], "rol": user["rol"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "id_usuario": user["id_usuario"],
        "email": user["email"],
        "rol": user["rol"],
        "puerta_usuario": user.get("puerta_usuario"),
    }
