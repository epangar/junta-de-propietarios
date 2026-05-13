from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generar_password_inicial(username: str) -> str:
    iniciales = "".join(parte[0].upper() for parte in username.split() if parte)
    return f"{iniciales}{datetime.now().year}"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password_plano: str, password_guardada: str) -> bool:
    if not password_guardada:
        return False
    try:
        if password_guardada.startswith("$2"):
            return pwd_context.verify(password_plano, password_guardada)
    except Exception:
        return False
    # Compatibilidad con bases de datos de pruebas que aún tengan texto plano.
    return password_plano == password_guardada
