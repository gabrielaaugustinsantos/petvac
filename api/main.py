"""
Ponto de entrada da API REST PetVac.
Registra todos os routers e configura middleware.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import ALLOWED_ORIGINS
from api.routes import auth, pets, tutores, vacinas, notificacoes, dashboard

app = FastAPI(
    title="PetVac API",
    description=(
        "API REST do sistema de gerenciamento de vacinação de pets. "
        "Conecta clínicas veterinárias e tutores em uma plataforma digital "
        "para controle de vacinas, histórico clínico e notificações."
    ),
    version="1.1.0",
    contact={"name": "Equipe PetVac"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router,          prefix="/auth",          tags=["Autenticação"])
app.include_router(pets.router,          prefix="/pets",          tags=["Pets"])
app.include_router(tutores.router,       prefix="/tutores",       tags=["Tutores"])
app.include_router(vacinas.router,       prefix="/vacinas",       tags=["Vacinas"])
app.include_router(notificacoes.router,  prefix="/notificacoes",  tags=["Notificações"])
app.include_router(dashboard.router,     prefix="/dashboard",     tags=["Dashboard"])


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="Status da API")
def health_check():
    """Verifica se a API está online."""
    return {"status": "ok", "app": "PetVac API", "version": "1.1.0"}
