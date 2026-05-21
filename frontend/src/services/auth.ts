import { api } from '@/lib/api'
import type { AuthData } from '@/types'

interface MessageResponse { mensagem: string; sucesso: boolean }

interface LoginBody        { email: string; senha: string }
interface RegisterBody     { nome: string; email: string; senha: string; cargo: string }
interface ResetSenhaBody   { email: string; nova_senha: string }

export const authService = {
  login:          (body: LoginBody)       => api.post<AuthData>('/auth/login', body),
  register:       (body: RegisterBody)    => api.post<MessageResponse>('/auth/register', body),
  logout:         ()                      => api.post<MessageResponse>('/auth/logout', {}),
  redefinirSenha: (body: ResetSenhaBody)  => api.post<MessageResponse>('/auth/redefinir-senha', body),
}
