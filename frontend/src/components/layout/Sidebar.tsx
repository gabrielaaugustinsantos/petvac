'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { href: '/dashboard',     label: 'Dashboard',      icon: '📊' },
  { href: '/tutores',       label: 'Tutores',         icon: '👤' },
  { href: '/pets',          label: 'Pets',            icon: '🐶' },
  { href: '/vacinas',       label: 'Vacinas',         icon: '💉' },
  { href: '/historico',     label: 'Histórico',       icon: '📋' },
  { href: '/notificacoes',  label: 'Notificações',    icon: '🔔' },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col shadow-sm shrink-0">
      {/* Logo */}
      <div className="px-6 py-5 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🐾</span>
          <div>
            <h1 className="text-xl font-bold text-primary">PetVac</h1>
            <p className="text-xs text-gray-400">Gestão de Vacinação</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(item => {
          const active = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
                ${active
                  ? 'bg-primary-light text-primary font-semibold'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
            >
              <span className="text-lg">{item.icon}</span>
              {item.label}
              {active && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-primary" />}
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="px-6 py-4 border-t border-gray-100">
        <p className="text-xs text-gray-400 text-center">PetVac v1.0</p>
      </div>
    </aside>
  )
}
