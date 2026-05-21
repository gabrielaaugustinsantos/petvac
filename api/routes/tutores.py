from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from api.schemas import TutorCreate, TutorUpdate, TutorResponse, MessageResponse
from api.deps import get_current_user
from api.utils.helpers import strip_emoji, is_error, df_to_records
import backend.services as services

router = APIRouter()


@router.get(
    "/",
    response_model=List[TutorResponse],
    summary="Listar tutores",
    description="Retorna todos os tutores cadastrados no sistema.",
)
def listar_tutores(_user: dict = Depends(get_current_user)):
    return df_to_records(services.listar_tutores())


@router.get(
    "/{id_tutor}",
    response_model=TutorResponse,
    summary="Buscar tutor por ID",
)
def buscar_tutor(id_tutor: int, _user: dict = Depends(get_current_user)):
    df = services.listar_tutores()
    resultado = df[df["idTutor"] == id_tutor]
    if resultado.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tutor não encontrado")
    return df_to_records(resultado)[0]


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar tutor",
    description="Cadastra um novo tutor responsável por pets.",
)
def cadastrar_tutor(body: TutorCreate, _user: dict = Depends(get_current_user)):
    msg = services.cadastrar_tutor(body.nome, body.telefone, body.email, body.endereco or "")
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.put(
    "/{id_tutor}",
    response_model=MessageResponse,
    summary="Atualizar tutor",
    description="Atualiza dados de um tutor existente. Apenas os campos enviados serão alterados.",
)
def atualizar_tutor(id_tutor: int, body: TutorUpdate, _user: dict = Depends(get_current_user)):
    novos_dados = {k: v for k, v in body.model_dump().items() if v is not None}
    if not novos_dados:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado para atualizar")
    msg = services.atualizar_tutor(id_tutor, novos_dados)
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.delete(
    "/{id_tutor}",
    response_model=MessageResponse,
    summary="Remover tutor",
    description="Remove um tutor do sistema permanentemente.",
)
def remover_tutor(id_tutor: int, _user: dict = Depends(get_current_user)):
    msg = services.remover_tutor(id_tutor)
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)
