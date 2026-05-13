from datetime import date
from fastapi import APIRouter, Depends
from sqlite3 import Connection
from app.database import get_db
from app.schemas.apartamento_schema import ApartamentoResponse
from app.services.apartamento_service import ApartamentoService
from app.services.security_service import propietario_puerta_required

router = APIRouter(prefix="/apartamento", tags=["Apartamento"])

@router.get("/{puerta}", response_model=ApartamentoResponse)
def ver_apartamento(puerta: str, db: Connection = Depends(get_db), user=Depends(propietario_puerta_required)):
    return ApartamentoService.ver_apartamento(db, user, puerta)

@router.get("/{puerta}/fecha", response_model=ApartamentoResponse)
def ver_fecha(puerta: str, fecha_inicio: date, fecha_fin: date, db: Connection = Depends(get_db), user=Depends(propietario_puerta_required)):
    return ApartamentoService.ver_apartamento_fecha(db, user, puerta, str(fecha_inicio), str(fecha_fin))
