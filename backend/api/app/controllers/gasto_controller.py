from datetime import date
from sqlite3 import Connection
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.database import get_db
from app.models.gasto_model import GastoModel
from app.schemas.gasto_schema import GastoApartamentoOut
from app.services.jwt_service import get_current_user

router = APIRouter(prefix="/gastos", tags=["Gasto apartamento"])


def validar_acceso_puerta(puerta: str, user: dict) -> None:
    if user["rol"] in ("admin", "junta"):
        return
    if user["rol"] == "propietario" and user.get("puerta_usuario") == puerta:
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a esta puerta")

@router.get("/listar_gasto/{puerta}", response_model=list[GastoApartamentoOut])
def listar_gasto(puerta: str, user: dict = Depends(get_current_user), db: Connection = Depends(get_db)):
    validar_acceso_puerta(puerta, user)
    datos = GastoModel.listar_por_puerta(db, puerta)
    if not datos:
        raise HTTPException(status_code=404, detail="No hay gastos para esa puerta")
    return datos

@router.get("/listar_gasto_fecha/{puerta}", response_model=list[GastoApartamentoOut])
def listar_gasto_fecha(
    puerta: str,
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    user: dict = Depends(get_current_user),
    db: Connection = Depends(get_db),
):
    validar_acceso_puerta(puerta, user)
    if fecha_fin < fecha_inicio:
        raise HTTPException(status_code=422, detail="fecha_fin no puede ser menor que fecha_inicio")
    return GastoModel.listar_por_puerta_fecha(db, puerta, str(fecha_inicio), str(fecha_fin))
