'use client'

import { useEffect, useState } from 'react'
import { vacinasService } from '@/services/vacinas'
import { dashboardService } from '@/services/dashboard'
import { notificacoesService } from '@/services/notificacoes'
import type { Vacina, DashboardMetrics } from '@/types'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Alert } from '@/components/ui/Alert'
import { PageSpinner } from '@/components/ui/Spinner'

export default function NotificacoesPage() {
  const [pendentes, setPendentes] = useState<Vacina[]>([])
  const [metrics,   setMetrics]   = useState<DashboardMetrics | null>(null)
  const [loading,   setLoading]   = useState(true)
  const [generating, setGenerating] = useState(false)
  const [error,   setError]   = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  async function load() {
    try {
      const [pend, m] = await Promise.all([vacinasService.pendentes(), dashboardService.metrics()])
      setPendentes(pend); setMetrics(m)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao carregar dados')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function gerarNotificacoes() {
    setGenerating(true); setError(null)
    try {
      const res = await notificacoesService.gerar()
      setSuccess(res.mensagem)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao gerar notificações')
    } finally {
      setGenerating(false)
    }
  }

  if (loading) return <PageSpinner />

  const atrasadas = pendentes.filter(v => v.atrasada)
  const futuras   = pendentes.filter(v => !v.atrasada)

  function diasAtraso(dataStr: string | null) {
    if (!dataStr) return 0
    return Math.floor((Date.now() - new Date(dataStr).getTime()) / 86400000)
  }

  function diasRestantes(dataStr: string | null) {
    if (!dataStr) return null
    return Math.ceil((new Date(dataStr).getTime() - Date.now()) / 86400000)
  }

  return (
    <div className="space-y-6">
      {error   && <Alert variant="error"   message={error}   onClose={() => setError(null)}   />}
      {success && <Alert variant="success" message={success} onClose={() => setSuccess(null)} />}

      {/* Stats + Ação */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Vacinas',  value: metrics?.total_vacinas  ?? 0, color: 'bg-blue-50' },
          { label: 'Pendentes',      value: metrics?.total_pendentes ?? 0, color: 'bg-yellow-50' },
          { label: 'Atrasadas',      value: metrics?.total_atrasadas ?? 0, color: 'bg-red-50' },
          { label: 'Em dia',         value: (metrics?.total_vacinas ?? 0) - (metrics?.total_pendentes ?? 0), color: 'bg-green-50' },
        ].map(s => (
          <div key={s.label} className={`${s.color} rounded-xl p-5 text-center border border-gray-100`}>
            <p className="text-2xl font-bold text-gray-800">{s.value}</p>
            <p className="text-sm text-gray-500">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="flex justify-end">
        <Button onClick={gerarNotificacoes} loading={generating} variant="outline">
          Gerar Notificações
        </Button>
      </div>

      {/* Atrasadas — crítico */}
      {atrasadas.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-red-200">
          <div className="px-6 py-4 border-b border-red-100 bg-red-50 rounded-t-xl flex items-center gap-2">
            <span className="text-lg">🚨</span>
            <h3 className="font-semibold text-red-800">Vacinas Atrasadas ({atrasadas.length})</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wide">
                  <th className="px-5 py-3">Pet ID</th>
                  <th className="px-5 py-3">Vacina</th>
                  <th className="px-5 py-3">Data Limite</th>
                  <th className="px-5 py-3">Atraso</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {atrasadas.map(v => (
                  <tr key={v.idVacina} className="hover:bg-red-50">
                    <td className="px-5 py-3 font-mono text-gray-400">#{v.idPet}</td>
                    <td className="px-5 py-3 font-medium">{v.nome}</td>
                    <td className="px-5 py-3 text-gray-600">{v.dataProximaDose || '—'}</td>
                    <td className="px-5 py-3">
                      <Badge variant="danger">{diasAtraso(v.dataProximaDose)} dias</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Pendentes futuras */}
      {futuras.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-100">
            <h3 className="font-semibold text-gray-800">Próximas Vacinações ({futuras.length})</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wide">
                  <th className="px-5 py-3">Pet ID</th>
                  <th className="px-5 py-3">Vacina</th>
                  <th className="px-5 py-3">Data</th>
                  <th className="px-5 py-3">Prazo</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {futuras.slice(0, 10).map(v => {
                  const dias = diasRestantes(v.dataProximaDose)
                  const variant = dias !== null && dias <= 3 ? 'danger' : dias !== null && dias <= 7 ? 'warning' : 'success'
                  return (
                    <tr key={v.idVacina} className="hover:bg-gray-50">
                      <td className="px-5 py-3 font-mono text-gray-400">#{v.idPet}</td>
                      <td className="px-5 py-3 font-medium">{v.nome}</td>
                      <td className="px-5 py-3 text-gray-600">{v.dataProximaDose || '—'}</td>
                      <td className="px-5 py-3">
                        {dias !== null
                          ? <Badge variant={variant}>{dias === 0 ? 'Hoje' : `${dias} dias`}</Badge>
                          : <span className="text-gray-400">—</span>
                        }
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {pendentes.length === 0 && (
        <div className="bg-white rounded-xl p-10 text-center shadow-sm border border-gray-100">
          <div className="text-4xl mb-2">✅</div>
          <p className="font-medium text-gray-800">Todos os pets estão em dia com a vacinação!</p>
        </div>
      )}
    </div>
  )
}
