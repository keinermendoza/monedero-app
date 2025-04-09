// vite.config.js
import path from 'path'
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: path.join(path.dirname(__dirname), "assets"),
    rollupOptions: {
      input: {
        main: path.resolve('./src/main.js'),
      }
    }
  }
})


