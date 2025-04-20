import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'
import formkit from 'unplugin-formkit/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    formkit({
      configFile: './formkit.config.ts',
    }),
    tailwindcss(),
    vue(),
    //vueDevTools()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
