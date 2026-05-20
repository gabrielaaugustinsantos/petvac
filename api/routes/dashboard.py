from fastapi import APIRouter, Depends
from api.schemas import DashboardMetrics
from api.deps import get_current_user
import backend.services as services
import pandas as pd

router = APIRouter()


@router.get("/", response_model=DashboardMetrics)
def get_dashboard(_user: dict = Depends(get_current_user)):
    pets_df = services.listar_pets()
    tutores_df = services.listar_tutores()
    pendentes_df = services.consultar_vacinas_pendentes()

    total_pets = len(pets_df)
    total_tutores = len(tutores_df)

    if pendentes_df.empty:
        total_pendentes = 0
        total_atrasadas = 0
        total_vacinas = total_pets  # fallback
    else:
        total_pendentes = len(pendentes_df)
        total_atrasadas = int(pendentes_df["atrasada"].sum()) if "atrasada" in pendentes_df.columns else 0
        total_vacinas = total_pendentes  # serviço atual só expõe pendentes; expandir se necessário

    from backend.database import carregar_dados, COLUNAS
    vacinas_df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
    total_vacinas = len(vacinas_df)

    return DashboardMetrics(
        total_tutores=total_tutores,
        total_pets=total_pets,
        total_vacinas=total_vacinas,
        total_pendentes=total_pendentes,
        total_atrasadas=total_atrasadas,
    )
