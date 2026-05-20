import streamlit as st
import pandas as pd
from backend.database import carregar_dados, COLUNAS
from pages.style import set_css
from backend.design_system import (
    header, success_box, error_box, info_box, section_title, COLORS
)

set_css()

# ============================================================================
# NOTIFICAÇÕES
# ============================================================================

header("Notificações", "🔔 Receba alertas sobre vacinações pendentes e atrasadas", emoji="🔔")

section_title("Sistema de Alertas", "⚠️")

try:
    pets_df = carregar_dados("data/pets.csv", COLUNAS["pets"])
    tutores_df = carregar_dados("data/tutores.csv", COLUNAS["tutores"])
    vacinas_df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
except:
    pets_df = pd.DataFrame()
    tutores_df = pd.DataFrame()
    vacinas_df = pd.DataFrame()

# ============================================================================
# VERIFICAR PENDÊNCIAS
# ============================================================================

if vacinas_df.empty:
    info_box("ℹ Nenhuma vacina registrada no sistema.")
else:
    # Filtrar vacinas pendentes e atrasadas
    pendentes_df = vacinas_df[vacinas_df["status"] == "pendente"]
    atrasadas_df = vacinas_df[
        (vacinas_df["status"] == "pendente") & 
        (pd.to_datetime(vacinas_df["dataProximaDose"], errors="coerce") < pd.Timestamp.now().normalize())
    ]

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📋 Total de Vacinas",
            value=len(vacinas_df),
            delta=None
        )
    
    with col2:
        st.metric(
            label="⏳ Pendentes",
            value=len(pendentes_df),
            delta=f"-{len(atrasadas_df)} atrasadas" if len(atrasadas_df) > 0 else "Nenhuma atrasada",
            delta_color="inverse" if len(atrasadas_df) > 0 else "normal"
        )
    
    with col3:
        st.metric(
            label="✅ Aplicadas",
            value=len(vacinas_df[vacinas_df["status"] != "pendente"])
        )

    # ============================================================================
    # VACINAS ATRASADAS (CRÍTICO)
    # ============================================================================

    if not atrasadas_df.empty:
        st.markdown("---")
        error_box(f"🚨 CRÍTICO: Você tem {len(atrasadas_df)} vacina(s) atrasada(s)!")
        
        section_title("Vacinas Atrasadas", "⚠️")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            border-left: 4px solid {COLORS['danger']};
            border-radius: 12px;
            padding: 16px;
            margin: 12px 0;
        ">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid #DC3545;">
                    <th style="text-align: left; padding: 12px; color: #333;">🐾 Pet ID</th>
                    <th style="text-align: left; padding: 12px; color: #333;">💉 Vacina</th>
                    <th style="text-align: left; padding: 12px; color: #333;">📅 Data</th>
                    <th style="text-align: left; padding: 12px; color: #333;">⚠️ Dias Atrasada</th>
                </tr>
        """, unsafe_allow_html=True)
        
        for _, row in atrasadas_df.iterrows():
            data_proxima = pd.to_datetime(row['dataProximaDose'], errors="coerce")
            dias_atrasados = (pd.Timestamp.now().normalize() - data_proxima).days
            
            st.markdown(f"""
                <tr style="border-bottom: 1px solid rgba(220, 53, 69, 0.3);">
                    <td style="padding: 10px; font-weight: 600;">{row['idPet']}</td>
                    <td style="padding: 10px;">{row['nome']}</td>
                    <td style="padding: 10px;">{row['dataProximaDose']}</td>
                    <td style="padding: 10px;">
                        <span style="background: #DC3545; color: white; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;">
                            {dias_atrasados} dias
                        </span>
                    </td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</table></div>", unsafe_allow_html=True)

    # ============================================================================
    # VACINAS PENDENTES (AVISOS)
    # ============================================================================

    if not pendentes_df.empty and atrasadas_df.empty:
        st.markdown("---")
        section_title("Próximas Vacinações", "📅")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fff3cd, #ffe69c);
            border-left: 4px solid {COLORS['warning']};
            border-radius: 12px;
            padding: 16px;
            margin: 12px 0;
        ">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid #F39C12;">
                    <th style="text-align: left; padding: 12px; color: #333;">🐾 Pet ID</th>
                    <th style="text-align: left; padding: 12px; color: #333;">💉 Vacina</th>
                    <th style="text-align: left; padding: 12px; color: #333;">📅 Data</th>
                    <th style="text-align: left; padding: 12px; color: #333;">📆 Dias até a Aplicação</th>
                </tr>
        """, unsafe_allow_html=True)
        
        for _, row in pendentes_df.head(10).iterrows():
            data_proxima = pd.to_datetime(row['dataProximaDose'], errors="coerce")
            dias_restantes = (data_proxima - pd.Timestamp.now().normalize()).days
            
            # Colorir baseado no tempo restante
            if dias_restantes <= 3:
                cor_alerta = "#F39C12"
                status = "🔴 PRÓXIMO"
            elif dias_restantes <= 7:
                cor_alerta = "#F39C12"
                status = "🟡 EM BREVE"
            else:
                cor_alerta = "#28A745"
                status = "🟢 AGENDADO"
            
            st.markdown(f"""
                <tr style="border-bottom: 1px solid rgba(243, 156, 18, 0.3);">
                    <td style="padding: 10px; font-weight: 600;">{row['idPet']}</td>
                    <td style="padding: 10px;">{row['nome']}</td>
                    <td style="padding: 10px;">{row['dataProximaDose']}</td>
                    <td style="padding: 10px;">
                        <span style="background: {cor_alerta}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;">
                            {dias_restantes} dias {status}
                        </span>
                    </td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</table></div>", unsafe_allow_html=True)
        
        if len(pendentes_df) > 10:
            st.caption(f"... e mais {len(pendentes_df) - 10} vacinações pendentes. Acesse a seção de Vacinas para ver todas.")

    # ============================================================================
    # RESUMO
    # ============================================================================

    st.markdown("---")
    section_title("Recomendações", "💡")

    if len(atrasadas_df) > 0:
        error_box(f"🚨 URGENTE: Aplique as {len(atrasadas_df)} vacina(s) atrasada(s) o mais breve possível!")
    elif len(pendentes_df) > 0:
        success_box(f"✓ {len(pendentes_df)} vacinações agendadas. Siga o calendário para manter os pets vacinados.")
    else:
        success_box("✓ Todos os pets estão em dia com suas vacinações!")
