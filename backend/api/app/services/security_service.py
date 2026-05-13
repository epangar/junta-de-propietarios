from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.jwt_service import verificar_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    return verificar_token(credentials.credentials)

def roles_required(roles: list[str]):
    def dependency(user: dict = Depends(get_current_user)):
        if user.get("rol") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para realizar esta acción")
        return user
    return dependency

def propietario_puerta_required(puerta: str, user: dict = Depends(get_current_user)):
    if user.get("rol") != "propietario":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo usuarios propietarios pueden acceder a este recurso")
    # La validación exacta contra BD se hace en el service/model para evitar spoofing.
    return user
