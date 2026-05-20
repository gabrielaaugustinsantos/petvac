"""
Validadores usando Pydantic para garantir integridade dos dados.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from backend.config import EMAIL_REGEX, PHONE_REGEX, CARGOS, ESPECIES, VACINA_STATUS


class UsuarioValidator(BaseModel):
    """Validação para dados de usuário."""
    nome: str
    email: str
    telefone: str
    cargo: str
    senha: Optional[str] = None
    
    @field_validator("nome")
    def nome_valido(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip()
    
    @field_validator("email")
    def email_valido(cls, v):
        import re
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Email inválido")
        return v.lower()
    
    @field_validator("telefone")
    def telefone_valido(cls, v):
        import re
        if not re.match(PHONE_REGEX, v.replace("-", "").replace(" ", "")):
            raise ValueError("Telefone deve ter 10-11 dígitos")
        return v
    
    @field_validator("cargo")
    def cargo_valido(cls, v):
        if v not in CARGOS:
            raise ValueError(f"Cargo deve ser um de: {CARGOS}")
        return v


class TutorValidator(BaseModel):
    """Validação para dados de tutor."""
    nome: str
    email: str
    telefone: str
    
    @field_validator("nome")
    def nome_valido(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip()
    
    @field_validator("email")
    def email_valido(cls, v):
        import re
        if v.strip() and not re.match(EMAIL_REGEX, v):
            raise ValueError("Email inválido")
        return v.lower() if v else v
    
    @field_validator("telefone")
    def telefone_valido(cls, v):
        import re
        if not re.match(PHONE_REGEX, v.replace("-", "").replace(" ", "")):
            raise ValueError("Telefone deve ter 10-11 dígitos")
        return v


class PetValidator(BaseModel):
    """Validação para dados de pet."""
    nome: str
    especie: str
    raca: str
    data_nascimento: str
    idTutor: int
    
    @field_validator("nome")
    def nome_valido(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        return v.strip()
    
    @field_validator("especie")
    def especie_valida(cls, v):
        if v not in ESPECIES:
            raise ValueError(f"Espécie deve ser uma de: {ESPECIES}")
        return v
    
    @field_validator("data_nascimento")
    def data_valida(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Data deve estar no formato YYYY-MM-DD")


class VacinaValidator(BaseModel):
    """Validação para dados de vacina."""
    nome: str
    data_aplicacao: str
    proxima_dose: Optional[str] = None
    status: str
    idPet: int
    
    @field_validator("nome")
    def nome_valido(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Nome da vacina deve ter pelo menos 2 caracteres")
        return v.strip()
    
    @field_validator("data_aplicacao")
    def data_aplicacao_valida(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Data deve estar no formato YYYY-MM-DD")
    
    @field_validator("proxima_dose")
    def proxima_dose_valida(cls, v):
        if v:
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Data deve estar no formato YYYY-MM-DD")
        return v
    
    @field_validator("status")
    def status_valido(cls, v):
        if v not in VACINA_STATUS:
            raise ValueError(f"Status deve ser um de: {VACINA_STATUS}")
        return v
