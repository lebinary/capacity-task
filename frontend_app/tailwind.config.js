/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0a1628',
          light: '#162642',
          dark: '#0f1d33',
        },
        secondary: {
          DEFAULT: '#3b82f6',
          hover: '#2563eb',
        },
        border: {
          DEFAULT: '#4b5563',
          divider: '#374151',
        },
        text: {
          primary: '#ffffff',
          secondary: '#d1d5db',
        },
        error: {
          bg: 'rgba(127, 29, 29, 0.2)',
          border: '#ef4444',
          text: '#f87171',
        },
        info: {
          bg: 'rgba(30, 58, 138, 0.2)',
          text: '#60a5fa',
        },
        disabled: '#4b5563',
      },
    },
  },
  plugins: [],
}
