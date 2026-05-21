'use client'

import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { authService } from '@/services/auth'
import { Alert } from '@/components/ui/Alert'
import { TIPO_USUARIO } from '@/types'

type Tab = 'login' | 'cadastro' | 'reset'

export default function LoginPage() {
  const { login } = useAuth()

  const [tab,     setTab]     = useState<Tab>('login')
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const [loginForm, setLoginForm] = useState({ email: '', senha: '' })
  const [cadForm,   setCadForm]   = useState({ nome: '', email: '', senha: '', confirmarSenha: '', cargo: 'recepcionista' })
  const [resetForm, setResetForm] = useState({ email: '', nova_senha: '', confirmarSenha: '' })

  function changeTab(t: Tab) { setTab(t); setError(null); setSuccess(null) }

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault(); setError(null); setLoading(true)
    try {
      login(await authService.login({ email: loginForm.email, senha: loginForm.senha }))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'E-mail ou senha incorretos.')
    } finally { setLoading(false) }
  }

  async function handleCadastro(e: React.FormEvent) {
    e.preventDefault(); setError(null); setSuccess(null)
    if (cadForm.senha !== cadForm.confirmarSenha) { setError('As senhas não coincidem.'); return }
    if (cadForm.senha.length < 6)                 { setError('Mínimo de 6 caracteres.'); return }
    setLoading(true)
    try {
      const res = await authService.register({ nome: cadForm.nome, email: cadForm.email, senha: cadForm.senha, cargo: cadForm.cargo })
      setSuccess(res.mensagem + ' Faça o login para entrar.')
      setCadForm({ nome: '', email: '', senha: '', confirmarSenha: '', cargo: 'recepcionista' })
      changeTab('login')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar conta.')
    } finally { setLoading(false) }
  }

  async function handleReset(e: React.FormEvent) {
    e.preventDefault(); setError(null); setSuccess(null)
    if (resetForm.nova_senha !== resetForm.confirmarSenha) { setError('As senhas não coincidem.'); return }
    if (resetForm.nova_senha.length < 6)                   { setError('Mínimo de 6 caracteres.'); return }
    setLoading(true)
    try {
      const res = await authService.redefinirSenha({ email: resetForm.email, nova_senha: resetForm.nova_senha })
      setSuccess(res.mensagem)
      setResetForm({ email: '', nova_senha: '', confirmarSenha: '' })
      changeTab('login')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao redefinir senha.')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen flex">

      {/* ── Painel esquerdo — laranja ── */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-400 via-primary to-primary-dark
                      flex-col items-center justify-center p-12 text-white relative overflow-hidden">
        <div className="relative z-10 text-center">
          <div className="text-8xl mb-6">🐾</div>
          <h1 className="text-5xl font-bold mb-4">PetVac</h1>
          <p className="text-xl text-orange-100 mb-3 font-medium">
            Sistema completo de gerenciamento veterinário
          </p>
          <p className="text-orange-200 text-sm">
            Controle de vacinas, histórico e notificações
          </p>
        </div>
      </div>

      {/* ── Painel direito — formulário ── */}
      <div className="flex-1 flex flex-col items-center justify-center p-6 bg-gray-50">

        {/* Logo mobile */}
        <div className="lg:hidden text-center mb-8">
          <span className="text-5xl">🐾</span>
          <h1 className="text-2xl font-bold text-primary mt-2">PetVac</h1>
        </div>

        <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">

          {/* Título dinâmico */}
          {tab === 'login' && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Entrar no Sistema</h2>
              <p className="text-sm text-gray-500 mt-1">Acesse sua conta no PetVac</p>
            </div>
          )}
          {tab === 'cadastro' && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Criar Conta</h2>
              <p className="text-sm text-gray-500 mt-1">Preencha os dados para se cadastrar</p>
            </div>
          )}
          {tab === 'reset' && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Redefinir Senha</h2>
              <p className="text-sm text-gray-500 mt-1">Informe seu e-mail e escolha uma nova senha</p>
            </div>
          )}

          {error   && <div className="mb-4"><Alert variant="error"   message={error}   onClose={() => setError(null)}   /></div>}
          {success && <div className="mb-4"><Alert variant="success" message={success} onClose={() => setSuccess(null)} /></div>}

          {/* ── Login ── */}
          {tab === 'login' && (
            <form onSubmit={handleLogin} className="space-y-5">
              <Field label="E-mail" icon="✉️">
                <input
                  type="email" required placeholder="Digite seu e-mail"
                  value={loginForm.email}
                  onChange={e => setLoginForm(f => ({ ...f, email: e.target.value }))}
                  className={inputCls}
                />
              </Field>
              <Field label="Senha" icon="🔒">
                <input
                  type="password" required placeholder="Digite sua senha"
                  value={loginForm.senha}
                  onChange={e => setLoginForm(f => ({ ...f, senha: e.target.value }))}
                  className={inputCls}
                />
              </Field>

              <div className="flex justify-end -mt-2">
                <button type="button" onClick={() => changeTab('reset')}
                  className="text-xs text-primary hover:underline font-medium">
                  Esqueceu a senha?
                </button>
              </div>

              <OrangeButton loading={loading}>Entrar</OrangeButton>

              <p className="text-center text-sm text-gray-500">
                Não tem conta?{' '}
                <button type="button" onClick={() => changeTab('cadastro')}
                  className="text-primary font-semibold hover:underline">
                  Criar conta
                </button>
              </p>
            </form>
          )}

          {/* ── Cadastro ── */}
          {tab === 'cadastro' && (
            <form onSubmit={handleCadastro} className="space-y-4">
              <Field label="Nome completo" icon="👤">
                <input
                  required placeholder="Seu nome completo"
                  value={cadForm.nome}
                  onChange={e => setCadForm(f => ({ ...f, nome: e.target.value }))}
                  className={inputCls}
                />
              </Field>
              <Field label="E-mail" icon="✉️">
                <input
                  type="email" required placeholder="seu@email.com"
                  value={cadForm.email}
                  onChange={e => setCadForm(f => ({ ...f, email: e.target.value }))}
                  className={inputCls}
                />
              </Field>
              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Tipo de Usuário</label>
                <select
                  value={cadForm.cargo}
                  onChange={e => setCadForm(f => ({ ...f, cargo: e.target.value }))}
                  className={inputCls}
                >
                  {TIPO_USUARIO.map(t => (
                    <option key={t.value} value={t.value}>{t.label}</option>
                  ))}
                </select>
              </div>
              <Field label="Senha" icon="🔒">
                <input
                  type="password" required placeholder="Mín. 6 caracteres"
                  value={cadForm.senha}
                  onChange={e => setCadForm(f => ({ ...f, senha: e.target.value }))}
                  className={inputCls}
                />
              </Field>
              <Field label="Confirmar senha" icon="🔒">
                <input
                  type="password" required placeholder="Repita a senha"
                  value={cadForm.confirmarSenha}
                  onChange={e => setCadForm(f => ({ ...f, confirmarSenha: e.target.value }))}
                  className={inputCls}
                />
              </Field>

              <OrangeButton loading={loading}>Criar conta</OrangeButton>

              <p className="text-center text-sm text-gray-500">
                Já tem conta?{' '}
                <button type="button" onClick={() => changeTab('login')}
                  className="text-primary font-semibold hover:underline">
                  Entrar
                </button>
              </p>
            </form>
          )}

          {/* ── Redefinir senha ── */}
          {tab === 'reset' && (
            <form onSubmit={handleReset} className="space-y-4">
              <Field label="E-mail cadastrado" icon="✉️">
                <input
                  type="email" required placeholder="seu@email.com"
                  value={resetForm.email}
                  onChange={e => setResetForm(f => ({ ...f, email: e.target.value }))}
                  className={inputCls}
                />
              </Field>
              <Field label="Nova senha" icon="🔒">
                <input
                  type="password" required placeholder="Mín. 6 caracteres"
                  value={resetForm.nova_senha}
                  onChange={e => setResetForm(f => ({ ...f, nova_senha: e.target.value }))}
                  className={inputCls}
                />
              </Field>
              <Field label="Confirmar nova senha" icon="🔒">
                <input
                  type="password" required placeholder="Repita a nova senha"
                  value={resetForm.confirmarSenha}
                  onChange={e => setResetForm(f => ({ ...f, confirmarSenha: e.target.value }))}
                  className={inputCls}
                />
              </Field>

              <OrangeButton loading={loading}>Redefinir senha</OrangeButton>

              <p className="text-center text-sm text-gray-500">
                <button type="button" onClick={() => changeTab('login')}
                  className="text-primary font-semibold hover:underline">
                  ← Voltar ao login
                </button>
              </p>
            </form>
          )}
        </div>

        <p className="text-xs text-gray-400 mt-6">Senhas protegidas com bcrypt · PetVac v1.1</p>
      </div>
    </div>
  )
}

/* ── Helpers de UI locais ── */
const inputCls = `w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm outline-none
  focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors bg-gray-50`

function Field({ label, icon, children }: { label: string; icon: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <div className="relative flex items-center">
        <span className="absolute left-3 text-gray-400 text-sm pointer-events-none">{icon}</span>
        <div className="w-full [&>input]:pl-9 [&>select]:pl-9">{children}</div>
      </div>
    </div>
  )
}

function OrangeButton({ loading, children }: { loading: boolean; children: React.ReactNode }) {
  return (
    <button
      type="submit"
      disabled={loading}
      className="w-full bg-primary hover:bg-primary-dark text-white font-semibold py-3 rounded-lg
                 transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
    >
      {loading && (
        <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
      )}
      {children}
    </button>
  )
}
