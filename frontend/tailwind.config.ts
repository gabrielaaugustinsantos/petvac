import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1E5F7A',
          dark: '#185168',
          light: '#E8F4F8',
        },
        success: '#28A745',
        danger: '#DC3545',
        warning: '#F39C12',
        info: '#17A2B8',
      },
    },
  },
  plugins: [],
}

export default config
