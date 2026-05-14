from datetime import date
from pydantic import BaseModel, Field, ConfigDict, model_validator

class BalanceBase(BaseModel):
    fecha: date | None = None
    ingresos: float = Field(default=0, ge=0)
    gastos: float = Field(default=0, ge=0)
    id_categoria: int | None = None

class BalanceCreate(BalanceBase):
    pass

class BalanceUpdate(BaseModel):
    fecha: date | None = None
    ingresos: float | None = Field(default=None, ge=0)
    gastos: float | None = Field(default=None, ge=0)
    id_categoria: int | None = None

class BalanceOut(BaseModel):
    id_balance: int
    fecha: date | None
    ingresos: float | None
    gastos: float | None
    resultado: float | None
    id_categoria: int | None
    categoria: str | None = None

    model_config = ConfigDict(from_attributes=True)

class BalanceRangoQuery(BaseModel):
    fecha_inicio: date
    fecha_fin: date

    @model_validator(mode="after")
    def validar_rango(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError("fecha_fin no puede ser menor que fecha_inicio")
        return self

class ResumenAnioOut(BaseModel):
    anio: int
    total_ingresos: float
    total_gastos: float
    saldo_cierre: float

class ResumenCategoriaOut(BaseModel):
    anio: int
    id_categoria: int | None
    categoria: str
    ingresos: float
    gastos: float
    saldo_cierre: float
    porcentaje_gastos: float
