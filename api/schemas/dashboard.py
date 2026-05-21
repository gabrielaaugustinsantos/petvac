from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_tutores: int
    total_pets: int
    total_vacinas: int
    total_pendentes: int
    total_atrasadas: int
