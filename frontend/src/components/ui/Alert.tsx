type AlertVariant = 'success' | 'error' | 'warning' | 'info'

interface AlertProps {
  variant: AlertVariant
  message: string
  onClose?: () => void
}

const styles: Record<AlertVariant, { bg: string; border: string; text: string; icon: string }> = {
  success: { bg: 'bg-green-50',  border: 'border-green-400', text: 'text-green-800', icon: '✓' },
  error:   { bg: 'bg-red-50',    border: 'border-red-400',   text: 'text-red-800',   icon: '✕' },
  warning: { bg: 'bg-yellow-50', border: 'border-yellow-400',text: 'text-yellow-800',icon: '⚠' },
  info:    { bg: 'bg-blue-50',   border: 'border-blue-400',  text: 'text-blue-800',  icon: 'ℹ' },
}

export function Alert({ variant, message, onClose }: AlertProps) {
  const s = styles[variant]

  return (
    <div className={`flex items-start gap-3 p-4 rounded-lg border-l-4 ${s.bg} ${s.border}`}>
      <span className={`font-bold ${s.text}`}>{s.icon}</span>
      <p className={`flex-1 text-sm ${s.text}`}>{message}</p>
      {onClose && (
        <button onClick={onClose} className={`${s.text} hover:opacity-70 text-lg leading-none`}>×</button>
      )}
    </div>
  )
}
