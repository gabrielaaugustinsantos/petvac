from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from api.schemas import PetCreate, PetUpdate, PetResponse, MessageResponse
from api.deps import get_current_user
import backend.services as services

router = APIRouter()


def _strip_emoji(msg: str) -> str:
    return msg.replace("✅", "").replace("❌", "").strip()


def _df_to_pets(df) -> List[dict]:
    df = df.fillna("")
    return df.to_dict(orient="records")


@router.get("/", response_model=List[PetResponse])
def listar_pets(_user: dict = Depends(get_current_user)):
    df = services.listar_pets()
    return _df_to_pets(df)


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_pet(body: PetCreate, _user: dict = Depends(get_current_user)):
    msg = services.cadastrar_pet(
        body.nome, body.especie, body.raca, body.dataNascimento, body.idTutor
    )
    if msg.startswith("❌"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)


@router.put("/{idPet}", response_model=MessageResponse)
def atualizar_pet(idPet: int, body: PetUpdate, _user: dict = Depends(get_current_user)):
    novos_dados = {k: v for k, v in body.model_dump().items() if v is not None}
    if not novos_dados:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado para atualizar")
    msg = services.atualizar_pet(idPet, novos_dados)
    if msg.startswith("❌"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)
