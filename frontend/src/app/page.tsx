'use client'

import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { authService } from '@/services/auth'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Alert } from '@/components/ui/Alert'
import { CARGOS } from '@/types'

type Tab = 'login' | 'cadastro'

export default function LoginPage() {
  const { login } = useAuth()

  const [tab, setTab] = useState<Tab>('login')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const [loginForm, setLoginForm] = useState({ nome: '', senha: '', cargo: 'recepcionista' })
  const [cadForm,   setCadForm]   = useState({ nome: '', senha: '', cargo: 'recepcionista' })

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const data = await authService.login(loginForm)
      login(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao fazer login')
    } finally {
      setLoading(false)
    }
  }

  async function handleCadastro(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setLoading(true)
    try {
      const res = await authService.register(cadForm)
      setSuccess(res.mensagem + ' Faça o login para entrar.')
      setCadForm({ nome: '', senha: '', cargo: 'recepcionista' })
      setTab('login')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao cadastrar')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-light to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-3">🐾</div>
          <h1 className="text-3xl font-bold text-primary">PetVac</h1>
          <p className="text-gray-500 mt-1">Sistema de Gerenciamento de Vacinação</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Tabs */}
          <div className="flex border-b border-gray-200 mb-6">
            {(['login', 'cadastro'] as Tab[]).map(t => (
              <button
                key={t}
                onClick={() => { setTab(t); setError(null); setSuccess(null) }}
                className={`flex-1 py-2.5 text-sm font-medium transition-colors capitalize
                  ${tab === t
                    ? 'border-b-2 border-primary text-primary'
                    : 'text-gray-500 hover:text-gray-700'}`}
              >
                {t === 'login' ? 'Entrar' : 'Criar conta'}
              </button>
            ))}
          </div>

          {error   && <div className="mb-4"><Alert variant="error"   message={error}   onClose={() => setError(null)}   /></div>}
          {success && <div className="mb-4"><Alert variant="success" message={success} onClose={() => setSuccess(null)} /></div>}

          {tab === 'login' ? (
            <form onSubmit={handleLogin} className="space-y-4">
              <Input
                label="Nome completo"
                placeholder="Seu nome..."
                value={loginForm.nome}
                onChange={e => setLoginForm(f => ({ ...f, nome: e.target.value }))}
                required
              />
              <Input
                label="Senha"
                type="password"
                placeholder="Sua senha..."
                value={loginForm.senha}
                onChange={e => setLoginForm(f => ({ ...f, senha: e.target.value }))}
                required
              />
              <Select
                label="Cargo"
                options={CARGOS}
                value={loginForm.cargo}
                onChange={e => setLoginForm(f => ({ ...f, cargo: e.target.value }))}
              />
              <Button type="submit" className="w-full mt-2" loading={loading} size="lg">
                Entrar
              </Button>
            </form>
          ) : (
            <form onSubmit={handleCadastro} className="space-y-4">
              <Input
                label="Nome completo"
                placeholder="Seu nome..."
                value={cadForm.nome}
                onChange={e => setCadForm(f => ({ ...f, nome: e.target.value }))}
                required
              />
              <Input
                label="Senha"
                type="password"
                placeholder="Escolha uma senha..."
                value={cadForm.senha}
                onChange={e => setCadForm(f => ({ ...f, senha: e.target.value }))}
                required
              />
              <Select
                label="Cargo"
                options={CARGOS}
                value={cadForm.cargo}
                onChange={e => setCadForm(f => ({ ...f, cargo: e.target.value }))}
              />
              <Button type="submit" className="w-full mt-2" loading={loading} size="lg">
                Criar conta
              </Button>
            </form>
          )}
        </div>

        <p className="text-center text-xs text-gray-400 mt-6">
          Senhas protegidas com bcrypt · PetVac v1.0
        </p>
      </div>
    </div>
  )
}
