---
title: Vercel Deployment Guide
type: guide
tags: [vercel, deployment, serverless, ci-cd, production]
related:
  - "[[overview]]"
  - "[[guides/getting-started]]"
sources:
  - vercel.json
  - package.json
  - next.config.ts
---

# Panduan Deployment ke Platform Vercel

## Gambaran Umum

Aegis-JKN dibangun menggunakan Next.js 16 App Router dengan React 19 dan Tailwind CSS v4. Aplikasi ini dioptimalkan untuk di-deploy secara instan ke Vercel tanpa perlu konfigurasi server rumit.

## Persiapan Konfigurasi untuk Vercel

Proyek ini telah dikonfigurasi agar ramah Vercel (*Vercel-ready*):
1. **Skrip Build Standar**: `package.json` menggunakan `"build": "next build"` standar.
2. **Postinstall Otomatis**: Skrip `"postinstall": "prisma generate"` memastikan Prisma Client otomatis terkompilasi selama proses build di lingkungan cloud Vercel.
3. **Konfigurasi Output**: `next.config.ts` tidak memaksakan mode standalone, memanfaatkan arsitektur Serverless Functions bawaan Vercel secara optimal.
4. **Vercel Manifest (`vercel.json`)**: Menyediakan konfigurasi framework Next.js yang bersih.

## Langkah Deployment via Vercel Dashboard

1. **Buka Vercel**: Masuk ke [vercel.com](https://vercel.com) menggunakan akun GitHub Anda.
2. **Import Git Repository**:
   - Klik tombol **"Add New..."** $\to$ **"Project"**.
   - Pilih repositori `biezz-2/Aegis-JKN`.
3. **Konfigurasi Project**:
   - **Framework Preset**: Next.js (otomatis terdeteksi).
   - **Root Directory**: `./` (default).
   - **Build Command**: `next build` (default).
   - **Output Directory**: `.next` (default).
   - **Install Command**: `bun install` atau `npm install` (default).
4. **Environment Variables**:
   Jika menggunakan database terkelola (misal: PostgreSQL / Supabase di tahap lanjutan), tambahkan variabel:
   - `DATABASE_URL` = URL koneksi database Anda.
5. **Klik "Deploy"**:
   Vercel akan mengklon repositori, menginstal dependensi, menjalankan `prisma generate`, memproses bundel Next.js, dan menerbitkan domain publik (contoh: `https://aegis-jkn.vercel.app`).

## Deployment via Vercel CLI (Alternatif)

Jika memiliki Vercel CLI di komputer lokal:
```bash
# Login ke Vercel
npx vercel login

# Deploy ke Preview
npx vercel

# Deploy langsung ke Production
npx vercel --prod
```
