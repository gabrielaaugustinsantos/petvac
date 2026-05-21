"""
Schemas Pydantic da API PetVac — organizados por domínio.
"""
from api.schemas.auth import LoginRequest, LoginResponse, CadastroUsuarioRequest, RedefinirSenhaRequest
from api.schemas.tutores import TutorCreate, TutorUpdate, TutorResponse
from api.schemas.pets import PetCreate, PetUpdate, PetResponse
from api.schemas.vacinas import VacinaCreate, VacinaUpdate, AplicarDoseRequest, AgendarVacinaRequest, VacinaResponse
from api.schemas.notificacoes import NotificacaoResponse
from api.schemas.dashboard import DashboardMetrics
from api.schemas.common import MessageResponse

__all__ = [
    # Auth
    "LoginRequest", "LoginResponse", "CadastroUsuarioRequest", "RedefinirSenhaRequest",
    # Tutores
    "TutorCreate", "TutorUpdate", "TutorResponse",
    # Pets
    "PetCreate", "PetUpdate", "PetResponse",
    # Vacinas
    "VacinaCreate", "VacinaUpdate", "AplicarDoseRequest", "AgendarVacinaRequest", "VacinaResponse",
    # Notificações
    "NotificacaoResponse",
    # Dashboard
    "DashboardMetrics",
    # Comum
    "MessageResponse",
]
