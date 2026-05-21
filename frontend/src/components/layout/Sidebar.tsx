'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'

interface NavItem {
  href:  string
  label: string
  icon:  string
}

// ── Menus por cargo ────────────────────────────────────────────────────────────

const navRecepcionista: NavItem[] = [
  { href: '/dashboard',    label: 'Dashboard',    icon: '📊' },
  { href: '/tutores',      label: 'Tutores',      icon: '👤' },
  { href: '/pets',         label: 'Pets',         icon: '🐶' },
  { href: '/notificacoes', label: 'Notificações', icon: '🔔' },
]

const navVeterinario: NavItem[] = [
  { href: '/dashboard',    label: 'Dashboard',         icon: '📊' },
  { href: '/vacinas',      label: 'Registrar Vacina',  icon: '💉' },
  { href: '/historico',    label: 'Histórico',         icon: '📋' },
  { href: '/notificacoes', label: 'Vacinas Pendentes', icon: '🔔' },
]

// ── Componente ─────────────────────────────────────────────────────────────────

export function Sidebar() {
  const pathname  = usePathname()
  const { user }  = useAuth()

  const navItems  = user?.cargo === 'veterinario' ? navVeterinario : navRecepcionista
  const cargoLabel = user?.cargo === 'veterinario' ? 'Veterinário(a)' : 'Recepcionista'

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col shadow-sm shrink-0">

      {/* Logo */}
      <div className="px-6 py-5 border-b border-orange-100 bg-gradient-to-r from-primary-light to-white">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🐾</span>
          <div>
            <h1 className="text-xl font-bold text-primary">PetVac</h1>
            <p className="text-xs text-gray-400">Gestão de Vacinação</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-0.5">
        {navItems.map(item => {
          const active = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
                ${active
                  ? 'bg-primary-light text-primary font-semibold border-l-4 border-primary pl-2'
                  : 'text-gray-600 hover:bg-orange-50 hover:text-primary'
                }`}
            >
              <span className="text-lg">{item.icon}</span>
              {item.label}
            </Link>
          )
        })}
      </nav>

      {/* Footer: cargo + versão */}
      <div className="px-4 py-4 border-t border-gray-100 space-y-2">
        <div className="flex items-center gap-2 px-2">
          <span className="w-2 h-2 rounded-full bg-primary shrink-0" />
          <span className="text-xs text-gray-500 font-medium">{cargoLabel}</span>
        </div>
        <p className="text-xs text-gray-400 text-center">PetVac v1.1</p>
      </div>
    </aside>
  )
}
