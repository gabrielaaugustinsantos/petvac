import { api } from '@/lib/api'
import type { DashboardMetrics } from '@/types'

export const dashboardService = {
  metrics: () => api.get<DashboardMetrics>('/dashboard/'),
}
