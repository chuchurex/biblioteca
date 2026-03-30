/** @type {import('tailwindcss').Config} */
import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#FAF7F2',  // Pergamino cálido (bg-light)
          100: '#EDE8E0',  // Crema suave (bg-warm)
          200: '#D5CBBF',  // Gris cálido
          300: '#8A9BB5',  // Gris azulado (texto sutil en fondos oscuros)
          400: '#D4A05A',  // Dorado (acento principal)
          500: '#2C4A6E',  // Azul medio (texto secundario)
          600: '#1E3A5F',  // Azul primario (tinta)
          700: '#152C4A',  // Azul oscuro
          800: '#0F1F35',  // Azul muy oscuro (text-primary)
          900: '#0A1628',  // Azul noche (bg-dark)
        },
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', ...defaultTheme.fontFamily.serif],
        body: ['"Nunito Sans"', ...defaultTheme.fontFamily.sans],
      },
      boxShadow: {
        'card': '0 2px 8px rgba(15, 31, 53, 0.06)',
        'card-hover': '0 16px 40px rgba(15, 31, 53, 0.14)',
        'glow': '0 0 20px rgba(212, 160, 90, 0.15)',
      }
    },
  },
  plugins: [],
}
