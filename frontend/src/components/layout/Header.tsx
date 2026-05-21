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

export function Header() {
  const { user, logout } = useAuth()
  const pathname = usePathname()

  const titles     = user?.cargo === 'veterinario' ? titlesVeterinario : titlesRecepcionista
  const title      = titles[pathname] ?? 'PetVac'
  const cargoLabel = user?.cargo === 'veterinario' ? 'Veterinário(a)' : 'Recepcionista'

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shrink-0">
      <h2 className="text-xl font-semibold text-gray-800">{title}</h2>

      <div className="flex items-center gap-4">
        <div className="text-right hidden sm:block">
          <p className="text-sm font-medium text-gray-800">{user?.nome}</p>
          <p className="text-xs text-gray-500">{cargoLabel}</p>
        </div>
        {/* Avatar com inicial */}
        <div className="w-9 h-9 rounded-full bg-primary flex items-center justify-center text-white font-bold text-sm">
          {user?.nome?.[0]?.toUpperCase() ?? '?'}
        </div>
        <Button variant="outline" size="sm" onClick={logout}>Sair</Button>
      </div>
    </header>
  )
}
