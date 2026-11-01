# Laporan Audit Kualitas Kode & Test - Aegis-JKN

Tanggal audit: 22 Oktober 2026
Kodebas: `N:\HEALTHKATHON\Aegis-JKN\` (branch `main`, commit `232ce79`, 133 file terlacak)
Spesifikasi acuan: `analysis/corpus/02-architecture.md`, `08-training-protocol.md`, `03-dataset-registry.md`, `10-simulation-dataset.md`
Mode: read-only. Tidak ada file yang diubah. Tidak ada dependency yang di-install.

---

## 1. Ringkasan Eksekutif

Aegis-JKN adalah **aplikasi visualisasi Next.js 16 (App Router) purely client-side** yang menampilkan data sintetis hardcoded. Ia bukan platform ML. Model MHGSL/GNN, XGBoost, SHAP, dan Late Fusion di dokumen spesifikasi **tidak ada satu pun yang diimplementasikan di repositori ini** - yang ada hanya visualisasi angka statis dan satu prototipe scoring JavaScript di dalam komponen upload CSV.

Hasil audit menunjukkan dua kelas masalah:

**Kelas A - Klaim spesifikasi yang tidak didukung bukti.** Dokumen `10-simulation-dataset.md` baris 154 mengklaim *"Unit test (tests/test_leakage.py) gagal keras jika kolom leakage masuk fitur"*. **Berkas tersebut tidak ada.** Tidak ada satu pun file Python, `configs/leakage.yaml`, `requirements.txt`, `pyproject.toml`, atau `data/raw/leakage_blocklist.yaml` di repositori. Tiga skrip `tests/*.sh` yang ada bahkan **tidak dapat dijalankan** - semuanya memanggil skrip di `../.zscripts/` yang tidak ada di repo (lihat §2).

**Kelas B - Quality gate yang dimatikan.** `next.config.ts` menyetel `typescript.ignoreBuildErrors: true`, sehingga `npm run build` **lolos** padahal `npx tsc --noEmit` melaporkan **8 error TypeScript**. `eslint.config.mjs` mematikan ~25 rule termasuk `no-explicit-any`, `ban-ts-comment`, dan `react-hooks/exhaustive-deps`. Hasilnya: lint **gagal** dengan 5 error, typecheck **gagal** dengan 8 error, build **lolos** secara semu - build masking, bukan build sehat.

### Tabel Severity

| Severity | Jumlah | Ringkasan |
|---|---|---|
| **CRITICAL** | 3 | Klaim `test_leakage.py` palsu; `ignoreBuildErrors` memblokir guard type-level; tidak ada test suite sama sekali (0 unit test untuk logika bisnis inti) |
| **HIGH** | 6 | Threshold risiko tidak konsisten di 4 tempat; Prisma schema orphan (model `User`/`Post` tidak/domain); 21 dependency tak terpakai; `noImplicitAny: false` + `no-explicit-any: off`; tidak ada CI; scoring fusion production-grade tidak ada |
| **MEDIUM** | 8 | 2 definisi `RiskLevel` duplikat; 3 salinan `RISK_COLORS`; 61 dari 74 komponen adalah `"use client"`; komponen 2.292 baris dengan 19 `useState`; `lib/db.ts` tidak pernah di-import; `api/route.ts` stub "Hello world"; tidak ada `loading.tsx`/`error.tsx`/`not-found.tsx` |
| **LOW** | 7 | 2 `@ts-expect-error` tidak terpakai; 3 key i18n hilang di interface `Dict`; `metadataBase`/`robots`/`alternates` tidak ada; 0 `aria-label` pada 31 `<button>`; `reactStrictMode: false`; bundle 2,2 MB tanpa dynamic import; `tailwindcss-animate` v3 + `tw-animate-css` v4 duplikat |

### Status build / lint / test

| Gerbang | Perintah | Exit | Status |
|---|---|---|---|
| Typecheck | `npx tsc --noEmit` | **1** | **GAGAL - 8 error** |
| Lint | `npm run lint` | **1** | **GAGAL - 5 error** |
| Build | `npm run build` | **0** | LOLOS, tetapi **masking** (`ignoreBuildErrors: true`) |
| Test | `npm test` | - | **SKRIP TIDAK ADA** |

---

## 2. Build & Test Inventory

### `npm run` (listing aktual)

```
Lifecycle scripts included in aegis-jkn@1.1.0:
  start         → next start
  postinstall   → prisma generate
available via `npm run-script`:
  dev           → next dev
  build         → next build
  lint          → eslint .
  db:push       → prisma db push --accept-data-loss
  db:generate   → prisma generate
  db:migrate    → prisma migrate dev
  db:reset      → prisma migrate reset
```

### TABEL Build & Test Inventory

| Script / tool | Ada? | Isi | Verdict |
|---|---|---|---|
| `dev` | Ya | `next dev` | OK |
| `build` | Ya | `next build` | Lolos, **tetapi masking type error** |
| `start` | Ya | `next start` | OK |
| `lint` | Ya | `eslint .` | **GAGAL, exit 1, 5 error** |
| `test` | **TIDAK** | - | **TIDAK ADA runner test apa pun** |
| `test:unit` / `test:e2e` / `test:coverage` | **TIDAK** | - | **TIDAK ADA** |
| `typecheck` / `type-check` | **TIDAK** | - | **TIDAK ADA** (harus manual `npx tsc --noEmit`) |
| `format` | TIDAK | - | Tidak ada (biome/prettier) |
| `postinstall` | Ya | `prisma generate` | OK, tapi tidak ada yang memakai DB |
| `db:push` / `db:migrate` / `db:reset` | Ya | perintah Prisma | **Berbahaya**: `--accept-data-loss` di `db:push`, tapi tidak ada model domain |
| `db:generate` | Ya | `prisma generate` | OK |
| Jest / Vitest / Playwright / Cypress | **TIDAK** | - | **Tidak ada di devDependencies** |
| pytest / unittest | **TIDAK** | - | **Tidak ada file `.py` sama sekali** |
| `tests/*.sh` | Ya (3 file) | Lihat §2b | **Tidak terkait dengan kode src, tidak bisa jalan** |
| CI (`.github/workflows`) | **TIDAK** | - | **TIDAK ADA direktori `.github/` sama sekali** |
| `vercel.json` | Ya | `{ framework: "nextjs" }` | Minimal, tanpa buildCommand/testCommand |

### 2b. Apa sebenarnya yang diuji oleh `tests/*.sh`

| File | Yang diuji | Verdict |
|---|---|---|
| `tests/database-runtime-build.sh` | Skrip `../.zscripts/database-runtime-build.sh` - membuat fake binary `bun` untuk memastikan `bun run db:push` dipanggil dengan `DATABASE_URL` SQLite absolut | **Tidak dapat dijalankan** - `../.zscripts/` tidak ada di repo. Tidak menyentuh satu baris pun `src/`. |
| `tests/python-runtime-build.sh` | Skrip `../.zscripts/python-runtime-build.sh` - menyalin `requirements.txt`/`.venv` ke build dir, mengabaikan `.venv/should-not-copy.py`, menangani proyek pyproject-only | **Tidak dapat dijalankan** - target `.zscripts/` tidak ada |
| `tests/python-runtime-container.sh` | Jalankan `python-runtime-build.sh` lalu `docker run` dengan image `z-ai-python-deploy-runner:test` untuk import `idna==3.10` | **Tidak dapat dijalankan** - target hilang **dan** butuh Docker + image privat |

Verifikasi:
```
$ ls -d .zscripts
ls: cannot access '.zscripts': No such file or directory
$ find . -maxdepth 3 -name "*.sh" -not -path "./node_modules/*"
./tests/database-runtime-build.sh
./tests/python-runtime-build.sh
./tests/python-runtime-container.sh
```
`git ls-files tests` → hanya 3 file `.sh` tersebut. **Ketiganya adalah tes harness build milik platform z-ai, bukan tes Aegis-JKN, dan semuanya menggantung pada direktori `.zscripts/` yang tidak ada dalam repositori.** Percobaan menjalankan `bash tests/database-runtime-build.sh` di mesin ini gagal (WSL timeout pada instance CreateVM).

**Kesimpulan: repositori ini memiliki 0 (nol) test otomatis yang dapat dieksekusi, dan 0 test yang menguji logika bisnis Aegis-JKN.**

---

## 3. Verifikasi `tests/test_leakage.py`

### **TIDAK ADA.**

Pencarian menyeluruh di `N:\HEALTHKATHON\Aegis-JKN\` (di luar `node_modules`):

| Artefak yang diklaim | Lokasi klaim | Status aktual |
|---|---|---|
| `tests/test_leakage.py` | `10-simulation-dataset.md:154` | **TIDAK ADA** |
| `configs/leakage.yaml` | `10-simulation-dataset.md:153` | **TIDAK ADA** (`configs/` tidak ada) |
| `data/raw/leakage_blocklist.yaml` | `10-simulation-dataset.md:190` | **TIDAK ADA** (`data/` tidak ada) |
| `data/raw/claims_300_v2.1.csv` | `10-simulation-dataset.md:184` | **TIDAK ADA** |
| `data/processed/features_300.parquet` | `10-simulation-dataset.md:192` | **TIDAK ADA** |
| `data/processed/graph_hetero.pt` | `10-simulation-dataset.md:194` | **TIDAK ADA** |
| Python / ML stack (PyTorch, PyG, XGBoost, sklearn, SHAP) | `10-simulation-dataset.md:160-175` | **TIDAK ADA** - nol `.py`, nol `requirements.txt`, nol `pyproject.toml` |

Bukti perintah:
```
find . -path ./node_modules -prune -o -name "*leakage*" -print   → (kosong)
find . -path ./node_modules -prune -o -name "test_*" -print        → (kosong)
find . -path ./node_modules -prune -o -name "*.test.*" -print       → (kosong)
Get-ChildItem -Recurse -Include *.py,requirements.txt,pyproject.toml
  → hanya node_modules/flatted/python/flatted.py (dependensi)
```

### Konsekuensi ke klaim spesifikasi

1. **Anti-leakage tidak dijamin oleh kode apa pun.** `03-dataset-registry.md` §7 menetapkan daftar blokir (Skor Fraud, Risiko, Status, Sinyal SHAP, Kontribusi Saluran, Modus, Sindikat, Alasan). Tidak ada kode yang menegakkan daftar ini. Tidak ada konfigurasi yang mendefinisikannya.
2. **Kriteria penerimaan "Integritas Data: 300 baris utuh, 0 kebocoran fitur"** dalam `10-simulation-dataset.md` **tidak dapat diverifikasi** - tidak ada yang mengukurnya.
3. **Tidak ada pipeline ML di repo ini sama sekali.** Fase 0–4 dalam rencana 8 minggu, XGBoost/MLP baseline, MHGSL PyG, SHAP per-saluran, GroupKFold - seluruhnya **berada di luar repositori**. Repo ini hanya *viewer* atas hasil yang di-hardcode.
4. **Angka di UI tidak dapat diaudit.** `oasis-data.ts` memuat `det_rate: 100`, `accuracy: 93`, `status: "SESUAI"`, `kontra_ok: 8/8` - semua konstanta hardcoded, tanpa artefak eksperimen yang dirujuk `02-architecture.md` §5.5 (`experiment_manifest.json`, checksum dataset, ID split, log metrik).
5. **Rekomendasi untuk dokumen:** kalimat di `10-simulation-dataset.md:154` harus diberi status "RENCANA ( Fase 0)" dan tidak boleh dibaca sebagai kapabilitas yang sudah ada. Audit ini merekomendasikan koreksi eksplisit pada baris tersebut.

---

## 4. Hasil typecheck / lint / build

### 4.1 `npx tsc --noEmit` → **EXIT CODE 1, 8 ERROR**

```
examples/websocket/frontend.tsx(4,20): error TS2307: Cannot find module 'socket.io-client' or its corresponding type declarations.
examples/websocket/server.ts(2,24): error TS2307: Cannot find module 'socket.io' or its corresponding type declarations.
src/components/mhgsl/fraud-drilldown-modal.tsx(120,19): error TS2578: Unused '@ts-expect-error' directive.
src/components/mhgsl/i18n.tsx(386,3): error TS2561: Object literal may only specify known properties, but 'mathTitle2b' does not exist in type 'Dict'. Did you mean to write 'mathTitle2'?
src/components/mhgsl/i18n.tsx(734,3): error TS2561: Object literal may only specify known properties, but 'mathTitle2b' does not exist in type 'Dict'. Did you mean to write 'mathTitle2'?
src/components/mhgsl/roadmap.tsx(71,50): error TS2551: Property 'roiTitle3' does not exist on type 'Dict'. Did you mean 'roiTitle1'?
src/components/mhgsl/roadmap.tsx(71,71): error TS2551: Property 'roiTitle4' does not exist on type 'Dict'. Did you mean 'roiTitle1'?
src/components/mhgsl/simulation.tsx(337,23): error TS2578: Unused '@ts-expect-error' directive.
```

Klasifikasi:
- **2× TS2307** - `examples/websocket/*` mengimpor `socket.io` yang tidak ada di `package.json`. Contoh tidak pernah dibuild, tetapi `tsconfig.json` `include: ["**/*.ts", "**/*.tsx"]` menyertakannya, sehingga `tsc` di level repo selalu gagal.
- **2× TS2561 / 2× TS2551** - bug i18n nyata: `mathTitle2b` ada di literal ID (`:386`) dan EN (`:734`) tapi **tidak ada di interface `Dict`** (`:98-99` hanya `mathTitle1`, `mathTitle2`). `roiTitle3`/`roiTitle4` dipakai di `roadmap.tsx:71` tapi interface hanya mendeklarasikan `roiTitle1`, `roiTitle2` (`:149-150`). Artinya **4 string sudah hardcoded di komponen, melewati i18n** - string `"ke"`/`"to"` juga inline di `roadmap.tsx:69`.
- **2× TS2578** - `@ts-expect-error` yang tidak lagi diperlukan karena `as React.CSSProperties` sudah menyelesaikan masalahnya. Direktif basi.

### 4.2 `npm run lint` → **EXIT CODE 1, 5 ERROR**

```
✖ 5 problems (5 errors, 0 warnings)
```
Seluruh 5 error adalah rule `react-hooks/set-state-in-effect` (React Compiler-era rule, aktif di `eslint-config-next` v16):

| File | Baris | Pola |
|---|---|---|
| `src/components/dataset/dataset-explorer.tsx` | 337 | `setCurrentPage(1)` sinkron dalam effect |
| `src/components/mhgsl/i18n.tsx` | 894 | `setLangState(stored)` sinkron dalam effect |
| `src/components/mhgsl/theme-toggle.tsx` | 14 | `React.useEffect(() => setMounted(true), [])` |
| `src/components/ui/carousel.tsx` | 98 | `onSelect(api)` sinkron dalam effect |
| `src/hooks/use-mobile.ts` | 14 | `setIsMobile(...)` sinkron dalam effect |

Kelima pola adalah "setState sinkron dalam effect" → menyebabkan cascading render. Bukan crash, tapi performance. Tidak ada `console` warning/error yang tersisa.

**Catatan konfigurasi:** `eslint.config.mjs` mematikan rule secara masif - `no-explicit-any: off`, `ban-ts-comment: off`, `no-unused-disable-directive: off`, `react-hooks/exhaustive-deps: off`, `react-hooks/purity: off`, `react-compiler/react-compiler: off`, `no-console: off`, `no-empty: off`, `prefer-const: off`, `no-unused-vars: off`.Efeknya: lint yang "hanya" melaporkan 5 error ini adalah hasil **setelah** ~25 guard dimatikan. Guard yang paling berbahaya dimatikan: `no-explicit-any` (menjadikan `any` legal) dan `exhaustive-deps` (menjadikan stale-closure bug tak terdeteksi).

### 4.3 `npm run build` → **EXIT CODE 0 (LOLOS)**

```
▲ Next.js 16.4.0 (Turbopack)
✓ Running next.config.ts took 2.3s
  Creating an optimized production build ...
✓ Compiled successfully in 93s
  Skipping validation of types          ← kuncinya
  Finished TypeScript config validation in 683ms ...
✓ Generating static pages using 7 workers (6/6) in 23.6s
  Finalizing page optimization ...

Route (app)
┌ ○ /
├ ○ /_not-found
├ ƒ /api
├ ○ /dataset
└ ○ /simulasi
```

**Build produksi benar-benar lolos secara teknis, tetapi hanya karena `typescript.ignoreBuildErrors: true` di `next.config.ts`.** Baris `Skipping validation of types` adalah bukti eksplisit bahwa 8 error typecheck di §4.1 dilewati tanpa komplain. Menghapus satu baris itu akan membuat build gagal.

Konfigurasi lain yang melemahkan build:
- `reactStrictMode: false` - React Strict Mode mati, bug render ganda tidak terdeteksi di dev.
- `next.config.ts` **tidak** punya `images.remotePatterns` - tidak relevan saat ini karena tidak ada `next/image` (0 penggunaan), tapi `icons.icon` di `layout.tsx` menunjuk URL eksternal `https://z-cdn.chatglm.cn/z-ai/static/logo.svg` yang dimuat sebagai favicon browser, bukan lewat optimizer.

---

## 5. Anti-Pattern Audit

### TABEL Temuan Anti-Pattern

| Temuan | Jumlah | Lokasi | Dampak |
|---|---|---|---|
| `@ts-expect-error` tidak terpakai | 2 | `src/components/mhgsl/fraud-drilldown-modal.tsx:120`, `src/components/mhgsl/simulation.tsx:337` | **Sedang** - error typecheck; indikasi directive dipinding tanpa verifikasi |
| `any` eksplisit (TS + eslint) | 5 | `src/components/oasis/oasis-dashboard.tsx:354, 420, 480, 580, 633` (semua di `formatter` recharts + `setActiveTab(v as any)`) | **Tinggi** - `oasis-dashboard.tsx:354` melemahkan tipe state tab; 4 `formatter` kehilangan tipe payload |
| `@ts-ignore` | 0 | - | Aman |
| `eslint-disable` inline | 0 | - | Aman |
| `TODO` / `FIXME` / `HACK` / `XXX` | **0** | - | Bagus - kode bersih dari debt marker |
| `console.*` di `src/` | **0** | - | Bagus - tidak ada debug log tersisa |
| `catch` kosong | 0 | - | Bagus (1 `catch {}` di `data-uploader.tsx:226` sudah menangani error) |
| Magic number di logika scoring | 8 | `src/components/mhgsl/data-uploader.tsx:117, 128-131, 137` | **Tinggi** - bobot fusion `0.38/0.41/-0.12/0.3` dan ambang `0.85/0.65/0.4` inline, tanpa konstanta bernama / versi |
| Deep nesting (indent ≥10 spasi) | 26 baris | dominan di `dataset-explorer.tsx` | **Sedang** - tabel+filter+modal dalam satu file |
| Komponen > 500 baris | 6 | `notion-datasets.ts` (9.403, data), `dataset-explorer.tsx` (2.292), `oasis-dashboard.tsx` (1.168), `i18n.tsx` (909), `oasis-data.ts` (893), `ui/sidebar.tsx` (726), `multi-channel-graph.tsx` (542) | **Tinggi** - `dataset-explorer.tsx` 2.292 baris + 19 `useState` |
| Duplikasi definisi tipe | 2 | `src/types/dataset.ts:1` vs `src/components/mhgsl/data.ts:5` - keduanya `export type RiskLevel = "low"\|"medium"\|"high"\|"fraud"` | **Tinggi** - divergensi label guaranteed |
| Duplikasi peta warna risiko | 3 | `data-uploader.tsx:151-154`, `fraud-drilldown-modal.tsx:48-51`, `multi-channel-graph.tsx:33-36` - identik 4/4 baris | **Sedang** - harus diubah di 3 tempat |
| Duplikasi i18n inline | 4 key | `i18n.tsx:386, 734` (`mathTitle2b`), `roadmap.tsx:71` (`roiTitle3/4`), `roadmap.tsx:69` (`"ke"`/`"to"` inline) | **Sedang** - ID/EN bisa berbeda diam-diam |
| `noImplicitAny: false` | 1 | `tsconfig.json:16` | **Tinggi** - implisit `any` legal di seluruh repo |
| `no-explicit-any: off` + `ban-ts-comment: off` | 2 | `eslint.config.mjs:10, 13` | **Tinggi** |
| `react-hooks/exhaustive-deps: off` | 1 | `eslint.config.mjs:19` | **Tinggi** - stale closure tak terdeteksi |
| `ignoreBuildErrors: true` | 1 | `next.config.ts:6` | **CRITICAL** - menutupi type error |
| `reactStrictMode: false` | 1 | `next.config.ts:10` | **Sedang** |
| `useState` per file | 67 total | `dataset-explorer.tsx` = **19** | **Tinggi** - state machine implisit, sulit diuji |
| `"use client"` | 61 / 74 tsx | termasuk `page.tsx` root, `layout.tsx` chain | **Tinggi** - seluruh 3 route terkirim sebagai JS bundle; tidak ada server component yang leveraging data |

### Duplikasi data - ringkas

| Data | Lokasi | Ukuran | Nature |
|---|---|---|---|
| 300 klaim Notion | `src/data/notion-datasets.ts:402` (`NOTION_CLAIMS_DATASET`) | ~9.403 baris file | Hardcoded TS object, tipenya `ClaimRecord[]` |
| 33 entri riset | `src/data/notion-datasets.ts:3` (`NOTION_RESEARCH_DATASET`) | idem | Hardcoded |
| 100 klaim simulasi | `src/data/oasis-data.ts:77` (`OASIS_DATA`) | 893 baris | Hardcoded, `status: "SESUAI"` |
| Data visualisasi MHGSL | `src/components/mhgsl/data.ts` (27 export) | 519 baris | Hardcoded di folder komponen, bukan `src/data/` |
| Kontrak data | `docs/api/data-contracts.md` | - | Ada di docs, tapi tidak ada tipe/validator yang mengikatnya |

**Verifikasi konsistensi dataset terhadap `03-dataset-registry.md`:**
- label risiko: low 240 / medium 10 / high 14 / fraud 36 → **cocok** dengan §3.2 (240/10/14/36).
- status: auto_clear 240 / review 24 / escalate 36 → **cocok**.
- total nominal: Rp 3.526.650.000 → **cocok** dengan §3.3.
- Borderline check: skor 0.40 → `medium`, 0.62 → `high`, 0.80 → `fraud`; tidak ada skor di 0.15–0.39 maupun 0.81–0.79 yang membuat celah. Konsisten dengan definisi "versi aktif".

**Jadi data hardcoded-nya sendiri akurat terhadap registry - masalahnya adalah tidak ada kode yang menjaga akurasi itu.**

---

## 6. Data Layer & State Management

### TABEL Data Layer

| Aspek | Temuan | Lokasi | Verdict |
|---|---|---|---|
| API route | `GET /api` mengembalikan `{ message: "Hello, world!" }` | `src/app/api/route.ts` | **Stub.** Tidak ada endpoint data, health-check, atau auth. Route `ƒ (Dynamic)` di build tapi serves nothing useful. |
| Prisma schema | Provider `sqlite`, 2 model: `User`, `Post` | `prisma/schema.prisma` | **ORPHAN.** Tidak ada model `Claim`, `Faskes`, `Patient`, `Score`, `Syndicate`. Kolom `User.email` unik + `Post.authorId` tanpa relasi foreign key - bukan domain Aegis-JKN sama sekali. |
| Prisma client | `src/lib/db.ts` - `new PrismaClient({ log: ['query'] })` + global-singleton pattern | `src/lib/db.ts` | **Tidak pernah di-import.** Nol file di `src/` mengimpor `@/lib/db`. Dead code. |
| Runtime Prisma | `log: ['query']` aktif di produksi | `src/lib/db.ts:10` | **Tinggi** - kalau suatu hari dipakai, log query production akan membanjiri log &.URL meng-sensitive |
| Data domain | 4 file, 100% hardcoded | `src/data/notion-datasets.ts`, `src/data/oasis-data.ts`, `src/components/mhgsl/data.ts` | Tidak ada fetch, tidak ada loader, tidak ada RSC data layer |
| State management | Nol library yang dipakai | - | `zustand` & `@tanstack/react-query` **terpasang tapi nol import**. Semua state lokal `useState` (67 pemakaian) |
| Server Actions | Tidak ada | - | Nol `use server` |
| Middleware | Tidak ada | - | Nol `middleware.ts` |
| Auth | `next-auth` **terpasang tapi nol import** | - | Tidak ada proteksi route. Jika route bertipe data sensitif ditambahkan, akan terbuka. |

**Kesimpulan: ini adalah SPA statis yang di-host di Next.js.** Tidak ada server/API layer sungguhan, tidak ada persistence, tidak ada auth. Prisma adalah sisa template boilerplate.

**Catatan `02-architecture.md` §3.1** ("lapisan ingest dan validasi": validasi tipe, rentang, kode, nilai wajib; tandai missing; buat identitas analitik; tolak skema tidak sesuai) - **tidak ada implementasinya**. Upload CSV di `data-uploader.tsx` melakukan parseCSV ringan tanpa validasi rentang kode ICD-10/ICD-9, tanpa tanda missingness, dan menerima skema apa pun yang punya kolom yang cocok.

---

## 7. Type Safety & Threshold Consistency

### 7.1 Tipe domain

| Entitas | Tipe ada? | Lokasi | Catatan |
|---|---|---|---|
| `ClaimRecord` | **Ya** | `src/types/dataset.ts:4` | 28 field, lengkap & good |
| `ResearchRecord` | **Ya** | `src/types/dataset.ts:45` | Lengkap |
| `RiskLevel` | **Ya, TERDUPLIKASI** | `src/types/dataset.ts:1` DAN `src/components/mhgsl/data.ts:5` | **2 definisi identik.** `data.ts` mendefinisikan sendiri alih-alih meng-import dari `@/types/dataset`. |
| `ClaimStatus` | **Ya** | `src/types/dataset.ts:2` = `"auto_clear" \| "review" \| "escalate"` | Sesuai spec §5.1 (terpisah dari risk label) - benar |
| `SentimentType` | Ya | `src/types/dataset.ts:3` | `"positif" \| "netral" \| "negatif"` |
| `Patient` | **TIDAK** | - | Tidak ada tipe patient, hanya string `pasien` |
| `Faskes` | **TIDAK** | - | Tidak ada tipe faskes |
| `Practitioner` / `Doctor` | **TIDAK** | - | Tidak ada tipe |
| `Score` | **TIDAK** | - | Tidak ada; skor = `number` telanjang |
| `Syndicate` | **TIDAK** | - | `sindikat: string \| null` |
| `Edge` / graph node | Ya (lokal) | `src/components/mhgsl/data.ts:68, 78` (`GraphNode`, `GraphEdge`) | Tidak ada tipe `HeteroData`/channel |

**Tipe label risiko ada dan lengkap** - memenuhi kebutuhan §7. Yang bermasalah adalah **duplikasi definisi**, sehingga perbaikan label di satu tempat bisa tidak berlaku di tempat lain.

### 7.2 TABEL Threshold - lokasi, nilai, status konsistensi

| Threshold | Lokasi | Nilai | Status konsistensi |
|---|---|---|---|
| Batas fraud (label) | `src/components/mhgsl/data-uploader.tsx:137` | `>= 0.85 → fraud` | ⚠️ **INKONSISTEN** dengan `oasis-dashboard.tsx:94-97` yang memakai `Fraud (>0.8)` |
| Batas high | `data-uploader.tsx:137` | `>= 0.65 → high` | ⚠️ **INKONSISTEN** dengan `oasis-dashboard.tsx:96` (`High (0.6-0.8)`) |
| Batas medium | `data-uploader.tsx:137` | `>= 0.4 → medium` | ⚠️ **INKONSISTEN** dengan `oasis-dashboard.tsx:95` (`Medium (0.35-0.6)`) |
| Batas low | `data-uploader.tsx:137` | `< 0.4 → low` | ⚠️ **INKONSISTEN** dengan `oasis-dashboard.tsx:94` (`Low (<0.35)`) |
| Batas risiko dataset | `src/data/notion-datasets.ts` (300 baris) | low <0.4, medium 0.4–0.61, high 0.62–0.79, fraud ≥0.80 | Konsisten dengan `oasis-dashboard` (0.35/0.6/0.8), **tidak** dengan `data-uploader` (0.4/0.65/0.85) |
| Bobot fusion late | `data-uploader.tsx:128-131` | feature `0.38`, semantic `0.41`, topology `-0.12`, bias `0.30` | ⚠️ Hardcoded inline, tanpa versi. Bandingkan `oasis-data.ts:81` `theta_feat: 0.85` - **nilai berbeda, konteks berbeda** (theta kemiripan vs bobot kanal) tapi tidak terdokumentasi |
| Bobot topologi | `data-uploader.tsx:99` | `Math.min(1, conc * 3)` | Magic number, tanpa konstanta |
| Normalisasi fitur | `data-uploader.tsx:117` | `Math.max(0, (avgSim - 0.6) * 2.5)` | Magic number, tanpa konstanta |
| Bobot semantik | `data-uploader.tsx:125` | `0.9 / 0.4 / 0.1` | Magic number, tanpa konstanta |
| Bobot kanal simulasi | `src/data/oasis-data.ts:81-82` | `theta_feat: 0.85`, `gamma_text: 0.1` | Hardcoded di data file; `gamma_text: 0.1` = 10% untuk kanal teks - **sangat besar** untuk kanal yang diklaim "opsional"/fallback |
| Ambang dump data | `oasis-data.ts:234-352` | `semantik: 0.6` (17×), `topologi: 0.8` | Hardcoded per-klaim, tanpa sumber |
| Threshold SHAP | `notion-datasets.ts` | `kontribusiSaluran: "T 0.32 · F 0.35 · S 0.26"` (string) | ⚠️ Kontribusi kanal disimpan sebagai **string**, bukan angka - tidak bisa dihitung/diuji |
| Threshold sentimen | - | **TIDAK ADA** | `sentiment` disimpan pre-komputasi (`skorSentimen` + `sentiment` string). Tidak ada kode yang memetakan skor→label, jadi konsistensi 300 baris **tidak dapat diverifikasi** |

### 7.3 Verifikasi apakah ambang dataset punya celah/tumpang tindih

Saya menghitung seluruh pasangan `(skorFraud, risiko)` dari 300 baris `notion-datasets.ts`:
```
0.04–0.14 → low     (240 baris)
0.40–0.53 → medium  (10 baris)
0.62–0.79 → high    (14 baris)
0.80–0.95 → fraud   (36 baris)
```
**Tidak ada celah, tidak ada tumpang tindih.** Data bersih secara numerik. Yang bermasalah adalah **tiga definisi ambang yang berbeda hidup berdampingan** (`data-uploader` 0.4/0.65/0.85, `oasis-dashboard` 0.35/0.6/0.8, dataset aktual 0.4/0.62/0.80).

> `03-dataset-registry.md` §4 secara eksplisit menuntut: *"Ambang skor harus disimpan di satu tempat dan diberi versi. Batas interval perlu ditulis tanpa celah atau tumpang tindih."* - **Persyaratan ini belum terpenuhi.** Tidak ada file konfigurasi ambang di repositori.

---

## 8. Struktur Next.js & Route Files

### TABEL Route Files

| Route | `page.tsx` | `loading.tsx` | `error.tsx` | `not-found.tsx` | Metadata | Build |
|---|---|---|---|---|---|---|
| `/` | Ya (`src/app/page.tsx`, `"use client"`) | ❌ | ❌ | ❌ | ❌ (metadata hanya di layout) | `○ Static` |
| `/dataset` | Ya (`src/app/dataset/page.tsx`) | ❌ | ❌ | ❌ | ✅ lengkap: title, description, keywords (10), openGraph | `○ Static` |
| `/simulasi` | Ya (`src/app/simulasi/page.tsx`) | ❌ | ❌ | ❌ | ✅ lengkap: title, description, keywords (7) - **tanpa openGraph** | `○ Static` |
| `/api` | `route.ts` (GET stub) | - | - | - | - | `ƒ Dynamic` |
| `/_not-found` | - | ❌ | ❌ | ❌ root-level | - | `○ Static` |

**Total file route khusus: 0.** Tidak ada satu pun `loading.tsx`, `error.tsx`, `not-found.tsx`, `global-error.tsx`, atau `template.tsx` di seluruh `src/app/`.

### Metadata & SEO

| Aspek | Status |
|---|---|
| `metadataBase` | ❌ **Tidak ada.** `openGraph.url` di `layout.tsx` = `https://chat.z.ai` (URL placeholder vendor, bukan domain Aegis-JKN) → OG image absolut akan salah resolve |
| `robots` | ❌ Tidak ada |
| `alternates.canonical` | ❌ Tidak ada |
| `viewport`/`themeColor` | ❌ Tidak ada |
| `openGraph` | ✅ di `layout.tsx` + `/dataset`; ❌ di `/simulasi` |
| `twitter` | ✅ di `layout.tsx`; ❌ di `/dataset` & `/simulasi` |
| `icons` | ⚠️ `icon` menunjuk `https://z-cdn.chatglm.cn/z-ai/static/logo.svg` - **logo CDN pihak ketiga**, bukan aset repo. Repo punya `public/logo.svg` yang **tidak dipakai** |
| `sitemap.ts` / `robots.ts` | ❌ Tidak ada |
| JSON-LD structured data | ❌ Tidak ada (padahal kontennya bergaya Wizard-of-Oz indeksi-friendly, schema.org `SoftwareApplication`/`Dataset` cocok) |

### Struktur & bundle

- **61 dari 74 file `.tsx` diberi `"use client"`**, termasuk `src/app/page.tsx` (root route). Konsekuensi: tidak ada server component yang menangani data; seluruh 3 route jadi JS bundle penuh.
- **`src/app/page.tsx` mengimpor 12 komponen `mhgsl/*` sekaligus**, termasuk `MultiChannelGraph` (542 baris), `Simulation` (457), `Comparison` (475), `FraudRing` (430) - semuanya berisi `recharts` + `framer-motion`. **Tidak ada `next/dynamic` / `lazy()` di seluruh repo** (0 hasil grep). Chunk terberat: 466 KB + 412 KB + 224 KB + 182 KB. Total `.next/static` = **2,2 MB**.
- `src/components/ui/` berisi 48 file shadcn boilerplate. Yang benar-benar dipakai: dialog, dropdown-menu, select, tabs, tooltip, switch, input, card, badge, button, checkbox, label, separator, progress, popover, accordion, alert-dialog, hover-card, menubar, scroll-area, radio-group, toggle, toggle-group, slider, avatar, aspect-ratio, collapsible, command, carousel, calendar, drawer, input-otp, resizable-panels, table, sonner, chart, toast, toaster, sidebar, context-menu, sheet, form. Hampir semuanya dipakai ≥1 kali.
- **0 file `.test.*` / `.spec.*` / `__tests__`** di repo - tidak ada test komponen, test hook, atau test util.

---

## 9. Dependency Audit

### TABEL Dependency Audit

| Dep | Versi installed | Dipakai? | Catatan |
|---|---|---|---|
| `next` | 16.4.0 | ✅ | Inti. `reactStrictMode: false` |
| `react` / `react-dom` | 19.3.0 | ✅ | react-dom via `next` (import eksplisit tidak ada → normal) |
| `typescript` | 5.9.3 | ✅ | Dev. `noImplicitAny: false` |
| `eslint` | 9.39.5 | ✅ | Dev |
| `eslint-config-next` | 16.1.1 | ✅ | Dev. Dipakai, tapi ~25 rule dimatikan manual |
| `@tailwindcss/postcss`, `tailwindcss` | 4.3.3 | ✅ | Tailwind v4 |
| `tw-animate-css` | 1.3.5 | ✅ | Di-import `globals.css` |
| `tailwindcss-animate` | 1.0.7 | ⚠️ | **Duplikat** - plugin Tailwind **v3**, dipakai di `tailwind.config.ts` bersamaan `tw-animate-css` (v4). Dua sistem animasi. V3 tidak kompatibel penuh dengan v4. |
| `@prisma/client` | 6.19.3 | ⚠️ | Hanya di `src/lib/db.ts` yang **tidak pernah di-import**. 0 query. |
| `prisma` | 6.19.3 | ⚠️ | Dev-dep-as-dep. Hanya untuk `generate`. Tidak ada migrasi (`prisma/migrations/` tidak ada). |
| `@radix-ui/react-*` (28 paket) | various | ✅ | Semua dipakai via `src/components/ui/*` |
| `class-variance-authority` | 0.7.1 | ✅ | 8 file |
| `clsx` | 2.1.1 | ✅ | 1 file |
| `tailwind-merge` | 3.3.1 | ✅ | 1 file (`lib/utils.ts`) |
| `lucide-react` | 0.525.0 | ✅ | 39 file |
| `framer-motion` | 12.43.0 | ✅ | 19 file - **sumber chunk 466 KB** |
| `recharts` | 2.15.4 | ✅ | 3 file - **sumber chunk 412 KB**. v2 (bukan v3) |
| `next-themes` | 0.4.6 | ✅ | 4 file |
| `sonner` | 2.0.6 | ✅ | 3 file |
| `cmdk` | 1.1.1 | ✅ | `ui/command.tsx` |
| `embla-carousel-react` | 8.6.0 | ✅ | `ui/carousel.tsx` |
| `input-otp` | 1.4.2 | ✅ | `ui/input-otp.tsx` |
| `react-day-picker` | 9.8.0 | ✅ | `ui/calendar.tsx` |
| `react-hook-form` | 7.60.0 | ✅ | `ui/form.tsx` |
| `react-resizable-panels` | 3.0.3 | ✅ | `ui/resizable-panels.tsx` |
| `vaul` | 1.1.2 | ✅ | `ui/drawer.tsx` |
| `@dnd-kit/core` | 6.3.1 | ❌ | **TIDAK DIPAKAI** |
| `@dnd-kit/sortable` | 10.0.0 | ❌ | **TIDAK DIPAKAI** |
| `@dnd-kit/utilities` | 3.2.2 | ❌ | **TIDAK DIPAKAI** |
| `@hookform/resolvers` | 5.1.1 | ❌ | **TIDAK DIPAKAI** |
| `@mdxeditor/editor` | 3.39.1 | ❌ | **TIDAK DIPAKAI** - dep besar (~1 MB+ tree), tidak ada MDX di repo |
| `@reactuses/core` | 6.0.5 | ❌ | **TIDAK DIPAKAI** |
| `@tanstack/react-query` | 5.104.1 | ❌ | **TIDAK DIPAKAI** |
| `@tanstack/react-table` | 8.21.3 | ❌ | **TIDAK DIPAKAI** - tabel di `dataset-explorer.tsx` dibuat manual |
| `date-fns` | 4.1.0 | ❌ | **TIDAK DIPAKAI** |
| `next-auth` | 4.24.15 | ❌ | **TIDAK DIPAKAI** - **risiko keamanan implisit**:Dependency auth terpasang tapi tidak aktif = ilusi proteksi |
| `next-intl` | 4.3.4 | ❌ | **TIDAK DIPAKAI** - i18n dibuat manual (`i18n.tsx`), despite `next-intl` being installed |
| `react-markdown` | 10.1.0 | ❌ | **TIDAK DIPAKAI** |
| `react-syntax-highlighter` | 15.6.1 | ❌ | **TIDAK DIPAKAI** - **berisiko**: `<code>` dari `react-markdown` tanpa sanitasi bisa XSS, tapi react-markdown justru tidak dipakai |
| `sharp` | 0.34.5 | ❌ | **TIDAK DIPAKAI** - biasanya otomatis oleh Next; dependency eksplisit tidak perlu |
| `uuid` | 11.1.0 | ❌ | **TIDAK DIPAKAI** - `crypto.randomUUID()` tersedia native |
| `z-ai-web-dev-sdk` | 0.0.18 | ❌ | **TIDAK DIPAKAI** - SDK vendor, package versi 0.x |
| `zod` | 4.0.2 | ❌ | **TIDAK DIPAKAI** - **peluang besar**: tidak ada validasi schema input apa pun |
| `zustand` | 5.0.6 | ❌ | **TIDAK DIPAKAI** |

**Ringkasan dependency:**
- **21 dari 66 dependency produksi tidak terpakai** (~32%).
- Estimasi ukuran node_modules tanpa 21 dep tersebut: penghematan signifikan - `@mdxeditor/editor` (~2 MB dengan seluruh tree CodeMirror), `@tanstack/react-query` + `@tanstack/react-table`, `@dnd-kit/*` (3 paket), `next-auth`, `next-intl`, `@reactuses/core`, `react-syntax-highlighter` (memuat `highlight.js` ~1 MB), `zod`, `zustand`.
- **Duplikasi Radix/shadcn:** tidak ada duplikasi Radix - 28 paket Radix semuanya dipakai. Yang duplikat adalah `tailwindcss-animate` (v3) vs `tw-animate-css` (v4).
- **Duplikasi lain:** `prisma` ada di `dependencies` (bukan `devDependencies`) sekaligus `@prisma/client` - `prisma` CLI seharusnya devDependency.
- **Deprecated / EOL:** `next-auth` v4 (basis v5 sudah keluar) - meski tak terpakai, masih menarik CVE.
- **Duplikasi lockfile:** `bun.lock` (322 KB) **dan** `package-lock.json` (532 KB) ada bersamaan. Dua lockfile = sumber kebenaran ganda, risiko install tidak deterministik.

### Bundle

| Metrik | Nilai |
|---|---|
| Total `.next/static` | **2,2 MB** |
| Chunk terberat | 466 KB, 412 KB, 224 KB, 182 KB, 160 KB, 143 KB |
| Chunk > 100 KB | 7 |
| `next/dynamic` / `lazy()` | **0** |
| Route static | `/`, `/dataset`, `/simulasi` - semua prerender penuh |
| HTML hasil prerender | `index.html` 157,6 KB · `dataset.html` 207,9 KB · `simulasi.html` 44,9 KB |
| Font | `next/font/google` Geist + Geist_Mono ✅ (self-host, optimal) |
| `<img>` | 0 - tidak ada masalah optimasi gambar (tidak ada gambar raster) |
| `next/image` | 0 - tidak relevan |

**Rekomendasi performa (arsip):** pisahkan `MultiChannelGraph`, `Simulation`, `Comparison`, `FraudRing` via `next/dynamic` + `ssr: false` (masing-masing membawa recharts/framer-motion). Potensi hemat chunk awal 400–600 KB pada route `/`.

---

## 10. Checklist Minimal Test Suite yang Harus Ada

Prioritas **P0** = menutupi klaim falsifikasi & quality gate yang dimatikan; **P1** = logika bisnis inti; **P2** = kualitas &-have; **P3** = Stretch.

| # | Pri | Test | Letak | Yang diverifikasi | Tool | Status |
|---|---|---|---|---|---|---|
| 1 | **P0** | `leakage.test.ts` - fail keras bila kolom terlarang masuk fitur | `tests/` | Kontrak `03-dataset-registry.md` §7. **Membongkar klaim `test_leakage.py` yang palsu.** Sumber kebenaran: 1 file konfigurasi blokir yang dibaca test, bukan konstanta inline | Vitest | ❌ Tidak ada |
| 2 | **P0** | `threshold.test.ts` - ambang skor & label risiko | `tests/` | Satu sumber kebenaran `RISK_THRESHOLDS`; setiap label `low\|medium\|high\|fraud` Falling pada rentang yang tepat; **tidak ada celah/tumpang tindih** antar label (§4 registry). Akan gagal hari ini: 3 definisi ambang berbeda | Vitest | ❌ Tidak ada |
| 3 | **P0** | `risk-label.test.ts` - konsistensi 300 baris | `tests/` | Untuk tiap baris `NOTION_CLAIMS_DATASET`: `label(skorFraud) === risiko`; `status` sesuai `risiko`; total nominal = Rp 3.526.650.000. Mengganti angka hardcoded jadi terverifikasi | Vitest | ❌ Tidak ada |
| 4 | **P0** | `npm run typecheck` sebagai gate + `ignoreBuildErrors: false` | `package.json`, `next.config.ts` | 8 error typecheck harus hilang; build harus **gagal** kalau ada regresi tipe | `tsc` | ❌ Script tidak ada; `ignoreBuildErrors: true` |
| 5 | **P0** | CI workflow: `typecheck` + `lint` + `build` + `test` | `.github/workflows/ci.yml` | Tidak ada regresi ke `main` tanpa gate hijau. `.github/` **tidak ada sama sekali** | GitHub Actions | ❌ Tidak ada |
| 6 | **P1** | `fusion-score.test.ts` - logika Late Fusion | `tests/` | `data-uploader.tsx` fusion: rentang [0,1]; monotonicitas (skor fitur naik → fusion naik); kasus batas tepat di tiap label; **kontribusi topologi negatif** (kamuflase) benar-benar menurunkan skor | Vitest | ❌ Tidak ada |
| 7 | **P1** | `dataset-integrity.test.ts` - bentuk data | `tests/` | 300 klaim, ID unik KLM001–KLM300, ID berurutan, tidak ada `null` di field wajib, `biayaRp` ≥ 0, `losHari` integer, `sentiment` sesuai `skorSentimen` (memverifikasi 300 baris yang saat ini tak punya kode pemetaan) | Vitest | ❌ Tidak ada |
| 8 | **P1** | `shap-consistency.test.ts` | `tests/` | `kontribusiSaluran` dipecah ke channel dan **jumlahnya = skor fusi** dalam toleransi; konsistensi SHAP ↔ kolom Alasan (kriteria "Konsistensi XAI" di `10-simulation-dataset.md`) | Vitest | ❌ Tidak ada |
| 9 | **P1** | `graph-builder.test.ts` | `tests/` | Simpul/edge referential integrity (setiap `source`/`target` edge ada di node list); tidak ada self-loop; tidak ada edge duplikat; jumlah channel = 3 sesuai spec | Vitest | ❌ Tidak ada |
| 10 | **P1** | `i18n.test.ts` - kelengkapan kamus | `tests/` | Setiap key di literal ID & EN harus ada di interface `Dict`; jumlah key ID == EN; semua key dipakai minimal sekali. **Menangkap 4 bug typecheck yang ada** (`mathTitle2b`, `roiTitle3`, `roiTitle4`) | Vitest | ❌ Tidak ada |
| 11 | **P2** | `es-lint-regression` - hentikan mematikan rule | `eslint.config.mjs` | Aktifkan `no-explicit-any` (error), `ban-ts-comment`, `exhaustive-deps`; repo harus tetap hijau → paksa perbaikan 5 `any` + 2 stale `@ts-expect-error` | ESLint | ❌ Rule dimatikan manual |
| 12 | **P2** | `no-implicit-any` | `tsconfig.json` | Ubah `noImplicitAny: false` → `true`; repo harus tetap kompilasi | `tsc` | ❌ Dimatikan |
| 13 | **P2** | `no-duplicate-types.test.ts` | `tests/` | Hanya satu definisi `RiskLevel`; hanya satu peta `RISK_COLORS`; tidak ada tipe domain duplikat di `src/types/` vs `src/components/` | ESLint rule custom / test | ❌ 2 duplikat `RiskLevel`, 3 duplikat `RISK_COLORS` |
| 14 | **P2** | `data-uploader.test.ts` - parse & validasi CSV | `tests/` | CSV parser: tolak skema salah, tandai missingness (`not_applicable` vs kosong), validasi rentang biaya | Vitest | ❌ Tidak ada |
| 15 | **P2** | `metadata.test.ts` - SEO | `tests/` | Tiap route punya `metadata.title` + `description`; `metadataBase` ada; `robots`/`canonical` ada; `openGraph` di semua route publik | Vitest | ❌ Tidak ada |
| 16 | **P2** | `component-smoke.test.tsx` | `tests/` | Render `Hero`, `FraudRing`, `DatasetExplorer` (300 baris) tanpa crash; smoke untuk `OasisDashboard` | Vitest + Testing Library | ❌ Tidak ada |
| 17 | **P2** | `route-files.test.ts` | `tests/` | Tiap route punya `loading.tsx` + `error.tsx` + `not-found.tsx` (App Router best practice) | Test file statis | ❌ 0 file route khusus |
| 18 | **P3** | `a11y.test.tsx` | `tests/` | `axe-core` pada komponen utama: kontras, label, landmark, navigasi keyboard | Vitest + axe | ❌ 31 `<button>` tanpa `aria-label` |
| 19 | **P3** | `bundle-budget.test.ts` | `tests/` | First-load JS route `/` ≤ 250 KB gzipped (saat ini jauh di atas) | size-limit | ❌ Tidak ada |
| 20 | **P3** | `no-unused-deps.test.ts` | `tests/` | `knip`/`depcheck`: 21 dependency mati dibersihkan; `bun.lock` vs `package-lock.json` memilih satu | knip | ❌ 21 dep mati |

### Catatan arsitektural untuk tim

Perintah yang benar-benar dijalankan dalam audit ini (semua di `N:\HEALTHKATHON\Aegis-JKN\`, tanpa install, tanpa modifikasi file):

```
npx tsc --noEmit          → exit 1, 8 error
npm run lint               → exit 1, 5 error (react-hooks/set-state-in-effect)
npm run build              → exit 0, "Skipping validation of types" (masking)
npm run                    → 9 script, tanpa `test`, tanpa `typecheck`
ls -d .zscripts             → No such file or directory (3 test .sh yatim)
find . -name "*leakage*"   → kosong
```

---

## Lampiran A - Ringkasan Angka

| Metrik | Nilai |
|---|---|
| File `src/` | 86 file (74 `.tsx`, 12 `.ts`) |
| Total LOC `src/` | 25.970 baris |
| File `src/data/` | 2 file, 10.296 baris (40% dari repo, 100% hardcoded) |
| File `src/components/mhgsl/` | 22 file, 4.520 baris |
| File `src/components/ui/` | 48 file (shadcn boilerplate) |
| Error typecheck | 8 |
| Error lint | 5 |
| Skrip npm | 9 (0 test, 0 typecheck) |
| Test otomatis yang dapat dijalankan | **0** |
| Assertion unit test untuk logika bisnis | **0** |
| Direktori `.github/` | tidak ada |
| Dependency produksi | 66 |
| Dependency tidak terpakai | 21 (32%) |
| Definisi `RiskLevel` | 2 (duplikat) |
| Peta warna risiko | 3 (duplikat identik) |
| Set ambang risiko berbeda | 3 (0.4/0.65/0.85 · 0.35/0.6/0.8 · 0.4/0.62/0.80) |
| Route tanpa `loading/error/not-found` | 3 dari 3 |
| Komponen `"use client"` | 61 dari 74 |
| `next/dynamic` | 0 |
| Bundle `.next/static` | 2,2 MB |
| Chunk > 100 KB | 7 |

## Lampiran B - Perintah Audit (reproduksi)

```bash
cd "N:\HEALTHKATHON\Aegis-JKN"

# Build & test inventory
npm run                                      # listing 9 script
ls -d .zscripts                              # → tidak ada
find . -maxdepth 3 -name "*.sh" -not -path "./node_modules/*"
git ls-files tests                            # → 3 file .sh

# Verifikasi test_leakage.py
find . -path ./node_modules -prune -o -name "*leakage*" -print   # → kosong
find . -path ./node_modules -prune -o -name "test_*" -print        # → kosong
Get-ChildItem -Recurse -Include *.py,requirements.txt,pyproject.toml
                                                    # → hanya di node_modules

# Quality gate
npx tsc --noEmit                             # exit 1, 8 error
npm run lint                                  # exit 1, 5 error
npm run build                                 # exit 0 (masking types)

# Anti-pattern
Select-String -Path src\**\*.tsx -Pattern "TODO|FIXME|HACK|XXX|console\.|@ts-ignore"
Select-String -Path src\**\*.tsx -Pattern ": any|as any"

# Threshold consistency
Select-String -Path src\**\*.tsx,src\data\*.ts -Pattern "0\.85|0\.65|0\.35|0\.8\b"

# Dependency audit
# grep import seluruh src terhadap 66 dependency
```
