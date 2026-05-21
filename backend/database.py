import pandas as pd
import os

def carregar_dados(caminho, colunas):
    if not os.path.exists(caminho):
        df = pd.DataFrame(columns=colunas)
        df.to_csv(caminho, index=False)
        return df
    try:
        df = pd.read_csv(caminho)

        # Garantir que TODAS as colunas existem
        for col in colunas:
            if col not in df.columns:
                df[col] = None

        # Reordenar
        df = df[colunas]

        return df

    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=colunas)
        df.to_csv(caminho, index=False)
        return df


def salvar_dados(df, caminho):
    df.to_csv(caminho, index=False)

COLUNAS = {
    "pets": ["idPet", "nome", "especie", "raca", "dataNascimento", "idTutor"],
    "tutores": ["idTutor", "nome", "telefone", "email", "endereco"],
    "vacinas": ["idVacina", "idPet", "nome", "dataAplicacao", "dataProximaDose", "status", "obs"],
    "usuarios": ["idUsuario", "nome", "email", "senha", "cargo"],
    "notificacoes": ["idNotificacao", "mensagem", "dataEnvio", "status"],
}
