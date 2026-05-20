import streamlit as st
import pandas as pd
from backend.services import consultar_historico_pet, listar_pets, listar_tutores
from pages.style import set_css
from backend.design_system import (
    header, success_box, error_box, info_box, section_title, COLORS
)

import pandas as pd
from datetime import datetime

set_css()


header("Histórico de Vacinas", "📖 Consulte o histórico completo de vacinações", emoji="📖")

section_title("Selecione um Pet", "🐾")

# ----- CARREGAR PETS E TUTORES -----
pets_df = listar_pets()
tutores_df = listar_tutores()

if pets_df.empty or tutores_df.empty:
    error_box("❌ Não há pets ou tutores cadastrados.")
else:
    # Renomear colunas para evitar conflitos
    pets_df = pets_df.rename(columns={"nome": "nome_pet"})
    tutores_df = tutores_df.rename(columns={"nome": "nome_tutor"})

    # Merge pet -> tutor
    pets_df = pets_df.merge(
        tutores_df[["idTutor", "nome_tutor"]],
        on="idTutor",
        how="left"
    )

    # Criar label completo do pet
    pets_df["label"] = pets_df.apply(
        lambda r: f"{r['idPet']} - {r['nome_pet']} ({r['raca']}) — Tutor: {r['nome_tutor']}",
        axis=1
    )

    # ----- SELEÇÃO DO PET -----
    pet_escolhido = st.selectbox(
        "🐾 Pet:",
        pets_df["label"],
        help="Selecione o pet para ver seu histórico de vacinações"
    )

    id_pet = int(pet_escolhido.split(" - ")[0])

    # ----- CONSULTAR HISTÓRICO -----
    if st.button("🔍 Consultar Histórico", use_container_width=True):
        resultado = consultar_historico_pet(id_pet)

        if isinstance(resultado, str):
            info_box(f"ℹ {resultado}")
        else:
            pet_name = pets_df[pets_df['idPet']==id_pet]['nome_pet'].iloc[0]
            success_box(f"✓ Histórico de vacinas do pet: {pet_name}")

            st.markdown("---")
            
            # Tabela de vacinações
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 16px;
                margin: 16px 0;
            ">
                <h3 style="color: {COLORS['primary']}; margin-bottom: 12px;">💉 Todas as Vacinações</h3>
            """, unsafe_allow_html=True)
            
            st.dataframe(resultado, use_container_width=True, height=300)

            total = len(resultado)
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="📊 Total de Registros", value=total)
            
            with col2:
                aplicadas = len(resultado[resultado["status"].isin(["aplicada", "concluída"])])
                st.metric(label="✅ Aplicadas", value=aplicadas)
            
            with col3:
                pendentes = len(resultado[resultado["status"] == "pendente"])
                st.metric(label="⏳ Pendentes", value=pendentes)

            st.markdown("</div>", unsafe_allow_html=True)

            # Exibir próximas doses
            if "dataProximaDose" in resultado.columns:
                # Converter para datas reais (evita erro de comparação)
                resultado["dataProximaDose"] = pd.to_datetime(
                    resultado["dataProximaDose"], errors="coerce"
                ).dt.date

                hoje = datetime.now().date()

                # Filtrar apenas doses com futura aplicação e não aplicadas
                proximas = resultado[
                    (resultado["dataProximaDose"].notna()) &
                    (resultado["dataProximaDose"] > hoje) &
                    (resultado["status"] != "aplicada") &
                    (resultado["status"] != "concluída")
                ]

                st.markdown("---")
                section_title("Próximas Doses Agendadas", "📅")

                if not proximas.empty:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #d4edda, #c3e6cb);
                        border-left: 4px solid {COLORS['success']};
                        border-radius: 12px;
                        padding: 16px;
                        margin: 12px 0;
                    ">
                    """, unsafe_allow_html=True)
                    
                    st.dataframe(
                        proximas[["nome", "dataProximaDose"]],
                        use_container_width=True,
                        height=200
                    )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    info_box("ℹ Nenhuma dose futura pendente para este pet.")
            
                