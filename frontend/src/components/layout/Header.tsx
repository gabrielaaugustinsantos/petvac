'use client'

import { usePathname } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/Button'

const titlesRecepcionista: Record<string, string> = {
  '/dashboard':    'Dashboard',
  '/tutores':      'Tutores',
  '/pets':         'Pets',
  '/notificacoes': 'Notificações',
}

const titlesVeterinario: Record<string, string> = {
  '/dashboard':    'Dashboard',
  '/vacinas':      'Registrar Vacina',
  '/historico':    'Histórico de Vacinação',
  '/notificacoes': 'Vacinas Pendentes',
}

interface HeaderProps {
  onMenuClick: () => void
}

export function Header({ onMenuClick }: HeaderProps) {
  const { user, logout } = useAuth()
  const pathname = usePathname()

  const titles     = user?.cargo === 'veterinario' ? titlesVeterinario : titlesRecepcionista
  const title      = titles[pathname] ?? 'PetVac'
  const cargoLabel = user?.cargo === 'veterinario' ? 'Veterinário(a)' : 'Recepcionista'

  return (
    <header className="bg-white border-b border-gray-200 px-4 md:px-6 py-3 md:py-4 flex items-center gap-3 shrink-0">
      {/* Hamburguer — visível apenas no mobile */}
      <button
        onClick={onMenuClick}
        className="md:hidden flex flex-col justify-center gap-1.5 w-8 h-8 shrink-0 text-gray-600 hover:text-gray-900 transition-colors"
        aria-label="Abrir menu"
      >
        <span className="block w-5 h-0.5 bg-current rounded-full" />
        <span className="block w-5 h-0.5 bg-current rounded-full" />
        <span className="block w-5 h-0.5 bg-current rounded-full" />
      </button>

      {/* Título da página */}
      <h2 className="flex-1 text-lg md:text-xl font-semibold text-gray-800 truncate">{title}</h2>

      {/* Info do usuário + logout */}
      <div className="flex items-center gap-2 md:gap-4 shrink-0">
        <div className="text-right hidden sm:block">
          <p className="text-sm font-medium text-gray-800">{user?.nome}</p>
          <p className="text-xs text-gray-500">{cargoLabel}</p>
        </div>
        <div className="w-9 h-9 rounded-full bg-primary flex items-center justify-center text-white font-bold text-sm shrink-0">
          {user?.nome?.[0]?.toUpperCase() ?? '?'}
        </div>
        <Button variant="outline" size="sm" onClick={logout}>Sair</Button>
      </div>
    </header>
  )
}
