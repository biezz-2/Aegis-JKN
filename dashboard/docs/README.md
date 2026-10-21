# Aegis-JKN Verifier Dashboard

Internal, client-side verifier workspace for the **synthetic** Aegis-JKN dataset. It is separate from the public educational showcase and must not be treated as a production BPJS system.

> **AI memberikan rekomendasi, bukan keputusan. Keputusan akhir ada pada verifikator.**

## Quick start

```bash
cd dashboard
npm i
npm run dev
```

Open `http://localhost:5175`. Other commands:

```bash
npm run typecheck  # svelte-check
npm test           # vitest run
npm run build      # vite build -> build/index.js (adapter-node)
npm run preview    # serve the production build
```

## Routes

| Route | Halaman |
|---|---|
| `/` | Landing page publik (Aegis JKN Flow). Tombol "Mulai Trial Gratis", "Lihat Demo", dan "Mulai Integrasi Sekarang" mengarah ke `/demo`. |
| `/demo` | **Dashboard Verifikator Aegis-JKN** — antrean klaim, EMR, bukti AI, graf sindikat, tindakan HITL, dan audit lokal. |

## Navigation

1. Filter atau cari di **Antrean klaim** (kiri).
2. Pilih satu record untuk menyinkronkan pane EMR dan AI.
3. Baca bukti klinis, skor, rincian tiga saluran, prosa bukti SHAP, dan—bila ada—graf sindikat turunan label.
4. Klik **Setujui Klaim**, **Minta Konfirmasi RS**, atau **Tolak**.
5. Isi catatan verifikator. Aksi bersifat append-only di penyimpanan lokal browser dan muncul di **Audit lokal**.

## Deployment (PM2)

```bash
cd dashboard && npm run build
cd .. && pm2 start ecosystem.config.cjs   # port 5175
pm2 logs aegis-dashboard
```

`ecosystem.config.cjs` menjalankan `dashboard/build/index.js` dengan `PORT=5175` dan `HOST=0.0.0.0`.

## Akses LAN dan Tailscale

Server Vite dan aplikasi adapter-node mendengarkan pada semua interface (`0.0.0.0`). Akses dari perangkat lain dengan alamat host:

```text
http://<IP-LAN-host>:5175
```

Pastikan firewall host mengizinkan TCP pada port yang dipakai, dan hanya bagikan dashboard sintetis ini kepada perangkat LAN/Tailnet yang dipercaya. `0.0.0.0` hanya membuat server dapat dijangkau; ia bukan autentikasi atau kontrol akses.

## Data statement

The dashboard reads `src/data/klaim-aegis-jkn-dataset.json`, a byte-identical copy of the canonical source. It contains 300 synthetic claims. No network request, external model, SATUSEHAT integration, V-Claim integration, or remote audit service exists.

The data does not contain INA-CBG tariff values or graph edges. The UI shows only `Biaya Rp`; it never invents a tariff delta. The graph is rendered only for an existing syndrome label and is explicitly marked as an illustration from the synthetic grouping.

## Ringkasan Indonesia

Dashboard ini adalah purwarupa internal untuk menelaah bukti pada dataset sintetis. Keputusan klaim selalu memerlukan aksi dan catatan manusia. Audit browser tidak immutable dan tidak boleh digunakan sebagai bukti legal atau rekam keputusan produksi.
