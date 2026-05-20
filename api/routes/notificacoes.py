from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from api.schemas import NotificacaoResponse, MessageResponse
from api.deps import get_current_user
from backend.database import carregar_dados, COLUNAS
import backend.services as services

router = APIRouter()


def _strip_emoji(msg: str) -> str:
    return msg.replace("✅", "").replace("❌", "").replace("ℹ️", "").strip()


@router.get("/", response_model=List[NotificacaoResponse])
def listar_notificacoes(_user: dict = Depends(get_current_user)):
    df = carregar_dados("data/notificacoes.csv", COLUNAS["notificacoes"])
    if df.empty:
        return []
    df = df.fillna("")
    return df.to_dict(orient="records")


@router.post("/gerar", response_model=MessageResponse)
def gerar_notificacoes(_user: dict = Depends(get_current_user)):
    msg = services.gerar_notificacoes_pendentes()
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=not msg.startswith("❌"))


@router.put("/{idNotificacao}/lida", response_model=MessageResponse)
def marcar_lida(idNotificacao: int, _user: dict = Depends(get_current_user)):
    msg = services.marcar_notificacao_como_lida(idNotificacao)
    if msg.startswith("❌"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)
