import type { AuthData } from '@/types'

const KEY = 'petvac_auth'

export function saveAuth(data: AuthData): void {
  localStorage.setItem(KEY, JSON.stringify(data))
}

export function getAuth(): AuthData | null {
  if (typeof window === 'undefined') return null
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? (JSON.parse(raw) as AuthData) : null
  } catch {
    return null
  }
}

export function clearAuth(): void {
  localStorage.removeItem(KEY)
}
