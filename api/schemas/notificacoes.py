from pydantic import BaseModel
from typing import Optional


class NotificacaoResponse(BaseModel):
    idNotificacao: int
    mensagem: str
    dataEnvio: Optional[str] = None
    status: str
    urgencia: Optional[str] = None  # "urgente" | "alerta" | "lembrete"
