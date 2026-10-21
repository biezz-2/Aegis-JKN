# Aegis-JKN Dashboard

**Dashboard Verifikator Aegis-JKN** adalah SPA client-side untuk menelaah **dataset klaim sintetis**. Ia membantu verifikator memprioritaskan pembacaan bukti; ia tidak terhubung ke SATUSEHAT, V-Claim, database, maupun layanan inferensi, dan tidak pernah menyetujui, menolak, atau menaikkan klaim secara otomatis.

> **AI memberi rekomendasi, bukan keputusan. Keputusan akhir ada pada verifikator.**

## Setup

```bash
cd dashboard
npm install
npm run dev        # http://localhost:5175
```

Perintah lain:

```bash
npm run typecheck  # svelte-check
npm test           # vitest run
npm run build      # vite build -> build/index.js (adapter-node)
```

Port dev dikunci **5175** (`strictPort`) di `vite.config.ts`.

## Rute aplikasi

| Rute | Halaman |
|---|---|
| `/` | Landing page publik (Aegis JKN Flow). Ketiga tombol mengarah ke `/demo`. |
| `/demo` | **Dashboard Verifikator Aegis-JKN** — antrean klaim, EMR, bukti AI, graf sindikat, tindakan HITL, dan audit lokal. |

## Deployment (PM2)

```bash
cd dashboard && npm run build
cd .. && pm2 start ecosystem.config.cjs   # PORT=5175, HOST=0.0.0.0
pm2 logs aegis-dashboard
```

`HOST=0.0.0.0` hanya membuat server dapat dijangkau; itu **bukan** autentikasi atau kontrol akses. Batasi TCP/5175 dengan firewall host ke jaringan tepercaya (LAN/tailnet).

Detail, termasuk kontrol yang wajib ada sebelum deploy non-demo, ada di [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Data sintetis

Sumber kanonik: `docs/datasets/klaim-aegis-jkn-dataset.json` (300 klaim sintetis). Salinan di `dashboard/src/data/` harus **byte-identik**; SHA-256 tercatat di `docs/DATA_SCHEMA.md`.

Dataset ini **tidak** memuat tarif INA-CBG pembanding, daftar graph edge produksi, maupun nilai SHAP numerik per fitur. UI tidak boleh mengarang nilai-nilai tersebut. Graf sindikat hanya muncul untuk label sindikat yang sudah ada dan ditandai sebagai kelompok sintetis.

Audit keputusan disimpan di `localStorage` browser untuk keperluan demonstrasi — itu **bukan** rekam audit produksi.

## Teknologi

- **Svelte 5** + SvelteKit
- **SvelteFlow** (`@xyflow/svelte`) — Flow builder premium
- **Tailwind CSS v4** + Shadcn Svelte
- **Lucide Svelte** — Icon set premium
- **Zod** + **Superforms** — Validasi form
- **Sonner** — Toaster notifikasi premium

## Desain Premium

- Color palette: Slate 950 + Blue/Cyan/Emerald gradient
- Typography: Geist + Inter variable
- Corner radius: 16px + 24px
- Shadows: 0 10px 15px -3px rgb(0 0 0 / 0.3)
- Animation: Tailwind animate-css + SvelteFlow edge animation

## Dokumentasi

- [Arsitektur](docs/ARCHITECTURE.md)
- [Tech stack](docs/TECH_STACK.md)
- [Panduan penggunaan dan pengembangan](docs/README.md)
- [Deployment internal](docs/DEPLOYMENT.md)
- [Kontrak dataset](../docs/DATA_SCHEMA.md)
