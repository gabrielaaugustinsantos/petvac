from pydantic import BaseModel, EmailStr
from typing import Optional


class TutorCreate(BaseModel):
    nome: str
    telefone: str
    email: str
    endereco: Optional[str] = ""


class TutorUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None


class TutorResponse(BaseModel):
    idTutor: int
    nome: str
    telefone: str
    email: str
    endereco: Optional[str] = ""
