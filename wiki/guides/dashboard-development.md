---
title: Dashboard Development
type: guide
tags: [development, verification, deployment]
related:
  - "[[Verifier Dashboard]]"
  - "[[Static Landing Page]]"
sources:
  - dashboard/package.json
  - dashboard/vite.config.ts
  - ecosystem.config.cjs
  - scripts/dev.mjs
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

## Running everything from the repo root

`npm install` at the root also installs `dashboard/` — the `postinstall` hook runs `prisma generate && npm install --prefix dashboard --no-audit --no-fund`. One command is enough for all three parts.

`npm run dev` at the root runs `scripts/dev.mjs`, a dependency-free orchestrator that spawns the showcase, the dashboard, and the landing server at once and prefixes their output with `[showcase]`, `[dashboard]`, and `[landing]`.

| Service | Dev port | Production port (PM2) |
|---|---|---|
| showcase (Next.js) | 3000, or the next free port | 3000 |
| dashboard (SvelteKit) | 5275 | 5175 |
| landing (static) | 5276 | 5176 |

Dev ports differ from the PM2 ports on purpose: Vite runs with `strictPort: true`, so reusing 5175 would fail to start while the production instance is still online.

The orchestrator checks each port before spawning and falls back to the next free one, so a port 3000 already taken by an unrelated process (e.g. a proxy for another project) does not break `npm run dev` — the startup summary prints the port that was actually used.

Cross-app links use the machine's LAN IPv4, so the landing → dashboard and dashboard → landing links keep working when opened from a phone on the same network, not just from `localhost`. Override with `DEV_SHOWCASE_PORT`, `DEV_DASHBOARD_PORT`, `DEV_LANDING_PORT`, or `DEV_PUBLIC_HOST`.

`Ctrl+C` terminates all three children.

## Deployment

```bash
cd dashboard && npm run build
cd .. && pm2 start ecosystem.config.cjs
pm2 logs aegis-dashboard
```

`ecosystem.config.cjs` manages two apps side by side:

| App | Script | Port | Type |
|---|---|---|---|
| `aegis-dashboard` | `dashboard/build/index.js` (adapter-node) | 5175 | internal tool |
| `aegis-landing` | `landing/serve.mjs` (node:http, no deps) | 5176 | public static showcase |

Both bind `HOST=0.0.0.0`. Separate ports, so no proxy rewrite is needed and each can be restarted independently. `aegis-landing` reads `DASHBOARD_URL`; `aegis-dashboard` reads `PUBLIC_LANDING_URL`.

See [[Static Landing Page]] for the placeholder substitution and the two-way link between them.

### PM2 "online" does not mean the port is listening

adapter-node registers a `SIGTERM` handler that calls `httpServer.close()`. If the process does not exit afterwards, the socket is closed but the process lingers — PM2 still reports `online` while the port is dead and the site is unreachable.

Check the listener directly instead of trusting the status:

```bash
ss -ltnp | grep 5175
```

If nothing is bound, `pm2 restart aegis-dashboard --update-env`.

**A restart is required after every rebuild.** adapter-node keeps the old build in memory; a new `npm run build` does not affect the running process.

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
