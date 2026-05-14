from datetime import date
from pydantic import BaseModel, ConfigDict

class GastoApartamentoOut(BaseModel):
    id_gasto_apto: int | None
    puerta: str | None
    fecha: date | None
    cuota_mes: float
    derrama: float
    pago: float | None
    deuda: float

    model_config = ConfigDict(from_attributes=True)
