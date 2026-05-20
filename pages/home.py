# pages/home.py - Dashboard principal
import streamlit as st
import pandas as pd
from pages.style import set_css
from backend.database import carregar_dados, COLUNAS
from backend.design_system import (
    header, metric_card, section_title, feature_card, COLORS, info_box
)

set_css()

# ============================================================================
# CARREGAR DADOS
# ============================================================================

try:
    pets_df = carregar_dados("data/pets.csv", COLUNAS["pets"])
    tutores_df = carregar_dados("data/tutores.csv", COLUNAS["tutores"])
    vacinas_df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
except:
    pets_df = pd.DataFrame()
    tutores_df = pd.DataFrame()
    vacinas_df = pd.DataFrame()

# Calcular métricas
total_tutores = len(tutores_df)
total_pets = len(pets_df)
total_vacinas = len(vacinas_df)

try:
    pendentes_df = vacinas_df[vacinas_df["status"] == "pendente"]
    atrasadas_df = vacinas_df[(vacinas_df["status"] == "pendente") & (pd.to_datetime(vacinas_df["dataProximaDose"], errors="coerce") < pd.Timestamp.now().normalize())]
    total_pendentes = len(pendentes_df)
    total_atrasadas = len(atrasadas_df)
except:
    total_pendentes = 0
    total_atrasadas = 0

# ============================================================================
# HEADER
# ============================================================================

header("Dashboard PetVac", "Bem-vindo! Aqui você vê um resumo do sistema.", emoji="📊")

# ============================================================================
# ALERTAS IMPORTANTES
# ============================================================================

if total_atrasadas > 0:
    info_box(f"⚠️ Você tem {total_atrasadas} vacina(s) atrasada(s)! Verifique a seção de Vacinas.")

# ============================================================================
# MÉTRICAS PRINCIPAIS (4 colunas)
# ============================================================================

section_title("Estatísticas Gerais", "📈")

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Tutores", total_tutores, emoji="👤", color="primary")

with col2:
    metric_card("Pets", total_pets, emoji="🐶", color="info")

with col3:
    metric_card("Vacinas", total_vacinas, emoji="💉", color="success")

with col4:
    color_alert = "danger" if total_pendentes > 5 else "warning" if total_pendentes > 0 else "success"
    metric_card("Pendentes", total_pendentes, emoji="⏳", color=color_alert)

# ============================================================================
# FEATURES
# ============================================================================

section_title("Funcionalidades Principais", "🚀")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    feature_card(
        emoji="👤",
        title="Gestão de Tutores",
        description="Cadastre e gerencie informações dos tutores de forma centralizada."
    )

with col_f2:
    feature_card(
        emoji="🐶",
        title="Cadastro de Pets",
        description="Registre e organize dados de todos os pets da clínica."
    )

with col_f3:
    feature_card(
        emoji="💉",
        title="Controle de Vacinas",
        description="Gerencie aplicações, datas e próximas doses de todas as vacinas."
    )

# ============================================================================
# ÚLTIMAS VACINAS PENDENTES
# ============================================================================

if total_pendentes > 0:
    section_title("Vacinas Pendentes Recentes", "⏰")
    
    # Mostrar as 5 primeiras pendentes
    display_vacinas = pendentes_df.head(5)
    
    if not display_vacinas.empty:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fff3cd, #ffe69c);
            border-left: 4px solid #f39c12;
            border-radius: 12px;
            padding: 16px;
            margin: 12px 0;
        ">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid rgba(0,0,0,0.1);">
                    <th style="text-align: left; padding: 8px;">Pet ID</th>
                    <th style="text-align: left; padding: 8px;">Vacina</th>
                    <th style="text-align: left; padding: 8px;">Data Próxima</th>
                    <th style="text-align: left; padding: 8px;">Status</th>
                </tr>
        """, unsafe_allow_html=True)
        
        for _, row in display_vacinas.iterrows():
            st.markdown(f"""
                <tr>
                    <td style="padding: 8px;">{row['idPet']}</td>
                    <td style="padding: 8px;">{row['nome']}</td>
                    <td style="padding: 8px;">{row['dataProximaDose']}</td>
                    <td style="padding: 8px;">
                        <span style="background: #f39c12; color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.85rem;">
                            {row['status'].upper()}
                        </span>
                    </td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</table></div>", unsafe_allow_html=True)
        
        if total_pendentes > 5:
            st.caption(f"... e mais {total_pendentes - 5} vacinas pendentes. Acesse a seção de Vacinas para ver todas.")

# ============================================================================
# QUICK STATS
# ============================================================================

st.markdown("---")
section_title("Informações Adicionais", "ℹ️")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    if total_pets > 0:
        media_vacinas = total_vacinas / total_pets
        st.markdown(f"""
        <div style="
            background: {COLORS['gray_light']};
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 2rem; color: {COLORS['primary']}; margin-bottom: 8px;">💉</div>
            <div style="color: {COLORS['gray']}; font-size: 0.9rem;">Média de Vacinas/Pet</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['primary']};">{media_vacinas:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

with col_info2:
    if total_tutores > 0:
        media_pets = total_pets / total_tutores
        st.markdown(f"""
        <div style="
            background: {COLORS['gray_light']};
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 2rem; color: {COLORS['info']}; margin-bottom: 8px;">🐶</div>
            <div style="color: {COLORS['gray']}; font-size: 0.9rem;">Média de Pets/Tutor</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['info']};">{media_pets:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

with col_info3:
    taxa_atraso = (total_atrasadas / total_pendentes * 100) if total_pendentes > 0 else 0
    cor = COLORS['danger'] if taxa_atraso > 20 else COLORS['warning'] if taxa_atraso > 10 else COLORS['success']
    st.markdown(f"""
    <div style="
        background: {COLORS['gray_light']};
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    ">
        <div style="font-size: 2rem; color: {cor}; margin-bottom: 8px;">⏱️</div>
        <div style="color: {COLORS['gray']}; font-size: 0.9rem;">Taxa de Atraso</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: {cor};">{taxa_atraso:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {COLORS['gray']}; font-size: 0.9rem; margin-top: 2rem;">
    <p>🐾 Última atualização: Agora | PetVac v1.0 com Segurança Bcrypt</p>
</div>
""", unsafe_allow_html=True)
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📖</div>
        <div class="feature-title">Histórico Completo</div>
        <p class="feature-desc">Visualize o histórico completo de cada pet.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align:center; color: gray;'>Navegue pelo menu lateral para acessar as funcionalidades.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: gray;'>Projeto acadêmico PetVac 🐾</p>", unsafe_allow_html=True)