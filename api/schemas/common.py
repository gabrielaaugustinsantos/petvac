from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Resposta genérica para operações de escrita."""
    mensagem: str
    sucesso: bool
