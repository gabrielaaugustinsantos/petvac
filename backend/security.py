"""
Funções de segurança: hash de senhas, verificação, etc.
"""
import bcrypt
from backend.config import HASH_ROUNDS


def hash_password(password: str) -> str:
    """
    Criptografa uma senha usando bcrypt.
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash da senha (string)
    """
    salt = bcrypt.gensalt(rounds=HASH_ROUNDS)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash.
    
    Args:
        password: Senha em texto plano
        hashed_password: Hash da senha armazenada
        
    Returns:
        True se a senha corresponde, False caso contrário
    """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except (ValueError, AttributeError):
        return False
