import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#F97316',   // orange-500
          dark:    '#EA580C',   // orange-600
          light:   '#FFF7ED',   // orange-50
          subtle:  '#FFEDD5',   // orange-100
        },
        success: '#16A34A',
        danger:  '#DC2626',
        warning: '#D97706',
        info:    '#2563EB',
      },
    },
  },
  plugins: [],
}

export default config
