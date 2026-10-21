import path from 'node:path';
import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [tailwindcss(), sveltekit()],
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
