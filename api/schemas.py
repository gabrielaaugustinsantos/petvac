from pydantic import BaseModel
from typing import Optional


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    nome: str
    senha: str
    cargo: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nome: str
    cargo: str

class CadastroUsuarioRequest(BaseModel):
    nome: str
    senha: str
    cargo: str


# ── Tutores ───────────────────────────────────────────────────────────────────

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


# ── Pets ──────────────────────────────────────────────────────────────────────

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


# ── Vacinas ───────────────────────────────────────────────────────────────────

class VacinaCreate(BaseModel):
    idPet: int
    nome: str
    dataAplicacao: Optional[str] = None
    dataProximaDose: Optional[str] = None

class AplicarDoseRequest(BaseModel):
    dataAplicacao: str
    dataProximaDose: Optional[str] = None

class VacinaResponse(BaseModel):
    idVacina: int
    idPet: int
    nome: str
    dataAplicacao: Optional[str] = None
    dataProximaDose: Optional[str] = None
    status: str
    atrasada: Optional[bool] = None


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardMetrics(BaseModel):
    total_tutores: int
    total_pets: int
    total_vacinas: int
    total_pendentes: int
    total_atrasadas: int


# ── Notificações ──────────────────────────────────────────────────────────────

class NotificacaoResponse(BaseModel):
    idNotificacao: int
    mensagem: str
    dataEnvio: str
    status: str


# ── Genérico ──────────────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    mensagem: str
    sucesso: bool
