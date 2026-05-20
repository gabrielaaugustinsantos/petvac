# 📚 PETVAC - DOCUMENTAÇÃO COMPLETA DO PROJETO

## 1. 🎯 OBJETIVO DO TRABALHO

O projeto **PetVac** é um **Sistema de Gerenciamento de Vacinação** para clínicas veterinárias. Ele permite:

- 👤 Cadastro de tutores (donos dos pets)
- 🐾 Cadastro de pets (animais de estimação)
- 💉 Registro e controle de vacinações
- 📖 Histórico de vacinações por pet
- 📋 Consulta de vacinas pendentes e atrasadas
- 🔔 Sistema de alertas e notificações

---

## 2. 🏗️ ARQUITETURA DO PROJETO

### Estrutura de Pastas

```
petvac-1/
├── app.py                          # Página principal (Login/Signup)
├── requirements.txt                # Dependências Python
├── Documentação.md                 # Docs iniciais
├── DESIGN_SYSTEM_FINAL.md         # Design system completo
│
├── backend/                        # Lógica de negócio
│   ├── __init__.py
│   ├── database.py                 # Carregar/salvar CSV
│   ├── services.py                 # Funções principais (CRUD)
│   ├── config.py                   # ⭐ Config centralizada
│   ├── security.py                 # ⭐ Bcrypt hashing
│   ├── validators.py               # ⭐ Pydantic validators
│   ├── logger.py                   # ⭐ Logging centralizado
│   ├── utils.py                    # ⭐ Funções auxiliares
│   ├── enums.py                    # ⭐ Enumerações de tipos
│   ├── design_system.py            # ⭐ Sistema de design (CSS + componentes)
│   ├── historico_vacinas.py
│   ├── notificacao.py
│   ├── pet.py
│   ├── tutor.py
│   └── usuario.py
│
├── pages/                          # Páginas Streamlit
│   ├── style.py                    # ⭐ CSS melhorado com contraste
│   ├── home.py                     # Dashboard principal
│   ├── cadastro_tutor.py           # ⭐ Reformulada com design system
│   ├── cadastro_pet.py             # ⭐ Reformulada com design system
│   ├── vacinas.py                  # ⭐ Reformulada com design system
│   ├── historico.py                # ⭐ Reformulada com design system
│   ├── _notificacoes.py            # ⭐ Nova página de alertas
│   └── cadastrar_usuario.py
│
└── data/                           # Dados (CSV)
    ├── usuarios.csv                # Users registrados
    ├── tutores.csv                 # Donos de pets
    ├── pets.csv                    # Animais
    ├── vacinas.csv                 # Registros de vacinação
    └── notificacoes.csv            # Alertas
```

**⭐ = Arquivos novos ou completamente reformulados**

---

## 3. 🔧 TECNOLOGIAS UTILIZADAS

### Backend
- **Python 3.14.4** - Linguagem principal
- **Streamlit** - Framework web (interface responsiva)
- **Pandas** - Manipulação de dados (CSV)
- **Bcrypt** - Hashing de senhas (segurança)
- **Pydantic** - Validação de dados com type hints
- **Python Logging** - Logs centralizados

### Frontend
- **Streamlit Components** - UI/UX
- **Custom CSS** - Design system personalizado
- **HTML/Markdown** - Renderização de componentes

### Banco de Dados
- **CSV** - Armazenamento de dados (sem SQL)

---

## 4. 💻 COMO TUDO FUNCIONA

### 4.1 Fluxo de Autenticação

```
┌─────────────────────────────────────────────────┐
│ app.py - Página de Login/Signup                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Usuário acessa http://localhost:8501       │
│  2. Vê dois TABS: "🔐 Login" e "📝 Cadastro"   │
│  3. Preenche:                                   │
│     - 👤 Nome completo                          │
│     - 🔒 Senha                                  │
│     - 💼 Cargo (Recepcionista/Veterinário)     │
│                                                  │
│  4. Clica "🚀 Entrar"                           │
│                                                  │
│  5. backend/services.login_usuario() valida   │
│     - Busca usuário no CSV                      │
│     - Compara senha com Bcrypt                  │
│     - Armazena em session_state                 │
│                                                  │
│  6. Se OK → Redireciona para Dashboard         │
│     Se ERRO → Mostra error_box com ❌           │
│                                                  │
└─────────────────────────────────────────────────┘
```

### 4.2 Segurança - Bcrypt Hashing

```python
# backend/security.py
from bcrypt import hashpw, checkpw, gensalt

def hash_password(password: str) -> str:
    """Converte senha em hash (nunca armazenado em texto)"""
    salt = gensalt(rounds=12)  # 12 rounds = muito seguro
    hashed = hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
    # Retorna: $2b$12$...xyz (impossível reverter)

def verify_password(password: str, hashed: str) -> bool:
    """Valida senha comparando com hash"""
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

**Benefício**: Senhas nunca são armazenadas em texto! Mesmo se o CSV for vazado, as senhas estão protegidas.

### 4.3 Validação com Pydantic

```python
# backend/validators.py
from pydantic import BaseModel, EmailStr, field_validator

class TutorValidator(BaseModel):
    name: str
    phone: str
    email: EmailStr  # Valida automaticamente formato de email
    
    @field_validator('name')
    def name_must_be_long(cls, v):
        if len(v) < 3:
            raise ValueError('Nome deve ter mínimo 3 caracteres')
        return v
```

**Benefício**: Rejeita dados inválidos ANTES de salvar no banco!

### 4.4 Design System Centralizado

```python
# backend/design_system.py
COLORS = {
    "primary": "#0d4a5f",        # Azul escuro
    "text_primary": "#1a1a1a",   # Preto (MUITO ESCURO para contraste)
    "success": "#229954",         # Verde
    "danger": "#c0392b",          # Vermelho
}

def header(title: str, subtitle: str = "", emoji: str = "🐾"):
    """Componente reutilizável de header"""
    st.markdown(f"<h1>{emoji} {title}</h1>", unsafe_allow_html=True)

def success_box(message: str):
    """Componente reutilizável de caixa de sucesso"""
    st.markdown(f"""
    <div style="background: #d4edda; border-left: 4px solid #229954;">
        ✓ {message}
    </div>
    """, unsafe_allow_html=True)
```

**Benefício**: Mesmo estilo em TODAS as páginas! Mudar uma cor muda em tudo.

### 4.5 Fluxo de Cadastro de Pet

```
┌─────────────────────────────────────────────────┐
│ pages/cadastro_pet.py                           │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Usuário preenche:                           │
│     - 🐾 Nome do Pet                            │
│     - 🦮 Espécie (dropdown com 🐶🐱🦜🐭)      │
│     - 🏷️ Raça                                   │
│     - 📅 Data de Nascimento                     │
│     - 👤 Tutor (seletor)                        │
│                                                  │
│  2. Clica "✅ Cadastrar Pet"                    │
│                                                  │
│  3. PetValidator valida TODOS os dados         │
│     - Nome não vazio                            │
│     - Espécie válida                            │
│     - Data válida                               │
│                                                  │
│  4. Se erro → error_box mostra mensagem         │
│  5. Se OK → services.cadastrar_pet() salva      │
│             em data/pets.csv                    │
│             success_box mostra "✓ Pet criado"  │
│             st.rerun() atualiza interface      │
│                                                  │
└─────────────────────────────────────────────────┘
```

### 4.6 Sistema de Vacinação

```python
# pages/vacinas.py
# 3 SEÇÕES PRINCIPAIS:

# Seção 1: Registrar Vacina
- Seleciona pet
- Inforna vacina (ex: Raiva)
- Marca se já foi aplicada
- Define próxima dose
- Salva em data/vacinas.csv

# Seção 2: Ver Pendências
- Consulta vacinas com status="pendente"
- Mostra em tabela com color-coded status
  - ⚠️ ATRASADA (vermelho) = data passou
  - ⏳ PENDENTE (amarelo) = próximo prazo

# Seção 3: Aplicar Dose
- Seleciona vacina pendente
- Registra data de aplicação
- Define próxima dose
- Muda status para "aplicada"
```

---

## 5. 📊 ESTRUTURA DE DADOS

### CSV: usuarios.csv
```csv
idUsuario,nome,email,telefone,senha_hash,cargo
1,Admin,admin@petvac.com,(11)98765-4321,$2b$12$...,Veterinario
```

### CSV: tutores.csv
```csv
idTutor,nome,telefone,email,endereco
1,João Silva,(11)98765-4321,joao@email.com,Rua X...
```

### CSV: pets.csv
```csv
idPet,nome,especie,raca,dataNascimento,idTutor
1,Rex,Cachorro,Labrador,2020-05-15,1
```

### CSV: vacinas.csv
```csv
idVacina,idPet,nome,status,dataAplicacao,dataProximaDose
1,1,Raiva,aplicada,2024-05-20,2025-05-20
```

---

## 6. 🎨 DESIGN SYSTEM - O QUE MUDOU

### Antes (Problema)
- Fontes com cores claras (#95a5a6 - cinza muito claro)
- Fundo branco + texto claro = **ilegível**
- Contraste ruim em toda a interface
- Design inconsistente entre páginas

### Depois (Solução)
```python
COLORS = {
    "text_primary": "#1a1a1a",    # Preto bem escuro
    "text_secondary": "#2c3e50",  # Azul bem escuro
    "gray": "#555555",             # Cinza escuro (em vez de #95a5a6)
}
```

### CSS Melhorado (pages/style.py)

```css
/* ANTES: Sem especificação clara */
.stMarkdown p { 
    color: #95a5a6;  /* CINZA CLARO = ILEGÍVEL */
}

/* DEPOIS: Forçado com !important */
.stMarkdown p, .stMarkdown span, .stMarkdown label {
    color: #1a1a1a !important;  /* PRETO = LEGÍVEL */
    font-weight: 500 !important;
}

input::placeholder {
    color: #555555 !important;  /* Cinza escuro */
    opacity: 0.7 !important;
}
```

### Resultado Visual
✅ Todas as labels agora **VISÍVEIS**
✅ Inputs com **CONTRASTE CLARO**
✅ Botões com **DESTAQUE**
✅ Mensagens de erro em **BANNERS COLORIDOS**

---

## 7. 📁 COMPONENTES PRINCIPAIS

### backend/services.py
**O coração da aplicação!** Contém todas as operações CRUD:

```python
def cadastrar_tutor(nome, telefone, email, endereco) → str
def atualizar_tutor(idTutor, novos_dados) → str
def listar_tutores() → DataFrame

def cadastrar_pet(nome, especie, raca, data, idTutor) → str
def registrar_vacina(idPet, nome, data_aplicacao, data_proxima) → str
def aplicar_dose(idVacina, dataAplicacao, dataProximaDose) → str
def consultar_vacinas_pendentes() → DataFrame
def login_usuario(nome, senha, cargo) → bool
```

### pages/style.py
**Aplica o design system** em TODA a interface:

```python
def set_css():
    # 1. Aplica GLOBAL_CSS do design_system.py
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    
    # 2. Configura página
    st.set_page_config(layout="wide")
    
    # 3. Aplica CSS ADICIONAL para melhorar contraste
    st.markdown(f"""<style>
        .stMarkdown p {{ color: {COLORS['text_primary']} !important; }}
        input {{ color: {COLORS['text_primary']} !important; }}
    </style>""")
```

**Deve ser chamado NO INÍCIO de cada página!**

```python
# pages/cadastro_tutor.py
from pages.style import set_css
set_css()  # ← SEMPRE primeira linha!
```

### backend/design_system.py
**380+ linhas** com:
- 🎨 Paleta de cores (COLORS dict)
- 📝 CSS global (GLOBAL_CSS string)
- 🧩 7 componentes reutilizáveis:
  - `header()` - Títulos padronizados
  - `metric_card()` - Cards de números
  - `section_title()` - Títulos de seção
  - `feature_card()` - Cards de funcionalidades
  - `success_box()` - Caixas verdes
  - `error_box()` - Caixas vermelhas
  - `info_box()` - Caixas azuis

---

## 8. 🔐 SEGURANÇA

### Implementações:
1. ✅ **Bcrypt hashing** - Senhas nunca em texto plano
2. ✅ **Pydantic validation** - Rejeita dados inválidos
3. ✅ **Session state** - Login armazenado em session
4. ✅ **Error handling** - Try-except em todas operações
5. ✅ **Type hints** - Detecta bugs em tempo de desenvolvimento
6. ✅ **Logging centralizado** - Rastreia operações críticas

---

## 9. 🚀 FLUXO DE EXECUÇÃO

### 1. Usuário acessa app
```
http://localhost:8501
      ↓
app.py executado
      ↓
set_css() aplica design system
      ↓
Mostra página de login com design moderno
```

### 2. Usuário faz login
```
Preenche formulário
      ↓
Clica "🚀 Entrar"
      ↓
login_usuario() valida com Bcrypt
      ↓
st.session_state["usuario"] = {dados}
      ↓
Redireciona para dashboard
```

### 3. Usuário navega (sidebar)
```
Clica em "cadastro tutor"
      ↓
Streamlit abre pages/cadastro_tutor.py
      ↓
set_css() aplica design novamente
      ↓
Mostra formulário com componentes do design system
```

---

## 10. 📈 ESTATÍSTICAS DO PROJETO

| Item | Quantidade |
|------|-----------|
| Linhas de código Python | 3000+ |
| Componentes Design System | 7 |
| Validadores Pydantic | 4 |
| Páginas Streamlit | 8 |
| Cores definidas | 8+ |
| Emojis usados | 30+ |
| Tabelas CSV | 5 |
| Funções em services.py | 15+ |

---

## 11. 💡 MELHORIAS FUTURAS SUGERIDAS

1. **Autenticação JWT** - Tokens em vez de session_state
2. **Banco de dados SQL** - PostgreSQL em vez de CSV
3. **Gráficos** - Matplotlib/Plotly para estatísticas
4. **Email** - Enviar notificações por email
5. **Mobile app** - App nativa iOS/Android
6. **Dark mode** - Tema escuro
7. **Export** - Gerar relatórios em PDF
8. **API REST** - Para integração com outras sistemas

---

## 12. 📝 RESUMO EXECUTIVO

**PetVac** é um sistema profissional de gerenciamento de vacinação que combina:

✅ **Backend robusto** - Python + Pandas + Bcrypt
✅ **Frontend moderno** - Streamlit + Design System custom
✅ **Segurança** - Hashing de senhas + Validação de dados
✅ **Usabilidade** - Interface intuitiva com emojis e cores
✅ **Manutenibilidade** - Código modular, reutilizável e bem documentado

**Resultado**: Uma aplicação pronta para produção que gerencia vacinações de forma segura e eficiente!

---

**Desenvolvido com ❤️ usando Python, Streamlit e muito design system!**
