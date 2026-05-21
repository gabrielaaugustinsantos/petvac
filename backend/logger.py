"""
Sistema centralizado de logging para PetVac.
"""
import logging
from datetime import datetime
from backend.config import BASE_DIR

# Criar diretório de logs se não existir
logs_dir = BASE_DIR / "logs"
logs_dir.mkdir(exist_ok=True)

# Configurar logger
logger = logging.getLogger("petvac")
logger.setLevel(logging.DEBUG)

# Handler para arquivo
file_handler = logging.FileHandler(
    logs_dir / f"petvac_{datetime.now().strftime('%Y%m%d')}.log",
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# Handler para console (apenas erros em produção)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formato das mensagens
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_info(message: str):
    """Registra uma informação."""
    logger.info(message)


def log_error(message: str, exception: Exception = None):
    """Registra um erro."""
    if exception:
        logger.error(f"{message}: {str(exception)}", exc_info=True)
    else:
        logger.error(message)


def log_warning(message: str):
    """Registra um aviso."""
    logger.warning(message)


def log_debug(message: str):
    """Registra informações de debug."""
    logger.debug(message)
