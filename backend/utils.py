"""
Funções utilitárias e helpers para eliminar duplicação de código.
"""
import pandas as pd
from typing import Optional, List, Dict, Any
from backend.config import CSV_FILES


def tutor_label(df: pd.DataFrame, id_tutor: int) -> str:
    """
    Retorna o label formatado de um tutor (nome e telefone).
    
    Args:
        df: DataFrame com tutores
        id_tutor: ID do tutor
        
    Returns:
        String formatada "Nome (TELEFONE)"
    """
    tutor = df[df["idTutor"] == id_tutor]
    if tutor.empty:
        return "Tutor não encontrado"
    nome = tutor.iloc[0]["nome"]
    telefone = tutor.iloc[0]["telefone"]
    return f"{nome} ({telefone})"


def pet_label(df: pd.DataFrame, id_pet: int) -> str:
    """
    Retorna o label formatado de um pet (nome e espécie).
    
    Args:
        df: DataFrame com pets
        id_pet: ID do pet
        
    Returns:
        String formatada "Nome - Espécie"
    """
    pet = df[df["idPet"] == id_pet]
    if pet.empty:
        return "Pet não encontrado"
    nome = pet.iloc[0]["nome"]
    especie = pet.iloc[0]["especie"]
    return f"{nome} - {especie}"


def prepare_pets_with_tutors(
    pets_df: pd.DataFrame, tutores_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Prepara DataFrame de pets com informações dos tutores.
    
    Args:
        pets_df: DataFrame com dados de pets
        tutores_df: DataFrame com dados de tutores
        
    Returns:
        DataFrame com pets e colunas de tutor mescladas
    """
    resultado = pets_df.merge(
        tutores_df[["idTutor", "nome", "telefone"]],
        on="idTutor",
        how="left",
        suffixes=("_pet", "_tutor")
    )
    resultado = resultado.rename(columns={
        "nome_pet": "pet_nome",
        "nome_tutor": "tutor_nome",
        "telefone": "tutor_telefone"
    })
    return resultado


def get_dict_options(
    df: pd.DataFrame, id_col: str, label_col: str
) -> Dict[str, int]:
    """
    Cria um dicionário de opções para selectbox do Streamlit.
    
    Args:
        df: DataFrame
        id_col: Nome da coluna de ID
        label_col: Nome da coluna de label
        
    Returns:
        Dicionário {label: id}
    """
    if df.empty:
        return {}
    return {row[label_col]: row[id_col] for _, row in df.iterrows()}


def format_date(date_str: str, format_output: str = "%d/%m/%Y") -> str:
    """
    Formata uma data de string para outro formato.
    
    Args:
        date_str: Data em formato YYYY-MM-DD
        format_output: Formato de saída desejado
        
    Returns:
        Data formatada
    """
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime(format_output)
    except (ValueError, TypeError):
        return date_str


def safe_merge(*dfs: pd.DataFrame, on: str = "id", how: str = "left") -> pd.DataFrame:
    """
    Faz um merge seguro de múltiplos DataFrames.
    
    Args:
        *dfs: DataFrames a mesclar
        on: Coluna para mesclar
        how: Tipo de merge (left, right, inner, outer)
        
    Returns:
        DataFrame mesclado
    """
    if not dfs:
        return pd.DataFrame()
    
    result = dfs[0]
    for df in dfs[1:]:
        if not df.empty:
            result = result.merge(df, on=on, how=how, suffixes=("", "_dup"))
    
    return result


def get_first_weekday(year: int, month: int, day_of_week: int) -> int:
    """
    Retorna o dia do primeiro dia da semana especificado em um mês.
    
    Args:
        year: Ano
        month: Mês (1-12)
        day_of_week: Dia da semana (0=segunda, 6=domingo)
        
    Returns:
        Dia do mês (1-31)
    """
    from datetime import datetime, timedelta
    
    # Primeiro dia do mês
    first_day = datetime(year, month, 1)
    
    # Calcular dias até o primeiro dia_of_week
    days_ahead = day_of_week - first_day.weekday()
    if days_ahead < 0:
        days_ahead += 7
    
    return 1 + days_ahead
