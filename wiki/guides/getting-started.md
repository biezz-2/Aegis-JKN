---
title: Getting Started & Local Setup
type: guide
tags: [setup, installation, local-development, bun, npm, nextjs]
related:
  - "[[overview]]"
  - "[[guides/vercel-deployment]]"
  - "[[reference/component-catalog]]"
sources:
  - package.json
  - tsconfig.json
  - next.config.ts
---

# Panduan Instalasi & Pengembangan Lokal

## Prasyarat Lingkungan
Pastikan perangkat Anda telah terinstal salah satu dari runtime JavaScript berikut:
- **Node.js**: Versi 20.x atau 22.x LTS (disertai `npm` atau `pnpm`).
- **Bun**: Versi 1.1+ (opsional, direkomendasikan untuk eksekusi cepat).

## Langkah Instalasi

### 1. Kloning Repositori
```bash
git clone https://github.com/biezz-2/Aegis-JKN.git
cd Aegis-JKN
```

### 2. Instalasi Dependensi
Jalankan salah satu perintah berikut:
```bash
# Menggunakan Bun
bun install

# Atau menggunakan NPM
npm install
```

### 3. Persiapan Database & Prisma (Opsional)
Aplikasi menyertakan skema Prisma untuk kebutuhan penyimpanan data relasional klaim di masa mendatang:
```bash
npx prisma generate
```

### 4. Menjalankan Server Pengembangan
```bash
# Menggunakan Bun
bun run dev

# Atau menggunakan NPM
npm run dev
```

Aplikasi akan berjalan secara lokal di [http://localhost:3000](http://localhost:3000).

## Pintasan Keyboard (Keyboard Shortcuts)

Saat aplikasi terbuka di browser:
- `T` : Toggle Mode Gelap / Terang (Dark / Light Theme).
- `P` : Ekspor / Cetak Halaman ke PDF (`window.print()`).
- `G` : Langsung scroll ke kanvas **Multi-Channel Graph**.
- `S` : Langsung scroll ke area **Simulasi Investigasi**.
- `ArrowRight` : Lanjut ke langkah simulasi berikutnya.
- `ArrowLeft` : Kembali ke langkah simulasi sebelumnya.
