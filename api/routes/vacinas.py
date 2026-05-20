from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Union
from api.schemas import VacinaCreate, AplicarDoseRequest, VacinaResponse, MessageResponse
from api.deps import get_current_user
import backend.services as services
import pandas as pd

router = APIRouter()


def _strip_emoji(msg: str) -> str:
    return msg.replace("✅", "").replace("❌", "").strip()


def _df_to_vacinas(df) -> List[dict]:
    df = df.copy()
    for col in df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns:
        df[col] = df[col].astype(str).replace("NaT", "")
    df = df.fillna("")
    if "atrasada" in df.columns:
        df["atrasada"] = df["atrasada"].astype(bool)
    return df.to_dict(orient="records")


@router.get("/pendentes", response_model=List[VacinaResponse])
def vacinas_pendentes(_user: dict = Depends(get_current_user)):
    df = services.consultar_vacinas_pendentes()
    if df.empty:
        return []
    return _df_to_vacinas(df)


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def registrar_vacina(body: VacinaCreate, _user: dict = Depends(get_current_user)):
    msg = services.registrar_vacina(
        body.idPet, body.nome, body.dataAplicacao, body.dataProximaDose
    )
    if msg.startswith("❌"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)


@router.post("/{idVacina}/aplicar", response_model=MessageResponse)
def aplicar_dose(idVacina: int, body: AplicarDoseRequest, _user: dict = Depends(get_current_user)):
    msg = services.aplicar_dose(idVacina, body.dataAplicacao, body.dataProximaDose)
    if msg.startswith("❌"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)


@router.get("/historico/{idPet}", response_model=List[VacinaResponse])
def historico_pet(idPet: int, _user: dict = Depends(get_current_user)):
    resultado = services.consultar_historico_pet(idPet)
    if isinstance(resultado, str):
        return []
    return _df_to_vacinas(resultado)
