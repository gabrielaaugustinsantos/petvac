import streamlit as st
from backend.services import login_usuario, logout_usuario, cadastrar_usuario
from backend.design_system import COLORS, success_box, error_box, info_box
from pages.style import set_css

set_css()

if "usuario" not in st.session_state:
    st.session_state["usuario"] = None


# ============================================================================
# PÁGINA DE LOGIN - DESIGN MODERNO
# ============================================================================

def pagina_login():
    """Página de login com design moderno e responsivo."""
    
    # Criar coluna central para o formulário
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Header com logo e título
        st.markdown(f"""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🐾</div>
            <h1 style="font-size: 2.5rem; color: {COLORS['primary']}; margin: 0;">PetVac</h1>
            <p style="color: {COLORS['gray']}; font-size: 1.1rem; margin: 0.5rem 0;">
                Sistema de Gerenciamento de Vacinação
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Container do formulário
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 10px 40px rgba(30, 95, 122, 0.15);
            border: 1px solid rgba(30, 95, 122, 0.1);
        ">
        """, unsafe_allow_html=True)
        
        # Inicializar session states
        if "mostrar_cadastro" not in st.session_state:
            st.session_state["mostrar_cadastro"] = False
        if "erro_login" not in st.session_state:
            st.session_state["erro_login"] = None
        
        # Abas: Login / Cadastro
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
        
        # ============== ABA LOGIN ==============
        with tab1:
            st.markdown("<h3 style='text-align: center;'>Faça seu login</h3>", unsafe_allow_html=True)
            
            # Exibir erro se houver
            if st.session_state["erro_login"]:
                error_box(st.session_state["erro_login"])
            
            nome = st.text_input(
                "👤 Nome completo",
                placeholder="Digite seu nome..."
            )
            
            senha = st.text_input(
                "🔒 Senha",
                type="password",
                placeholder="Digite sua senha..."
            )
            
            cargo = st.selectbox(
                "💼 Cargo",
                ["recepcionista", "veterinario"],
                format_func=lambda x: "👨‍⚕️ Veterinário" if x == "veterinario" else "👨‍💼 Recepcionista"
            )
            
            # Botão Login
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                if st.button("🚀 Entrar", use_container_width=True, type="primary"):
                    sucesso, msg = login_usuario(nome, senha, cargo)
                    
                    if sucesso:
                        st.session_state["usuario"] = {"nome": nome, "senha": senha, "cargo": cargo}
                        st.session_state["erro_login"] = None
                        st.session_state["mostrar_cadastro"] = False
                        success_box(msg.replace("✅", "").strip())
                        st.balloons()
                        st.rerun()
                    else:
                        st.session_state["erro_login"] = msg.replace("❌", "").strip()
                        st.rerun()
        
        # ============== ABA CADASTRO ==============
        with tab2:
            st.markdown("<h3 style='text-align: center;'>Criar nova conta</h3>", unsafe_allow_html=True)
            
            nome_cad = st.text_input(
                "👤 Nome completo",
                placeholder="Digite seu nome completo...",
                key="nome_cad"
            )
            
            email_cad = st.text_input(
                "📧 Email",
                placeholder="seu.email@example.com",
                key="email_cad"
            )
            
            telefone_cad = st.text_input(
                "📱 Telefone",
                placeholder="(11) 99999-9999",
                key="telefone_cad"
            )
            
            senha_cad = st.text_input(
                "🔒 Senha",
                type="password",
                placeholder="Escolha uma senha segura...",
                key="senha_cad"
            )
            
            cargo_cad = st.selectbox(
                "💼 Cargo",
                ["recepcionista", "veterinario"],
                format_func=lambda x: "👨‍⚕️ Veterinário" if x == "veterinario" else "👨‍💼 Recepcionista",
                key="cargo_cad"
            )
            
            # Botão Cadastro
            if st.button("✅ Criar Conta", use_container_width=True, type="primary"):
                sucesso, msg = cadastrar_usuario(nome_cad, senha_cad, cargo_cad)
                
                if sucesso:
                    success_box(msg.replace("✅", "").strip())
                    info_box("Agora faça o login com suas credenciais.")
                    st.balloons()
                    st.session_state["mostrar_cadastro"] = False
                    st.session_state["erro_login"] = None
                    st.rerun()
                else:
                    error_box(msg.replace("❌", "").strip())
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown(f"""
        <div style="text-align: center; margin-top: 2rem; color: {COLORS['gray']}; font-size: 0.9rem;">
            <p>🐾 PetVac v1.0 | Sistema seguro com criptografia bcrypt</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# VERIFICAÇÃO DE LOGIN
# ============================================================================

if st.session_state["usuario"] is None:
    pagina_login()
    st.stop()


# ============================================================================
# PÁGINA PRINCIPAL (APÓS LOGIN)
# ============================================================================

# Header com usuário logado
col_header1, col_header2, col_header3 = st.columns([2, 1, 1])

with col_header1:
    usuario = st.session_state["usuario"]
    cargo_display = "👨‍⚕️ Veterinário" if usuario['cargo'] == 'veterinario' else "👨‍💼 Recepcionista"
    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <p style="color: {COLORS['gray']}; margin: 0;">Bem-vindo(a),</p>
        <h2 style="margin: 0; color: {COLORS['primary']};">{usuario['nome']}</h2>
        <p style="color: {COLORS['gray']}; margin: 0.5rem 0 0 0;">{cargo_display}</p>
    </div>
    """, unsafe_allow_html=True)

with col_header3:
    if st.button("🚪 Sair", use_container_width=True):
        usuario = st.session_state["usuario"]
        logout_usuario(usuario["nome"], usuario["senha"], usuario["cargo"])
        st.session_state["usuario"] = None
        st.rerun()


st.divider()

# Navegação
pages = [
    st.Page("pages/home.py", title="🏠 Início"), 
    st.Page("pages/cadastro_tutor.py", title="👤 Tutores"),
    st.Page("pages/cadastro_pet.py", title="🐶 Pets"),
    st.Page("pages/vacinas.py", title="💉 Vacinas"),
    st.Page("pages/historico.py", title="📋 Histórico"),
    st.Page("pages/cadastrar_usuario.py", title="👥 Usuários")
]

navigator = st.navigation(pages)
navigator.run()