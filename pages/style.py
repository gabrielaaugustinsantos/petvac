"""
Gerenciador de estilos e temas do PetVac.
Aplica CSS global e configurações de tema.
"""
import streamlit as st
from backend.design_system import GLOBAL_CSS, COLORS


def set_css():
    """
    Aplica o CSS global e configurações de tema da aplicação.
    Deve ser chamado no início de cada página.
    """
    # Aplicar CSS global
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    
    # Configurar página
    st.set_page_config(
        page_title="PetVac - Sistema de Vacinação",
        page_icon="🐾",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # CSS adicional para melhor contraste e legibilidade
    st.markdown(f"""
    <style>
        /* Margens e padding padrão */
        .main {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        
        /* Fundo e cores principais */
        .stApp {{
            background-color: #f8f9fa;
        }}
        
        /* Titles e labels com ALTO CONTRASTE */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
            color: {COLORS['primary']} !important;
            font-weight: 700 !important;
        }}
        
        .stMarkdown p, .stMarkdown span, .stMarkdown label {{
            color: {COLORS['text_primary']} !important;
            font-weight: 500 !important;
        }}
        
        /* Inputs com melhor contraste */
        .stTextInput input, .stTextArea textarea,
        .stNumberInput input, .stDateInput input {{
            color: {COLORS['text_primary']} !important;
            background-color: white !important;
            border: 2px solid #ddd !important;
        }}
        
        /* Selectbox com cor diferenciada */
        .stSelectbox {{
            background-color: transparent !important;
        }}
        
        .stSelectbox label {{
            color: {COLORS['text_primary']} !important;
        }}
        
        [data-baseweb="select"] {{
            background-color: white !important;
            width: 100% !important;
        }}
        
        [data-baseweb="select"] > div {{
            background-color: #f0f4f8 !important;
            border: 2px solid #b0c4de !important;
        }}
        
        /* Button do selectbox - principal */
        [data-baseweb="select"] button {{
            background-color: #f0f4f8 !important;
            border: 2px solid #b0c4de !important;
            color: {COLORS['primary']} !important;
            font-weight: 600 !important;
            height: 45px !important;
        }}
        
        [data-baseweb="select"] button:hover {{
            background-color: #e6f0fa !important;
            border-color: #4682b4 !important;
        }}
        
        [data-baseweb="select"] button:focus {{
            background-color: #e6f0fa !important;
            outline: none !important;
        }}
        
        /* Menu do selectbox - opções */
        [data-baseweb="popover"] {{
            background-color: white !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }}
        
        [data-baseweb="menu"] {{
            background-color: white !important;
        }}
        
        [data-baseweb="menu"] > div {{
            background-color: white !important;
        }}
        
        [data-baseweb="menu"] [role="option"] {{
            color: {COLORS['text_primary']} !important;
            background-color: white !important;
            font-weight: 500 !important;
        }}
        
        [data-baseweb="menu"] [role="option"]:hover {{
            background-color: #f0f4f8 !important;
            color: {COLORS['primary']} !important;
            border-radius: 8px !important;
        }}
        
        [data-baseweb="menu"] [role="option"][aria-selected="true"] {{
            background-color: #e6f0fa !important;
            color: {COLORS['primary']} !important;
            font-weight: 600 !important;
        }}
        
        /* Input/Search dentro do selectbox - OCULTAR apenas a barra de busca */
        [data-baseweb="menu"] [data-baseweb="input"] {{
            display: none !important;
        }}
        
        [role="listbox"] [data-baseweb="input"] {{
            display: none !important;
        }}
        
        [data-baseweb="menu"] input {{
            display: none !important;
        }}
        
        /* Garante que qualquer input dentro de popovers/menus seja ocultado */
        div[data-baseweb="popover"] input {{
            display: none !important;
        }}
        
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: {COLORS['gray']} !important;
            opacity: 0.7 !important;
        }}
        
        /* Header/Banner superior do Streamlit */
        [data-testid="stAppHeader"] {{
            background-color: {COLORS['primary']} !important;
            position: sticky !important;
            top: 0 !important;
            z-index: 100 !important;
        }}
        
        [data-testid="stAppHeader"] button {{
            color: white !important;
        }}
        
        [data-testid="stAppHeader"] button svg {{
            color: white !important;
            fill: white !important;
        }}
        
        /* Cabeçalho da página (PetVac) - Forçar branco */
        /* Aplicar apenas aos elementos de texto, não ao container */
        .stMarkdown div[style*="text-align: center"] h1 {{
            color: white !important;
            background-color: {COLORS['primary']} !important;
            padding: 1.5rem !important;
            margin: 0 -1.5rem !important;
            width: calc(100% + 3rem) !important;
            position: relative !important;
            left: -1.5rem !important;
        }}
        
        .stMarkdown div[style*="text-align: center"] p {{
            color: white !important;
            background-color: {COLORS['primary']} !important;
            padding: 0 1.5rem 1.5rem !important;
            margin: 0 -1.5rem !important;
            width: calc(100% + 3rem) !important;
            position: relative !important;
            left: -1.5rem !important;
        }}
        
        /* Emoji precisa de fundo também */
        .stMarkdown div[style*="text-align: center"] > div:first-child {{
            background-color: {COLORS['primary']} !important;
            padding-top: 1.5rem !important;
            margin: -1.5rem -1.5rem 0 -1.5rem !important;
            width: calc(100% + 3rem) !important;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
            padding-top: 2rem;
        }}
        
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown span {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: white !important;
        }}
        
        /* Remove top padding */
        [data-testid="stAppViewContainer"] {{
            padding-top: 0;
        }}
        
        /* Botões com melhor estilo */
        .stButton > button {{
            background: {COLORS['gradient_primary']} !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            border: none !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 12px;
        }}
        
        .stTabs [data-baseweb="tab-list"] button {{
            border-radius: 12px !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
        }}
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: {COLORS['primary']} !important;
            border-bottom: 3px solid {COLORS['secondary']} !important;
        }}
        
        /* Dividers */
        hr {{
            border: none !important;
            border-top: 2px solid #e0e0e0 !important;
            margin: 2rem 0 !important;
        }}
    </style>
    """, unsafe_allow_html=True)