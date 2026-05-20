import { api } from '@/lib/api'
import type { AuthData } from '@/types'

interface MessageResponse { mensagem: string; sucesso: boolean }
interface LoginBody { nome: string; senha: string; cargo: string }

export const authService = {
  login:    (body: LoginBody)  => api.post<AuthData>('/auth/login', body),
  register: (body: LoginBody)  => api.post<MessageResponse>('/auth/register', body),
  logout:   (body: LoginBody)  => api.post<MessageResponse>('/auth/logout', body),
}
