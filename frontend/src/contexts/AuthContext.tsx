'use client'

import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import type { AuthData } from '@/types'
import { saveAuth, getAuth, clearAuth } from '@/lib/auth'

interface AuthContextType {
  user: AuthData | null
  isLoading: boolean
  login: (data: AuthData) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    setUser(getAuth())
    setIsLoading(false)
  }, [])

  function login(data: AuthData) {
    saveAuth(data)
    setUser(data)
    router.push('/dashboard')
  }

  function logout() {
    clearAuth()
    setUser(null)
    router.push('/')
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth deve ser usado dentro de AuthProvider')
  return ctx
}
