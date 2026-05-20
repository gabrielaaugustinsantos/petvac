import streamlit as st
import pandas as pd
from datetime import date
from backend.services import registrar_vacina, consultar_vacinas_pendentes, aplicar_dose, listar_tutores, listar_pets
from pages.style import set_css
from backend.design_system import (
    header, success_box, error_box, info_box, section_title, COLORS
)
from backend.validators import VacinaValidator
from pydantic import ValidationError

set_css()


def tutor_label(row):
    return f"{row['idTutor']} - {row['nome']} ({row['telefone']})"


def pet_label(row):
    return f"{row['idPet']} - {row['nome_pet']} ({row['raca']}) — Tutor: {row['nome_tutor']}"


tutores_df = listar_tutores()
pets_df = listar_pets()


# ============================================================================
# REGISTRO DE VACINA
# ============================================================================

header("Registro de Vacina", "📝 Registre novas vacinações", emoji="💉")

if pets_df.empty or tutores_df.empty:
    error_box("❌ Cadastre pets e tutores antes de registrar vacinas.")
    pets_df = pd.DataFrame()
else:
    pets_df = pets_df.merge(
        tutores_df.rename(columns={"nome": "nome_tutor"})[["idTutor", "nome_tutor"]],
        on="idTutor",
        how="left"
    )
    pets_df = pets_df.rename(columns={"nome": "nome_pet"})

col1, col2 = st.columns([1, 1])

with col1:
    section_title("Seleção do Pet", "🐾")
    
    if not pets_df.empty:
        pet_escolhido = st.selectbox(
            "Pet a vacinar:",
            pets_df.apply(pet_label, axis=1),
            help="Selecione o pet"
        )
        idPet = int(pet_escolhido.split(" - ")[0])
    else:
        error_box("❌ Nenhum pet disponível.")
        idPet = None
    
    section_title("Informações da Vacina", "💉")
    nome_vacina = st.text_input("🏷️ Nome da Vacina", placeholder="Ex: Raiva, Polivalente...")

with col2:
    section_title("Datas", "📅")
    
    foi_aplicada = st.checkbox("✅ A vacina já foi aplicada?")
    
    data_aplicacao = None
    if foi_aplicada:
        data_aplicacao = st.date_input("📅 Data da Aplicação", value=date.today())
    
    data_proxima_dose = st.date_input("📅 Data da Próxima Dose (opcional)", value=None)

if st.button("✅ Registrar Vacina", use_container_width=True):
    if idPet and nome_vacina:
        try:
            vacina_validada = VacinaValidator(
                name=nome_vacina
            )
            msg = registrar_vacina(
                idPet,
                nome_vacina,
                str(data_aplicacao) if data_aplicacao else None,
                str(data_proxima_dose) if data_proxima_dose else None
            )
            success_box(f"✓ {msg}")
            st.rerun()
        except ValidationError as e:
            error_box(f"❌ Erro de validação: {str(e)}")
    else:
        error_box("❌ Selecione um pet válido e informe o nome da vacina.")


# ============================================================================
# VACINAS PENDENTES
# ============================================================================

st.markdown("---")
header("Vacinas Pendentes", "⏰ Vacinações que ainda não foram aplicadas", emoji="📋")

section_title("Consultar Pendências", "🔍")

if st.button("📊 Consultar Vacinas Pendentes", use_container_width=True):
    pendentes = consultar_vacinas_pendentes()
    if pendentes.empty:
        info_box("ℹ Nenhuma vacina pendente encontrada.")
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fff3cd, #ffe69c);
            border-left: 4px solid #f39c12;
            border-radius: 12px;
            padding: 16px;
            margin: 12px 0;
        ">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid #f39c12;">
                    <th style="text-align: left; padding: 12px; color: #333;">🐾 Pet</th>
                    <th style="text-align: left; padding: 12px; color: #333;">💉 Vacina</th>
                    <th style="text-align: left; padding: 12px; color: #333;">📅 Próxima Dose</th>
                    <th style="text-align: left; padding: 12px; color: #333;">⏳ Status</th>
                </tr>
        """, unsafe_allow_html=True)
        
        for _, row in pendentes.iterrows():
            status_color = "#DC3545" if pd.to_datetime(row['dataProximaDose'], errors="coerce") < pd.Timestamp.now().normalize() else "#F39C12"
            status_text = "⚠️ ATRASADA" if pd.to_datetime(row['dataProximaDose'], errors="coerce") < pd.Timestamp.now().normalize() else "⏳ PENDENTE"
            
            st.markdown(f"""
                <tr style="border-bottom: 1px solid rgba(243, 156, 18, 0.3);">
                    <td style="padding: 10px;">ID: {row['idPet']}</td>
                    <td style="padding: 10px; font-weight: 600;">{row['nome']}</td>
                    <td style="padding: 10px;">{row['dataProximaDose']}</td>
                    <td style="padding: 10px;">
                        <span style="background: {status_color}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;">
                            {status_text}
                        </span>
                    </td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</table></div>", unsafe_allow_html=True)


# ============================================================================
# APLICAR DOSE
# ============================================================================

st.markdown("---")
header("Aplicar Dose", "✅ Registre a aplicação de uma vacina", emoji="💉")

pend = consultar_vacinas_pendentes()

if not pend.empty:
    section_title("Seleção da Vacina", "💊")
    
    pets_df = listar_pets().rename(columns={"nome": "nome_pet"})
    tutores_df = listar_tutores().rename(columns={"nome": "nome_tutor"})

    # Merge vacina -> pet
    pend = pend.merge(
        pets_df[["idPet", "nome_pet", "raca", "idTutor"]],
        on="idPet",
        how="left"
    )

    # Merge pet -> tutor
    pend = pend.merge(
        tutores_df[["idTutor", "nome_tutor"]],
        on="idTutor",
        how="left"
    )

    pend["label"] = pend.apply(
        lambda r: (
            f"{r['idVacina']} - {r['nome_pet']} "
            f"(Tutor: {r['nome_tutor']}) — Vacina: {r['nome']}"
        ),
        axis=1
    )

    col1, col2 = st.columns([1, 1])
    
    with col1:
        vacina_sel = st.selectbox(
            "💊 Selecione uma vacina pendente:",
            pend["label"],
            help="Escolha qual vacina será aplicada"
        )
        idVacina = int(vacina_sel.split(" - ")[0])
    
    with col2:
        section_title("Datas de Aplicação", "📅")
        dataAplicacao = st.date_input("📅 Data da Aplicação", value=date.today())
        dataProximaDose = st.date_input("📅 Próxima Dose (opcional)", value=None)

    if st.button("✅ Aplicar Dose", use_container_width=True):
        try:
            prox = str(dataProximaDose) if dataProximaDose else None
            msg = aplicar_dose(idVacina, dataAplicacao, prox)
            success_box(f"✓ {msg}")
            st.rerun()
        except Exception as e:
            error_box(f"❌ Erro ao aplicar dose: {str(e)}")
else:
    info_box("ℹ Nenhuma vacina pendente para aplicar.")