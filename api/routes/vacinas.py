from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from api.schemas import VacinaCreate, AplicarDoseRequest, AgendarVacinaRequest, VacinaResponse, MessageResponse
from api.deps import get_current_user
from api.utils.helpers import strip_emoji, is_error, df_to_records
import backend.services as services

router = APIRouter()


@router.get(
    "/pendentes",
    response_model=List[VacinaResponse],
    summary="Vacinas pendentes",
    description="Lista vacinas com status 'pendente', incluindo flag de atraso.",
)
def vacinas_pendentes(_user: dict = Depends(get_current_user)):
    df = services.consultar_vacinas_pendentes()
    if df.empty:
        return []
    return df_to_records(df)


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar vacina",
    description="Registra uma nova vacina para um pet. Status é calculado automaticamente.",
)
def registrar_vacina(body: VacinaCreate, _user: dict = Depends(get_current_user)):
    msg = services.registrar_vacina(
        body.idPet, body.nome, body.dataAplicacao, body.dataProximaDose, body.obs
    )
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.post(
    "/{id_vacina}/aplicar",
    response_model=MessageResponse,
    summary="Aplicar dose pendente",
    description="Marca uma vacina pendente como aplicada e registra a próxima dose, se informada.",
)
def aplicar_dose(id_vacina: int, body: AplicarDoseRequest, _user: dict = Depends(get_current_user)):
    msg = services.aplicar_dose(id_vacina, body.dataAplicacao, body.dataProximaDose, body.obs)
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.patch(
    "/{id_vacina}/agendar",
    response_model=MessageResponse,
    summary="Agendar vacina",
    description="Atualiza a data da próxima dose sem alterar o status. Mantém a vacina como pendente.",
)
def agendar_vacina(id_vacina: int, body: AgendarVacinaRequest, _user: dict = Depends(get_current_user)):
    msg = services.agendar_vacina(id_vacina, body.dataAgendamento)
    if is_error(msg):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.get(
    "/historico/{id_pet}",
    response_model=List[VacinaResponse],
    summary="Histórico de vacinação",
    description="Retorna todo o histórico de vacinas de um pet específico, ordenado por data.",
)
def historico_pet(id_pet: int, _user: dict = Depends(get_current_user)):
    resultado = services.consultar_historico_pet(id_pet)
    if isinstance(resultado, str):
        return []
    return df_to_records(resultado)
