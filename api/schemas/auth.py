from pydantic import BaseModel, EmailStr
from typing import Literal


class LoginRequest(BaseModel):
    email: str
    senha: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nome: str
    cargo: str


class CadastroUsuarioRequest(BaseModel):
    nome: str
    email: str
    senha: str
    cargo: Literal["recepcionista", "veterinario"]


class RedefinirSenhaRequest(BaseModel):
    email: str
    nova_senha: str
