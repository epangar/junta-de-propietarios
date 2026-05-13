from fastapi import APIRouter, Depends
from sqlite3 import Connection
from app.database import get_db
from app.schemas.balance_schema import ResumenAnioResponse, ResumenCategoriaResponse
from app.services.balance_service import BalanceService
from app.services.security_service import get_current_user

router = APIRouter(prefix="/resumen", tags=["Resumen"])

@router.get("/{anio}", response_model=ResumenAnioResponse)
def resumen_anio(anio: int, db: Connection = Depends(get_db), user=Depends(get_current_user)):
    return BalanceService.resumen_anio(db, anio)

@router.get("/{anio}/categorias", response_model=list[ResumenCategoriaResponse])
def resumen_categoria(anio: int, db: Connection = Depends(get_db), user=Depends(get_current_user)):
    return BalanceService.resumen_categoria(db, anio)
