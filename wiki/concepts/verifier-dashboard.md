---
title: Verifier Dashboard
type: concept
tags: [sveltekit, svelte, vite, hitl, dashboard]
related:
  - "[[Aegis-JKN Overview]]"
  - "[[Dataset Contract]]"
  - "[[Academic Paper]]"
  - "[[Dashboard Development]]"
sources:
  - dashboard/src/
  - dashboard/docs/ARCHITECTURE.md
---

# Verifier Dashboard

The SvelteKit dashboard provides a claims queue with filter/search, an EMR evidence pane, a synthetic AI-evidence pane, conditional syndicate grouping, and note-required human decisions.

## Halaman depan internal

`src/routes/+page.svelte` bukan lagi halaman pemasaran generik. Isinya sekarang berasal dari dataset sintetis yang tertanam (`lib/claims.ts`), bukan angka karangan:

- Empat stat tile dihitung saat render: total klaim, jumlah antrean eskalasi, jumlah sindikat, dan nilai klaim yang tereskalasi.
- Baris "Distribusi antrean" menampilkan auto-clear / review / escalate lengkap dengan mean skor fraud, nilai klaim, dan lebar bar proporsional.
- Alur triase digambar oleh `FlowCanvas.svelte`: Klaim masuk → Tier-1 Aturan → Tier-2 XGBoost → Tier-3 GCN → Antrean verifikator. Node terakhir adalah penskalaan antrean, bukan persetujuan otomatis.

Nilai yang tidak berasal dari dataset tidak boleh muncul sebagai angka. Label seperti "2.4K dokter aktif" atau "99.7% uptime" tidak punya sumber dan sudah dihapus.

## Routes

| Route | Purpose |
|---|---|
| `/` | Internal landing page for the verifier tool. Every number on it is computed from the bundled synthetic dataset; CTAs link to `/demo`. |
| `/demo` | **Dashboard Verifikator Aegis-JKN** — the verifier workspace. |

## Data flow

`RawClaim` preserves the actual source fields. `lib/claims.ts` normalizes only in memory, filters/sorts locally, and exposes a selected claim to UI panels. The `auditLog` store (`store/auditLog.ts`, a Svelte `writable`) appends human actions to device-local `localStorage` scoped by source hash.

## Boundaries

The dashboard never trains or executes a model, never calls SATUSEHAT/V-Claim, and never auto-approves a claim. The syndicate graph is a transparent grouping derived from the existing `Sindikat` label, not discovered graph intelligence. Audit entries are device-local demonstration data, not a production audit trail.

## Diagram alur (FlowCanvas)

Rantai lima tahap digambar **vertikal**, bukan horizontal. Kanvas hero berada di kolom setengah (580px), dan rantai horizontal memaksa zoom `fitView` turun ke 0,54 — label 16px lalu ter-render 8,6px, terlalu kecil untuk dibaca. Vertikal + `fitViewOptions={{ minZoom: 0.75 }}` menjaga label tetap terbaca.

Tiga hal yang harus benar agar tepinya tegak lurus:

1. **Handle node di atas/bawah** (`Position.Top` / `Position.Bottom`). Handle kiri/kanan pada rantai vertikal membuat garis tepi melintang diagonal.
2. **Lebar node seragam** (190px). Posisi Svelte Flow adalah sudut kiri-atas, jadi node dengan lebar berbeda punya pusat berbeda.
3. **Ramp ordinal, bukan trio kategorikal.** Tahap berurutan, bukan identitas: satu hue biru terang→gelap (`#9ec5f4` → `#184f95`), lolos `validate_palette.js --ordinal` pada permukaan `#020617`. Warna teks tiap langkah ditentukan kontrasnya terhadap langkah itu — langkah terang memakai tinta gelap, bukan putih.

Diagram bersifat statis: `nodesDraggable={false}`, `nodesConnectable={false}`, `elementsSelectable={false}`. Pan/zoom tetap hidup. Minimap diberi warna node eksplisit — default-nya `rgb(43,43,43)` di atas latar `rgb(20,20,20)`, praktis tidak terbaca.

## Palet graf

Slot kategorikal yang dipakai di `ShapChart.svelte` dan `SyndicateNode.svelte` adalah `#3987e5` (topologi), `#d95926` (fitur), `#199e70` (semantik) — set yang sama dengan `landing/assets/landing.css`. Trio lama `#3b82f6` / `#22c55e` / `#eab308` gagal uji pemisahan CVD (ΔE 4.2 pada pasangan hijau-kuning) dan tidak boleh dipakai sebagai warna seri. Jalur `landing/` adalah acuan palet yang sudah tervalidasi.

## Local development

Run `cd dashboard && npm i && npm run dev` and open `http://localhost:5175`. See `dashboard/docs/README.md` and `dashboard/docs/DEPLOYMENT.md` for safeguards.
