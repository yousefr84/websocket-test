import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(),tailwindcss(),],
  server: {
    host: '127.0.0.1',  // 👈 این خط رو اضافه کن
    port: 5173          // (اختیاری) اگه پورت خاصی می‌خوای
  }
})
