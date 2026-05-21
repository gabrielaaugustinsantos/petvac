from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from api.schemas import PetCreate, PetUpdate, PetResponse, MessageResponse
from api.deps import get_current_user
from api.utils.helpers import strip_emoji, is_error, df_to_records
import backend.services as services

router = APIRouter()


@router.get(
    "/",
    response_model=List[PetResponse],
    summary="Listar pets",
    description="Retorna todos os pets cadastrados no sistema.",
)
def listar_pets(_user: dict = Depends(get_current_user)):
    return df_to_records(services.listar_pets())


@router.get(
    "/{id_pet}",
    response_model=PetResponse,
    summary="Buscar pet por ID",
)
def buscar_pet(id_pet: int, _user: dict = Depends(get_current_user)):
    df = services.listar_pets()
    resultado = df[df["idPet"] == id_pet]
    if resultado.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet não encontrado")
    return df_to_records(resultado)[0]


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar pet",
    description="Cadastra um novo pet associado a um tutor existente.",
)
def cadastrar_pet(body: PetCreate, _user: dict = Depends(get_current_user)):
    msg = services.cadastrar_pet(
        body.nome, body.especie, body.raca, body.dataNascimento, body.idTutor
    )
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.put(
    "/{id_pet}",
    response_model=MessageResponse,
    summary="Atualizar pet",
    description="Atualiza dados de um pet existente. Apenas os campos enviados serão alterados.",
)
def atualizar_pet(id_pet: int, body: PetUpdate, _user: dict = Depends(get_current_user)):
    novos_dados = {k: v for k, v in body.model_dump().items() if v is not None}
    if not novos_dados:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado para atualizar")
    msg = services.atualizar_pet(id_pet, novos_dados)
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.delete(
    "/{id_pet}",
    response_model=MessageResponse,
    summary="Remover pet",
    description="Remove um pet do sistema permanentemente.",
)
def remover_pet(id_pet: int, _user: dict = Depends(get_current_user)):
    msg = services.remover_pet(id_pet)
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)
