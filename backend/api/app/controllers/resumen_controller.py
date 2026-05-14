from sqlite3 import Connection
from fastapi import APIRouter, Depends, Path
from app.database import get_db
from app.models.balance_model import BalanceModel
from app.schemas.balance_schema import ResumenAnioOut, ResumenCategoriaOut
from app.services.jwt_service import get_current_user

router = APIRouter(prefix="/resumen", tags=["Resumen"], dependencies=[Depends(get_current_user)])

@router.get("/anio/{anio}", response_model=ResumenAnioOut)
def resumen_anio(anio: int = Path(ge=2000, le=2100), db: Connection = Depends(get_db)):
    return BalanceModel.resumen_anio(db, anio)

@router.get("/categoria/{anio}", response_model=list[ResumenCategoriaOut])
def resumen_categoria(anio: int = Path(ge=2000, le=2100), db: Connection = Depends(get_db)):
    return BalanceModel.resumen_categoria(db, anio)
