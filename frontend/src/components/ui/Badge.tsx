type BadgeVariant = 'success' | 'warning' | 'danger' | 'info' | 'gray'

interface BadgeProps {
  variant?: BadgeVariant
  children: React.ReactNode
  className?: string
}

const variants: Record<BadgeVariant, string> = {
  success: 'bg-green-100 text-green-700',
  warning: 'bg-yellow-100 text-yellow-700',
  danger:  'bg-red-100 text-red-700',
  info:    'bg-blue-100 text-blue-700',
  gray:    'bg-gray-100 text-gray-600',
}

export function Badge({ variant = 'gray', children, className = '' }: BadgeProps) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${variants[variant]} ${className}`}>
      {children}
    </span>
  )
}

export function statusBadge(status: string, atrasada?: boolean) {
  if (atrasada) return { variant: 'danger' as const, label: 'Atrasada' }
  if (status === 'pendente')  return { variant: 'warning' as const, label: 'Pendente' }
  if (status === 'aplicada')  return { variant: 'success' as const, label: 'Aplicada' }
  if (status === 'concluída') return { variant: 'info'    as const, label: 'Concluída' }
  return { variant: 'gray' as const, label: status }
}
