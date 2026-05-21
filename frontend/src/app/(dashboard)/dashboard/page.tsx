'use client'

import { useEffect, useState } from 'react'
import { dashboardService } from '@/services/dashboard'
import { vacinasService } from '@/services/vacinas'
import type { DashboardMetrics, Vacina } from '@/types'
import { Badge, statusBadge } from '@/components/ui/Badge'
import { Alert } from '@/components/ui/Alert'
import { PageSpinner } from '@/components/ui/Spinner'

function MetricCard({ label, value, icon, accent }: { label: string; value: number; icon: string; accent: string }) {
  return (
    <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 flex items-center gap-4">
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl ${accent}`}>
        {icon}
      </div>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const [metrics, setMetrics]   = useState<DashboardMetrics | null>(null)
  const [pendentes, setPendentes] = useState<Vacina[]>([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState<string | null>(null)

  useEffect(() => {
    Promise.all([dashboardService.metrics(), vacinasService.pendentes()])
      .then(([m, p]) => { setMetrics(m); setPendentes(p) })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <PageSpinner />

  return (
    <div className="space-y-6">
      {error && <Alert variant="error" message={error} onClose={() => setError(null)} />}

      {metrics && metrics.total_atrasadas > 0 && (
        <Alert variant="warning" message={`Atenção: ${metrics.total_atrasadas} vacina(s) atrasada(s) requerem ação imediata.`} />
      )}

      {/* Métricas */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="Tutores"   value={metrics?.total_tutores  ?? 0} icon="👤" accent="bg-orange-50" />
        <MetricCard label="Pets"      value={metrics?.total_pets     ?? 0} icon="🐶" accent="bg-green-50" />
        <MetricCard label="Vacinas"   value={metrics?.total_vacinas  ?? 0} icon="💉" accent="bg-purple-50" />
        <MetricCard
          label="Pendentes"
          value={metrics?.total_pendentes ?? 0}
          icon="⏳"
          accent={(metrics?.total_atrasadas ?? 0) > 0 ? 'bg-red-50' : 'bg-yellow-50'}
        />
      </div>

      {/* Vacinas Pendentes */}
      {pendentes.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-100">
            <h3 className="font-semibold text-gray-800">Vacinas Pendentes</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 text-left text-gray-500 text-xs uppercase tracking-wide">
                  <th className="px-6 py-3">ID Pet</th>
                  <th className="px-6 py-3">Vacina</th>
                  <th className="px-6 py-3">Próxima Dose</th>
                  <th className="px-6 py-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {pendentes.slice(0, 8).map(v => {
                  const badge = statusBadge(v.status, v.atrasada)
                  return (
                    <tr key={v.idVacina} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-3 font-mono text-gray-500">#{v.idPet}</td>
                      <td className="px-6 py-3 font-medium">{v.nome}</td>
                      <td className="px-6 py-3 text-gray-600">{v.dataProximaDose || '—'}</td>
                      <td className="px-6 py-3">
                        <Badge variant={badge.variant}>{badge.label}</Badge>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
            {pendentes.length > 8 && (
              <p className="text-center text-sm text-gray-400 py-3">
                +{pendentes.length - 8} vacinas pendentes — acesse a seção Vacinas para ver todas.
              </p>
            )}
          </div>
        </div>
      )}

      {pendentes.length === 0 && !loading && (
        <div className="bg-white rounded-xl p-8 text-center shadow-sm border border-gray-100">
          <div className="text-4xl mb-2">✅</div>
          <p className="font-medium text-gray-800">Todos os pets estão em dia com a vacinação!</p>
        </div>
      )}
    </div>
  )
}
