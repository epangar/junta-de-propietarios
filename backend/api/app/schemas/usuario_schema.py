from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UsuarioCreate(BaseModel):
    email: EmailStr
    rol: str = Field(pattern="^(admin|junta|propietario)$")
    puerta_usuario: str | None = None
    activo: bool = True

class UsuarioUpdate(BaseModel):
    usermail: EmailStr | None = None
    email: EmailStr | None = None
    rol: str | None = Field(default=None, pattern="^(admin|junta|propietario)$")
    activo: bool | None = None
    puerta_usuario: str | None = None

class UsuarioOut(BaseModel):
    id_usuario: int
    email: EmailStr
    rol: str
    puerta_usuario: str | None
    fecha_creacion: datetime | None
    fecha_modificacion: datetime | None
    activo: bool

    model_config = ConfigDict(from_attributes=True)

class UsuarioCreadoOut(UsuarioOut):
    password_inicial: str
