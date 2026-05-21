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


def remover_pet(idPet: int) -> str:
    """
    Remove um pet do sistema.

    Args:
        idPet: ID do pet a ser removido

    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        df = carregar_dados("data/pets.csv", COLUNAS["pets"])
        if idPet not in df["idPet"].values:
            return "❌ Pet não encontrado."
        df = df[df["idPet"] != idPet]
        salvar_dados(df, "data/pets.csv")
        log_info(f"Pet {idPet} removido com sucesso")
        return "✅ Pet removido com sucesso!"
    except Exception as e:
        log_error(f"Erro ao remover pet {idPet}", e)
        return "❌ Erro ao remover pet"


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


def remover_tutor(idTutor: int) -> str:
    """
    Remove um tutor do sistema.

    Args:
        idTutor: ID do tutor a ser removido

    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        df = carregar_dados("data/tutores.csv", COLUNAS["tutores"])
        if idTutor not in df["idTutor"].values:
            return "❌ Tutor não encontrado."
        df = df[df["idTutor"] != idTutor]
        salvar_dados(df, "data/tutores.csv")
        log_info(f"Tutor {idTutor} removido com sucesso")
        return "✅ Tutor removido com sucesso!"
    except Exception as e:
        log_error(f"Erro ao remover tutor {idTutor}", e)
        return "❌ Erro ao remover tutor"


# ---------- VACINAS E HISTÓRICO ----------

def registrar_vacina(
    idPet: int,
    nome: str,
    dataAplicacao: Optional[str] = None,
    dataProximaDose: Optional[str] = None,
    obs: Optional[str] = None,
) -> str:
    """
    Registra uma nova vacina com status automático baseado na data.

    Args:
        idPet: ID do pet
        nome: Nome da vacina
        dataAplicacao: Data de aplicação (YYYY-MM-DD ou None)
        dataProximaDose: Data da próxima dose (YYYY-MM-DD ou None)
        obs: Observações opcionais sobre a aplicação

    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        # Validar dados
        VacinaValidator(
            nome=nome,
            data_aplicacao=dataAplicacao or None,
            proxima_dose=dataProximaDose or None,
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
            "status": status,
            "obs": obs or "",
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


def aplicar_dose(
    idVacina: int,
    dataAplicacao: str,
    dataProximaDose: Optional[str] = None,
    obs: Optional[str] = None,
) -> str:
    """
    Marca uma vacina como aplicada e registra a próxima dose.

    Args:
        idVacina: ID da vacina pendente
        dataAplicacao: Data da aplicação
        dataProximaDose: Data da próxima dose (opcional)
        obs: Observações opcionais sobre a aplicação

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
            "status": "aplicada",
            "obs": obs or "",
        }

        novo_registro_df = pd.DataFrame([novo_registro])
        df = pd.concat([df, novo_registro_df], ignore_index=True)

        salvar_dados(df, "data/vacinas.csv")
        log_info(f"Vacina {idVacina} do pet {idPet} marcada como aplicada")
        return "✅ Dose aplicada com sucesso!"
    except Exception as e:
        log_error(f"Erro ao aplicar dose", e)
        return "❌ Erro ao aplicar dose"


def agendar_vacina(idVacina: int, dataAgendamento: str) -> str:
    """
    Atualiza apenas a dataProximaDose de uma vacina pendente, sem alterar o status.
    Usado para agendar uma data futura de aplicação sem dar a vacina como concluída.

    Args:
        idVacina: ID da vacina a agendar
        dataAgendamento: Nova data para a próxima dose (YYYY-MM-DD)

    Returns:
        Mensagem de sucesso ou erro
    """
    try:
        df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
        idx = df.index[df["idVacina"] == idVacina]
        if idx.empty:
            return "❌ Vacina não encontrada."
        df.loc[idx, "dataProximaDose"] = str(dataAgendamento)
        salvar_dados(df, "data/vacinas.csv")
        log_info(f"Vacina {idVacina} agendada para {dataAgendamento}")
        return "✅ Vacina agendada com sucesso!"
    except Exception as e:
        log_error("Erro ao agendar vacina", e)
        return "❌ Erro ao agendar vacina"


# ---------- LOGIN & AUTENTICAÇÃO ----------

def login_usuario(email: str, senha: str) -> Tuple[bool, str, dict]:
    """
    Autentica um usuário pelo email e senha.

    Args:
        email: E-mail do usuário
        senha: Senha em texto plano

    Returns:
        Tupla (sucesso: bool, mensagem: str, dados: dict)
        dados contém nome e cargo quando sucesso=True
    """
    try:
        df = carregar_dados("data/usuarios.csv", COLUNAS["usuarios"])

        if df.empty:
            log_warning("Tentativa de login sem usuários cadastrados")
            return False, "❌ Não há usuários cadastrados.", {}

        email_norm = email.strip().lower()
        df["email_norm"] = df["email"].astype(str).str.strip().str.lower()

        match = df[df["email_norm"] == email_norm]

        if match.empty:
            log_warning(f"Falha de login: email {email} não encontrado")
            return False, "❌ E-mail ou senha incorretos.", {}

        index = match.index[0]
        senha_hash = str(df.loc[index, "senha"])

        if not verify_password(senha, senha_hash):
            log_warning(f"Falha de login: senha incorreta para {email}")
            return False, "❌ E-mail ou senha incorretos.", {}

        nome  = str(df.loc[index, "nome"])
        cargo = str(df.loc[index, "cargo"])
        log_info(f"Login bem-sucedido: {nome} ({cargo})")
        return True, f"✅ Bem-vindo(a), {nome}!", {"nome": nome, "cargo": cargo}

    except Exception as e:
        log_error("Erro ao fazer login", e)
        return False, "❌ Erro ao fazer login.", {}


def cadastrar_usuario(nome: str, email: str, senha: str, cargo: str) -> Tuple[bool, str]:
    """
    Cadastra um novo usuário com senha criptografada.

    Args:
        nome:  Nome completo
        email: E-mail único do usuário
        senha: Senha em texto plano
        cargo: recepcionista ou veterinario

    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    try:
        UsuarioValidator(nome=nome, email=email, telefone="11900000000", cargo=cargo, senha=senha)

        df = carregar_dados("data/usuarios.csv", COLUNAS["usuarios"])

        # E-mail deve ser único
        email_norm = email.strip().lower()
        if not df.empty and email_norm in df["email"].astype(str).str.strip().str.lower().values:
            return False, "❌ Já existe uma conta com esse e-mail."

        novo_id = int(df["idUsuario"].max()) + 1 if not df.empty else 1
        novo_usuario = {
            "idUsuario": novo_id,
            "nome": nome.strip(),
            "email": email_norm,
            "senha": hash_password(senha),
            "cargo": cargo,
        }

        df = pd.concat([df, pd.DataFrame([novo_usuario])], ignore_index=True)
        salvar_dados(df, "data/usuarios.csv")

        log_info(f"Usuário '{nome}' cadastrado com sucesso (Cargo: {cargo})")
        return True, "✅ Conta criada com sucesso!"

    except ValueError as e:
        log_error(f"Erro ao validar dados do usuário: {e}")
        return False, f"❌ {e}"
    except Exception as e:
        log_error("Erro ao cadastrar usuário", e)
        return False, "❌ Erro ao cadastrar usuário."


def logout_usuario() -> str:
    """Logout é gerenciado pelo cliente via JWT — sem estado no servidor."""
    return "👋 Logout realizado com sucesso."


def redefinir_senha(email: str, nova_senha: str) -> Tuple[bool, str]:
    """
    Redefine a senha de um usuário a partir do e-mail.

    Args:
        email:      E-mail cadastrado
        nova_senha: Nova senha em texto plano

    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    try:
        if len(nova_senha.strip()) < 6:
            return False, "❌ A nova senha deve ter pelo menos 6 caracteres."

        df = carregar_dados("data/usuarios.csv", COLUNAS["usuarios"])
        email_norm = email.strip().lower()
        df["email_norm"] = df["email"].astype(str).str.strip().str.lower()

        match = df[df["email_norm"] == email_norm]
        if match.empty:
            # Mensagem genérica para não confirmar existência de e-mails
            return True, "✅ Se o e-mail existir, a senha foi redefinida."

        index = match.index[0]
        df.loc[index, "senha"] = hash_password(nova_senha)
        df = df.drop(columns=["email_norm"])
        salvar_dados(df, "data/usuarios.csv")

        log_info(f"Senha redefinida para o e-mail {email}")
        return True, "✅ Senha redefinida com sucesso!"

    except Exception as e:
        log_error("Erro ao redefinir senha", e)
        return False, "❌ Erro ao redefinir senha."


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