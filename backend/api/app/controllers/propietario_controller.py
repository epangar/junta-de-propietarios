from datetime import date
from fastapi import APIRouter, Depends
from sqlite3 import Connection
from app.database import get_db
from app.schemas.propietario_schema import PropietarioResponse, PropietarioCreate, PropietarioUpdate
from app.services.propietario_service import PropietarioService
from app.services.security_service import roles_required

router = APIRouter(prefix="/propietarios", tags=["Propietarios"])

@router.get("", response_model=list[PropietarioResponse], dependencies=[Depends(roles_required(["admin"]))])
def ver_propietarios(db: Connection = Depends(get_db)):
    return PropietarioService.listar(db)

@router.get("/fecha", response_model=list[PropietarioResponse], dependencies=[Depends(roles_required(["admin"]))])
def propietario_fecha(fecha_inicio: date, fecha_fin: date, db: Connection = Depends(get_db)):
    return PropietarioService.filtrar_fecha(db, str(fecha_inicio), str(fecha_fin))

@router.get("/puerta/{puerta}", response_model=PropietarioResponse, dependencies=[Depends(roles_required(["admin"]))])
def propietario_puerta(puerta: str, db: Connection = Depends(get_db)):
    return PropietarioService.buscar_por_puerta(db, puerta)

@router.patch("/{puerta}", response_model=PropietarioResponse, dependencies=[Depends(roles_required(["admin"]))])
def modificar_propietario(puerta: str, data: PropietarioUpdate, db: Connection = Depends(get_db)):
    return PropietarioService.actualizar(db, puerta, data)

@router.post("", response_model=PropietarioResponse, dependencies=[Depends(roles_required(["admin"]))])
def insertar_propietario(data: PropietarioCreate, db: Connection = Depends(get_db)):
    return PropietarioService.crear(db, data)
