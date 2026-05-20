"""
Serviços e lógica de negócio do sistema PetVac.
Centraliza operações de cadastro, atualização e consulta de dados.
"""
from typing import Tuple, Optional
from datetime import date, datetime
import pandas as pd

from backend.database import carregar_dados, salvar_dados, COLUNAS
from backend.pet import Pet
from backend.tutor import Tutor
from backend.vacina import Vacina
from backend.usuario import Usuario
from backend.historico_vacinas import HistoricoVacinas
from backend.notificacao import Notificacao
from backend.security import hash_password, verify_password
from backend.validators import PetValidator, TutorValidator, UsuarioValidator, VacinaValidator
from backend.logger import log_info, log_error, log_warning
from backend.utils import prepare_pets_with_tutors


# ---------- PETS ----------

def cadastrar_pet(nome: str, especie: str, raca: str, dataNascimento: str, idTutor: int) -> str:
    """
    Cadastra um novo pet no sistema com validação de dados.
    
    Args:
        nome: Nome do pet
        especie: Espécie do pet
        raca: Raça do pet
        dataNascimento: Data de nascimento (YYYY-MM-DD)
        idTutor: ID do tutor responsável
        
    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        # Validar dados
        PetValidator(
            nome=nome,
            especie=especie,
            raca=raca,
            data_nascimento=dataNascimento,
            idTutor=idTutor
        )
        
        df = carregar_dados("data/pets.csv", COLUNAS["pets"])
        novo_id = len(df) + 1
        pet = Pet(novo_id, nome, especie, raca, dataNascimento, idTutor)
        
        novo_pet_df = pd.DataFrame([vars(pet)])
        df = pd.concat([df, novo_pet_df], ignore_index=True)
        
        salvar_dados(df, "data/pets.csv")
        log_info(f"Pet '{nome}' cadastrado com sucesso (ID: {novo_id})")
        return "✅ Pet cadastrado com sucesso!"
    except ValueError as e:
        log_error(f"Erro ao validar dados do pet: {str(e)}")
        return f"❌ Erro: {str(e)}"
    except Exception as e:
        log_error(f"Erro ao cadastrar pet", e)
        return "❌ Erro ao cadastrar pet"


def atualizar_pet(idPet: int, novos_dados: dict) -> str:
    """
    Atualiza dados de um pet existente.
    
    Args:
        idPet: ID do pet
        novos_dados: Dicionário com novos dados
        
    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        df = carregar_dados("data/pets.csv", COLUNAS["pets"])
        pet = Pet(idPet, None, None, None, None, None)
        df = pet.atualizar_pet(df, novos_dados)
        
        salvar_dados(df, "data/pets.csv")
        log_info(f"Pet {idPet} atualizado com sucesso")
        return "✅ Pet atualizado com sucesso!"
    except Exception as e:
        log_error(f"Erro ao atualizar pet {idPet}", e)
        return "❌ Erro ao atualizar pet"


def listar_pets() -> pd.DataFrame:
    """Lista todos os pets cadastrados."""
    return carregar_dados("data/pets.csv", COLUNAS["pets"])


# ---------- TUTORES ----------

def cadastrar_tutor(nome: str, telefone: str, email: str, endereco: str = "") -> str:
    """
    Cadastra um novo tutor com validação de dados.
    
    Args:
        nome: Nome do tutor
        telefone: Telefone (10-11 dígitos)
        email: Email válido
        endereco: Endereço (opcional)
        
    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        # Validar dados
        TutorValidator(nome=nome, email=email, telefone=telefone)
        
        df = carregar_dados("data/tutores.csv", COLUNAS["tutores"])
        novo_id = len(df) + 1
        tutor = Tutor(novo_id, nome, telefone, email, endereco)
        
        novo_tutor_df = pd.DataFrame([vars(tutor)])
        df = pd.concat([df, novo_tutor_df], ignore_index=True)
        
        salvar_dados(df, "data/tutores.csv")
        log_info(f"Tutor '{nome}' cadastrado com sucesso (ID: {novo_id})")
        return "✅ Tutor cadastrado com sucesso!"
    except ValueError as e:
        log_error(f"Erro ao validar dados do tutor: {str(e)}")
        return f"❌ Erro: {str(e)}"
    except Exception as e:
        log_error(f"Erro ao cadastrar tutor", e)
        return "❌ Erro ao cadastrar tutor"


def atualizar_tutor(idTutor: int, novos_dados: dict) -> str:
    """
    Atualiza dados de um tutor existente.
    
    Args:
        idTutor: ID do tutor
        novos_dados: Dicionário com novos dados
        
    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        df = carregar_dados("data/tutores.csv", COLUNAS["tutores"])
        tutor = Tutor(idTutor, None, None, None, None)
        df = tutor.atualizar_tutor(df, novos_dados)
        
        salvar_dados(df, "data/tutores.csv")
        log_info(f"Tutor {idTutor} atualizado com sucesso")
        return "✅ Tutor atualizado com sucesso!"
    except Exception as e:
        log_error(f"Erro ao atualizar tutor {idTutor}", e)
        return "❌ Erro ao atualizar tutor"


def listar_tutores() -> pd.DataFrame:
    """Lista todos os tutores cadastrados."""
    return carregar_dados("data/tutores.csv", COLUNAS["tutores"])


# ---------- VACINAS E HISTÓRICO ----------

def registrar_vacina(idPet: int, nome: str, dataAplicacao: Optional[str] = None, 
                     dataProximaDose: Optional[str] = None) -> str:
    """
    Registra uma nova vacina com status automático baseado na data.
    
    Args:
        idPet: ID do pet
        nome: Nome da vacina
        dataAplicacao: Data de aplicação (YYYY-MM-DD ou None)
        dataProximaDose: Data da próxima dose (YYYY-MM-DD ou None)
        
    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        # Validar dados
        VacinaValidator(
            nome=nome,
            data_aplicacao=dataAplicacao or "",
            proxima_dose=dataProximaDose,
            status="pendente",
            idPet=idPet
        )
        
        df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
        novo_id = len(df) + 1

        def to_date_or_none(v):
            if v is None or v == "":
                return None
            if isinstance(v, date):
                return v
            try:
                return pd.to_datetime(v, errors="coerce").date()
            except Exception:
                return None

        dataAplicacao_date = to_date_or_none(dataAplicacao)
        dataProximaDose_date = to_date_or_none(dataProximaDose)

        hoje = datetime.now().date()

        # Determinar status
        if dataAplicacao_date is None:
            status = "pendente"
        elif dataAplicacao_date <= hoje:
            status = "aplicada"
        else:
            status = "pendente"  # Agendamento futuro

        vacina = {
            "idVacina": novo_id,
            "idPet": idPet,
            "nome": nome,
            "dataAplicacao": str(dataAplicacao_date) if dataAplicacao_date else "",
            "dataProximaDose": str(dataProximaDose_date) if dataProximaDose_date else "",
            "status": status
        }

        novo_vacina_df = pd.DataFrame([vacina])
        df = pd.concat([df, novo_vacina_df], ignore_index=True)
        
        salvar_dados(df, "data/vacinas.csv")
        log_info(f"Vacina '{nome}' do pet {idPet} registrada com sucesso (Status: {status})")
        return "✅ Vacina registrada com sucesso!"
    except ValueError as e:
        log_error(f"Erro ao validar dados da vacina: {str(e)}")
        return f"❌ Erro: {str(e)}"
    except Exception as e:
        log_error(f"Erro ao registrar vacina", e)
        return "❌ Erro ao registrar vacina"


def consultar_vacinas_pendentes() -> pd.DataFrame:
    """
    Retorna vacinas com status 'pendente' ou que estão atrasadas.
    
    Returns:
        DataFrame com vacinas pendentes/atrasadas
    """
    df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
    if df.empty:
        return pd.DataFrame()
    
    hoje = pd.Timestamp.now().normalize()

    df["dataProximaDose"] = pd.to_datetime(df["dataProximaDose"], errors="coerce")
    df["dataAplicacao"] = pd.to_datetime(df["dataAplicacao"], errors="coerce")

    pendentes = df[df["status"] == "pendente"].copy()
    pendentes["atrasada"] = pendentes["dataProximaDose"] < hoje

    return pendentes


def consultar_historico_pet(idPet: int):
    """
    Retorna histórico de vacinação de um pet.
    
    Args:
        idPet: ID do pet
        
    Returns:
        DataFrame com histórico ordenado por data
    """
    df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
    historico = df[df["idPet"] == idPet]

    if historico.empty:
        return "Nenhum registro de vacina para este pet."

    historico["dataAplicacao"] = pd.to_datetime(historico["dataAplicacao"], errors="coerce")
    historico["dataProximaDose"] = pd.to_datetime(historico["dataProximaDose"], errors="coerce")
    historico = historico.sort_values(by=["dataAplicacao", "dataProximaDose"], ascending=True)

    return historico


def aplicar_dose(idVacina: int, dataAplicacao: str, dataProximaDose: Optional[str] = None) -> str:
    """
    Marca uma vacina como aplicada e registra a próxima dose.
    
    Args:
        idVacina: ID da vacina pendente
        dataAplicacao: Data da aplicação
        dataProximaDose: Data da próxima dose (opcional)
        
    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])

        vacina_antiga = df[df["idVacina"] == idVacina]
        if vacina_antiga.empty:
            return "❌ Vacina não encontrada."

        idPet = int(vacina_antiga.iloc[0]["idPet"])
        nome = vacina_antiga.iloc[0]["nome"]

        # Atualizar status da vacina antiga
        df.loc[df["idVacina"] == idVacina, "status"] = "concluída"

        # Registrar nova dose
        novo_id = len(df) + 1
        novo_registro = {
            "idVacina": novo_id,
            "idPet": idPet,
            "nome": nome,
            "dataAplicacao": str(dataAplicacao),
            "dataProximaDose": str(dataProximaDose) if dataProximaDose else "",
            "status": "aplicada"
        }

        novo_registro_df = pd.DataFrame([novo_registro])
        df = pd.concat([df, novo_registro_df], ignore_index=True)

        salvar_dados(df, "data/vacinas.csv")
        log_info(f"Vacina {idVacina} do pet {idPet} marcada como aplicada")
        return "✅ Dose aplicada com sucesso!"
    except Exception as e:
        log_error(f"Erro ao aplicar dose", e)
        return "❌ Erro ao aplicar dose"


# ---------- LOGIN & AUTENTICAÇÃO ----------

def login_usuario(nome: str, senha: str, cargo: str) -> Tuple[bool, str]:
    """
    Autentica um usuário com validação segura de senha usando bcrypt.
    
    Args:
        nome: Nome do usuário
        senha: Senha em texto plano
        cargo: Cargo do usuário
        
    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    try:
        df = carregar_dados("data/usuarios.csv", COLUNAS["usuarios"])

        if df.empty:
            log_warning(f"Tentativa de login sem usuários cadastrados")
            return False, "❌ Não há usuários cadastrados."

        # Normalização forte dos inputs
        nome_norm = nome.strip().lower()
        cargo_norm = cargo.strip().lower()

        # Criar colunas normalizadas apenas em memória
        df["nome_norm"] = df["nome"].astype(str).str.strip().str.lower()
        df["cargo_norm"] = df["cargo"].astype(str).str.strip().str.lower()

        match_index = df[
            (df["nome_norm"] == nome_norm) &
            (df["cargo_norm"] == cargo_norm)
        ].index

        if match_index.empty:
            log_warning(f"Falha de login: usuário/cargo {nome}/{cargo} não encontrado")
            return False, "❌ Usuário ou cargo inválidos."

        # Verificar senha usando bcrypt
        index = match_index[0]
        senha_hash = df.loc[index, "senha"]
        
        if not verify_password(senha, senha_hash):
            log_warning(f"Falha de login: senha incorreta para {nome}")
            return False, "❌ Senha incorreta."

        # Marcar como logado
        df.loc[index, "logado"] = True
        df = df.drop(columns=["nome_norm", "cargo_norm"])
        salvar_dados(df, "data/usuarios.csv")

        usuario_nome = df.loc[index, "nome"]
        log_info(f"Login bem-sucedido: {usuario_nome} ({cargo})")
        return True, f"✅ Login realizado! Bem-vindo(a), {usuario_nome}."
        
    except Exception as e:
        log_error(f"Erro ao fazer login", e)
        return False, "❌ Erro ao fazer login"


def cadastrar_usuario(nome: str, senha: str, cargo: str) -> Tuple[bool, str]:
    """
    Cadastra um novo usuário com senha criptografada usando bcrypt.
    
    Args:
        nome: Nome do usuário
        senha: Senha em texto plano
        cargo: Cargo do usuário
        
    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    try:
        # Validar dados
        UsuarioValidator(nome=nome, email="temp@temp.com", telefone="1234567890", 
                        cargo=cargo, senha=senha)
        
        df = carregar_dados("data/usuarios.csv", COLUNAS["usuarios"])
        novo_id = len(df) + 1

        # Hash da senha com bcrypt
        senha_hash = hash_password(senha)

        novo_usuario = {
            "idUsuario": novo_id,
            "nome": nome,
            "senha": senha_hash,
            "cargo": cargo,
            "logado": False
        }

        novo_usuario_df = pd.DataFrame([novo_usuario])
        df = pd.concat([df, novo_usuario_df], ignore_index=True)
        salvar_dados(df, "data/usuarios.csv")

        log_info(f"Usuário '{nome}' cadastrado com sucesso (Cargo: {cargo})")
        return True, "✅ Usuário cadastrado com sucesso!"
        
    except ValueError as e:
        log_error(f"Erro ao validar dados do usuário: {str(e)}")
        return False, f"❌ Erro: {str(e)}"
    except Exception as e:
        log_error(f"Erro ao cadastrar usuário", e)
        return False, "❌ Erro ao cadastrar usuário"


def logout_usuario(nome: str, senha: str, cargo: str) -> str:
    """
    Desloga um usuário do sistema.
    
    Args:
        nome: Nome do usuário
        senha: Senha em texto plano
        cargo: Cargo do usuário
        
    Returns:
        Mensagem de sucesso
    """
    try:
        df = carregar_dados("data/usuarios.csv", COLUNAS["usuarios"])

        if df.empty:
            return "⚠️ Nenhum usuário cadastrado."

        if "logado" not in df.columns:
            return "⚠️ Nenhum usuário está logado atualmente."

        # Buscar por nome, cargo e verificar senha
        nome_norm = nome.strip().lower()
        cargo_norm = cargo.strip().lower()

        df["nome_norm"] = df["nome"].astype(str).str.strip().str.lower()
        df["cargo_norm"] = df["cargo"].astype(str).str.strip().str.lower()

        match_index = df[
            (df["nome_norm"] == nome_norm) &
            (df["cargo_norm"] == cargo_norm)
        ].index

        if match_index.empty or not verify_password(senha, df.loc[match_index[0], "senha"]):
            return "❌ Credenciais inválidas para logout."

        index = match_index[0]
        df.loc[index, "logado"] = False
        df = df.drop(columns=["nome_norm", "cargo_norm"])

        salvar_dados(df, "data/usuarios.csv")
        log_info(f"Logout realizado por {nome}")
        
        return f"👋 Logout realizado. Até logo, {nome}!"
        
    except Exception as e:
        log_error(f"Erro ao fazer logout", e)
        return "❌ Erro ao fazer logout"


# ---------- NOTIFICAÇÕES ----------

def gerar_notificacoes_pendentes() -> str:
    """
    Gera notificações para vacinas pendentes ou atrasadas.
    
    Returns:
        Mensagem com número de notificações geradas
    """
    try:
        vacinas = consultar_vacinas_pendentes()
        if vacinas.empty:
            return "ℹ️ Nenhuma vacina pendente."
        
        df_not = carregar_dados("data/notificacoes.csv", COLUNAS["notificacoes"])
        count = 0
        
        for _, v in vacinas.iterrows():
            atrasada_str = " (ATRASADA!)" if v.get("atrasada", False) else ""
            msg = f"Vacina '{v['nome']}' do pet {v['idPet']} está pendente!{atrasada_str}"
            notificacao = Notificacao(len(df_not) + 1, msg, datetime.now().strftime("%Y-%m-%d"), "pendente")
            
            notificacao_df = pd.DataFrame([vars(notificacao)])
            df_not = pd.concat([df_not, notificacao_df], ignore_index=True)
            count += 1
        
        salvar_dados(df_not, "data/notificacoes.csv")
        log_info(f"{count} notificações geradas para vacinas pendentes")
        return f"✅ {count} notificações geradas."
        
    except Exception as e:
        log_error(f"Erro ao gerar notificações", e)
        return "❌ Erro ao gerar notificações"


def marcar_notificacao_como_lida(idNotificacao: int) -> str:
    """
    Marca uma notificação como lida.
    
    Args:
        idNotificacao: ID da notificação
        
    Returns:
        Mensagem de sucesso
    """
    try:
        df = carregar_dados("data/notificacoes.csv", COLUNAS["notificacoes"])
        
        if idNotificacao not in df["idNotificacao"].values:
            return "❌ Notificação não encontrada."
        
        df.loc[df["idNotificacao"] == idNotificacao, "status"] = "lida"
        salvar_dados(df, "data/notificacoes.csv")
        log_info(f"Notificação {idNotificacao} marcada como lida")
        return "✅ Notificação marcada como lida"
        
    except Exception as e:
        log_error(f"Erro ao marcar notificação como lida", e)
        return "❌ Erro ao marcar notificação"
    return f"Notificação {idNotificacao} marcada como lida."