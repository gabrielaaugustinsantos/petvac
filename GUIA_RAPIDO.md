# 🚀 Guia Rápido das Novas Funcionalidades

## Como Usar as Melhorias Implementadas

### 1. 🔐 Hash de Senhas (Segurança)

**Usar em login:**
```python
from backend.security import hash_password, verify_password

# Ao cadastrar usuário
senha_segura = hash_password("senha_do_usuario")
banco.salvar(senha_segura)

# Ao fazer login
entrada_usuario = "senha_do_usuario"
is_valid = verify_password(entrada_usuario, senha_armazenada)
if is_valid:
    print("Login autorizado")
```

---

### 2. ✔️ Validação de Dados (Pydantic)

**Validar entrada antes de salvar:**
```python
from backend.validators import TutorValidator, PetValidator, UsuarioValidator

# Tutor
try:
    tutor_validado = TutorValidator(
        nome="João Silva",
        email="joao@test.com",
        telefone="11987654321"
    )
    print("Tutor válido")
except ValueError as e:
    print(f"Erro: {e}")

# Pet
try:
    pet_validado = PetValidator(
        nome="Rex",
        especie="Cachorro",
        raca="Labrador",
        data_nascimento="2020-05-15",
        idTutor=1
    )
except ValueError as e:
    print(f"Erro: {e}")

# Usuário
try:
    usuario_validado = UsuarioValidator(
        nome="Maria",
        email="maria@test.com",
        telefone="11987654321",
        cargo="veterinario",
        senha="senha123"
    )
except ValueError as e:
    print(f"Erro: {e}")
```

---

### 3. 📝 Logging Centralizado

**Registrar operações importantes:**
```python
from backend.logger import log_info, log_error, log_warning

# Operação bem-sucedida
log_info("Pet 'Rex' cadastrado com sucesso (ID: 42)")
# → Arquivo: logs/petvac_20250507.log
# → Saída: [2025-05-07 10:30:45] INFO - Pet 'Rex' cadastrado...

# Erro
try:
    resultado = funcao_critica()
except Exception as e:
    log_error("Erro ao processar vakchina", e)
    # → Com stack trace completo

# Aviso
if dados_suspeitos:
    log_warning("Dados com formato incomum detectados")
```

---

### 4. 🧰 Helpers Reutilizáveis

**Usar em pages e serviços:**
```python
from backend.utils import (
    tutor_label, pet_label, prepare_pets_with_tutors,
    get_dict_options, format_date
)

# Formatar tutor para exibição
label = tutor_label(df_tutores, id_tutor=1)
# → "João Silva (11987654321)"

# Formatar pet
label = pet_label(df_pets, id_pet=5)
# → "Rex - Cachorro"

# Preparar dados com merge automático
df_completo = prepare_pets_with_tutors(df_pets, df_tutores)
# → DataFrame com pet_nome, pet_especie, tutor_nome, tutor_telefone

# Criar opções para selectbox do Streamlit
opcoes = get_dict_options(df_tutores, "idTutor", "nome")
# → {"João Silva": 1, "Maria Santos": 2, ...}

# Formatar datas
data_formatada = format_date("2025-05-07", "%d/%m/%Y")
# → "07/05/2025"
```

---

### 5. 🏗️ Configurações Centralizadas

**Usar em vez de hardcode:**
```python
from backend.config import (
    CSV_FILES, EMAIL_REGEX, PHONE_REGEX,
    CARGOS, ESPECIES, VACINA_STATUS
)

# Acessar arquivo de pet
df_pets = pd.read_csv(CSV_FILES["pets"])

# Usar lista de cargos válidos
cargos_disponiveis = CARGOS  # ["recepcionista", "veterinario", "admin"]

# Usar lista de espécies
especies_validas = ESPECIES  # ["Cachorro", "Gato", ...]

# Usar status de vacina
status_possivel = VACINA_STATUS  # ["pendente", "aplicada", "concluída"]
```

---

### 6. 🔤 Enums para Type-Safety

**Em vez de strings mágicas:**
```python
from backend.enums import VacinaStatus, Cargo, Especie

# Antes (❌ String mágica)
if status == "pendente":
    fazer_algo()

# Depois (✅ Type-safe)
if status == VacinaStatus.PENDENTE:
    fazer_algo()

# Comparar status
status = VacinaStatus.APLICADA
print(status == VacinaStatus.APLICADA)  # True

# Iterar sobre valores
for cargo in Cargo:
    print(cargo.value)  # "recepcionista", "veterinario", "admin"
```

---

### 7. 📋 Type Hints em Services

**Todas funções têm tipos agora:**
```python
from backend.services import (
    cadastrar_pet, cadastrar_tutor,
    registrar_vacina, login_usuario
)
from typing import Tuple

# Função com type hints
resultado: str = cadastrar_pet(
    nome="Rex",
    especie="Cachorro",
    raca="Labrador",
    dataNascimento="2020-05-15",
    idTutor=1
)

# Função que retorna tupla
sucesso: bool
mensagem: str
sucesso, mensagem = login_usuario("admin", "senha123", "veterinario")
```

---

## 📂 Estrutura de Logs

```
logs/
├── petvac_20250507.log
├── petvac_20250508.log
└── petvac_20250509.log
```

Cada arquivo contém:
```
2025-05-07 10:30:45 - petvac - INFO - Pet 'Rex' cadastrado com sucesso (ID: 42)
2025-05-07 10:31:02 - petvac - ERROR - Erro ao atualizar pet: Email inválido
Traceback (most recent call last):
  File "backend/services.py", line 45, in cadastrar_tutor
    TutorValidator(nome=nome, email=email, telefone=telefone)
...
```

---

## ⚠️ Migrando Código Antigo

### Remover _append()
```python
# ❌ Antigo
df = df._append(novo_dado, ignore_index=True)

# ✅ Novo
novo_df = pd.DataFrame([novo_dado])
df = pd.concat([df, novo_df], ignore_index=True)
```

### Adicionar Validação
```python
# ❌ Antigo
def cadastrar(nome, email):
    # Sem validação
    salvar(nome, email)

# ✅ Novo
def cadastrar(nome, email):
    TutorValidator(nome=nome, email=email, telefone="1234567890")
    # Validado antes de salvar
    salvar(nome, email)
```

### Adicionar Logging
```python
# ❌ Antigo
def operacao():
    return "Sucesso"

# ✅ Novo
def operacao():
    try:
        resultado = fazer_algo()
        log_info(f"Operação concluída com sucesso: {resultado}")
        return resultado
    except Exception as e:
        log_error("Erro na operação", e)
        raise
```

---

## 🧪 Testar as Melhorias

```bash
# Executar testes
python test_improvements.py

# Saída esperada:
# ============================================================
# TESTANDO IMPORTAÇÕES
# ============================================================
# ✅ backend.config
# ✅ backend.security
# ... (todos os módulos)
# ============================================================
# ✅ TODOS OS TESTES PASSARAM
# ============================================================
```

---

## 🎯 Checklist de Integração

Para integrar as melhorias em um novo código:

- [ ] Importar `validators` e validar entrada
- [ ] Importar `security` se envolver senhas
- [ ] Importar `logger` e registrar operações importantes
- [ ] Importar `utils` para helpers reutilizáveis
- [ ] Importar `config` para valores centralizados
- [ ] Adicionar type hints em funções
- [ ] Usar enums em vez de strings mágicas
- [ ] Testar com `pytest` (próximo passo)

---

## 📖 Documentação Adicional

- **MELHORIAS.md**: Documentação técnica detalhada
- **RELATORIO_MELHORIAS.md**: Relatório completo com métricas
- **README.md**: Instruções de setup

---

## 💡 Exemplos Práticos

### Exemplo 1: Cadastrar Tutor com Validação e Logging

```python
from backend.services import cadastrar_tutor

resultado = cadastrar_tutor(
    nome="João Silva",
    telefone="11987654321",
    email="joao@example.com"
)
print(resultado)  # ✅ Tutor cadastrado com sucesso!
```

**O que acontece internamente:**
1. ✅ Validação com Pydantic
2. ✅ Log de sucesso em arquivo
3. ✅ Dados salvos com segurança
4. ✅ Mensagem com emoji para usuário

### Exemplo 2: Fazer Login com Bcrypt

```python
from backend.services import login_usuario

sucesso, mensagem = login_usuario(
    nome="admin",
    senha="minha_senha_secreta",
    cargo="veterinario"
)

if sucesso:
    print(mensagem)  # ✅ Login realizado! Bem-vindo(a), admin.
else:
    print(mensagem)  # ❌ Senha incorreta.
```

**Segurança:**
1. Senha comparada com bcrypt (hash)
2. Cada tentativa de login registrada
3. Falhas também registradas

### Exemplo 3: Usar Helpers em Página Streamlit

```python
import streamlit as st
from backend.utils import get_dict_options, tutor_label

# Carregar dados
df_tutores = carregar_dados("data/tutores.csv", COLUNAS["tutores"])

# Criar opções para selectbox
opcoes = get_dict_options(df_tutores, "idTutor", "nome")

# Usar no Streamlit
tutor_selecionado = st.selectbox("Escolha um tutor", options=opcoes)

# Exibir label formatado
if tutor_selecionado:
    label = tutor_label(df_tutores, tutor_selecionado)
    st.write(f"Tutor selecionado: {label}")
```

---

**Última atualização**: 7 de maio de 2026
