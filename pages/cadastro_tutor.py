import streamlit as st
from backend.services import cadastrar_tutor, atualizar_tutor, listar_tutores
from pages.style import set_css
from backend.design_system import (
    header, success_box, error_box, info_box, section_title, COLORS
)
from backend.validators import TutorValidator
from pydantic import ValidationError

set_css()


def tutor_label(row):
    return f"{row['idTutor']} - {row['nome']} ({row['telefone']})"


def pet_label(row):
    return f"{row['idPet']} - {row['nome']} ({row['raca']}) — Tutor: {row['nome_tutor']}"


# ============================================================================
# CADASTRO DE TUTOR
# ============================================================================

header("Cadastro de Tutor", "📝 Adicione novos tutores ao sistema", emoji="🐕")

col1, col2 = st.columns([1, 1])

with col1:
    section_title("Dados do Tutor", "📋")
    nome = st.text_input("👤 Nome completo", placeholder="Digite o nome do tutor...")
    telefone = st.text_input("📱 Telefone", placeholder="(11) 99999-9999")
    email = st.text_input("📧 E-mail", placeholder="tutor@example.com")

with col2:
    section_title("Localização", "📍")
    endereco = st.text_area("🏠 Endereço", placeholder="Digite o endereço completo...", height=150)

if st.button("✅ Cadastrar Tutor", use_container_width=True):
    try:
        # Validar dados usando Pydantic
        tutor_validado = TutorValidator(
            name=nome,
            phone=telefone,
            email=email
        )
        
        if not endereco:
            error_box("❌ Endereço é obrigatório!")
        else:
            msg = cadastrar_tutor(nome, telefone, email, endereco)
            success_box(f"✓ {msg}")
            st.rerun()
    
    except ValidationError as e:
        error_msgs = []
        for error in e.errors():
            field = error['loc'][0]
            msg = error['msg']
            error_msgs.append(f"• {field}: {msg}")
        
        error_box("❌ Erro de validação:\n" + "\n".join(error_msgs))


# ============================================================================
# ATUALIZAÇÃO DE TUTOR
# ============================================================================

st.markdown("---")
header("Atualizar Tutor", "✏️ Modifique informações de tutores existentes", emoji="✏️")

tutores_df = listar_tutores()

if not tutores_df.empty:
    section_title("Selecione o Tutor", "👥")
    
    tutor_escolhido = st.selectbox(
        "Tutor a atualizar:",
        tutores_df.apply(tutor_label, axis=1),
        help="Selecione o tutor que deseja modificar"
    )
    idTutor = int(tutor_escolhido.split(" - ")[0])
    tutor_atual = tutores_df[tutores_df['idTutor'] == idTutor].iloc[0]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        section_title("Novos Dados", "📝")
        novo_nome = st.text_input(
            "👤 Novo nome (opcional)",
            value="",
            placeholder=f"Atual: {tutor_atual['nome']}"
        )
        novo_telefone = st.text_input(
            "📱 Novo telefone (opcional)",
            value="",
            placeholder=f"Atual: {tutor_atual['telefone']}"
        )
        novo_email = st.text_input(
            "📧 Novo email (opcional)",
            value="",
            placeholder=f"Atual: {tutor_atual['email']}"
        )
    
    with col2:
        section_title("Localização", "📍")
        novo_endereco = st.text_area(
            "🏠 Novo endereço (opcional)",
            value="",
            placeholder=f"Atual: {tutor_atual['endereco']}",
            height=150
        )

    if st.button("🔄 Atualizar Tutor", use_container_width=True):
        novos_dados = {}
        try:
            # Validar apenas os dados preenchidos
            if novo_nome:
                tutor_validado = TutorValidator(
                    name=novo_nome,
                    phone=tutor_atual['telefone'],
                    email=tutor_atual['email']
                )
                novos_dados["nome"] = novo_nome
            
            if novo_telefone:
                tutor_validado = TutorValidator(
                    name=tutor_atual['nome'],
                    phone=novo_telefone,
                    email=tutor_atual['email']
                )
                novos_dados["telefone"] = novo_telefone
            
            if novo_email:
                tutor_validado = TutorValidator(
                    name=tutor_atual['nome'],
                    phone=tutor_atual['telefone'],
                    email=novo_email
                )
                novos_dados["email"] = novo_email
            
            if novo_endereco:
                novos_dados["endereco"] = novo_endereco

            if novos_dados:
                msg = atualizar_tutor(idTutor, novos_dados)
                success_box(f"✓ {msg}")
                st.rerun()
            else:
                error_box("❌ Preencha ao menos um campo para atualizar.")
        
        except ValidationError as e:
            error_msgs = []
            for error in e.errors():
                field = error['loc'][0]
                msg = error['msg']
                error_msgs.append(f"• {field}: {msg}")
            error_box("❌ Erro de validação:\n" + "\n".join(error_msgs))
else:
    info_box("ℹ Nenhum tutor cadastrado ainda. Comece cadastrando um novo tutor!")
