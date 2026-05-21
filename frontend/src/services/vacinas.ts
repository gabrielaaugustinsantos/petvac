import { api } from '@/lib/api'
import type { Vacina } from '@/types'

interface MessageResponse { mensagem: string; sucesso: boolean }

export interface VacinaCreate {
  idPet: number
  nome: string
  dataAplicacao?: string | null
  dataProximaDose?: string | null
}

export interface AplicarDoseBody {
  dataAplicacao: string
  dataProximaDose?: string | null
}

export const vacinasService = {
  pendentes:  ()                                        => api.get<Vacina[]>('/vacinas/pendentes'),
  registrar:  (body: VacinaCreate)                      => api.post<MessageResponse>('/vacinas/', body),
  aplicar:    (id: number, body: AplicarDoseBody)       => api.post<MessageResponse>(`/vacinas/${id}/aplicar`, body),
  agendar:    (id: number, dataAgendamento: string)     => api.patch<MessageResponse>(`/vacinas/${id}/agendar`, { dataAgendamento }),
  historico:  (idPet: number)                           => api.get<Vacina[]>(`/vacinas/historico/${idPet}`),
}
