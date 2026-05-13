from datetime import date
from fastapi import APIRouter, Depends
from sqlite3 import Connection
from app.database import get_db
from app.schemas.balance_schema import BalanceCreate, BalanceUpdate, BalanceResponse
from app.services.balance_service import BalanceService
from app.services.security_service import get_current_user, roles_required

router = APIRouter(prefix="/balance", tags=["Balance general"])

@router.get("", response_model=list[BalanceResponse])
def ver_balance(db: Connection = Depends(get_db), user=Depends(get_current_user)):
    return BalanceService.listar(db)

@router.get("/rango", response_model=list[BalanceResponse])
def ver_balance_rango(fecha_inicio: date, fecha_fin: date, db: Connection = Depends(get_db), user=Depends(get_current_user)):
    return BalanceService.listar_rango(db, str(fecha_inicio), str(fecha_fin))

@router.post("", response_model=BalanceResponse, dependencies=[Depends(roles_required(["admin"]))])
def agregar_dato_balance(data: BalanceCreate, db: Connection = Depends(get_db)):
    return BalanceService.crear(db, data)

@router.put("/{id_balance}", response_model=BalanceResponse, dependencies=[Depends(roles_required(["admin"]))])
def editar_balance(id_balance: int, data: BalanceUpdate, db: Connection = Depends(get_db)):
    return BalanceService.actualizar(db, id_balance, data)
