from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BalanceBase(BaseModel):
    resultado: Optional[float] = 0
    fecha: date
    gastos: Optional[float] = 0
    ingresos: Optional[float] = 0

class BalanceCreate(BalanceBase):
    pass

class BalanceUpdate(BaseModel):
    resultado: Optional[float] = None
    fecha: Optional[date] = None
    gastos: Optional[float] = None
    ingresos: Optional[float] = None

class BalanceResponse(BalanceBase):
    id_balance: int

class ResumenAnioResponse(BaseModel):
    anio: int
    total_ingresos: float
    total_gastos: float
    saldo_cierre: float

class ResumenCategoriaResponse(BaseModel):
    anio: int
    categoria: str
    ingresos: float
    gastos: float
    saldo_cierre: float
    porcentaje_gastos: float
