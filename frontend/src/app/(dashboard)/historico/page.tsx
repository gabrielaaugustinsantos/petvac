'use client'

import { useEffect, useState } from 'react'
import { vacinasService } from '@/services/vacinas'
import { petsService } from '@/services/pets'
import { tutoresService } from '@/services/tutores'
import type { Vacina, Pet, Tutor } from '@/types'
import { Button } from '@/components/ui/Button'
import { Select } from '@/components/ui/Select'
import { Badge, statusBadge } from '@/components/ui/Badge'
import { Alert } from '@/components/ui/Alert'
import { PageSpinner } from '@/components/ui/Spinner'

export default function HistoricoPage() {
  const [pets,      setPets]      = useState<Pet[]>([])
  const [tutores,   setTutores]   = useState<Tutor[]>([])
  const [historico, setHistorico] = useState<Vacina[] | null>(null)
  const [loading,   setLoading]   = useState(true)
  const [searching, setSearching] = useState(false)
  const [error,     setError]     = useState<string | null>(null)
  const [selectedPet, setSelectedPet] = useState<string>('')

  useEffect(() => {
    Promise.all([petsService.listar(), tutoresService.listar()])
      .then(([p, t]) => {
        setPets(p); setTutores(t)
        if (p.length > 0) setSelectedPet(String(p[0].idPet))
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  function nomeTutor(idTutor: number) {
    return tutores.find(t => t.idTutor === idTutor)?.nome ?? '—'
  }

  async function consultar() {
    if (!selectedPet) return
    setSearching(true); setError(null)
    try {
      setHistorico(await vacinasService.historico(Number(selectedPet)))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao consultar histórico')
    } finally {
      setSearching(false)
    }
  }

  if (loading) return <PageSpinner />

  const petOptions = pets.map(p => ({
    value: p.idPet,
    label: `${p.nome} (${p.especie}) — Tutor: ${nomeTutor(p.idTutor)}`,
  }))

  const hoje = new Date()
  const proximasDoses = historico?.filter(v =>
    v.dataProximaDose &&
    new Date(v.dataProximaDose) > hoje &&
    v.status !== 'aplicada' &&
    v.status !== 'concluída'
  ) ?? []

  const stats = historico ? {
    total:    historico.length,
    aplicadas: historico.filter(v => v.status === 'aplicada' || v.status === 'concluída').length,
    pendentes: historico.filter(v => v.status === 'pendente').length,
  } : null

  return (
    <div className="space-y-6">
      {error && <Alert variant="error" message={error} onClose={() => setError(null)} />}

      {pets.length === 0 ? (
        <Alert variant="info" message="Nenhum pet cadastrado. Cadastre pets para consultar o histórico." />
      ) : (
        <>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 className="font-semibold text-gray-800 mb-4">Selecione um Pet</h3>
            <div className="flex gap-3">
              <div className="flex-1">
                <Select
                  options={petOptions}
                  value={selectedPet}
                  onChange={e => { setSelectedPet(e.target.value); setHistorico(null) }}
                />
              </div>
              <Button onClick={consultar} loading={searching}>Consultar</Button>
            </div>
          </div>

          {historico !== null && (
            <>
              {/* Stats */}
              {stats && (
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { label: 'Total', value: stats.total, color: 'text-gray-800' },
                    { label: 'Aplicadas', value: stats.aplicadas, color: 'text-green-600' },
                    { label: 'Pendentes', value: stats.pendentes, color: 'text-yellow-600' },
                  ].map(s => (
                    <div key={s.label} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 text-center">
                      <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                      <p className="text-sm text-gray-500">{s.label}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Histórico completo */}
              {historico.length === 0 ? (
                <div className="bg-white rounded-xl p-8 text-center shadow-sm border border-gray-100 text-gray-400">
                  <div className="text-4xl mb-2">📋</div>
                  <p>Nenhum registro de vacina para este pet.</p>
                </div>
              ) : (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100">
                  <div className="px-6 py-4 border-b border-gray-100">
                    <h3 className="font-semibold text-gray-800">Todas as Vacinações</h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wide">
                          <th className="px-5 py-3">ID</th>
                          <th className="px-5 py-3">Vacina</th>
                          <th className="px-5 py-3">Aplicada em</th>
                          <th className="px-5 py-3">Próxima Dose</th>
                          <th className="px-5 py-3">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {historico.map(v => {
                          const badge = statusBadge(v.status, v.atrasada)
                          return (
                            <tr key={v.idVacina} className="hover:bg-gray-50">
                              <td className="px-5 py-3 font-mono text-gray-400">#{v.idVacina}</td>
                              <td className="px-5 py-3 font-medium">{v.nome}</td>
                              <td className="px-5 py-3 text-gray-600">{v.dataAplicacao || '—'}</td>
                              <td className="px-5 py-3 text-gray-600">{v.dataProximaDose || '—'}</td>
                              <td className="px-5 py-3"><Badge variant={badge.variant}>{badge.label}</Badge></td>
                            </tr>
                          )
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Próximas doses */}
              {proximasDoses.length > 0 && (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100">
                  <div className="px-6 py-4 border-b border-green-100 bg-green-50 rounded-t-xl">
                    <h3 className="font-semibold text-green-800">Próximas Doses Agendadas</h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wide">
                          <th className="px-5 py-3">Vacina</th>
                          <th className="px-5 py-3">Data</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {proximasDoses.map(v => (
                          <tr key={v.idVacina} className="hover:bg-gray-50">
                            <td className="px-5 py-3 font-medium">{v.nome}</td>
                            <td className="px-5 py-3 text-gray-600">{v.dataProximaDose}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          )}
        </>
      )}
    </div>
  )
}
