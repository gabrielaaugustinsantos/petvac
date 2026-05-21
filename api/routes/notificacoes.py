from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from api.schemas import NotificacaoResponse, MessageResponse
from api.deps import get_current_user
from api.utils.helpers import strip_emoji, is_error, df_to_records
from backend.database import carregar_dados, COLUNAS
import backend.services as services

router = APIRouter()


@router.get(
    "/",
    response_model=List[NotificacaoResponse],
    summary="Listar notificações",
    description="Retorna todas as notificações geradas, ordenadas pela mais recente.",
)
def listar_notificacoes(_user: dict = Depends(get_current_user)):
    df = carregar_dados("data/notificacoes.csv", COLUNAS["notificacoes"])
    if df.empty:
        return []
    return df_to_records(df)


@router.post(
    "/gerar",
    response_model=MessageResponse,
    summary="Gerar notificações",
    description="Analisa vacinas pendentes/atrasadas e cria notificações para cada uma.",
)
def gerar_notificacoes(_user: dict = Depends(get_current_user)):
    msg = services.gerar_notificacoes_pendentes()
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=not is_error(msg))


@router.put(
    "/{id_notificacao}/lida",
    response_model=MessageResponse,
    summary="Marcar como lida",
    description="Atualiza o status de uma notificação para 'lida'.",
)
def marcar_lida(id_notificacao: int, _user: dict = Depends(get_current_user)):
    msg = services.marcar_notificacao_como_lida(id_notificacao)
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)
