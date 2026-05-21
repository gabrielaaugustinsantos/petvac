from pydantic import BaseModel
from typing import Optional


class PetCreate(BaseModel):
    nome: str
    especie: str
    raca: str
    dataNascimento: str
    idTutor: int


class PetUpdate(BaseModel):
    nome: Optional[str] = None
    especie: Optional[str] = None
    raca: Optional[str] = None
    dataNascimento: Optional[str] = None
    idTutor: Optional[int] = None


class PetResponse(BaseModel):
    idPet: int
    nome: str
    especie: str
    raca: str
    dataNascimento: str
    idTutor: int
