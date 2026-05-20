"""
Sistema de Design do PetVac - Componentes reutilizáveis e CSS centralizado.
Define cores, tipografia, componentes e animações para toda aplicação.
"""

import streamlit as st
from typing import Optional, List, Tuple

# ============================================================================
# PALETA DE CORES
# ============================================================================

COLORS = {
    # Primária - Azul Petrol (mais escuro para melhor contraste)
    "primary": "#0d4a5f",
    "primary_light": "#1e5f7a",
    "primary_dark": "#082e3e",
    
    # Secundária - Rosa/Coral (mais vibrante)
    "secondary": "#e74c3c",
    "secondary_light": "#ec7063",
    "secondary_dark": "#c0392b",
    
    # Status (com melhor contraste)
    "success": "#229954",
    "warning": "#d68910",
    "danger": "#c0392b",
    "info": "#2471a3",
    
    # Neutros (melhorados para contraste)
    "white": "#ffffff",
    "black": "#1a1a1a",
    "gray_light": "#f8f9fa",
    "gray": "#555555",  # Mais escuro
    "gray_dark": "#2c3e50",  # Muito mais escuro
    "text_primary": "#1a1a1a",  # Texto principal - bem escuro
    "text_secondary": "#2c3e50",  # Texto secundário
    
    # Gradient
    "gradient_primary": "linear-gradient(135deg, #0d4a5f, #1e5f7a)",
    "gradient_secondary": "linear-gradient(135deg, #e74c3c, #ec7063)",
}

# ============================================================================
# CSS GLOBAL
# ============================================================================

GLOBAL_CSS = f"""
<style>
    /* Importar fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Reset e base */
    * {{
        font-family: 'Poppins', sans-serif;
    }}

    body {{
        background-color: {COLORS['gray_light']};
        color: {COLORS['text_primary']};
        font-size: 1rem;
    }}

    p, span, label, div {{
        color: {COLORS['text_primary']};
    }}

    /* Texto */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['primary']};
        font-weight: 700;
    }}

    h1 {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}

    h2 {{
        font-size: 2rem;
        margin-bottom: 1rem;
    }}

    h3 {{
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }}

    /* Botões */
    .stButton > button {{
        background: {COLORS['gradient_primary']};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 95, 122, 0.3);
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 95, 122, 0.4);
    }}

    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* Input fields */
    input, textarea, select {{
        border-radius: 12px !important;
        border: 2px solid #ccc !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        color: {COLORS['text_primary']} !important;
        background-color: white !important;
        transition: all 0.3s ease !important;
    }}

    input::placeholder {{
        color: {COLORS['gray']} !important;
        opacity: 0.7 !important;
    }}

    input:focus, textarea:focus, select:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 3px rgba(13, 74, 95, 0.1) !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* Selectbox */
    .stSelectbox > div > div {{
        border-radius: 12px !important;
    }}

    /* Dividers */
    hr {{
        margin: 2rem 0;
        border: none;
        border-top: 2px solid {COLORS['gray_light']};
    }}

    /* Cards de métrica */
    .metric-card {{
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 4px solid {COLORS['primary']};
        transition: all 0.3s ease;
    }}

    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }}

    /* Alert messages */
    .stSuccess {{
        background-color: #d4edda;
        border-color: {COLORS['success']};
        border-radius: 12px;
    }}

    .stError {{
        background-color: #f8d7da;
        border-color: {COLORS['danger']};
        border-radius: 12px;
    }}

    .stWarning {{
        background-color: #fff3cd;
        border-color: {COLORS['warning']};
        border-radius: 12px;
    }}

    .stInfo {{
        background-color: #d1ecf1;
        border-color: {COLORS['info']};
        border-radius: 12px;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {{
        border-radius: 12px 12px 0 0;
        font-weight: 600;
        color: {COLORS['gray']};
    }}

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: {COLORS['primary']};
        border-bottom: 3px solid {COLORS['primary']};
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {COLORS['gray_light']};
        border-radius: 12px;
        padding: 12px 16px;
        font-weight: 600;
    }}

    /* Container */
    .container {{
        background: white;
        border-radius: 15px;
        padding: 24px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin: 16px 0;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {COLORS['gradient_primary']};
    }}

    [data-testid="stSidebar"] a {{
        color: white !important;
    }}

    /* Dataframe */
    .dataframe {{
        border-radius: 12px;
        overflow: hidden;
    }}

    /* Código */
    pre {{
        background-color: {COLORS['gray_dark']};
        color: {COLORS['white']};
        border-radius: 12px;
        padding: 16px;
        font-family: 'Courier New', monospace;
    }}
</style>
"""


# ============================================================================
# COMPONENTES REUTILIZÁVEIS
# ============================================================================

def header(title: str, subtitle: str = "", emoji: str = "🐾"):
    """
    Cria um header padrão para páginas.
    
    Args:
        title: Título principal
        subtitle: Subtítulo (opcional)
        emoji: Emoji a exibir (padrão: 🐾)
    """
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{emoji}</h1>", 
                   unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    
    if subtitle:
        st.markdown(f"<p style='color: {COLORS['gray']}; font-size: 1.1rem;'>{subtitle}</p>", 
                   unsafe_allow_html=True)
    st.markdown("---")


def metric_card(label: str, value: str | int, emoji: str = "", 
                color: str = "primary", help_text: str = ""):
    """
    Cria um card de métrica com estilo.
    
    Args:
        label: Rótulo da métrica
        value: Valor a exibir
        emoji: Emoji (opcional)
        color: Cor (primary, success, warning, danger, info)
        help_text: Texto de ajuda ao passar o mouse
    """
    color_value = COLORS.get(color, COLORS["primary"])
    
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {color_value};" title="{help_text}">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">{emoji}</div>
        <div style="color: {COLORS['gray']}; font-size: 0.9rem; font-weight: 500;">{label}</div>
        <div style="color: {color_value}; font-size: 2rem; font-weight: 700;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def section_title(title: str, emoji: str = ""):
    """Cria um título de seção com estilo."""
    st.markdown(f"""
    <div style="margin-top: 2rem; margin-bottom: 1.5rem;">
        <h3 style="color: {COLORS['primary']}; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 2rem;">{emoji}</span>
            {title}
        </h3>
        <div style="height: 3px; background: {COLORS['gradient_primary']}; width: 100%; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)


def success_box(message: str):
    """Cria uma caixa de sucesso com estilo."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-left: 4px solid {COLORS['success']};
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    ">
        <div style="color: {COLORS['success']}; font-weight: 600; font-size: 1.1rem;">
            ✓ {message}
        </div>
    </div>
    """, unsafe_allow_html=True)


def error_box(message: str):
    """Cria uma caixa de erro com estilo."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        border-left: 4px solid {COLORS['danger']};
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    ">
        <div style="color: {COLORS['danger']}; font-weight: 600; font-size: 1.1rem;">
            ✗ {message}
        </div>
    </div>
    """, unsafe_allow_html=True)


def info_box(message: str):
    """Cria uma caixa de informação com estilo."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #d1ecf1, #bee5eb);
        border-left: 4px solid {COLORS['info']};
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    ">
        <div style="color: {COLORS['info']}; font-weight: 600; font-size: 1.1rem;">
            ℹ {message}
        </div>
    </div>
    """, unsafe_allow_html=True)


def feature_card(emoji: str, title: str, description: str):
    """Cria um card de feature com estilo."""
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 15px;
        padding: 24px;
        border: 2px solid {COLORS['gray_light']};
        text-align: center;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 3rem; margin-bottom: 12px;">{emoji}</div>
        <h4 style="color: {COLORS['primary']}; margin: 8px 0;">{title}</h4>
        <p style="color: {COLORS['gray']}; margin: 8px 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def button_group(buttons: List[Tuple[str, str]]) -> Optional[str]:
    """
    Cria um grupo de botões em linha.
    
    Args:
        buttons: Lista de tuplas (label, key)
        
    Returns:
        Chave do botão pressionado ou None
    """
    cols = st.columns(len(buttons))
    for col, (label, key) in zip(cols, buttons):
        with col:
            if st.button(label, key=key, use_container_width=True):
                return key
    return None
