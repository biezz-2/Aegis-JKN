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
  - scripts/dev.mjs
  - src/app/health/route.ts
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

`npm install` di root memasang **dua** pohon dependensi sekaligus. Hook `postinstall` di `package.json` menjalankan `prisma generate` lalu `npm install --prefix dashboard --no-audit --no-fund`, sehingga `dashboard/node_modules` terisi tanpa perintah terpisah.

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

`npm run dev` menjalankan **ketiga bagian repo sekaligus** lewat `scripts/dev.mjs` (orkestrator tanpa dependensi baru — hanya `node:child_process`). Ringkasan alamat dicetak setelah ketiganya siap:

| Bagian | Alamat dev | Peran |
|---|---|---|
| Showcase MHGSL (Next.js) | `http://localhost:3000` | visualisasi 3 kanal, simulasi upcoding, fraud ring |
| Dashboard Verifikator (SvelteKit) | `http://localhost:5275` | antrean klaim, panel bukti AI, tindakan HITL |
| Landing page statis | `http://localhost:5276` | halaman promosi publik, tanpa dependensi |

Catatan penting:

- **Port dev ≠ port produksi.** Produksi PM2 memakai dashboard `:5175` dan landing `:5176`. Port dev sengaja dibedakan karena Vite memakai `strictPort: true` — kalau sama, dev gagal start saat instance produksi masih online.
- **Port 3000 bisa fallback.** Kalau port itu sudah dipegang proses lain, orkestrator mencari port bebas berikutnya dan ringkasannya menampilkan port yang benar. Showcase Next.js dipanggil tanpa `--port` supaya ia sendiri yang memutuskan, sehingga tidak pernah bentrok.
- **Tautan antar-aplikasi pakai IP LAN.** Dashboard menerima `PUBLIC_LANDING_URL`, landing menerima `DASHBOARD_URL`; keduanya diisi alamat `http://<ip-lan>:<port>` supaya tautannya tetap berlaku saat dibuka dari ponsel di jaringan yang sama, bukan hanya dari `localhost`.
- **`Ctrl+C` menghentikan ketiganya** sekaligus.
- **`GET /health` di showcase menjawab 200.** Port dev showcase berada di rentang 3000-3050, yang tumpang tindih dengan rentang alokasi port bridge WhatsApp Hermes (3001-3999). Saat Hermes memindai port itu, ia mengirim `GET /health`; tanpa route `src/app/health/route.ts` setiap probe berakhir 404 dan muncul sebagai error di log dev. Route itu sengaja tidak menyamar sebagai bridge — body-nya jujur (`{"status":"ok"}`), bukan tiruan schema bridge yang memuat `session`.

Menjalankan satu bagian saja:
```bash
npm run dev:showcase    # hanya Next.js
npm run dev:dashboard   # hanya SvelteKit
npm run dev:landing     # hanya landing page statis
```

Override port lewat env: `DEV_SHOWCASE_PORT`, `DEV_DASHBOARD_PORT`, `DEV_LANDING_PORT`, `DEV_PUBLIC_HOST`.

## Pintasan Keyboard (Keyboard Shortcuts)

Saat aplikasi terbuka di browser:
- `T` : Toggle Mode Gelap / Terang (Dark / Light Theme).
- `P` : Ekspor / Cetak Halaman ke PDF (`window.print()`).
- `G` : Langsung scroll ke kanvas **Multi-Channel Graph**.
- `S` : Langsung scroll ke area **Simulasi Investigasi**.
- `ArrowRight` : Lanjut ke langkah simulasi berikutnya.
- `ArrowLeft` : Kembali ke langkah simulasi sebelumnya.
