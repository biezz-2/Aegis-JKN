---
title: Static Landing Page
type: concept
tags: [landing, static-site, svg, charts, accessibility, no-dependencies, deployment]
related:
  - "[[Aegis-JKN Overview]]"
  - "[[Verifier Dashboard]]"
  - "[[Dashboard Development]]"
  - "[[Dataset Contract]]"
sources:
  - landing/index.html
  - landing/assets/landing.css
  - landing/assets/landing.js
  - landing/serve.mjs
---

# Static Landing Page

Halaman landing Aegis-JKN yang berdiri sendiri di `landing/`: HTML + CSS + JavaScript tanpa dependensi, tanpa build step, tanpa framework. Berdampingan dengan *showcase* MHGSL Next.js dan **Dashboard Verifikator** SvelteKit — ketiganya tidak saling menimpa.

## Struktur

| Path | Isi |
|---|---|
| `landing/index.html` | 1725 baris, 17 `<section>`, 26 `<a>`, 12 `<svg>` (10 inline + 2 dari `landing.js`) |
| `landing/assets/landing.css` | design token (`:root` custom property) + tata letak |
| `landing/assets/landing.js` | 554 baris, dua graf SVG yang dibangun tangan |
| `landing/serve.mjs` | server statis tanpa dependensi (`node:http`), dilayani PM2 sebagai app `aegis-landing` di port **5176** |

Section bernomor `id` untuk navigasi anchor: `masalah`, `pilar`, `arsitektur`, `kamuflase`, `sindikat`, `pipeline`, `xai`, `hitl`, `kepatuhan`, `simulasi`, `kpi`, `perbandingan`, `risiko`, `roadmap`, `tim`, `cta`.

## Dua graf SVG

| Graf | Data | Fungsi |
|---|---|---|
| Kontribusi kanal per antrean | Rata-rata kontribusi Topologi / Fitur / Semantik | Slot kategorikal `--series-*` 1–3 |
| Skor fraud per antrean | Mean + rentang skor yang terobservasi | Palet status (hijau / kuning / merah) |

Kedua graf dibangun tanpa library. Setiap nilai yang digambar juga tersedia di tabel di bawah graf, jadi tooltip menambah informasi, bukan menjadi satu-satunya jalan accessing data. Ambang antrean (0,35 dan 0,70) digambar sebagai garis putus-putus, bukan hanya disebut di teks.

Angka pada graf dihitung dari 300 baris `dashboard/src/data/klaim-aegis-jkn-dataset.json` dan diverifikasi ulang terhadap file tersebut.

**Nama kanal ditulis di setiap bar, bukan hanya di grup pertama.** Identitas bar tidak boleh bergantung pada warna saja — label kanal (Topologi / Fitur / Semantik) muncul pada semua bar. Label langsung berupa angka hanya pada nilai ekstrem (puncak 0,305); sisanya dibaca dari sumbu, tooltip, dan tabel.

**Sumbu nilai pada graf horizontal adalah sumbu X.** Catatan di bawah graf menyebut "Sumbu X = …"; memakai "Sumbu Y" akan menyesatkan pembaca.

## Server statis

Landing page dilayani `landing/serve.mjs` — server `node:http` tanpa dependensi. Alasannya, `pm2 serve` bukan app yang bisa di-restart dari `ecosystem.config.cjs`; `serve.mjs` adalah entry point yang restartable dengan `autorestart`.

Dua aturan yang tidak boleh dilanggar di `serve.mjs`:

**Path harus diperiksa ulang terhadap root, bukan hanya dinormalisasi.** `normalize` saja belum cukup — `..%2f..%2f` bisa keluar dari akar setelah decode. `resolveSafe()` menormalisasi, resolve, lalu membandingkan hasilnya dengan `ROOT`; di luar itu dikembalikan `null` (→ 404).

**URL dashboard disuntik saat request, bukan ditulis mati di markup.** Placeholder `{{DASHBOARD_URL}}` di HTML diganti `DASHBOARD_URL` dari environment saat file `.html` dikirim. Jadi IP dan port tidak perlu di-hardcode di `index.html` dan satu env var cukup untuk memindahkan deployment.

## Aturan implementasi

**`text-anchor` adalah atribut SVG, bukan properti CSS.** Menuliskannya lewat `node.style.textAnchor` diabaikan tanpa error — sumbu dan label pun diam-diam tidak ikut di-center, dan nama kanal meluber keluar dari gutter-nya. Helper `text()` memisahkan keduanya: anchor lewat `setAttribute('text-anchor', ...)`, sisanya (`fill`, `fontSize`, `fontWeight`) lewat `node.style`.

**Closure per-iterasi wajib pada loop `var`.** Handler yang dibuat di dalam loop `var` menangkap variabel loop yang bersifat function-scoped, sehingga setiap target hover menampilkan data iterasi terakhir. Bungkus dengan IIFE, atau pakai `let`.

**Handler lepas butuh `this` yang benar.** `tip.hide` yang dipasang lewat `addEventListener` menerima `this` = elemen listener, bukan objek Tooltip. Bind di konstruktor (`this.hide = this.hide.bind(this)`).

**Elemen di luar scope konstruktor disimpan di instance.** `holder` hanya ada di scope konstruktor; `show()` membutuhkannya, jadi simpan sebagai `this.holder`, bukan free variable.

## Verifikasi

Landing page diuji lewat Chromium sungguhan, bukan inspeksi markup:

| Cek | Hasil |
|---|---|
| Section / SVG / link | 17 / 12 / 26 |
| Error konsol | `[]` |
| Hover 12 hit target | masing-masing menampilkan grupnya sendiri |
| Tooltip hilang saat pointer leave & blur | ya |
| Tooltip tetap di dalam holder | ya |
| Viewport sempit (720px) | graf digeser horizontal (`overflow-x: auto`, `min-width: 660px`) |

## Hubungan dengan aplikasi utama

Kedua aplikasi saling tertaut dua arah:

| Arah | Mekanisme | Sumber |
|---|---|---|
| Landing → Dashboard | Tombol "Buka Dashboard" di nav dan di section CTA, href berisi placeholder `{{DASHBOARD_URL}}` yang diganti server saat request | `landing/index.html` |
| Dashboard → Landing | Tautan "Ringkasan proyek & landing page" di hero, URL dibaca dari `env.PUBLIC_LANDING_URL` via `$env/dynamic/public` | `dashboard/src/routes/+page.svelte` |

`$env/dynamic/public` dibaca saat runtime, jadi perpindahan host landing page **tidak menuntut rebuild dashboard** — cukup `pm2 restart aegis-dashboard --update-env`.

Sisa CTA di `dashboard/src/routes/+page.svelte` tetap menuju `/demo` (route di dalam dashboard itu sendiri).

## Aturan overflow horizontal

Landing page wajib muat tanpa scroll horizontal. Tiga penyebab yang pernah muncul dan aturan yang menutupnya:

**Track grid `1fr` harus `minmax(0, 1fr)`.** `1fr` punya minimum `auto` (min-content), jadi kolom yang isinya `white-space: nowrap` akan memaksa track melebar melebihi viewport. `.grid-2`, `.grid-3`, `.hero-grid`, `.pipeline-row`, `.roadmap-row`, dan `.footer-grid` semuanya collapsed ke `1fr` di breakpoint — versi `minmax(0, 1fr)` wajib.

**Item flex/grid yang berisi `nowrap` butuh `min-width: 0`.** `.formula` memakai `white-space: nowrap` + `overflow-x: auto`; tanpa `min-width: 0` ia memakai min-width `auto` dan ikut melebar. Rumus lalu tetap bisa digeser di dalam kotaknya sendiri.

**Header flex tidak wrap.** Di bawah 640px sub-judul brand dan tombol nav non-CTA disembunyikan; yang tersisa hanya logo+nama dan tombol dashboard. Satu tombol nav tambahan saja sudah cukup untuk membuat baris melebihi lebar container.

Tabel lebar dan diagram SVG **boleh** melebihi lebar viewport asalkan berada di dalam container `overflow-x: auto` (`.table-scroll`, `.chart-scroll`, `.diagram`) — isinya ter-clip dan bisa digeser, sedangkan halaman itself tidak ikut bergeser.

