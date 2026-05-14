from datetime import datetime, timedelta, timezone
from typing import Any
from sqlite3 import Connection

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.database import get_db
from app.utils.row import row_to_dict

# HTTPBearer hace que Swagger solo pida un token en Authorize.
# En Swagger puedes pegar únicamente el JWT generado por /auth/login.
security = HTTPBearer(
    scheme_name="Bearer Token",
    description="Introduce únicamente el token JWT generado por /auth/login. No hace falta escribir 'Bearer'.",
)


def create_access_token(data: dict[str, Any]) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Connection = Depends(get_db),
) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o caducado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    row = db.execute(
        "SELECT * FROM Usuario WHERE id_usuario = ? AND activo = 1",
        (user_id,),
    ).fetchone()
    user = row_to_dict(row)
    if user is None:
        raise credentials_exception
    return user


def require_roles(*roles: str):
    def dependency(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        if current_user["rol"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para esta operación",
            )
        return current_user

    return dependency
