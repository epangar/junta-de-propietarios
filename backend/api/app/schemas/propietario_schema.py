from pydantic import BaseModel, EmailStr, ConfigDict

class PropietarioOut(BaseModel):
    puerta: str | None
    nombre_propietario: str | None
    telefono: str | None
    email: EmailStr | None
    estado: str | None

    model_config = ConfigDict(from_attributes=True)

class PropietarioUpdate(BaseModel):
    puerta: str | None = None
    nombre_propietario: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None
    estado: str | None = None
