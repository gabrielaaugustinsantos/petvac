'use client'

import { useEffect, useState, useMemo } from 'react'
import { vacinasService } from '@/services/vacinas'
import { petsService }    from '@/services/pets'
import { tutoresService } from '@/services/tutores'
import { useAuth } from '@/contexts/AuthContext'
import type { Vacina, Pet, Tutor } from '@/types'
import { Alert }       from '@/components/ui/Alert'
import { PageSpinner } from '@/components/ui/Spinner'

// ── Tipos ─────────────────────────────────────────────────────────────────────

type Urgencia = 'urgente' | 'alerta' | 'lembrete'

interface NotifCard {
  vacina:   Vacina
  pet:      Pet
  tutor:    Tutor | null
  urgencia: Urgencia
  diasInfo: string
}

type Filtro = 'todas' | Urgencia

// ── Helpers ───────────────────────────────────────────────────────────────────

function calcUrgencia(v: Vacina): { urgencia: Urgencia; diasInfo: string } {
  if (v.atrasada) {
    const dias = v.dataProximaDose
      ? Math.floor((Date.now() - new Date(v.dataProximaDose).getTime()) / 86_400_000)
      : 0
    return {
      urgencia: 'urgente',
      diasInfo: dias > 0 ? `Vencida há ${dias} dia${dias !== 1 ? 's' : ''}` : 'Vencida hoje',
    }
  }
  if (!v.dataProximaDose) return { urgencia: 'lembrete', diasInfo: 'Sem data definida' }

  const dias = Math.ceil((new Date(v.dataProximaDose).getTime() - Date.now()) / 86_400_000)
  if (dias <= 7)  return { urgencia: 'alerta',   diasInfo: `Vence em ${dias} dia${dias !== 1 ? 's' : ''}` }
  if (dias <= 30) return { urgencia: 'lembrete', diasInfo: `Vence em ${dias} dias` }
  return { urgencia: 'lembrete', diasInfo: `Vence em ${dias} dias` }
}

/** Monta link wa.me com mensagem pré-preenchida */
function whatsappLink(tutor: Tutor, petNome: string, vacinaNome: string, diasInfo: string): string {
  const tel = tutor.telefone.replace(/\D/g, '')
  const msg = encodeURIComponent(
    `Olá ${tutor.nome}! 👋 Passando para lembrar que *${petNome}* está com a vacina *${vacinaNome}* pendente (${diasInfo}). Por favor, entre em contato para agendar a aplicação. Obrigado! — PetVac 🐾`
  )
  return `https://wa.me/55${tel}?text=${msg}`
}

const urgenciaConfig: Record<Urgencia, { label: string; badge: string; border: string; icon: string; textColor: string }> = {
  urgente:  { label: 'Urgente',  badge: 'bg-red-600 text-white',    border: 'border-l-red-500',    icon: '⚠️', textColor: 'text-red-600'    },
  alerta:   { label: 'Alerta',   badge: 'bg-primary text-white',    border: 'border-l-primary',    icon: '🔔', textColor: 'text-primary'    },
  lembrete: { label: 'Lembrete', badge: 'bg-yellow-400 text-white', border: 'border-l-yellow-400', icon: '📋', textColor: 'text-yellow-600'  },
}

const titulos: Record<Urgencia, string> = {
  urgente:  'Vacina Vencida',
  alerta:   'Vacina Próxima',
  lembrete: 'Lembrete de Vacina',
}

// ── Componente principal ──────────────────────────────────────────────────────

export default function NotificacoesPage() {
  const { user } = useAuth()
  const isVet = user?.cargo === 'veterinario'

  const [pendentes,  setPendentes]  = useState<Vacina[]>([])
  const [pets,       setPets]       = useState<Pet[]>([])
  const [tutores,    setTutores]    = useState<Tutor[]>([])
  const [loading,    setLoading]    = useState(true)
  const [error,      setError]      = useState<string | null>(null)
  const [success,    setSuccess]    = useState<string | null>(null)
  const [filtro,     setFiltro]     = useState<Filtro>('todas')

  // Estado do form inline de aplicação (somente vet)
  const [aplicandoId,   setAplicandoId]   = useState<number | null>(null)
  const [dataAplicacao, setDataAplicacao] = useState('')
  const [salvando,      setSalvando]      = useState(false)

  async function load() {
    setLoading(true)
    try {
      const [pend, p, t] = await Promise.all([
        vacinasService.pendentes(),
        petsService.listar(),
        tutoresService.listar(),
      ])
      setPendentes(pend); setPets(p); setTutores(t)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao carregar notificações')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function abrirAplicacao(idVacina: number) {
    setAplicandoId(idVacina)
    setDataAplicacao(new Date().toISOString().split('T')[0]) // padrão = hoje
  }

  function cancelarAplicacao() {
    setAplicandoId(null)
    setDataAplicacao('')
  }

  async function confirmarAplicacao(idVacina: number) {
    if (!dataAplicacao) return
    setSalvando(true); setError(null)
    try {
      await vacinasService.aplicar(idVacina, { dataAplicacao })
      setSuccess('Vacina aplicada com sucesso!')
      cancelarAplicacao()
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao aplicar vacina')
    } finally {
      setSalvando(false)
    }
  }

  // ── Cards enriquecidos ─────────────────────────────────────────────────────
  const cards: NotifCard[] = useMemo(() => {
    return pendentes.map(v => {
      const pet   = pets.find(p => p.idPet === v.idPet) ?? null
      const tutor = pet ? tutores.find(t => t.idTutor === pet.idTutor) ?? null : null
      const { urgencia, diasInfo } = calcUrgencia(v)
      return { vacina: v, pet: pet!, tutor, urgencia, diasInfo }
    }).filter(c => c.pet)
  }, [pendentes, pets, tutores])

  const filtrados = filtro === 'todas' ? cards : cards.filter(c => c.urgencia === filtro)

  const contagem: Record<Filtro, number> = {
    todas:    cards.length,
    urgente:  cards.filter(c => c.urgencia === 'urgente').length,
    alerta:   cards.filter(c => c.urgencia === 'alerta').length,
    lembrete: cards.filter(c => c.urgencia === 'lembrete').length,
  }

  if (loading) return <PageSpinner />

  const filtros: { id: Filtro; label: string }[] = [
    { id: 'todas',    label: 'Todas' },
    { id: 'urgente',  label: 'Urgentes' },
    { id: 'alerta',   label: 'Alertas' },
    { id: 'lembrete', label: 'Lembretes' },
  ]

  return (
    <div className="space-y-6">
      {error   && <Alert variant="error"   message={error}   onClose={() => setError(null)}   />}
      {success && <Alert variant="success" message={success} onClose={() => setSuccess(null)} />}

      {/* ── Barra de filtros ── */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">🔔 Filtrar Notificações</h3>
        <div className="flex gap-2 flex-wrap">
          {filtros.map(f => (
            <button
              key={f.id}
              onClick={() => setFiltro(f.id)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors
                ${filtro === f.id
                  ? 'bg-primary text-white shadow-sm'
                  : 'bg-gray-100 text-gray-600 hover:bg-orange-50 hover:text-primary'}`}
            >
              {f.label}
              <span className={`ml-1.5 text-xs font-bold ${filtro === f.id ? 'text-orange-200' : 'text-gray-400'}`}>
                {contagem[f.id]}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* ── Lista de cards ── */}
      {filtrados.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center shadow-sm border border-gray-100">
          <div className="text-5xl mb-3">✅</div>
          <p className="font-semibold text-gray-700 text-lg">Nenhuma notificação</p>
          <p className="text-gray-500 text-sm mt-1">
            {filtro === 'todas'
              ? 'Todos os pets estão em dia com a vacinação!'
              : `Nenhuma notificação do tipo "${filtro}".`}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtrados.map((card, i) => {
            const cfg      = urgenciaConfig[card.urgencia]
            const titulo   = titulos[card.urgencia]
            const vacinaId = card.vacina.idVacina
            const aplicando = aplicandoId === vacinaId

            return (
              <div
                key={`${vacinaId}-${i}`}
                className={`bg-white rounded-xl shadow-sm border border-gray-100 border-l-4 ${cfg.border} p-5 transition-all`}
              >
                {/* Cabeçalho */}
                <div className="flex items-center gap-3">
                  <span className="text-xl">{cfg.icon}</span>
                  <h4 className="font-semibold text-gray-800">{titulo}</h4>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${cfg.badge}`}>
                    {cfg.label}
                  </span>
                </div>

                {/* Corpo */}
                <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1 text-sm text-gray-600">
                    <p>
                      <span className="text-gray-400">🐾 Pet: </span>
                      <span className="font-medium text-gray-800">{card.pet.nome}</span>
                      <span className="text-gray-400 ml-1">({card.pet.especie})</span>
                    </p>
                    {card.tutor && (
                      <>
                        <p>
                          <span className="text-gray-400">👤 Tutor: </span>
                          <span className="font-medium text-primary">{card.tutor.nome}</span>
                        </p>
                        <p>
                          <span className="text-gray-400">📞 Telefone: </span>
                          <span>{card.tutor.telefone}</span>
                        </p>
                      </>
                    )}
                  </div>

                  <div className="space-y-1 text-sm text-gray-600">
                    <p>
                      <span className="text-gray-400">💉 Vacina: </span>
                      <span className="font-medium text-gray-800">{card.vacina.nome}</span>
                    </p>
                    {card.vacina.dataProximaDose && (
                      <p>
                        <span className="text-gray-400">📅 Próxima dose: </span>
                        <span>{card.vacina.dataProximaDose}</span>
                      </p>
                    )}
                    <p>
                      <span className="text-gray-400">Status: </span>
                      <span className={`font-semibold ${cfg.textColor}`}>{card.diasInfo}</span>
                    </p>
                  </div>
                </div>

                {/* ── Form inline de aplicação (só vet) ── */}
                {isVet && aplicando && (
                  <div className="mt-4 p-4 bg-orange-50 rounded-lg border border-orange-100">
                    <p className="text-sm font-medium text-gray-700 mb-3">
                      💉 Data de aplicação de <strong>{card.vacina.nome}</strong>:
                    </p>
                    <div className="flex items-center gap-3 flex-wrap">
                      <input
                        type="date"
                        value={dataAplicacao}
                        onChange={e => setDataAplicacao(e.target.value)}
                        className="border border-gray-300 rounded-lg px-3 py-2 text-sm
                                   focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary"
                      />
                      <button
                        onClick={() => confirmarAplicacao(vacinaId)}
                        disabled={!dataAplicacao || salvando}
                        className="px-4 py-2 text-sm font-semibold bg-primary text-white
                                   rounded-lg hover:bg-primary-dark transition-colors
                                   disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {salvando ? '⏳ Salvando...' : '✓ Confirmar'}
                      </button>
                      <button
                        onClick={cancelarAplicacao}
                        className="px-4 py-2 text-sm font-medium text-gray-600
                                   border border-gray-300 rounded-lg hover:border-gray-400 transition-colors"
                      >
                        Cancelar
                      </button>
                    </div>
                  </div>
                )}

                {/* ── Ações ── */}
                <div className="mt-4 flex gap-3 flex-wrap">
                  {/* Notificar via WhatsApp — disponível para todos os cargos */}
                  {card.tutor?.telefone && (
                    <a
                      href={whatsappLink(card.tutor, card.pet.nome, card.vacina.nome, card.diasInfo)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 text-sm font-medium border border-gray-300 text-gray-700
                                 rounded-lg hover:border-primary hover:text-primary transition-colors"
                    >
                      📲 Notificar
                    </a>
                  )}

                  {/* Aplicar Vacina — somente veterinário */}
                  {isVet && !aplicando && (
                    <button
                      onClick={() => abrirAplicacao(vacinaId)}
                      className="px-4 py-2 text-sm font-semibold bg-primary text-white
                                 rounded-lg hover:bg-primary-dark transition-colors"
                    >
                      💉 Aplicar Vacina
                    </button>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
