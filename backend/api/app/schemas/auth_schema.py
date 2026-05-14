from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id_usuario: int
    email: EmailStr
    rol: str
    puerta_usuario: str | None = None

class MessageResponse(BaseModel):
    message: str
