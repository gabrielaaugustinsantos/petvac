import { api } from '@/lib/api'
import type { Notificacao } from '@/types'

interface MessageResponse { mensagem: string; sucesso: boolean }

export const notificacoesService = {
  listar: ()                  => api.get<Notificacao[]>('/notificacoes/'),
  gerar:  ()                  => api.post<MessageResponse>('/notificacoes/gerar', {}),
  marcarLida: (id: number)    => api.put<MessageResponse>(`/notificacoes/${id}/lida`, {}),
}
