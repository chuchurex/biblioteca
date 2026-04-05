/** @type {import('tailwindcss').Config} */
import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#F0EDE8',  // Crema calido (texto primario)
          100: '#9A968E',  // Texto secundario
          200: '#5A574F',  // Texto muted
          300: '#222228',  // Hover state
          400: '#E8B04A',  // Dorado (acento principal)
          500: '#1A1A20',  // Cards, paneles
          600: '#141418',  // Superficie elevada
          700: '#0C0C0E',  // Fondo principal
          800: '#C4785A',  // Terracota (acento)
          900: '#0C0C0E',  // Alias fondo
        },
        accent: '#E8B04A',
        warm: '#C4785A',
        cool: '#5A8EC4',
        green: '#5AC47A',
      },
      fontFamily: {
        display: ['"DM Serif Display"', ...defaultTheme.fontFamily.serif],
        body: ['"DM Sans"', ...defaultTheme.fontFamily.sans],
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0, 0, 0, 0.2)',
        'card-hover': '0 20px 60px rgba(0, 0, 0, 0.4)',
        'glow': '0 0 20px rgba(232, 176, 74, 0.15)',
        'glow-strong': '0 8px 32px rgba(232, 176, 74, 0.15)',
      }
    },
  },
  plugins: [],
}
