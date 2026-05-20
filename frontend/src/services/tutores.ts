import { api } from '@/lib/api'
import type { Tutor } from '@/types'

interface MessageResponse { mensagem: string; sucesso: boolean }

export interface TutorCreate {
  nome: string
  telefone: string
  email: string
  endereco?: string
}

export const tutoresService = {
  listar:     ()                              => api.get<Tutor[]>('/tutores/'),
  cadastrar:  (body: TutorCreate)             => api.post<MessageResponse>('/tutores/', body),
  atualizar:  (id: number, body: Partial<TutorCreate>) => api.put<MessageResponse>(`/tutores/${id}`, body),
}
