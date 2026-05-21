"""
Configurações centralizadas da API PetVac.
Lê variáveis de ambiente com fallback para desenvolvimento local.
"""
import os

# Segurança JWT
SECRET_KEY: str = os.environ.get("PETVAC_SECRET_KEY", "petvac-dev-secret-mude-em-producao")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("PETVAC_TOKEN_EXPIRE_MINUTES", "480"))  # 8h

# CORS — em produção defina PETVAC_ALLOWED_ORIGINS="https://meusite.com"
_raw_origins = os.environ.get("PETVAC_ALLOWED_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in _raw_origins.split(",")]
