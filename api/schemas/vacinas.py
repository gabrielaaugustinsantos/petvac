from pydantic import BaseModel
from typing import Optional


class VacinaCreate(BaseModel):
    idPet: int
    nome: str
    dataAplicacao: Optional[str] = None
    dataProximaDose: Optional[str] = None
    obs: Optional[str] = None


class VacinaUpdate(BaseModel):
    nome: Optional[str] = None
    dataAplicacao: Optional[str] = None
    dataProximaDose: Optional[str] = None
    status: Optional[str] = None
    obs: Optional[str] = None


class AplicarDoseRequest(BaseModel):
    dataAplicacao: str
    dataProximaDose: Optional[str] = None
    obs: Optional[str] = None


class AgendarVacinaRequest(BaseModel):
    dataAgendamento: str


class VacinaResponse(BaseModel):
    idVacina: int
    idPet: int
    nome: str
    dataAplicacao: Optional[str] = None
    dataProximaDose: Optional[str] = None
    status: str
    obs: Optional[str] = None
    atrasada: Optional[bool] = None
