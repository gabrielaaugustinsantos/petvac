from fastapi import APIRouter, Depends

from api.schemas import DashboardMetrics
from api.deps import get_current_user
from backend.database import carregar_dados, COLUNAS
import backend.services as services

router = APIRouter()


@router.get(
    "/",
    response_model=DashboardMetrics,
    summary="Métricas do dashboard",
    description="Retorna contagens consolidadas de tutores, pets, vacinas e alertas.",
)
def get_dashboard(_user: dict = Depends(get_current_user)):
    pets_df    = services.listar_pets()
    tutores_df = services.listar_tutores()
    vacinas_df = carregar_dados("data/vacinas.csv", COLUNAS["vacinas"])
    pendentes_df = services.consultar_vacinas_pendentes()

    total_atrasadas = 0
    if not pendentes_df.empty and "atrasada" in pendentes_df.columns:
        total_atrasadas = int(pendentes_df["atrasada"].sum())

    return DashboardMetrics(
        total_tutores=len(tutores_df),
        total_pets=len(pets_df),
        total_vacinas=len(vacinas_df),
        total_pendentes=len(pendentes_df) if not pendentes_df.empty else 0,
        total_atrasadas=total_atrasadas,
    )
