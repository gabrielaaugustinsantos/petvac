import { api } from '@/lib/api'
import type { Pet } from '@/types'

interface MessageResponse { mensagem: string; sucesso: boolean }

export interface PetCreate {
  nome: string
  especie: string
  raca: string
  dataNascimento: string
  idTutor: number
}

export const petsService = {
  listar:    ()                               => api.get<Pet[]>('/pets/'),
  cadastrar: (body: PetCreate)                => api.post<MessageResponse>('/pets/', body),
  atualizar: (id: number, body: Partial<PetCreate>) => api.put<MessageResponse>(`/pets/${id}`, body),
}
