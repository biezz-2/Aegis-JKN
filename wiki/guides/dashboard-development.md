---
title: Dashboard Development
type: guide
tags: [development, verification, deployment]
related:
  - "[[Verifier Dashboard]]"
sources:
  - dashboard/package.json
  - dashboard/vite.config.ts
  - ecosystem.config.cjs
---

# Dashboard Development

```bash
cd dashboard
npm i
npm run typecheck
npm test
npm run build
npm run dev
```

The dev server is pinned to port **5175** (`strictPort`) in `vite.config.ts`.

## Deployment

```bash
cd dashboard && npm run build
cd .. && pm2 start ecosystem.config.cjs
pm2 logs aegis-dashboard
```

`ecosystem.config.cjs` runs `dashboard/build/index.js` (adapter-node) with `PORT=5175`, `HOST=0.0.0.0`.

## Path aliases

`@` maps to `src/` — declared in `svelte.config.js` (SvelteKit alias) and `vite.config.ts` (Vitest alias). Both are required: Vite resolves it for the app and for tests.

## Svelte 5 conventions

- Components use runes (`$props()`, `$state`, `$derived`), not `export let`.
- `class` is a reserved word in Svelte 5, so component styles accept it as a prop via `let { class: className = '' } = $props()`.
- `@xyflow/svelte` v1 requires `nodeTypes` to map to Svelte **components**, and its `colorMode="dark"` prop is needed for dark-theme controls.

## Aturan angka di UI

Angka pada halaman depan dan panel mana pun harus berasal dari `lib/claims.ts` (dataset sintetis) atau diberi label eksplisit sebagai simulasi. Jangan menulis angka sebagai filler. Kalau nilainya tidak bisa ditelusuri ke sumber di repo, jangan tampilkan.

## Palet seri

Warna seri di komponen SvelteKit memakai set tervalidasi `#3987e5` / `#d95926` / `#199e70`. Set lama `#3b82f6` / `#22c55e` / `#eab308` gagal uji CVD pada `node scripts/validate_palette.js` — jangan dikembalikan tanpa diuji ulang.

Tiga warna seri itu untuk **kategori** (identitas). Untuk data **berurutan** (tahap, tier, level) pakai satu hue dengan ramp ordinal — contoh alur triase di `FlowCanvas.svelte` memakai `#9ec5f4` → `#184f95`. Uji dengan `node scripts/validate_palette.js "<ramp>" --mode dark --surface "#020617" --ordinal`; lightness harus monoton, celah ΔL antar langkah ≥ 0,06, dan langkah paling gelap tetap ≥ 2:1 terhadap permukaan.

Teks di atas fill berwarna punya aturan sendiri: langkah terang butuh tinta gelap, langkah gelap butuh putih. Hitung kontrasnya, jangan asal pakai `color: white`.

## Before changing the synthetic source

Obtain explicit approval. Recalculate its SHA-256, audit the schema, update `docs/DATA_SCHEMA.md`, and refresh the dashboard copy only as a byte-identical transfer.
