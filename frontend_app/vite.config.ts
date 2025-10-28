import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const frontendPort = process.env.FRONTEND_PORT;
if (!frontendPort) {
  throw new Error('FRONTEND_PORT environment variable is not defined');
}

export default defineConfig({
  plugins: [react()],
  server: {
    port: parseInt(frontendPort),
  },
})
