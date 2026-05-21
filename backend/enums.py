"""
Enumerações para melhorar tipagem e evitar strings mágicas.
"""
from enum import Enum


class VacinaStatus(str, Enum):
    """Status possíveis de uma vacina."""
    PENDENTE = "pendente"
    APLICADA = "aplicada"
    CONCLUIDA = "concluída"


class Cargo(str, Enum):
    """Cargos de usuários do sistema."""
    RECEPCIONISTA = "recepcionista"
    VETERINARIO = "veterinario"
    ADMIN = "admin"


class Especie(str, Enum):
    """Espécies de pets suportadas."""
    CACHORRO = "Cachorro"
    GATO = "Gato"
    PASSARO = "Pássaro"
    COELHO = "Coelho"
    HAMSTER = "Hamster"
    OUTRO = "Outro"
