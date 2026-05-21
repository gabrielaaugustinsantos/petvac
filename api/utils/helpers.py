"""
Utilitários compartilhados entre os módulos da API.
"""
import pandas as pd
from typing import Any


# ── Limpeza de strings ────────────────────────────────────────────────────────

_EMOJIS = ["✅", "❌", "ℹ️", "⚠️", "👋"]


def strip_emoji(text: str) -> str:
    """Remove emojis de mensagens vindas da camada de serviço."""
    for emoji in _EMOJIS:
        text = text.replace(emoji, "")
    return text.strip()


def is_error(msg: str) -> bool:
    """Retorna True se a mensagem indica um erro (começa com ❌)."""
    return msg.startswith("❌")


# ── Conversão de DataFrames ───────────────────────────────────────────────────

def df_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Converte um DataFrame para lista de dicts, tratando NaN e datas."""
    df = df.copy()

    # Converte colunas datetime para string legível
    for col in df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns:
        df[col] = df[col].dt.strftime("%Y-%m-%d").where(df[col].notna(), other="")

    # NaT → string vazia; NaN → string vazia para colunas de texto
    df = df.fillna("")

    # Garante que colunas booleanas sejam bool
    for col in df.select_dtypes(include=["bool", "object"]).columns:
        if col == "atrasada":
            df[col] = df[col].astype(bool)

    return df.to_dict(orient="records")
