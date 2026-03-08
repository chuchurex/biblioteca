/** @type {import('tailwindcss').Config} */
import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#F5F7FA',   // Gris muy claro (bg-light)
          100: '#E8ECF1',  // Gris claro (bg-warm)
          200: '#C9D1DC',  // Gris azulado
          300: '#8A9BB5',  // Gris medio
          400: '#1E6B52',  // Verde acento (marcapáginas)
          500: '#2C4A6E',  // Azul medio
          600: '#1E3A5F',  // Azul primario (tinta)
          700: '#152C4A',  // Azul oscuro
          800: '#0F1F35',  // Azul muy oscuro (text-primary)
          900: '#0A1628',  // Azul noche (bg-dark)
        },
      },
      fontFamily: {
        body: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      boxShadow: {
        'card': '0 2px 8px rgba(15, 31, 53, 0.08)',
        'card-hover': '0 8px 24px rgba(15, 31, 53, 0.12)',
      }
    },
  },
  plugins: [],
}
