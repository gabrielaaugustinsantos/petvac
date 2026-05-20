export interface Tutor {
  idTutor: number
  nome: string
  telefone: string
  email: string
  endereco: string
}

export interface Pet {
  idPet: number
  nome: string
  especie: string
  raca: string
  dataNascimento: string
  idTutor: number
}

export interface PetComTutor extends Pet {
  nomeTutor: string
}

export interface Vacina {
  idVacina: number
  idPet: number
  nome: string
  dataAplicacao: string | null
  dataProximaDose: string | null
  status: 'pendente' | 'aplicada' | 'concluída'
  atrasada?: boolean
}

export interface VacinaComPet extends Vacina {
  nomePet: string
  nomeTutor: string
}

export interface Notificacao {
  idNotificacao: number
  mensagem: string
  dataEnvio: string
  status: string
}

export interface DashboardMetrics {
  total_tutores: number
  total_pets: number
  total_vacinas: number
  total_pendentes: number
  total_atrasadas: number
}

export interface AuthData {
  access_token: string
  token_type: string
  nome: string
  cargo: string
}

export type Cargo = 'recepcionista' | 'veterinario' | 'admin'

export const ESPECIES = ['Cachorro', 'Gato', 'Pássaro', 'Coelho', 'Hamster', 'Outro'] as const
export const CARGOS: { value: Cargo; label: string }[] = [
  { value: 'recepcionista', label: 'Recepcionista' },
  { value: 'veterinario', label: 'Veterinário' },
]
