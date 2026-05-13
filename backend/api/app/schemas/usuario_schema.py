from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

Rol = Literal["admin", "junta", "contabilidad", "propietario"]

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    rol: Rol

class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    rol: Optional[Rol] = None
    activo: Optional[int] = Field(default=None, ge=0, le=1)

class UsuarioResponse(BaseModel):
    id_usuario: int
    username: str
    email: EmailStr
    rol: str
    activo: int
    fecha_creacion: str | None = None
    fecha_modificacion: str | None = None

class UsuarioCreateResponse(UsuarioResponse):
    password_inicial: str
