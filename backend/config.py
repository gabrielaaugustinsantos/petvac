"""
Configurações centralizadas do sistema PetVac.
"""
import os
from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).parent.parent

# Diretório de dados
DATA_DIR = BASE_DIR / "data"

# Arquivos de dados
CSV_FILES = {
    "usuarios": DATA_DIR / "usuarios.csv",
    "pets": DATA_DIR / "pets.csv",
    "tutores": DATA_DIR / "tutores.csv",
    "vacinas": DATA_DIR / "vacinas.csv",
    "notificacoes": DATA_DIR / "notificacoes.csv",
}

# Configurações de segurança
HASH_ROUNDS = 12  # Número de rounds para bcrypt

# Configurações de validação
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PHONE_REGEX = r"^\d{10,11}$"  # 10-11 dígitos

# Status de vacina
VACINA_STATUS = ["pendente", "aplicada", "concluída"]

# Cargos de usuário
CARGOS = ["recepcionista", "veterinario", "admin"]

# Espécies de pets
ESPECIES = ["Cachorro", "Gato", "Pássaro", "Coelho", "Hamster", "Outro"]
