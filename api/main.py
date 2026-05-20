from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, pets, tutores, vacinas, notificacoes, dashboard

app = FastAPI(
    title="PetVac API",
    description="API REST do sistema de gerenciamento de vacinação de pets",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,          prefix="/auth",          tags=["Autenticação"])
app.include_router(pets.router,          prefix="/pets",          tags=["Pets"])
app.include_router(tutores.router,       prefix="/tutores",       tags=["Tutores"])
app.include_router(vacinas.router,       prefix="/vacinas",       tags=["Vacinas"])
app.include_router(notificacoes.router,  prefix="/notificacoes",  tags=["Notificações"])
app.include_router(dashboard.router,     prefix="/dashboard",     tags=["Dashboard"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "PetVac API", "version": "1.0.0"}
