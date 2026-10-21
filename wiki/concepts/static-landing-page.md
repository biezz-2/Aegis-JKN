---
title: Static Landing Page
type: concept
tags: [landing, static-site, svg, charts, accessibility, no-dependencies]
related:
  - "[[Aegis-JKN Overview]]"
  - "[[Verifier Dashboard]]"
  - "[[Dashboard Development]]"
  - "[[Dataset Contract]]"
sources:
  - landing/index.html
  - landing/assets/landing.css
  - landing/assets/landing.js
---

# Static Landing Page

Halaman landing Aegis-JKN yang berdiri sendiri di `landing/`: HTML + CSS + JavaScript tanpa dependensi, tanpa build step, tanpa framework. Berdampingan dengan *showcase* MHGSL Next.js dan **Dashboard Verifikator** SvelteKit — ketiganya tidak saling menimpa.

## Struktur

| Path | Isi |
|---|---|
| `landing/index.html` | 1725 baris, 17 `<section>`, 26 `<a>`, 14 `<svg>` |
| `landing/assets/landing.css` | 1190 baris, design token (`:root` custom property) + tata letak |
| `landing/assets/landing.js` | 554 baris, dua graf SVG yang dibangun tangan |

Section bernomor `id` untuk navigasi anchor: `masalah`, `pilar`, `arsitektur`, `kamuflase`, `sindikat`, `pipeline`, `xai`, `hitl`, `kepatuhan`, `simulasi`, `kpi`, `perbandingan`, `risiko`, `roadmap`, `tim`, `cta`.

## Dua graf SVG

| Graf | Data | Fungsi |
|---|---|---|
| Kontribusi kanal per antrean | Rata-rata kontribusi Topologi / Fitur / Semantik | Slot kategorikal `--series-*` 1–3 |
| Skor fraud per antrean | Mean + rentang skor yang terobservasi | Palet status (hijau / kuning / merah) |

Kedua graf dibangun tanpa library. Setiap nilai yang digambar juga tersedia di tabel di bawah graf, jadi tooltip menambah informasi, bukan menjadi satu-satunya jalan accessing data. Ambang antrean (0,35 dan 0,70) digambar sebagai garis putus-putus, bukan hanya disebut di teks.

Angka pada graf dihitung dari 300 baris `dashboard/src/data/klaim-aegis-jkn-dataset.json` dan diverifikasi ulang terhadap file tersebut.

## Aturan implementasi

**`text-anchor` adalah atribut SVG, bukan properti CSS.** Menuliskannya lewat `node.style.textAnchor` diabaikan tanpa error — sumbu dan label pun diam-diam tidak ikut di-center. Gunakan `setAttribute('text-anchor', ...)`.

**Closure per-iterasi wajib pada loop `var`.** Handler yang dibuat di dalam loop `var` menangkap variabel loop yang bersifat function-scoped, sehingga setiap target hover menampilkan data iterasi terakhir. Bungkus dengan IIFE, atau pakai `let`.

**Handler lepas butuh `this` yang benar.** `tip.hide` yang dipasang lewat `addEventListener` menerima `this` = elemen listener, bukan objek Tooltip. Bind di konstruktor (`this.hide = this.hide.bind(this)`).

**Elemen di luar scope konstruktor disimpan di instance.** `holder` hanya ada di scope konstruktor; `show()` membutuhkannya, jadi simpan sebagai `this.holder`, bukan free variable.

## Verifikasi

Landing page diuji lewat Chromium sungguhan, bukan inspeksi markup:

| Cek | Hasil |
|---|---|
| Section / SVG / link | 17 / 14 / 26 |
| Error konsol | `[]` |
| Hover 12 hit target | masing-masing menampilkan grupnya sendiri |
| Tooltip hilang saat pointer leave & blur | ya |
| Tooltip tetap di dalam holder | ya |
| Viewport sempit (720px) | graf digeser horizontal (`overflow-x: auto`, `min-width: 660px`) |

## Hubungan dengan aplikasi utama

Landing page statis bersifat naratif dan tidak terhubung ke dashboard. Yang mengarah ke dashboard adalah CTA di `dashboard/src/routes/+page.svelte` (SvelteKit) — ketiga tombolnya menuju `/demo`. Landing page statis memakai anchor internal (`#arsitektur`, `#cta`) dan tidak pernah meninggalkan dokumen.
