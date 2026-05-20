from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from api.schemas import TutorCreate, TutorUpdate, TutorResponse, MessageResponse
from api.deps import get_current_user
import backend.services as services

router = APIRouter()


def _strip_emoji(msg: str) -> str:
    return msg.replace("✅", "").replace("❌", "").strip()


def _df_to_tutores(df) -> List[dict]:
    df = df.fillna("")
    return df.to_dict(orient="records")


@router.get("/", response_model=List[TutorResponse])
def listar_tutores(_user: dict = Depends(get_current_user)):
    df = services.listar_tutores()
    return _df_to_tutores(df)


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_tutor(body: TutorCreate, _user: dict = Depends(get_current_user)):
    msg = services.cadastrar_tutor(body.nome, body.telefone, body.email, body.endereco or "")
    if msg.startswith("❌"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)


@router.put("/{idTutor}", response_model=MessageResponse)
def atualizar_tutor(idTutor: int, body: TutorUpdate, _user: dict = Depends(get_current_user)):
    novos_dados = {k: v for k, v in body.model_dump().items() if v is not None}
    if not novos_dados:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado para atualizar")
    msg = services.atualizar_tutor(idTutor, novos_dados)
    if msg.startswith("❌"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)
