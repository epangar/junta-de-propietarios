from sqlite3 import Connection
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models.propietario_model import PropietarioModel
from app.schemas.propietario_schema import PropietarioOut, PropietarioUpdate
from app.services.jwt_service import require_roles

router = APIRouter(prefix="/propietarios", tags=["Propietario"], dependencies=[Depends(require_roles("admin", "junta"))])

@router.get("/listar_propietario", response_model=list[PropietarioOut])
def listar_propietario(db: Connection = Depends(get_db)):
    return PropietarioModel.listar(db)

@router.get("/ver_propietario_puerta/{puerta}", response_model=PropietarioOut)
def ver_propietario_puerta(puerta: str, db: Connection = Depends(get_db)):
    propietario = PropietarioModel.por_puerta(db, puerta)
    if propietario is None:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return propietario

@router.get("/ver_propietario_nombre/{nombre_propietario}", response_model=list[PropietarioOut])
def ver_propietario_nombre(nombre_propietario: str, db: Connection = Depends(get_db)):
    return PropietarioModel.por_nombre(db, nombre_propietario)

@router.get("/ver_propietario_estado/{estado}", response_model=list[PropietarioOut])
def ver_propietario_estado(estado: str, db: Connection = Depends(get_db)):
    return PropietarioModel.por_estado(db, estado)

@router.patch("/modificar_propietario/{puerta}", response_model=PropietarioOut)
def modificar_propietario(puerta: str, payload: PropietarioUpdate, db: Connection = Depends(get_db)):
    propietario = PropietarioModel.actualizar_por_puerta(db, puerta, payload.model_dump(exclude_unset=True))
    if propietario is None:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return propietario
