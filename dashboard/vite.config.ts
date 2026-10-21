import path from 'node:path';
import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [tailwindcss(), sveltekit()],
  // The repo root has a Next.js postcss.config.mjs; Vite would otherwise walk
  // up and load it, breaking the @tailwindcss/vite plugin. This app has no
  // PostCSS config of its own.
  css: { postcss: { plugins: [] } },
  resolve: {
    alias: {
      '@': path.resolve('./src')
    }
  },
  server: {
    port: 5175,
    strictPort: true
  },
  preview: {
    port: 5175
  },
  test: {
    include: ['src/**/*.test.ts'],
    environment: 'node'
  }
});
