import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Allow external access if needed(e.g.docker)
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/run': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/run_sse': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/apps': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/stories': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
