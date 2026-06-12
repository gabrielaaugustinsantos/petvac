'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'

interface NavItem {
  href:  string
  label: string
  icon:  string
}

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

export interface SidebarProps {
  open:    boolean
  onClose: () => void
}

function SidebarBody({
  navItems,
  cargoLabel,
  onClose,
  pathname,
}: {
  navItems:   NavItem[]
  cargoLabel: string
  onClose:    () => void
  pathname:   string
}) {
  return (
    <>
      {/* Logo */}
      <div className="px-6 py-5 border-b border-orange-100 bg-gradient-to-r from-primary-light to-white flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🐾</span>
          <div>
            <h1 className="text-xl font-bold text-primary">PetVac</h1>
            <p className="text-xs text-gray-400">Gestão de Vacinação</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="md:hidden text-gray-400 hover:text-gray-600 text-2xl leading-none"
          aria-label="Fechar menu"
        >
          ×
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {navItems.map(item => {
          const active = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onClose}
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

      {/* Footer */}
      <div className="px-4 py-4 border-t border-gray-100 space-y-2 shrink-0">
        <div className="flex items-center gap-2 px-2">
          <span className="w-2 h-2 rounded-full bg-primary shrink-0" />
          <span className="text-xs text-gray-500 font-medium">{cargoLabel}</span>
        </div>
        <p className="text-xs text-gray-400 text-center">PetVac v1.1</p>
      </div>
    </>
  )
}

export function Sidebar({ open, onClose }: SidebarProps) {
  const pathname   = usePathname()
  const { user }   = useAuth()

  const navItems   = user?.cargo === 'veterinario' ? navVeterinario : navRecepcionista
  const cargoLabel = user?.cargo === 'veterinario' ? 'Veterinário(a)' : 'Recepcionista'

  return (
    <>
      {/* ── Desktop: sidebar fixa no fluxo ─────────────────────────────────── */}
      <aside className="hidden md:flex w-64 bg-white border-r border-gray-200 flex-col shadow-sm shrink-0">
        <SidebarBody
          navItems={navItems}
          cargoLabel={cargoLabel}
          onClose={onClose}
          pathname={pathname}
        />
      </aside>

      {/* ── Mobile: overlay deslizante ─────────────────────────────────────── */}
      <div
        className={`md:hidden fixed inset-0 z-40 transition-opacity duration-200
          ${open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
      >
        {/* Backdrop */}
        <div className="fixed inset-0 bg-black/50" onClick={onClose} />

        {/* Panel */}
        <aside
          className={`absolute inset-y-0 left-0 w-72 bg-white flex flex-col shadow-xl
            transform transition-transform duration-200
            ${open ? 'translate-x-0' : '-translate-x-full'}`}
        >
          <SidebarBody
            navItems={navItems}
            cargoLabel={cargoLabel}
            onClose={onClose}
            pathname={pathname}
          />
        </aside>
      </div>
    </>
  )
}
