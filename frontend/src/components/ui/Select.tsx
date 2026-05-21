import type { SelectHTMLAttributes } from 'react'

interface Option {
  value: string | number
  label: string
}

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: Option[]
  placeholder?: string
}

export function Select({ label, error, options, placeholder, className = '', id, ...props }: SelectProps) {
  const selectId = id ?? label?.toLowerCase().replace(/\s+/g, '-')

  return (
    <div className="flex flex-col gap-1">
      {label && (
        <label htmlFor={selectId} className="text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <select
        id={selectId}
        className={`border rounded-lg px-3 py-2 text-sm outline-none transition-colors
          focus:ring-2 focus:ring-primary/20 focus:border-primary bg-white
          ${error ? 'border-red-400' : 'border-gray-300'}
          disabled:bg-gray-100 disabled:cursor-not-allowed
          ${className}`}
        {...props}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {options.map(opt => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  )
}
