# 🐾 PetVac – Sistema de Gestão de Vacinação de Pets

Sistema web para clínicas veterinárias gerenciarem tutores, pets, vacinas e notificações de pendências.

---

## 🚀 Como Rodar

### Pré-requisitos
- [Python 3.10+](https://python.org)
- [Node.js 18+](https://nodejs.org)
- [Git](https://git-scm.com)

---

### 1. Clonar o repositório

```bash
git clone https://github.com/gabrielaaugustinsantos/petvac.git
cd petvac
```

---

### 2. Backend (Terminal 1)

```bash
# Criar e ativar ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

# Instalar dependências e rodar
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

✅ API em `http://localhost:8000`  
✅ Documentação em `http://localhost:8000/docs`

---

### 3. Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

✅ Sistema em `http://localhost:3000`

---

### 4. Primeiro acesso

Abra `http://localhost:3000` e crie uma conta na aba **"Cadastrar"** escolhendo o tipo:
- **Recepcionista** — cadastra tutores, pets e envia notificações
- **Veterinário(a)** — registra e aplica vacinas, consulta histórico

> ⚠️ Se o `.venv\Scripts\activate` falhar no Windows, rode antes:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

---

## 🏗️ Arquitetura

```
Frontend (Next.js 14 + TypeScript + Tailwind)
        ↓  HTTP REST + JWT
API (FastAPI + Python)
        ↓
Lógica de Negócio (services.py + Pydantic)
        ↓
Dados (CSV + Pandas)
```

---

## 📂 Estrutura

```
petvac/
├── api/                    ← API REST (FastAPI)
│   ├── main.py             • Aplicação + CORS
│   ├── auth_utils.py       • JWT
│   ├── deps.py             • Autenticação nas rotas
│   ├── config.py           • Configurações (SECRET_KEY, etc.)
│   ├── routes/             • auth · tutores · pets · vacinas · notificacoes · dashboard
│   ├── schemas/            • Schemas Pydantic por domínio
│   └── utils/              • Helpers compartilhados
│
├── backend/                ← Lógica de negócio
│   ├── services.py         • Todas as operações do sistema
│   ├── database.py         • Leitura/escrita CSV
│   ├── validators.py       • Validação de dados
│   ├── security.py         • bcrypt (hash de senhas)
│   └── pet · tutor · vacina · usuario · notificacao (modelos)
│
├── frontend/               ← Interface web
│   └── src/
│       ├── app/
│       │   ├── page.tsx              • Login / Cadastro / Redefinir senha
│       │   └── (dashboard)/
│       │       ├── dashboard/        • Métricas em tempo real
│       │       ├── tutores/          • CRUD tutores
│       │       ├── pets/             • CRUD pets
│       │       ├── vacinas/          • Registrar e aplicar vacinas
│       │       ├── historico/        • Histórico por pet
│       │       └── notificacoes/     • Alertas + notificação WhatsApp
│       ├── components/               • Button, Input, Badge, Alert, Modal...
│       ├── services/                 • Chamadas à API REST
│       ├── contexts/                 • AuthContext (JWT global)
│       └── types/                    • Tipos TypeScript
│
└── data/                   ← Persistência
    ├── pets.csv
    ├── tutores.csv
    ├── vacinas.csv
    ├── usuarios.csv
    └── notificacoes.csv
```

---

## 📡 Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/login` | Login com email + senha → JWT |
| POST | `/auth/register` | Cadastrar usuário |
| POST | `/auth/redefinir-senha` | Redefinir senha |
| GET | `/tutores/` | Listar tutores |
| POST | `/tutores/` | Cadastrar tutor |
| GET | `/pets/` | Listar pets |
| POST | `/pets/` | Cadastrar pet |
| GET | `/vacinas/pendentes` | Vacinas pendentes/atrasadas |
| POST | `/vacinas/` | Registrar vacina |
| POST | `/vacinas/{id}/aplicar` | Aplicar dose |
| GET | `/vacinas/historico/{idPet}` | Histórico por pet |
| GET | `/dashboard/metrics` | Métricas gerais |

Documentação interativa completa: **`http://localhost:8000/docs`**

---

## 🔐 Autenticação

Login com **email + senha** → API retorna token JWT → frontend envia em todas as requisições via `Authorization: Bearer <token>`. Senhas armazenadas com **bcrypt**.

---

## 🛠️ Stack

| Camada | Tecnologia |
|--------|------------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| API | FastAPI, Pydantic v2, python-jose |
| Backend | Python, Pandas, bcrypt |
| Dados | CSV |
