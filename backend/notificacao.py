from datetime import datetime
from typing import Optional


class Notificacao:
    def __init__(
        self,
        idNotificacao: int,
        mensagem: str,
        dataEnvio: Optional[str] = None,
        status: str = "pendente",
    ):
        self.idNotificacao = idNotificacao
        self.mensagem = mensagem
        self.dataEnvio = dataEnvio or datetime.now().strftime("%Y-%m-%d")
        self.status = status

    def enviarNotificacao(self) -> str:
        if self.status == "pendente":
            self.status = "enviada"
            self.dataEnvio = datetime.now().strftime("%Y-%m-%d")
            return f"Notificação {self.idNotificacao} enviada."
        return "Notificação já foi enviada."

    def marcarComoLida(self) -> None:
        self.status = "lida"
