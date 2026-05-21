# PetVac – Sistema de Gerenciamento de Vacinação de Pets

## Visão Geral

O **PetVac** é uma plataforma digital de gerenciamento de saúde animal que conecta clínicas veterinárias e tutores em um ecossistema integrado. O sistema permite o cadastro de pets e tutores, registro e acompanhamento de vacinas, consulta de histórico clínico e alertas automáticos sobre vacinações pendentes ou vencidas.

A proposta central é unir tecnologia e cuidado animal, promovendo rastreabilidade, transparência e organização no histórico de saúde dos animais — enquanto veterinários e recepcionistas têm acesso a uma ferramenta ágil e confiável.

---

## Tecnologias

| Camada       | Tecnologia                        |
|--------------|-----------------------------------|
| Frontend     | Next.js 14 (React + TypeScript)   |
| API REST     | FastAPI (Python)                  |
| Backend      | Python (lógica de negócio)        |
| Banco de dados | Arquivos CSV via Pandas          |
| Autenticação | JWT Bearer Token (python-jose)    |
| Segurança    | bcrypt para hash de senhas        |

---

## Arquitetura

O sistema segue uma **arquitetura em camadas** com separação clara de responsabilidades:

```
Frontend (Next.js)
      ↓  HTTP / JSON
API REST (FastAPI) — porta 8000
      ↓  chamadas de função
Backend (services.py + classes de domínio)
      ↓  leitura / escrita
Banco de dados (CSV via Pandas)
```

### Estrutura de pastas

```
petvac-1/
│
├── api/                        ← API REST (FastAPI)
│   ├── main.py                 ← app FastAPI, CORS, registro de routers
│   ├── config.py               ← variáveis de ambiente (secret, CORS, etc.)
│   ├── auth_utils.py           ← geração e validação de JWT
│   ├── deps.py                 ← dependency injection (get_current_user)
│   ├── schemas/                ← schemas Pydantic por domínio
│   │   ├── auth.py
│   │   ├── pets.py
│   │   ├── tutores.py
│   │   ├── vacinas.py
│   │   ├── notificacoes.py
│   │   ├── dashboard.py
│   │   └── common.py
│   ├── routes/                 ← endpoints REST por recurso
│   │   ├── auth.py
│   │   ├── pets.py
│   │   ├── tutores.py
│   │   ├── vacinas.py
│   │   ├── notificacoes.py
│   │   └── dashboard.py
│   └── utils/
│       └── helpers.py          ← utilitários compartilhados
│
├── backend/                    ← Lógica de negócio e domínio
│   ├── services.py             ← operações CRUD e regras de negócio
│   ├── database.py             ← acesso a CSV (carregar/salvar)
│   ├── validators.py           ← validação com Pydantic
│   ├── security.py             ← hash e verificação de senha (bcrypt)
│   ├── logger.py               ← sistema de logs
│   ├── pet.py                  ← classe Pet
│   ├── tutor.py                ← classe Tutor
│   ├── vacina.py               ← classe Vacina
│   ├── usuario.py              ← classe Usuario
│   ├── notificacao.py          ← classe Notificacao
│   └── historico_vacinas.py    ← classe HistoricoVacinas
│
├── frontend/                   ← Interface web (Next.js)
│   └── src/
│       ├── app/(dashboard)/    ← páginas autenticadas
│       ├── components/         ← componentes reutilizáveis
│       ├── services/           ← clientes da API REST
│       ├── types/              ← tipos TypeScript
│       └── lib/api.ts          ← cliente HTTP base
│
├── data/                       ← Arquivos CSV (banco de dados)
│   ├── pets.csv
│   ├── tutores.csv
│   ├── vacinas.csv
│   ├── usuarios.csv
│   └── notificacoes.csv
│
└── requirements.txt
```

---

## API REST

A API REST é o coração do sistema. Toda a comunicação entre frontend e backend passa por ela.

**Base URL:** `http://localhost:8000`  
**Documentação interativa:** `http://localhost:8000/docs` (Swagger UI)  
**Autenticação:** JWT Bearer Token (obtido via `/auth/login`)

### Endpoints

#### Autenticação (`/auth`)

| Método | Endpoint         | Descrição                              | Auth |
|--------|------------------|----------------------------------------|------|
| POST   | `/auth/login`    | Autentica e retorna JWT                | ❌   |
| POST   | `/auth/register` | Cadastra novo usuário                  | ❌   |
| POST   | `/auth/logout`   | Encerra sessão                         | ✅   |

#### Pets (`/pets`)

| Método | Endpoint         | Descrição                              | Auth |
|--------|------------------|----------------------------------------|------|
| GET    | `/pets/`         | Lista todos os pets                    | ✅   |
| GET    | `/pets/{id}`     | Busca pet por ID                       | ✅   |
| POST   | `/pets/`         | Cadastra novo pet                      | ✅   |
| PUT    | `/pets/{id}`     | Atualiza dados do pet                  | ✅   |
| DELETE | `/pets/{id}`     | Remove pet do sistema                  | ✅   |

#### Tutores (`/tutores`)

| Método | Endpoint           | Descrição                              | Auth |
|--------|--------------------|----------------------------------------|------|
| GET    | `/tutores/`        | Lista todos os tutores                 | ✅   |
| GET    | `/tutores/{id}`    | Busca tutor por ID                     | ✅   |
| POST   | `/tutores/`        | Cadastra novo tutor                    | ✅   |
| PUT    | `/tutores/{id}`    | Atualiza dados do tutor                | ✅   |
| DELETE | `/tutores/{id}`    | Remove tutor do sistema                | ✅   |

#### Vacinas (`/vacinas`)

| Método | Endpoint                     | Descrição                              | Auth |
|--------|------------------------------|----------------------------------------|------|
| GET    | `/vacinas/pendentes`         | Lista vacinas pendentes/atrasadas      | ✅   |
| POST   | `/vacinas/`                  | Registra nova vacina                   | ✅   |
| POST   | `/vacinas/{id}/aplicar`      | Aplica dose pendente                   | ✅   |
| GET    | `/vacinas/historico/{id_pet}`| Histórico de vacinação do pet          | ✅   |

#### Notificações (`/notificacoes`)

| Método | Endpoint                        | Descrição                              | Auth |
|--------|---------------------------------|----------------------------------------|------|
| GET    | `/notificacoes/`                | Lista todas as notificações            | ✅   |
| POST   | `/notificacoes/gerar`           | Gera notificações para vacinas pendentes | ✅ |
| PUT    | `/notificacoes/{id}/lida`       | Marca notificação como lida            | ✅   |

#### Dashboard (`/dashboard`)

| Método | Endpoint       | Descrição                              | Auth |
|--------|----------------|----------------------------------------|------|
| GET    | `/dashboard/`  | Métricas consolidadas do sistema       | ✅   |

---

## Modelos de Dados

### Tutor
| Campo     | Tipo   | Descrição                  |
|-----------|--------|----------------------------|
| idTutor   | int    | Identificador único        |
| nome      | str    | Nome completo              |
| telefone  | str    | Telefone (10–11 dígitos)   |
| email     | str    | E-mail válido              |
| endereco  | str    | Endereço (opcional)        |

### Pet
| Campo          | Tipo   | Descrição                        |
|----------------|--------|----------------------------------|
| idPet          | int    | Identificador único              |
| nome           | str    | Nome do pet                      |
| especie        | str    | Espécie (Cachorro, Gato, etc.)   |
| raca           | str    | Raça                             |
| dataNascimento | str    | Data de nascimento (YYYY-MM-DD)  |
| idTutor        | int    | FK → Tutor responsável           |

### Vacina
| Campo          | Tipo   | Descrição                             |
|----------------|--------|---------------------------------------|
| idVacina       | int    | Identificador único                   |
| idPet          | int    | FK → Pet vacinado                     |
| nome           | str    | Nome da vacina                        |
| dataAplicacao  | str    | Data de aplicação (YYYY-MM-DD)        |
| dataProximaDose| str    | Data da próxima dose (YYYY-MM-DD)     |
| status         | str    | pendente / aplicada / concluída       |
| obs            | str    | Observações sobre a aplicação         |

### Usuario
| Campo    | Tipo   | Descrição                            |
|----------|--------|--------------------------------------|
| idUsuario| int    | Identificador único                  |
| nome     | str    | Nome do usuário                      |
| senha    | str    | Hash bcrypt da senha                 |
| cargo    | str    | recepcionista ou veterinario         |

---

## Relações entre Entidades

```
Tutor  1 ──── N  Pet
Pet    1 ──── N  Vacina
Pet    1 ──── 1  HistoricoVacinas
```

---

## Fluxos Principais

### Cadastro de Tutor e Pet
1. Recepcionista faz login (`POST /auth/login`)
2. Cadastra o tutor (`POST /tutores/`)
3. Cadastra o pet associado ao tutor (`POST /pets/`)

### Registro de Vacina
1. Veterinário ou recepcionista seleciona o pet
2. Registra a vacina com nome, datas e observações (`POST /vacinas/`)
3. Status é calculado automaticamente (pendente/aplicada)

### Consulta de Histórico
1. Usuário seleciona o pet
2. Sistema retorna histórico completo ordenado por data (`GET /vacinas/historico/{id_pet}`)

### Alertas e Notificações
1. Sistema analisa vacinas com próxima dose vencida ou próxima (`GET /vacinas/pendentes`)
2. Gera notificações automáticas (`POST /notificacoes/gerar`)
3. Recepcionista visualiza e marca como lida (`PUT /notificacoes/{id}/lida`)

---

## Como Executar

### Backend (API FastAPI)
```bash
uvicorn api.main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

Acesse o sistema em `http://localhost:3000`  
Acesse a documentação da API em `http://localhost:8000/docs`
