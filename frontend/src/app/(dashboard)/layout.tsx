'use client'

import { useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'
import { Spinner } from '@/components/ui/Spinner'

// Rotas permitidas por cargo
const ROTAS_POR_CARGO: Record<string, string[]> = {
  recepcionista: ['/dashboard', '/tutores', '/pets', '/notificacoes'],
  veterinario:   ['/dashboard', '/vacinas', '/historico', '/notificacoes'],
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth()
  const router   = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    if (isLoading) return

    // Sem sessão → login
    if (!user) {
      router.push('/')
      return
    }

    // Rota não permitida para o cargo → redireciona ao dashboard
    const permitidas = ROTAS_POR_CARGO[user.cargo] ?? ['/dashboard']
    if (!permitidas.includes(pathname)) {
      router.push('/dashboard')
    }
  }, [user, isLoading, pathname, router])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!user) return null

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
