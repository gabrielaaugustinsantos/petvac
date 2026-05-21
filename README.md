# 🐾 PetVac – Sistema de Gerenciamento de Vacinação de Pets

## 📌 Descrição do Projeto

O **PetVac** é um sistema desenvolvido para auxiliar **clínicas veterinárias** no gerenciamento de:

- Pets e seus tutores
- Usuários internos (veterinários e recepcionistas)
- Vacinas: datas de aplicação, próximas doses e histórico completo
- Alertas de vacinas pendentes e atrasadas

O sistema foi projetado para uso **exclusivo da clínica**, garantindo que apenas profissionais autorizados tenham acesso às informações.

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python** – Lógica de negócio e API REST
- **FastAPI** – Camada de API REST com documentação automática (Swagger)
- **Pandas** – Manipulação e persistência de dados em arquivos CSV
- **Pydantic** – Validação de dados
- **bcrypt** – Criptografia de senhas
- **python-jose** – Autenticação via JWT
- **CSV** – Armazenamento dos dados (`pets.csv`, `tutores.csv`, `vacinas.csv`, `usuarios.csv`)

### Frontend
- **Next.js 14** – Framework React com App Router
- **React** – Interface de usuário
- **TypeScript** – Tipagem estática
- **Tailwind CSS** – Estilização

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura em **3 camadas bem separadas**:

```
Frontend (Next.js/React)
        ↓  HTTP/JSON
API REST (FastAPI/Python)
        ↓
Lógica de Negócio (services.py + Pandas)
        ↓
Dados (CSV)
```

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Python 3.10+
- Node.js 18+
- npm

---

### 1. Clonar o repositório

```bash
git clone <repo-url>
cd petvac-1
```

---

### 2. Instalar dependências Python

```bash
pip install -r requirements.txt
pip install fastapi uvicorn "python-jose[cryptography]" python-multipart
```

---

### 3. Rodar a API (backend)

```bash
python -m uvicorn api.main:app --reload --port 8000
```

A API ficará disponível em:
- **http://localhost:8000** — endpoints REST
- **http://localhost:8000/docs** — documentação interativa (Swagger UI)

---

### 4. Instalar dependências do frontend

```bash
cd frontend
npm install
```

---

### 5. Rodar o frontend

```bash
npm run dev
```

O sistema ficará disponível em **http://localhost:3000**.

> Os dois servidores precisam estar rodando ao mesmo tempo (cada um em um terminal separado).

---

### 6. Criar o primeiro usuário

Na tela de login, acesse a aba **"Criar conta"** e cadastre um usuário com cargo `recepcionista` ou `veterinario`. Após o cadastro, faça login normalmente.

---

## 📂 Estrutura do Projeto

```
petvac-1/
│
├── backend/                    ← Lógica de negócio (Python + Pandas)
│   ├── services.py             • Todas as operações do sistema
│   ├── database.py             • Leitura/escrita dos CSVs
│   ├── validators.py           • Validação de dados com Pydantic
│   ├── security.py             • Hash e verificação de senhas (bcrypt)
│   ├── config.py               • Configurações globais
│   ├── pet.py / tutor.py / vacina.py / usuario.py   • Modelos de domínio
│   └── notificacao.py / historico_vacinas.py
│
├── api/                        ← API REST (FastAPI)
│   ├── main.py                 • App FastAPI + CORS + registro de rotas
│   ├── schemas.py              • Schemas de request/response (Pydantic)
│   ├── auth_utils.py           • Geração e verificação de tokens JWT
│   ├── deps.py                 • Dependência de autenticação
│   └── routes/
│       ├── auth.py             • POST /auth/login, /register, /logout
│       ├── pets.py             • GET/POST /pets, PUT /pets/{id}
│       ├── tutores.py          • GET/POST /tutores, PUT /tutores/{id}
│       ├── vacinas.py          • POST /vacinas, GET /pendentes, POST /{id}/aplicar
│       ├── dashboard.py        • GET /dashboard (métricas)
│       └── notificacoes.py     • GET/POST /notificacoes
│
├── frontend/                   ← Interface web (Next.js + React + TypeScript)
│   └── src/
│       ├── app/                • Páginas (App Router)
│       │   ├── page.tsx        • Login / Cadastro
│       │   └── (dashboard)/
│       │       ├── dashboard/  • Métricas e vacinas pendentes
│       │       ├── tutores/    • CRUD de tutores
│       │       ├── pets/       • CRUD de pets
│       │       ├── vacinas/    • Registrar e aplicar vacinas
│       │       ├── historico/  • Histórico por pet
│       │       └── notificacoes/ • Alertas de pendência e atraso
│       ├── components/         • Componentes reutilizáveis (Button, Modal, etc.)
│       ├── services/           • Funções que chamam a API REST
│       ├── contexts/           • AuthContext (estado global de autenticação)
│       ├── lib/                • Cliente HTTP e helpers de auth
│       └── types/              • Tipos TypeScript do domínio
│
└── data/                       ← Dados persistidos em CSV
    ├── pets.csv
    ├── tutores.csv
    ├── vacinas.csv
    ├── usuarios.csv
    └── notificacoes.csv
```

---

## 🔐 Autenticação

O sistema usa **JWT (JSON Web Token)**:

1. O usuário faz login com nome, senha e cargo
2. A API valida as credenciais (bcrypt) e retorna um token JWT
3. O frontend armazena o token e o envia em todas as requisições (`Authorization: Bearer <token>`)
4. Rotas não autenticadas retornam `401 Unauthorized`
