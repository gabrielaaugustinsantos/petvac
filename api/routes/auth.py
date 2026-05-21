from fastapi import APIRouter, HTTPException, status, Depends

from api.schemas import (
    LoginRequest, LoginResponse,
    CadastroUsuarioRequest, RedefinirSenhaRequest,
    MessageResponse,
)
from api.auth_utils import create_access_token
from api.deps import get_current_user
from api.utils.helpers import strip_emoji, is_error
import backend.services as services

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticar usuário",
    description="Realiza login com e-mail e senha. Retorna JWT Bearer válido por 8 horas.",
)
def login(body: LoginRequest):
    sucesso, msg, dados = services.login_usuario(body.email, body.senha)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=strip_emoji(msg))

    token = create_access_token({"nome": dados["nome"], "cargo": dados["cargo"], "email": body.email})
    return LoginResponse(access_token=token, nome=dados["nome"], cargo=dados["cargo"])


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar conta",
    description="Cadastra um novo usuário. O e-mail deve ser único no sistema.",
)
def register(body: CadastroUsuarioRequest):
    sucesso, msg = services.cadastrar_usuario(body.nome, body.email, body.senha, body.cargo)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Encerrar sessão",
    description="O cliente deve descartar o token JWT. Sem estado no servidor.",
)
def logout(_user: dict = Depends(get_current_user)):
    return MessageResponse(mensagem="Logout realizado com sucesso.", sucesso=True)


@router.post(
    "/redefinir-senha",
    response_model=MessageResponse,
    summary="Redefinir senha",
    description=(
        "Redefine a senha associada ao e-mail informado. "
        "Sempre retorna sucesso para não confirmar a existência do e-mail."
    ),
)
def redefinir_senha(body: RedefinirSenhaRequest):
    sucesso, msg = services.redefinir_senha(body.email, body.nova_senha)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strip_emoji(msg))
    return MessageResponse(mensagem=strip_emoji(msg), sucesso=True)
