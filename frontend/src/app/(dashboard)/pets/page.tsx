'use client'

import { useEffect, useState } from 'react'
import { petsService, type PetCreate } from '@/services/pets'
import { tutoresService } from '@/services/tutores'
import type { Pet, Tutor } from '@/types'
import { ESPECIES } from '@/types'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Modal } from '@/components/ui/Modal'
import { Alert } from '@/components/ui/Alert'
import { PageSpinner } from '@/components/ui/Spinner'

const empty: PetCreate = { nome: '', especie: 'Cachorro', raca: '', dataNascimento: '', idTutor: 0 }

export default function PetsPage() {
  const [pets,    setPets]    = useState<Pet[]>([])
  const [tutores, setTutores] = useState<Tutor[]>([])
  const [loading, setLoading] = useState(true)
  const [saving,  setSaving]  = useState(false)
  const [error,   setError]   = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const [modal,  setModal]  = useState<'novo' | 'editar' | null>(null)
  const [form,   setForm]   = useState<PetCreate>(empty)
  const [editId, setEditId] = useState<number | null>(null)

  async function load() {
    try {
      const [p, t] = await Promise.all([petsService.listar(), tutoresService.listar()])
      setPets(p)
      setTutores(t)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao carregar dados')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function nomeTutor(id: number) {
    return tutores.find(t => t.idTutor === id)?.nome ?? `#${id}`
  }

  function openNovo() {
    setForm({ ...empty, idTutor: tutores[0]?.idTutor ?? 0 })
    setModal('novo')
  }

  function openEditar(p: Pet) {
    setForm({ nome: p.nome, especie: p.especie, raca: p.raca, dataNascimento: p.dataNascimento, idTutor: p.idTutor })
    setEditId(p.idPet)
    setModal('editar')
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      const res = modal === 'novo'
        ? await petsService.cadastrar(form)
        : await petsService.atualizar(editId!, form)
      setSuccess(res.mensagem)
      setModal(null)
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao salvar')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <PageSpinner />

  const especieOptions = ESPECIES.map(e => ({ value: e, label: e }))
  const tutorOptions   = tutores.map(t => ({ value: t.idTutor, label: `${t.nome} (${t.telefone})` }))

  return (
    <div className="space-y-4">
      {error   && <Alert variant="error"   message={error}   onClose={() => setError(null)}   />}
      {success && <Alert variant="success" message={success} onClose={() => setSuccess(null)} />}

      {tutores.length === 0 && (
        <Alert variant="warning" message="Cadastre um tutor antes de registrar pets." />
      )}

      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-500">{pets.length} pet(s) cadastrado(s)</p>
        <Button onClick={openNovo} disabled={tutores.length === 0}>+ Novo Pet</Button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        {pets.length === 0 ? (
          <div className="p-10 text-center text-gray-400">
            <div className="text-4xl mb-2">🐶</div>
            <p>Nenhum pet cadastrado ainda.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wide">
                  <th className="px-5 py-3">ID</th>
                  <th className="px-5 py-3">Nome</th>
                  <th className="px-5 py-3">Espécie</th>
                  <th className="px-5 py-3">Raça</th>
                  <th className="px-5 py-3">Nascimento</th>
                  <th className="px-5 py-3">Tutor</th>
                  <th className="px-5 py-3" />
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {pets.map(p => (
                  <tr key={p.idPet} className="hover:bg-gray-50 transition-colors">
                    <td className="px-5 py-3 font-mono text-gray-400">#{p.idPet}</td>
                    <td className="px-5 py-3 font-medium">{p.nome}</td>
                    <td className="px-5 py-3">{p.especie}</td>
                    <td className="px-5 py-3 text-gray-600">{p.raca}</td>
                    <td className="px-5 py-3 text-gray-600">{p.dataNascimento}</td>
                    <td className="px-5 py-3 text-gray-600">{nomeTutor(p.idTutor)}</td>
                    <td className="px-5 py-3">
                      <Button variant="ghost" size="sm" onClick={() => openEditar(p)}>Editar</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal open={modal !== null} title={modal === 'novo' ? 'Novo Pet' : 'Editar Pet'} onClose={() => setModal(null)}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Nome do pet" value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} required />
          <Select label="Espécie" options={especieOptions} value={form.especie} onChange={e => setForm(f => ({ ...f, especie: e.target.value }))} />
          <Input label="Raça" value={form.raca} onChange={e => setForm(f => ({ ...f, raca: e.target.value }))} required />
          <Input label="Data de nascimento" type="date" value={form.dataNascimento} onChange={e => setForm(f => ({ ...f, dataNascimento: e.target.value }))} required />
          <Select
            label="Tutor"
            options={tutorOptions}
            value={form.idTutor}
            onChange={e => setForm(f => ({ ...f, idTutor: Number(e.target.value) }))}
          />
          <div className="flex gap-3 pt-2">
            <Button type="button" variant="secondary" className="flex-1" onClick={() => setModal(null)}>Cancelar</Button>
            <Button type="submit" className="flex-1" loading={saving}>
              {modal === 'novo' ? 'Cadastrar' : 'Salvar'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
