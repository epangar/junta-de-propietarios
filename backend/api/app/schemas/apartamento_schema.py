from pydantic import BaseModel

class ApartamentoResponse(BaseModel):
    id_apto: int
    puerta: str
    cuota_mes: float | None = 0
    derrama: float | None = 0
    deuda: float | None = 0
    estado: str
