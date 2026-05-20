from fastapi import APIRouter, HTTPException, status, Depends
from api.schemas import LoginRequest, LoginResponse, CadastroUsuarioRequest, MessageResponse
from api.auth_utils import create_access_token
from api.deps import get_current_user
import backend.services as services

router = APIRouter()


def _strip_emoji(msg: str) -> str:
    return msg.replace("✅", "").replace("❌", "").replace("ℹ️", "").strip()


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest):
    sucesso, msg = services.login_usuario(body.nome, body.senha, body.cargo)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_strip_emoji(msg))

    token = create_access_token({"nome": body.nome, "cargo": body.cargo})
    return LoginResponse(access_token=token, nome=body.nome, cargo=body.cargo)


@router.post("/register", response_model=MessageResponse)
def register(body: CadastroUsuarioRequest):
    sucesso, msg = services.cadastrar_usuario(body.nome, body.senha, body.cargo)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_strip_emoji(msg))
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)


@router.post("/logout", response_model=MessageResponse)
def logout(body: LoginRequest, _user: dict = Depends(get_current_user)):
    msg = services.logout_usuario(body.nome, body.senha, body.cargo)
    return MessageResponse(mensagem=_strip_emoji(msg), sucesso=True)
