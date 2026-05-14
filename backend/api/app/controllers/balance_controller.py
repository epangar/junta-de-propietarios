from datetime import date
from sqlite3 import Connection
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.database import get_db
from app.models.balance_model import BalanceModel
from app.schemas.balance_schema import BalanceCreate, BalanceUpdate, BalanceOut
from app.services.jwt_service import get_current_user, require_roles

router = APIRouter(prefix="/balance", tags=["Balance general"])

@router.get("/ver_balance", response_model=list[BalanceOut])
def ver_balance(_: dict = Depends(get_current_user), db: Connection = Depends(get_db)):
    return BalanceModel.listar(db)

@router.get("/ver_balance_rango", response_model=list[BalanceOut])
def ver_balance_rango(
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    _: dict = Depends(get_current_user),
    db: Connection = Depends(get_db),
):
    if fecha_fin < fecha_inicio:
        raise HTTPException(status_code=422, detail="fecha_fin no puede ser menor que fecha_inicio")
    return BalanceModel.listar_rango(db, str(fecha_inicio), str(fecha_fin))

@router.patch("/editar_balance/{id_balance}", response_model=BalanceOut)
def editar_balance(
    id_balance: int,
    payload: BalanceUpdate,
    _: dict = Depends(require_roles("admin")),
    db: Connection = Depends(get_db),
):
    balance = BalanceModel.actualizar(db, id_balance, payload.model_dump(exclude_unset=True))
    if balance is None:
        raise HTTPException(status_code=404, detail="Balance no encontrado")
    return balance

@router.post("/agregar_dato_balance", response_model=BalanceOut, status_code=status.HTTP_201_CREATED)
def agregar_dato_balance(
    payload: BalanceCreate,
    _: dict = Depends(require_roles("admin")),
    db: Connection = Depends(get_db),
):
    return BalanceModel.crear(db, payload.model_dump())
