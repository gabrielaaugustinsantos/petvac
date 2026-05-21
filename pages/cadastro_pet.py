import streamlit as st
import pandas as pd
from backend.services import cadastrar_pet, atualizar_pet, listar_pets, listar_tutores
from pages.style import set_css
from backend.design_system import (
    header, success_box, error_box, info_box, section_title, COLORS
)
from backend.validators import PetValidator
from pydantic import ValidationError

set_css()


def tutor_label(row):
    return f"{row['idTutor']} - {row['nome']} ({row['telefone']})"


def pet_label(row):
    return f"{row['idPet']} - {row['nome']} ({row['raca']}) — Tutor: {row['nome_tutor']}"


tutores_df = listar_tutores()
pets_df = listar_pets()


# ============================================================================
# CADASTRO DE PET
# ============================================================================

header("Cadastro de Pet", "📝 Registre novos animais de estimação", emoji="🐕")

col1, col2 = st.columns([1, 1])

with col1:
    section_title("Informações do Pet", "📋")
    nome = st.text_input("🐾 Nome do Pet", placeholder="Digite o nome do pet...")
    especie = st.selectbox("🦮 Espécie", ["🐶 Cachorro", "🐱 Gato", "🦜 Ave", "🐭 Roedor"])
    raca = st.text_input("🏷️ Raça", placeholder="Digite a raça...")

with col2:
    section_title("Data e Tutor", "📅")
    dataNascimento = st.date_input("📅 Data de Nascimento")
    
    if not tutores_df.empty:
        tutor_pet = st.selectbox(
            "👤 Tutor do Pet",
            tutores_df.apply(tutor_label, axis=1),
            help="Selecione o tutor responsável"
        )
        idTutor_pet = int(tutor_pet.split(" - ")[0])
    else:
        error_box("❌ Cadastre um tutor antes de registrar pets.")
        idTutor_pet = None

if st.button("✅ Cadastrar Pet", use_container_width=True):
    if idTutor_pet:
        try:
            # Validar dados
            pet_validado = PetValidator(
                name=nome,
                species=especie.split(" ")[1],
                breed=raca
            )
            msg = cadastrar_pet(nome, especie.split(" ")[1], raca, dataNascimento, idTutor_pet)
            success_box(f"✓ {msg}")
            st.rerun()
        except ValidationError as e:
            error_msgs = []
            for error in e.errors():
                field = error['loc'][0]
                msg = error['msg']
                error_msgs.append(f"• {field}: {msg}")
            error_box("❌ Erro de validação:\n" + "\n".join(error_msgs))
    else:
        error_box("❌ Selecione um tutor válido.")


# ============================================================================
# ATUALIZAÇÃO DE PET
# ============================================================================

st.markdown("---")
header("Atualizar Pet", "✏️ Modifique informações de pets existentes", emoji="✏️")

pets_df = listar_pets()

# 🔥 Merge pets + tutores para incluir nome do tutor no label
if not pets_df.empty and not tutores_df.empty:
    pets_df_merged = pets_df.merge(
        tutores_df[['idTutor', 'nome']],
        on='idTutor',
        how='left',
        suffixes=('', '_tutor')
    )
else:
    info_box("ℹ Nenhum pet cadastrado ainda.")
    pets_df_merged = pd.DataFrame()

if not pets_df_merged.empty:
    section_title("Selecione o Pet", "🐾")
    
    pet_escolhido = st.selectbox(
        "Pet a atualizar:",
        pets_df_merged.apply(pet_label, axis=1),
        help="Selecione o pet que deseja modificar"
    )
    idPet = int(pet_escolhido.split(" - ")[0])
    pet_atual = pets_df_merged[pets_df_merged['idPet'] == idPet].iloc[0]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        section_title("Novos Dados", "📝")
        novo_nome = st.text_input(
            "🐾 Novo nome (opcional)",
            value="",
            placeholder=f"Atual: {pet_atual['nome']}"
        )
        nova_especie = st.selectbox(
            "🦮 Nova espécie (opcional)",
            ["Manter"] + ["🐶 Cachorro", "🐱 Gato", "🦜 Ave", "🐭 Roedor"],
            help="Deixe 'Manter' para não alterar"
        )
        nova_raca = st.text_input(
            "🏷️ Nova raça (opcional)",
            value="",
            placeholder=f"Atual: {pet_atual['raca']}"
        )
    
    with col2:
        section_title("Mais Informações", "ℹ️")
        nova_data = st.date_input("📅 Nova data de nascimento (opcional)")
        
        tutor_novo = st.selectbox(
            "👤 Novo tutor (opcional)",
            ["Manter"] + list(tutores_df.apply(tutor_label, axis=1)),
            help="Deixe 'Manter' para não alterar"
        )

    if st.button("🔄 Atualizar Pet", use_container_width=True):
        novos_dados = {}
        try:
            if novo_nome:
                novos_dados["nome"] = novo_nome
            
            if nova_especie != "Manter":
                novos_dados["especie"] = nova_especie.split(" ")[1]
            
            if nova_raca:
                novos_dados["raca"] = nova_raca
            
            if nova_data:
                novos_dados["dataNascimento"] = str(nova_data)
            
            if tutor_novo != "Manter":
                novos_dados["idTutor"] = int(tutor_novo.split(" - ")[0])

            if novos_dados:
                msg = atualizar_pet(idPet, novos_dados)
                success_box(f"✓ {msg}")
                st.rerun()
            else:
                error_box("❌ Preencha ao menos um campo para atualizar.")
        
        except (ValidationError, ValueError) as e:
            error_box(f"❌ Erro ao atualizar: {str(e)}")
