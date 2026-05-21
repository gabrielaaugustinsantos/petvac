'use client'

import { useEffect, useState } from 'react'
import { vacinasService } from '@/services/vacinas'
import { petsService } from '@/services/pets'
import { tutoresService } from '@/services/tutores'
import type { Vacina, Pet, Tutor } from '@/types'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Badge, statusBadge } from '@/components/ui/Badge'
import { Alert } from '@/components/ui/Alert'
import { PageSpinner } from '@/components/ui/Spinner'

export default function VacinasPage() {
  const [pendentes, setPendentes] = useState<Vacina[]>([])
  const [pets,    setPets]    = useState<Pet[]>([])
  const [tutores, setTutores] = useState<Tutor[]>([])
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  // Form: registrar
  const [regForm, setRegForm] = useState({
    idPet: '',
    nome: '',
    dataAplicacao: '',
    dataProximaDose: '',
    jaAplicada: false,
  })

  // Form: aplicar dose
  const [apForm, setApForm] = useState({
    idVacina: '',
    dataAplicacao: new Date().toISOString().split('T')[0],
    dataProximaDose: '',
  })

  const [savingReg, setSavingReg] = useState(false)
  const [savingAp,  setSavingAp]  = useState(false)

  async function load() {
    try {
      const [p, t, pend] = await Promise.all([petsService.listar(), tutoresService.listar(), vacinasService.pendentes()])
      setPets(p); setTutores(t); setPendentes(pend)
      if (p.length > 0) setRegForm(f => ({ ...f, idPet: String(p[0].idPet) }))
      if (pend.length > 0) setApForm(f => ({ ...f, idVacina: String(pend[0].idVacina) }))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao carregar dados')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function nomePetComTutor(idPet: number) {
    const pet = pets.find(p => p.idPet === idPet)
    if (!pet) return `Pet #${idPet}`
    const tutor = tutores.find(t => t.idTutor === pet.idTutor)
    return `${pet.nome} (${pet.especie}) — ${tutor?.nome ?? 'sem tutor'}`
  }

  async function handleRegistrar(e: React.FormEvent) {
    e.preventDefault()
    setSavingReg(true); setError(null)
    try {
      const res = await vacinasService.registrar({
        idPet: Number(regForm.idPet),
        nome: regForm.nome,
        dataAplicacao: regForm.jaAplicada && regForm.dataAplicacao ? regForm.dataAplicacao : null,
        dataProximaDose: regForm.dataProximaDose || null,
      })
      setSuccess(res.mensagem)
      setRegForm(f => ({ ...f, nome: '', dataAplicacao: '', dataProximaDose: '', jaAplicada: false }))
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao registrar vacina')
    } finally {
      setSavingReg(false)
    }
  }

  async function handleAplicar(e: React.FormEvent) {
    e.preventDefault()
    setSavingAp(true); setError(null)
    try {
      const res = await vacinasService.aplicar(Number(apForm.idVacina), {
        dataAplicacao: apForm.dataAplicacao,
        dataProximaDose: apForm.dataProximaDose || null,
      })
      setSuccess(res.mensagem)
      setApForm(f => ({ ...f, dataProximaDose: '' }))
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao aplicar dose')
    } finally {
      setSavingAp(false)
    }
  }

  if (loading) return <PageSpinner />

  const petOptions     = pets.map(p => ({ value: p.idPet, label: nomePetComTutor(p.idPet) }))
  const vacinaOptions  = pendentes.map(v => ({ value: v.idVacina, label: `#${v.idVacina} – ${v.nome} (Pet ${v.idPet})` }))

  return (
    <div className="space-y-6">
      {error   && <Alert variant="error"   message={error}   onClose={() => setError(null)}   />}
      {success && <Alert variant="success" message={success} onClose={() => setSuccess(null)} />}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Registrar Vacina */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-gray-800 mb-4">Registrar Vacina</h3>
          {pets.length === 0 ? (
            <Alert variant="warning" message="Cadastre pets antes de registrar vacinas." />
          ) : (
            <form onSubmit={handleRegistrar} className="space-y-4">
              <Select label="Pet" options={petOptions} value={regForm.idPet} onChange={e => setRegForm(f => ({ ...f, idPet: e.target.value }))} />
              <Input label="Nome da vacina" placeholder="Ex: Raiva, Polivalente..." value={regForm.nome} onChange={e => setRegForm(f => ({ ...f, nome: e.target.value }))} required />

              <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                <input
                  type="checkbox"
                  checked={regForm.jaAplicada}
                  onChange={e => setRegForm(f => ({ ...f, jaAplicada: e.target.checked }))}
                  className="rounded border-gray-300"
                />
                Vacina já foi aplicada
              </label>

              {regForm.jaAplicada && (
                <Input label="Data de aplicação" type="date" value={regForm.dataAplicacao} onChange={e => setRegForm(f => ({ ...f, dataAplicacao: e.target.value }))} />
              )}

              <Input label="Próxima dose (opcional)" type="date" value={regForm.dataProximaDose} onChange={e => setRegForm(f => ({ ...f, dataProximaDose: e.target.value }))} />

              <Button type="submit" className="w-full" loading={savingReg}>Registrar</Button>
            </form>
          )}
        </div>

        {/* Aplicar Dose */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-gray-800 mb-4">Aplicar Dose Pendente</h3>
          {pendentes.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <div className="text-3xl mb-2">✅</div>
              <p className="text-sm">Nenhuma vacina pendente.</p>
            </div>
          ) : (
            <form onSubmit={handleAplicar} className="space-y-4">
              <Select label="Vacina pendente" options={vacinaOptions} value={apForm.idVacina} onChange={e => setApForm(f => ({ ...f, idVacina: e.target.value }))} />
              <Input label="Data de aplicação" type="date" value={apForm.dataAplicacao} onChange={e => setApForm(f => ({ ...f, dataAplicacao: e.target.value }))} required />
              <Input label="Próxima dose (opcional)" type="date" value={apForm.dataProximaDose} onChange={e => setApForm(f => ({ ...f, dataProximaDose: e.target.value }))} />
              <Button type="submit" className="w-full" loading={savingAp}>Aplicar Dose</Button>
            </form>
          )}
        </div>
      </div>

      {/* Tabela de Pendentes */}
      {pendentes.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-100">
            <h3 className="font-semibold text-gray-800">Vacinas Pendentes ({pendentes.length})</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wide">
                  <th className="px-5 py-3">ID</th>
                  <th className="px-5 py-3">Pet</th>
                  <th className="px-5 py-3">Vacina</th>
                  <th className="px-5 py-3">Próxima Dose</th>
                  <th className="px-5 py-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {pendentes.map(v => {
                  const badge = statusBadge(v.status, v.atrasada)
                  return (
                    <tr key={v.idVacina} className="hover:bg-gray-50">
                      <td className="px-5 py-3 font-mono text-gray-400">#{v.idVacina}</td>
                      <td className="px-5 py-3">{nomePetComTutor(v.idPet)}</td>
                      <td className="px-5 py-3 font-medium">{v.nome}</td>
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
    </div>
  )
}
