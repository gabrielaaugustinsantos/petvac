'use client'

import { useEffect, useState } from 'react'
import { tutoresService, type TutorCreate } from '@/services/tutores'
import type { Tutor } from '@/types'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Modal } from '@/components/ui/Modal'
import { Alert } from '@/components/ui/Alert'
import { PageSpinner } from '@/components/ui/Spinner'

const empty: TutorCreate = { nome: '', telefone: '', email: '', endereco: '' }

export default function TutoresPage() {
  const [tutores, setTutores]   = useState<Tutor[]>([])
  const [loading, setLoading]   = useState(true)
  const [saving,  setSaving]    = useState(false)
  const [error,   setError]     = useState<string | null>(null)
  const [success, setSuccess]   = useState<string | null>(null)

  const [modal, setModal]   = useState<'novo' | 'editar' | null>(null)
  const [form,  setForm]    = useState<TutorCreate>(empty)
  const [editId, setEditId] = useState<number | null>(null)

  async function load() {
    try {
      setTutores(await tutoresService.listar())
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao carregar tutores')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function openNovo() { setForm(empty); setModal('novo') }

  function openEditar(t: Tutor) {
    setForm({ nome: t.nome, telefone: t.telefone, email: t.email, endereco: t.endereco })
    setEditId(t.idTutor)
    setModal('editar')
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      const res = modal === 'novo'
        ? await tutoresService.cadastrar(form)
        : await tutoresService.atualizar(editId!, form)
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

  return (
    <div className="space-y-4">
      {error   && <Alert variant="error"   message={error}   onClose={() => setError(null)}   />}
      {success && <Alert variant="success" message={success} onClose={() => setSuccess(null)} />}

      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-500">{tutores.length} tutor(es) cadastrado(s)</p>
        <Button onClick={openNovo}>+ Novo Tutor</Button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        {tutores.length === 0 ? (
          <div className="p-10 text-center text-gray-400">
            <div className="text-4xl mb-2">👤</div>
            <p>Nenhum tutor cadastrado ainda.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wide">
                  <th className="px-5 py-3">ID</th>
                  <th className="px-5 py-3">Nome</th>
                  <th className="px-5 py-3">Telefone</th>
                  <th className="px-5 py-3">E-mail</th>
                  <th className="px-5 py-3">Endereço</th>
                  <th className="px-5 py-3" />
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {tutores.map(t => (
                  <tr key={t.idTutor} className="hover:bg-gray-50 transition-colors">
                    <td className="px-5 py-3 font-mono text-gray-400">#{t.idTutor}</td>
                    <td className="px-5 py-3 font-medium">{t.nome}</td>
                    <td className="px-5 py-3 text-gray-600">{t.telefone}</td>
                    <td className="px-5 py-3 text-gray-600">{t.email}</td>
                    <td className="px-5 py-3 text-gray-600 truncate max-w-[160px]">{t.endereco || '—'}</td>
                    <td className="px-5 py-3">
                      <Button variant="ghost" size="sm" onClick={() => openEditar(t)}>Editar</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal
        open={modal !== null}
        title={modal === 'novo' ? 'Novo Tutor' : 'Editar Tutor'}
        onClose={() => setModal(null)}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Nome completo" value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} required />
          <Input label="Telefone" placeholder="11999999999" value={form.telefone} onChange={e => setForm(f => ({ ...f, telefone: e.target.value }))} required />
          <Input label="E-mail" type="email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} required />
          <Input label="Endereço (opcional)" value={form.endereco} onChange={e => setForm(f => ({ ...f, endereco: e.target.value }))} />
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
