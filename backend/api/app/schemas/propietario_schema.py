from pydantic import BaseModel, EmailStr
from typing import Optional

class PropietarioResponse(BaseModel):
    id_apto: int
    puerta: str
    propietario: str | None = None
    telefono: str | None = None
    email: str | None = None
    cuota_mes: float | None = 0
    derrama: float | None = 0
    deuda: float | None = 0
    estado: str

class PropietarioCreate(BaseModel):
    id_edificio: Optional[int] = None
    cuota_mes: Optional[float] = 0
    derrama: Optional[float] = 0
    deuda: Optional[float] = 0
    propietario: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    id_usuario: Optional[int] = None

class PropietarioUpdate(BaseModel):
    id_edificio: Optional[int] = None
    cuota_mes: Optional[float] = None
    derrama: Optional[float] = None
    deuda: Optional[float] = None
    estado: Optional[str] = None
    propietario: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    id_usuario: Optional[int] = None
