# 08 - Audit Implementasi UI Aegis-JKN terhadap Spesifikasi

Tanggal audit: 22 Oktober 2026
Kodebas: `N:\HEALTHKATHON\Aegis-JKN\` (read-only, tidak diubah)
Spesifikasi acuan: `analysis/corpus/00-dashboard.md`, `01-proposal.md`, `02-architecture.md`, `05-decision-scope.md`, `10-simulation-dataset.md`
Basis pemeriksaan: `npx tsc --noEmit` (8 error), pembacaan seluruh 20 file `src/components/mhgsl/*`, 2 file dataset besar, `src/app/*`, `prisma/schema.prisma`, `package.json`, `docs/user-guide/navigation.md`, dan penghitungan konstanta hardcoded lewat skrip.

---

## 1. Ringkasan Eksekutif

Audit ini menilai bukan apakah UI-nya **bagus**, tetapi apakah UI **berjujur** dan **lengkap** terhadap arsitektur yang ditulis. Jawabannya: UI secara visual matang, tetapi secara epistemis belum dapat dipertanggungjawabkan.

Tiga klaim tata kelola dari `00-dashboard.md` §4 ("belum boleh disebut hasil tervalidasi") dilanggar secara langsung oleh antarmuka: metrik model (`AUPRC 0.91`, `ROC-AUC 0.95`, `Precision 0.92` di `data.ts:253,300,295`), angka **`93%`** yang muncul sebagai KPI utama di `/simulasi` (`oasis-dashboard.tsx:334`, sumber `oasis-data.ts:97`), dan estimasi penghematan finansial (`Rp 1,2 M/bulan`, `Rp 14,4 M/tahun` di `fraud-ring.tsx:415`, `roadmap.tsx:34`). Ketiganya disajikan sebagai hasil, bukan sebagai simulasi.

Di sisi lain, **halaman utama (`/`) tidak memakai dataset sama sekali**. Seluruh 489 baris `src/components/mhgsl/data.ts` adalah konstanta tulisan tangan: 12 node graf, 20 edge, 4 langkah simulasi, 5 atribusi SHAP, 3 profil forensik. Angka "300 klaim", "40 pasien", "9 sindikat" yang ada di `data.ts:502-519` (`DATASET_METRICS`) justru **tidak pernah diimpor** satu pun modul. Dua route yang benar-benar memakai data nyata (`/dataset` → 300 klaim + 33 entri riset; `/simulasi` → payload 100-klaim v1) tidak terhubung ke `/` dan tidak punya backend.

Yang paling konsekuensial untuk sebuah sistem *human-in-the-loop*: **audit trail tidak ada sama sekali**. `prisma/schema.prisma` masih berupa boilerplate `User`/`Post`, `src/lib/db.ts` tidak pernah diimpor siapa pun, dan `src/app/api/route.ts` masih `Hello, world!`. Tidak ada satu pun tempat di UI untuk merekam tindakan reviewer, alasan override, versi model, atau status tindak lanjut - ketujuh field wajib yang diminta `02-architecture.md` §3.6.

### 1.1 Tabel severity

| Severity | Jumlah | Cakupan utama |
|---|---|---|
| **Kritis** | 7 | Halaman utama tanpa data nyata; metrik fabrikasi; angka 93% & penghematan finansial melanggar governance; audit trail absen; tanpa server; tanpa review/override |
| **Tinggi** | 14 | i18n parsial 6 komponen; `lang` HTML mati; 4 TS error disembunyikan; a11y SVG/queue; tanpa error/loading boundary; Roadmap status by-index; badge "SESUAI" dari literal; CSV parser lemah; "5 entitas" vs 8 node; "14 edge" vs 13 |
| **Sedang** | 23 | `navigation.md` 12 klaim salah; klaim DP-CTGAN di footer; hero/EN mismatch; diskon 1000× ID vs EN; 4 export mati; 20 dependensi mati; sort in-place; metadata placeholder z.ai; render ganda riset; angka hardcoded di explorer; iframe dashboard kedua |
| **Rendah** | 11 | `@ts-expect-error` mati; shortcut andal pada teks tombol; tidak ada test suite; target analisis; copy; ketiadaan unit test ML; dan lain-lain |
| **TOTAL** | **55** | |

### 1.2 Ringkasan hitungan data mock

| Metrik | Nilai |
|---|---|
| Konstanta/mock item hardcoded di `src/components/mhgsl/data.ts` | **101** (12 node, 20 edge, 5 formula, 3 channel, 5 pipeline, 6 baris perbandingan, 6 AUPRC, 4 radar, 6 metrik, 4 langkah sim, 5 SHAP, 4 progres kanal, 3 profil, 6 pilar, 4 roadmap, 4 ROI, 4 hero stat, 17 field dataset-metrics) |
| Mock di `fraud-ring.tsx` | **35** (15 node + 20 edge) |
| Mock di `multi-channel-graph.tsx` | **2** (2 metapath chain) |
| Titik data graf karangan di `comparison.tsx:372-378` | **20** (4 metode × 5 epoch) |
| **Total item mock di halaman utama** | **158** |
| String i18n didefinisikan (`i18n.tsx`, 2 locale) | **296** (148 key × 2) |
| Key i18n **mati** (tidak pernah dipakai) | **55** dari 148 |
| Baris komponen **tanpa** dukungan i18n | **4.402** (`dataset-explorer.tsx` 2159 + `oasis-dashboard.tsx` 1116 + `multi-channel-graph.tsx` 521 + `fraud-ring.tsx` 521→411 + `math-formulas.tsx` 272 + `fraud-drilldown-modal.tsx` 243) |
| Baris data **nyata** di repo | **9.401** (`notion-datasets.ts`: 300 klaim + 33 riset) |
| Real data terpakai di route | **2 dari 3** (`/dataset`, `/simulasi`); route `/` = **0%** |
| Porsi file `src/` yang memakai dataset | 2 dari 24 file aplikasi |

---

## 2. Inventarisasi Route & Fitur

### 2.1 Route

| Route | File | Baris | Komponen | Data | Interaksi nyata? |
|---|---|---|---|---|---|
| `/` | `src/app/page.tsx:1-101` | 101 | Navbar, Hero, ProblemSection, Architecture, MultiChannelGraph, Simulation, MathFormulas, Comparison, FraudRing, Roadmap, Footer, BackToTop | **0% nyata** (semua dari `data.ts`) | Sebagian (simulasi, graf, uploader) |
| `/dataset` | `src/app/dataset/page.tsx:1-29` | 29 | `DatasetExplorer` | **100% nyata** (300 klaim + 33 riset) | Ya (filter, sort, paging, ekspor CSV/JSON, sheet detail) |
| `/simulasi` | `src/app/simulasi/page.tsx:1-19` | 19 | `OasisDashboard` | Payload statis `oasis-data.ts` (100 klaim v1) | Terbaca saja (tab, filter, pilih item) |
| `/api` | `src/app/api/route.ts:1-5` | 5 | - | - | **Stub** `{"message":"Hello, world!"}` |

Tidak ada `error.tsx`, `loading.tsx`, `not-found.tsx`, `route.ts` lain, atau API handler kedua di `src/app/` (hanya 6 file: `api/route.ts`, `dataset/page.tsx`, `globals.css`, `layout.tsx`, `page.tsx`, `simulasi/page.tsx`).

### 2.2 Komponen `src/components/mhgsl/` (baris)

| Komponen | Baris | i18n? | Sumber angka | Catatan |
|---|---|---|---|---|
| `architecture.tsx` | 159 | ya | `data.ts:171-206` (PIPELINE 5 tahap) | Statis |
| `back-to-top.tsx` | 40 | tidak | - | `aria-label` ada |
| `comparison.tsx` | 460 | ya | `data.ts:249-301` | 4 tab; 2 graf hardcode inline |
| `data-uploader.tsx` | 469 | ya | **menghitung sendiri** | Satu-satunya komputasi klien |
| `fraud-drilldown-modal.tsx` | 243 | **tidak** | `data.ts:412-499` | 3 profil |
| `glossary.tsx` | 398 | ya | kamus lokal | Search ok |
| `lang-toggle.tsx` | 41 | ya | - | `localStorage` |
| `multi-channel-graph.tsx` | 521 | **tidak** | `data.ts:87-137` | SVG 12 node |
| `problem-section.tsx` | 165 | ya (sebagian) | literal `79,88,97` | 3 angka tak bersumber |
| `shortcuts-hint.tsx` | 53 | ya | - | - |
| `theme-toggle.tsx` | 51 | ya | - | `aria-label` ada |
| `use-count-up.ts` | 76 | - | - | dipakai `roadmap.tsx:34` |
| `use-keyboard-shortcuts.ts` | 46 | - | - | 6 shortcut global |
| `simulation.tsx` | 438 | ya | `data.ts:304-355` | State machine, tanpa komputasi |
| `navbar.tsx` | 245 | ya | - | 7 anchor + 2 link route |
| `fraud-ring.tsx` | 411 | **tidak** | `fraud-ring.tsx:15-45` | 15 node, 20 edge |
| `roadmap.tsx` | 187 | ya | `i18n.tsx:465-490` | Status by-index |
| `hero.tsx` | 238 | ya | `data.ts:19-24` | Pakai `HERO_STATS`, bukan `t.heroStats` |
| `data.ts` | 489 | - | - | 101 konstanta |
| `i18n.tsx` | 869 | ya | - | 148 key × 2 locale |
| `footer.tsx` | 112 | ya | `i18n.tsx:492-524` | - |
| `math-formulas.tsx` | 272 | **tidak** | `data.ts:210-247` | Render LaTeX manual, tanpa KaTeX |

### 2.3 Komponen besar

| Komponen | Baris | i18n? | Sumber | Catatan |
|---|---|---|---|---|
| `src/components/dataset/dataset-explorer.tsx` | 2159 | **tidak** | `notion-datasets.ts:3,402` | 300 klaim + 33 riset; compute `metrics` di `215-241` |
| `src/components/oasis/oasis-dashboard.tsx` | 1116 | **tidak** | `oasis-data.ts` | 100 klaim v1; 4 tab; iframe HTML 150 KB |
| `src/data/oasis-data.ts` | 886 | - | - | Payload statis hasil simulasi |
| `src/data/notion-datasets.ts` | 9401 | - | - | **Satu-satunya sumber data nyata** |
| `src/lib/db.ts` | 13 | - | Prisma | **Tidak pernah diimpor** |
| `src/types/dataset.ts` | 56 | - | - | `ClaimRecord`/`ResearchRecord` |

Total `src/components/ui/*` (shadcn) = 66 file, 4.900 baris; hanya `progress.tsx`, `tabs.tsx`, `card.tsx`, `sheet.tsx`, `dialog.tsx`, `select.tsx`, `table.tsx`, `badge.tsx`, `button.tsx`, `toaster.tsx` yang benar-benar dipakai.

---

## 3. Data Flow: Mock vs Nyata

### 3.1 Peta asal data per surface

| Surface | File | Sumber angka | Nyata/mock | Komentar |
|---|---|---|---|---|
| Hero stat | `data.ts:19-24` | konstanta | **MOCK** | `2.000.000+` klaim/hari, `±1.000` verifikator - tak bersumber |
| Hero stat (EN) | `i18n.tsx:556-561` | konstanta | **MOCK** | Duplikat `t.heroStats`, tak pernah dipakai |
| Problem section | `problem-section.tsx:79,88,97` | literal | **MOCK** | `±2.000.000`, `≈1.000`, `3–7%` |
| Pipeline | `data.ts:171-206` | konstanta | MOCK naratif | 5 tahap, benar secara konsep |
| Graf MHGSL | `data.ts:87-137` | 12 node + 20 edge | **MOCK** | Koordinat SVG, bobot edge tulis tangan |
| Simulasi | `data.ts:304-355` | 4 langkah + 5 SHAP | **MOCK** | Skor 0.32/0.61/0.84/0.94 konstanta |
| SHAP | `data.ts:340-346` | 5 atribut | **MOCK** | 0.41/0.28/0.19/0.12/−0.07 |
| Benchmark AUPRC | `data.ts:253,258-265,294-301` | 6+6+4 metrik | **MOCK** | AUPRC 0.71→0.91, ROC-AUC 0.95, Precision 0.92 |
| Tren epoch | `comparison.tsx:372-378` | 20 titik | **MOCK** | Karangan di dalam JSX |
| Delta/klaim | `comparison.tsx:134,203,207,211` | literal | **MOCK** | `+0.20`, `+20%`, `×3`, `−42%` |
| Fraud ring | `fraud-ring.tsx:15-45` | 15 node + 20 edge | **MOCK** | Legend bilang 14 edge, aktual 13 |
| Profil forensics | `data.ts:412-499` | 3 profil | **MOCK** | 10 evidence, 10 timeline, 12 metrik |
| ROI | `roadmap.tsx:34`, `i18n.tsx:453-462` | konstanta | **MOCK** | `14.4` → "Rp 14,4 M" |
| Roadmap | `i18n.tsx:465-490` | konstanta | MOCK naratif | 4 fase, salinan `data.ts:358-387` |
| Uploader | `data-uploader.tsx:79-148` | **dihitung** | **KOMPUTASI** | Satu-satunya kalkulasi klien |
| Dataset explorer | `notion-datasets.ts:3,402` | 300+33 | **NYATA** | `dataset-explorer.tsx:215-241` hitung KPI dari data |
| Oasis dashboard | `oasis-data.ts:1-886` | 100 klaim v1 | **STATIS** | Hasil simulasi yang disalin tangan ke TS |
| API | `api/route.ts:3-5` | - | **TIDAK ADA** | `Hello, world!` |

### 3.2 Hitungan konstanta hardcoded (path:line)

| # | Konstanta | Lokasi | Jumlah |
|---|---|---|---|
| 1 | `HERO_STATS` | `src/components/mhgsl/data.ts:19-24` | 4 |
| 2 | `RISK_PILLARS` | `data.ts:27-85` | 6 |
| 3 | `MHGSL_NODES` | `data.ts:87-109` | 12 (8 di-flag `risk:"fraud"`) |
| 4 | `MHGSL_EDGES` | `data.ts:111-137` | 20 (12 topologi, 4 fitur, 4 semantik) |
| 5 | `CHANNELS` | `data.ts:140-169` | 3 |
| 6 | `PIPELINE` | `data.ts:171-206` | 5 |
| 7 | `FORMULAS` | `data.ts:210-247` | 5 |
| 8 | `COMPARISON_ROWS` | `data.ts:249-256` | 6 |
| 9 | `AUPRC_DATA` | `data.ts:258-265` | 6 |
| 10 | `RADAR_DATA` | `data.ts:270-291` | 4 |
| 11 | `METRIC_DETAIL` | `data.ts:294-301` | 6 |
| 12 | `SIM_STEPS` | `data.ts:304-337` | 4 |
| 13 | `SHAP_ATTRS` | `data.ts:340-346` | 5 |
| 14 | `CHANNEL_PROGRESS` | `data.ts:350-355` | 4 |
| 15 | `ROADMAP` | `data.ts:358-387` | 4 (**mati**) |
| 16 | `ROI_STATS` | `data.ts:390-395` | 4 (**mati**) |
| 17 | `FRAUD_PROFILES` | `data.ts:412-499` | 3 |
| 18 | `DATASET_METRICS` | `data.ts:502-519` | 17 field (**mati**) |
| 19 | `ringNodes` | `fraud-ring.tsx:15-33` | 15 |
| 20 | `ringEdges` | `fraud-ring.tsx:35-45` | 20 (13 fraud + 7 normal) |
| 21 | `metapathChains` | `multi-channel-graph.tsx:54-57` | 2 |
| 22 | Graf konvergensi | `comparison.tsx:372-378` | 20 titik |
| 23 | `OASIS_DATA` | `src/data/oasis-data.ts:80-886` | 806 baris statis |
| 24 | Key i18n | `i18n.tsx:7-179` (iface), `181-528` (id), `530-875` (en) | 148 key × 2 locale |

**Total item mock teridentifikasi: 158 di halaman utama + 806 baris payload statis `/simulasi`.**

### 3.3 Entitas hardcoded vs dataset-derived

| Entitas | Jumlah di UI (mock) | Jumlah di dataset nyata | Sumber nyata | Selisih |
|---|---|---|---|---|
| Klaim | 3 diklaim di `SIM_STEPS`/profil (KLM001-003) | **300** (KLM001-KLM300) | `notion-datasets.ts:402` | 297 tidak pernah muncul di `/` |
| Pasien | 5 di graf (`data.ts:89-93`) | **40** (P01-P40) | `notion-datasets.ts` | 35 tidak muncul |
| Dokter | 3 di graf (`data.ts:96-98`) | **20** (D01-D20) | `notion-datasets.ts` | 17 tidak muncul |
| Faskes | 1 di graf (`data.ts:101`) | **10** (RS_A-RS_J) | `notion-datasets.ts` | 9 tidak muncul |
| Sindikat | 1 di graf + 1 di ring | **9** (SYND-01..09) | `notion-datasets.ts` | 8 tidak muncul |
| Sentence/risiko | 3 baris (`data.ts:304-337`) | 240 low / 10 medium / 14 high / 36 fraud | `notion-datasets.ts` (terverifikasi) | - |
| Kontradiksi narasi | 8 (klaim statis oasis) | **12** pada data 300 | `notion-datasets.ts` | Data v1 (8) ≠ data v2 (12) |
| Total nominal | `dataset-explorer.tsx:764` tulis "Rp 3,53 M" | **Rp 3.526.650.000** | hitung di `dataset-explorer.tsx:225` | Judul kartu salah satuan ("M" vs Miliar) |

Verifikasi ulang atas dump lokal (independen dari spec): 300 record, `status` = 240 auto_clear / 24 review / 36 escalate, `risiko` = 240 low / 10 medium / 14 high / 36 fraud, total `biayaRp` = 3.526.650.000, 9 sindikat, 12 klaim dengan `kontradiksiNarasi: true`. Semua cocok dengan `00-dashboard.md` §3.

### 3.4 Temuan kunci data-flow

| ID | Severity | Temuan | Bukti |
|---|---|---|---|
| F-01 | Kritis | **Route `/` tidak memakai dataset sama sekali.** Satu-satunya sumber data nyata (300 klaim) tidak pernah masuk ke komponen home. `DATASET_METRICS` yang berisi angka "300/40/20/10/9" justru **0 referensi** di luar `data.ts`. | `src/components/mhgsl/data.ts:502-519` (export mati); `src/app/page.tsx:89-99` (tidak ada import dataset) |
| F-02 | Kritis | **Benchmark metrik model difabrikasi tanpa experiment ID/split/prediksi.** `AUPRC 0.91`, `ROC-AUC 0.95`, `Precision 0.92`, `Recall 0.90` disajikan sebagai hasil komparatif 4 model. Tidak ada satu pun artefak eksperimen di repo (`configs/`, `scripts/`, `data/`, `experiments/` - semuanya **tidak ada**). | `data.ts:253,258-265,294-301`; `comparison.tsx:126-136`; `comparison.tsx:372-378` |
| F-03 | Kritis | **Angka 93% (accuracy) tampil sebagai KPI utama** di `/simulasi` - persis angka yang `00-dashboard.md:47` larang dipublikasikan. Kartu KPI tidak punya qualifier "simulasi sintetis, prevalensi oversampled"; label kejujuran hanya muncul di tab lain (`oasis-dashboard.tsx:255`). | `src/components/oasis/oasis-dashboard.tsx:334`; sumber `src/data/oasis-data.ts:97`; `analysis/corpus/00-dashboard.md:47` |
| F-04 | Kritis | **Estimasi penghematan finansial ditampilkan sebagai hasil.** `Rp 1,2 M / bulan (Rp 14,4 M / tahun)` - termasuk kategori "penghematan/penyelamatan finansial" yang dinyatakan belum boleh diklaim (`00-dashboard.md:50`), dan `05-decision-scope.md:64` menyebut "klaim penghematan nasional yang diekstrapolasi dari dataset sintetis" sebagai **out-of-scope**. | `src/components/mhgsl/fraud-ring.tsx:415`; `src/components/mhgsl/roadmap.tsx:34-37`; `src/components/mhgsl/i18n.tsx:443,459-462` |
| F-05 | Kritis | **Audit trail tidak ada di seluruh sistem.** Tidak ada model DB untuk audit, tidak ada importer Prisma, tidak ada endpoint untuk mencatat tindakan. Klaim "log audit dan evaluasi yang dapat direproduksi" (`05-decision-scope.md:58`) dan butir fitur inti "Audit trail" (`01-proposal.md:60`) tidak terpenuhi. | `prisma/schema.prisma:16-32` (hanya `User`/`Post`); `src/lib/db.ts:7` (0 importer); `src/app/api/route.ts:3-5` |
| F-06 | Kritis | **Tidak ada backend sama sekali.** Satu-satunya route API mengembalikan `{"message":"Hello, world!"}`. Tidak ada endpoint model, ingest, verifikasi, atau penyimpanan. | `src/app/api/route.ts:1-5` |
| F-07 | Kritis | **Tidak ada kontrol review/override di UI mana pun.** Tidak ada tombol "Setujui/Tolak/Eskalasi", tidak ada input alasan override, tidak ada pencatatan status tindak lanjut - padahal `02-architecture.md:47` mewajibkan field "tindakan reviewer, alasan override, dan status tindak lanjut", dan `01-proposal.md:64` mensyaratkan sistem "harus memungkinkan override manusia dan merekam alasannya". Antrean `/simulasi` hanya bisa dibaca. | `src/components/oasis/oasis-dashboard.tsx:798-830` (list `<div onClick>` tanpa aksi); `src/components/dataset/dataset-explorer.tsx:1973-2170` (sheet detail, tanpa aksi) |
| F-25 | Sedang | **Diskon satuan 1000× antara locale.** ID: "Rp 1,2 M / bulan (Rp 14,4 M / tahun)"; EN: "Rp 1.2 B / month (Rp 14.4 B / year)". Salah satu pasti salah; UI bilingual menampilkan dua besaran berbeda dari "satu" fakta. | `src/components/mhgsl/i18n.tsx:443` vs `i18n.tsx:791` |

---

## 4. Angka Hardcoded di UI yang Melanggar Governance

Acuan: `00-dashboard.md:46-52` ("Belum boleh disebut hasil tervalidasi") dan `00-dashboard.md:9` ("Dataset tersebut bukan bukti prevalensi fraud atau kerugian aktual JKN"); `10-simulation-dataset.md:181` ("Semua metrik WAJIB disertai label: 'simulasi sintetis, prevalensi oversampled'").

| # | Angka | Lokasi (path:line) | Screen | Dikualifikasi? | Dampak |
|---|---|---|---|---|---|
| 1 | `93%` (Akurasi) | `src/components/oasis/oasis-dashboard.tsx:334`; nilai di `src/data/oasis-data.ts:97` | `/simulasi` - KPI kartu pertama | **Tidak** di kartu; label kejujuran hanya di `oasis-dashboard.tsx:255` (tab lain) | **LANGGAR LANGSUNG** `00-dashboard.md:47`. Angka tak tervalidasi tampil sebagai headline. |
| 2 | `AUPRC 0.91` (MHGSL) | `src/components/mhgsl/data.ts:264`; tabel `data.ts:253` | `/` tab AUPRC | **Tidak** (label hanya "Skor relatif (0–1)…" di `comparison.tsx:129`) | Metrik model tanpa eksperimen; setara angka AUPRC yang dilarang 0,9142 (`00-dashboard.md:47`). |
| 3 | `ROC-AUC 0.95` | `src/components/mhgsl/data.ts:300` | `/` tab Matriks | **Tidak** | Setara forbidden ROC-AUC 0,9825 (`00-dashboard.md:47`). |
| 4 | `Precision 0.92` / `Recall 0.90` / `F1 0.91` | `src/components/mhgsl/data.ts:295-297` | `/` tab Matriks & Radar | **Tidak** | Setara forbidden precision 94,12% (`00-dashboard.md:47`). |
| 5 | `Rp 1,2 M / bulan (Rp 14,4 M / tahun)` | `src/components/mhgsl/fraud-ring.tsx:415`; `i18n.tsx:443` | `/` - verdict auditor | **Tidak** | **LANGGAR** `00-dashboard.md:50` + out-of-scope `05-decision-scope.md:64`. |
| 6 | `Rp 14,4 M` (annual savings counter) | `src/components/mhgsl/roadmap.tsx:34-37` | `/` - kartu ROI | **Tidak**; sub-teks hanya "Asumsi 3% tingkat fraud… basis 5 FKRTL" (`i18n.tsx:461-462`) | Penghematan diasumsikan, bukan dihitung; ini kontradiktif dengan poin 5 (M vs B). |
| 7 | `+20%` lonjakan AUPRC | `src/components/mhgsl/data.ts:23`; `i18n.tsx:211,560`; `comparison.tsx:203` | `/` - hero + tab AUPRC | **Tidak** | Klaim performa model tanpa baseline terukur. |
| 8 | `Δ +0.20` MHGSL vs XGBoost | `src/components/mhgsl/comparison.tsx:134` | `/` - header graf AUPRC | **Tidak** | Diferensiasi absolut dari angka fabrikasi. |
| 9 | `×3` "perspektif graf" | `src/components/mhgsl/comparison.tsx:207` | `/` - 3 chip ringkasan | **Tidak** | Tidak jelas rujukan; mendekati klaim throughput 3,2× (`00-dashboard.md:49`) yang tak terverifikasi. |
| 10 | `−42% false negatives` | `src/components/mhgsl/comparison.tsx:211` | `/` - 3 chip ringkasan | **Tidak** | Klaim recall improvement; tak ada data pendukung. |
| 11 | `4.563 Saluran Fitur Kosinus Dikonfirmasi` | `src/components/oasis/oasis-dashboard.tsx:376`; angka di `src/data/oasis-data.ts:98` | `/simulasi` - header tab | **Tidak** | Klaim konfirmasi 4.563 edge; graf edge nyata yang dihitung (`data.ts:111-137`) hanya 20. |
| 12 | `Hit Rate: 16/16 (100%)` + badge `100% Sempurna` | `src/components/oasis/oasis-dashboard.tsx:591,560` | `/simulasi` - graf sindikat | **Tidak** | Kebetulan true (semua 16 klaim sindikat sengaja dimasukkan ke antrean 20), tetapi disajikan sebagai bukti performa. |
| 13 | `14 dari 14 berkas fraud (100%) terjaring` / `100% recall` | `src/components/oasis/oasis-dashboard.tsx:546,697,659` | `/simulasi` - matriks kepatuhan | **Tidak** | Angka rekap dari dataset v1 (100 klaim), bukan v2 (300 klaim) yang aktif. |
| 14 | Matriks kepatuhan: 4× `TERPENUHI` | `src/components/oasis/oasis-dashboard.tsx:681,693,705,717` | `/simulasi` | **Tidak**; badge "SESUAI" dari literal `oasis-data.ts:95-96` | Menyatakan kepatuhan protokol tanpa artefak verifikasi; `status`/`ok` adalah konstanta, bukan hasil pemeriksaan. |
| 15 | `Protokol v2.1 SESUAI` | `src/components/oasis/oasis-dashboard.tsx:198` | `/simulasi` | **Tidak** | Nilai literal `oasis-data.ts:95-96`. |
| 16 | `2.000.000+` klaim/hari, `±1.000` verifikator | `src/components/mhgsl/data.ts:20-21`; `i18n.tsx:208-209,557-558`; `problem-section.tsx:79,88` | `/` - hero + pilar masalah | **Tidak** | Angka eksternal tak bersumber; rasio 2.000:1 dipakai sebagai argumen risiko (`problem-section.tsx:90`). |
| 17 | `3–7%` estimasi potensi fraud | `src/components/mhgsl/problem-section.tsx:97` | `/` - pilar masalah | Ya, sebagian: sub-teks "dari total nilai klaim nasional" (`i18n.tsx:233`) | Angka literatur, bukan hasil; risikonya disamarkan sebagai KPI visual sebesar 30px. |
| 18 | `20 mnt → 3 mnt`, `1.000 → ~6.700` | `src/components/mhgsl/i18n.tsx:454-455`; `data.ts:391-392` | `/` - ROI | **Tidak** | Klaim efisiensi operasional; tak terkait 45%/3,2× forbidden, tapi tetap tanpa sumber. |
| 19 | `4.2×` di atas peer, `+4.2σ` deviasi peer | `src/components/mhgsl/data.ts:428` (evidence), `data.ts:439` (metrik) | `/` - modal drilldown | **Tidak** | Angka forensik karangan; 4.2-sigma disebut diam-diam. |
| 20 | `Rp 3,53 M` (kartu "Nilai Klaim") | `src/components/dataset/dataset-explorer.tsx:764` | `/dataset` - kartu KPI | Ya, ada baris kedua `formatRupiah(metrics.totalCost)` (`dataset-explorer.tsx:768`) | **Salah satuan**: total sebenarnya Rp 3.526.650.000 (Miliar). Judul besar salah, angka kecil benar. |
| 21 | `16.7%` (High/Fraud) | `src/components/dataset/dataset-explorer.tsx:722` | `/dataset` - kartu KPI | **Tidak** (angka hitung 50/300 = 16,67% benar, tapi label `%` hardcode) | Persentase hardcode; pecah bila dataset berubah. |
| 22 | `Auto-Clear (240)`, `Manual Review (24)`, `Escalate (36)` | `src/components/dataset/dataset-explorer.tsx:909-911` | `/dataset` - dropdown filter | **Tidak** | Angka benar saat ini, tetapi hardcode, bukan dihitung dari `NOTION_CLAIMS_DATASET`. |
| 23 | `8 dari 8 klaim kontradiksi` | `src/components/oasis/oasis-dashboard.tsx:721`; `oasis-data.ts:105-106` | `/simulasi` | **Tidak** | Data v1. Data 300-claim sebenarnya punya **12** klaim kontradiksi - `/dataset` dan `/simulasi` saling bertentangan. |
| 24 | `±6.667` kapasitas verifikator + "telaah 20→3 mnt/berkas" | `src/components/oasis/oasis-dashboard.tsx:345,347` | `/simulasi` - KPI ROI | **Tidak** | Angka 6.667 = 1.000×6,67 hasil slider ROI, bukan hasil pengukuran. |

**Total 24 grup angka** di UI yang tidak disertai kualifikasi "simulasi sintetis, prevalensi oversampled", 5 di antaranya melanggar daftar larangan `00-dashboard.md:46-52` secara literal (poin 1, 3, 4, 5, dan turunan 2/6).

---

## 5. Spec vs UI Gap

| Fitur | Ada di spec? | Ada di kode? (path:line) | Deviasi | Dampak |
|---|---|---|---|---|
| **Audit trail** (versi model, waktu prediksi, alasan, tindakan verifikator, perubahan keputusan) | Ya - `01-proposal.md:60`; `00-dashboard.md:55` (fitur inti); `05-decision-scope.md:58` (in-scope) | **TIDAK ADA** - `prisma/schema.prisma:16-32` hanya `User`/`Post`; `src/lib/db.ts:7` 0 importer; `src/app/api/route.ts:3-5` stub | **Total** | Fitur inti MVP yang dianggarkan sebagai in-scope tidak terimplementasi di mana pun. |
| **Human-in-the-loop: override manusia + rekam alasan** | Ya - `01-proposal.md:64`; `02-architecture.md:10` | **TIDAK ADA** - `oasis-dashboard.tsx:798-830` (antrean read-only); `dataset-explorer.tsx:1973-2170` (sheet tanpa aksi) | **Total** | Prinsip desain #1 `02-architecture.md:10` ("keputusan akhir berada pada verifikator") tidak punya mekanisme. |
| **Antarmuka verifikator: 7 field wajib** | Ya - `02-architecture.md:40-47` | Sebagian: `dataset-explorer.tsx:2047-2168` (ID klaim, risiko+skor, alasan, sinyal SHAP `2152`, kontribusi kanal `2161`) | **4 dari 7 hilang**: (a) aturan yang terpicu, (b) sumber & waktu data, (c) **versi model & threshold**, (d) **tindakan reviewer + alasan override + status tindak lanjut** | Tidak memenuhi kriteria penerimaan MVP `02-architecture.md:104` ("UI membedakan skor, dugaan anomali, dan keputusan verifikator"). |
| **Validasi tipe/rentang/kode/nilai wajib saat ingest** | Ya - `02-architecture.md:19-23` | Lemah - `data-uploader.tsx:60-77` (`split(",")` polos), `79-148` (tanpa validasi skema) | **Total** untuk kasus CSV/JSON; tidak ada lapis server | "menolak skema yang tidak sesuai dan menyimpan log kesalahan" tidak terpenuhi. |
| **Rule engine Tier 1 dengan ID/versi/sumber/kasus uji** | Ya - `02-architecture.md:25-26` | **TIDAK ADA** di UI maupun kode | **Total** | Aturan tidak punya identitas; tidak bisa diaudit. |
| **Baseline tabular (XGBoost) & benchmark reproducible** | Ya - `02-architecture.md:28`; `05-decision-scope.md:54` | Hanya narasi: `comparison.tsx:249-256`, `data.ts:258-265`; **tidak ada** `scripts/`, `configs/`, `experiments/` | **Total** | Angka AUPRC tidak dapat direproduksi; `02-architecture.md:102` ("metrik dapat dihitung ulang dari prediksi tersimpan") gagal. |
| **Graph heterogen 3 saluran + edge dengan arah/sifat temporal/dasar** | Ya - `02-architecture.md:30-36` | Tervisualisasi: `multi-channel-graph.tsx:255-460`, data `data.ts:111-137` | **Parsial** | Edge tidak punya metadata arah/temporal/leakage; `02-architecture.md:31` mensyaratkan. |
| **SHAP per-saluran (3 kanal) + "SHAP bukan bukti kausal"** | Ya - `02-architecture.md:38`; `10-simulation-dataset.md:169-170` | Ada visual: `data.ts:340-346` (5 atribut, 3 kanal), `simulation.tsx:349-395`; **tanpa disclaimer kausalitas** | **Parsial** | Atribusi ditampilkan tanpa peringatan "tidak boleh digambarkan sebagai bukti kausal" (`02-architecture.md:38`). |
| **Late fusion `p_fused = p_graph + γ·f_text·(1−p_graph)`** | Ya - `02-architecture.md:37-38`; `10-simulation-dataset.md:166,172` | Hanya teks LaTeX: `math-formulas.tsx:244-253`; **tidak ada implementasi** (γ=0,10 hanya konstanta di `data.ts:384`/i18n) | **Total** | Text channel tidak ada; `02-architecture.md:13` ("fail-safe… tidak mengarang hasil") dilanggar karena formula ditampilkan tanpa implementasi. |
| **Split group-aware (GroupKFold/LOGO) & manifest** | Ya - `02-architecture.md:66-70`; `10-simulation-dataset.md:156-157` | **TIDAK ADA** - `data.ts:363` dan `i18n.tsx:470` **menyebut** `configs/leakage.yaml` & GroupKFold/LOGO, tapi folder `configs/`, `data/`, `scripts/` **tidak ada** di repo | **Total** | Roadmap UI dan repo tidak sinkron: item Fase 0 yang ditampilkan sebagai "Berlangsung" tidak punya artefak. |
| **Anti-leakage + `leakage.yaml` + unit test** | Ya - `10-simulation-dataset.md:126-127,153-154` | **TIDAK ADA** | **Total** | `10-simulation-dataset.md:115` menyatakan v2.1 *belum* memenuhi syarat; UI tidak menandainya. |
| **Text channel / social media 48 posting (24 Twitter + 24 Reddit)** | Ya - `10-simulation-dataset.md:104-108,172` | Ada: `oasis-data.ts` (twFeed 24, rdFeed 24), dirender `oasis-dashboard.tsx:953-1122` | **Parsial** | Hanya statis; tak ada fusion teks di UI. |
| **Dataset explorer / 33 entri riset** | Ya - `00-dashboard.md:38` | Ada, lengkap: `dataset-explorer.tsx` 2159 baris, `notion-datasets.ts:3` | **Lengkap** | - (satu-satunya fitur spec yang benar-benar tuntas) |
| **Uploader data mandiri** | Ya - implisit (`02-architecture.md:19`) | Ada: `data-uploader.tsx:1-469`, dipasang di `comparison.tsx:92` | **Ada tapi tidak di Navbar** | `docs/user-guide/navigation.md:12` dan `:110` menyatakan ada di Navbar - tidak ada. |
| **9 sindikat SYND-01..09 + hit-rate** | Ya - `10-simulation-dataset.md:132-143` | Hanya 5 sindikat (v1) di `oasis-data.ts:100-110`; 9 sindikat hanya di teks `dataset-explorer.tsx:752` | **Parsial** | `/simulasi` (yang diklaim "v2.1") hanya menguji 5 sindikat; `/dataset` menampilkan 9 tanpa evaluasi hit-rate. |
| **Triage vs vonis fraud (dibedakan)** | Ya - `02-architecture.md:42` ("kategori triase, bukan vonis fraud"); out-of-scope `05-decision-scope.md:60` | **Dilanggar** - `dataset-explorer.tsx:81` label "Fraud Terkonfirmasi" dan `:1928` "Escalate (Fraud Terkonfirmasi / Penyidikan)"; `/simulasi` memakai istilah yang sama di `oasis-dashboard.tsx:546` "Kecurangan: 14 berkas (100% terjaring)" | **Total** | Bahasa UI menyebut "terkonfirmasi" pada data simulasi. |
| **Klaim penghematan nasional** | Out-of-scope - `05-decision-scope.md:64` | **Ada** - `fraud-ring.tsx:415`, `roadmap.tsx:34-37` | **Langgar scope** | Angka penghematan tampil sebagai hasil, bukan sebagai proyeksi. |
| **UI yang TIDAK ada di spec**: dashboard HTML standalone `public/dashboard-aegis-jkn.html` (150 KB) | Tidak | Ya - `oasis-dashboard.tsx:1155-1159` iframe; `public/dashboard-aegis-jkn.html` | **UI kedua tanpa versioning** | Angka di iframe terpisah dari komponen React; tidak sinkron, tidak terlacak versinya. |
| **UI yang TIDAK ada di spec**: `src/components/oasis/oasis-dashboard.tsx` (1.116 baris) sebagai route `/simulasi` | Tidak disebut di corpus | Ya - `src/app/simulasi/page.tsx:1-19` | **Di luar desain** | 1.116 baris UI dengan badge kepatuhan sendiri, tidak tercakup acceptance criteria. |
| **UI yang TIDAK ada di spec**: kartu "Nilai Klaim" hardcode, kompatibilitas `next-intl` (dipaketkan tapi dipakai i18n manual) | - | `dataset-explorer.tsx:764`; `package.json:63` | **Yatim** | `next-intl` terpasang tapi tidak dipakai - i18n manual menghindari routing locale yang memang tak ada. |
| **UI yang TIDAK ada di spec**: 4 tab benchmark, graf radar, tren epoch | Tidak | `comparison.tsx:96-113,218-260,365-378` | **Di luar desain** | 20 titik data karangan (`comparison.tsx:372-378`) memenuhi ruang visual. | |
| **Kontrol akses berbasis peran (RBAC)** | Ya - `02-architecture.md:90`; `05-decision-scope.md` | **TIDAK ADA** - `package.json:62` `next-auth` terpasang, 0 importer | **Total** | Semua halaman terbuka untuk publik; tidak ada peran verifikator vs auditor. |
| **Log akses, retensi, prosedur insiden** | Ya - `02-architecture.md:93` | **TIDAK ADA** | **Total** | Tidak ada jejak audit akses. |
| **Pemisahan data N/A vs data hilang** | Ya - `02-architecture.md:21`, `02-architecture.md:99` | Parsial - `notion-datasets.ts` `losHari: number` (tipe non-nullable, `src/types/dataset.ts:17`) | **Parsial** | 109 baris LOS kosong di corpus tidak direpresentasikan; UI tidak membedakan. |
| **Data dictionary 8 entitas FHIR** | Ya - `02-architecture.md:49-58` | Parsial - `src/types/dataset.ts:5-34` (7 dari 8 entitas; tanpa `Referral` sebagai entitas) | **Parsial** | `Referral` dilebur menjadi field string `rujukan` (`types/dataset.ts:11`). |
| **Penggunaan `next-intl` / routing locale** | Tidak | Tidak | - | `package.json:63` `next-intl` tidak terpakai (lihat §6). |

---

## 6. Temuan Kualitas Kode

### 6.1 Aksesibilitas

| ID | Severity | Temuan | Bukti |
|---|---|---|---|
| F-16 | Tinggi | **Node graf SVG tidak dapat diakses keyboard.** `<g onClick>` tanpa `role="button"`, `tabIndex`, atau handler keyboard. 12 node di `/` dan 15 node di ring praktis tak terjangkau keyboard/screen reader. | `src/components/mhgsl/multi-channel-graph.tsx:383-390`; `src/components/mhgsl/fraud-ring.tsx:207-213` |
| F-17 | Tinggi | **Antrean investigasi bukan kontrol interaktif.** Baris antrean pakai `<div onClick>` - tak fokus, tak dapat diaktifkan Enter/Space, tanpa peran ARIA. | `src/components/oasis/oasis-dashboard.tsx:803-811` |
| F-18 | Tinggi | **Tombol tutup panel detail tidak punya nama aksesibel.** Hanya glyph `✕`, tanpa `aria-label`. | `src/components/mhgsl/multi-channel-graph.tsx:485-490` |
| F-53 | Sedang | **Keyboard shortcut global tetap aktif saat fokus di tombol/link.** Guard hanya mengecualikan `INPUT`/`TEXTAREA`/`SELECT`/`contentEditable`; menekan `t`/`p`/`g`/`s` di atas sebuah tombol memicu aksi global (mis. print dialog). | `src/components/mhgsl/use-keyboard-shortcuts.ts:26-33` |
| F-54 | Sedang | **Shortcut panah mencari tombol lewat teks.** `textContent?.trim() === "Next"` - rapuh terhadap perubahan label/i18n, dan tidak punya fallback yang benar untuk mode EN/ID. | `src/app/page.tsx:63-66` (dan `:73-76` untuk "Prev") |
| F-55 | Sedang | **`<html lang>` tidak pernah berubah.** Dikunci `"id"`; setelah pindah ke EN, screen reader tetap membaca bahasa Indonesia. | `src/app/layout.tsx:61` |
| F-56 | Sedang | **Teks 10-11px dipakai luas** untuk data audit kritis (label, sumbu graf, sub-teks KPI) - di bawah ambang keterbacaan. Contoh `text-[10px]` pada poin penghematan dan pada tabel ringkasan. | `src/components/mhgsl/roadmap.tsx:121`; `src/components/oasis/oasis-dashboard.tsx:336,347`; `src/components/mhgsl/comparison.tsx:132` |
| F-23 | Rendah | **Graf SVG tanpa `<title>`/`aria-label` deskriptif**, tanpa alternatif tabel yang setara untuk data metrik. | `src/components/mhgsl/multi-channel-graph.tsx:255`; `src/components/mhgsl/fraud-ring.tsx:150-160` |
| F-57 | Rendah | **Kartu KPI berbasis warna saja** untuk status risiko (hijau/amber/rose) tanpa ikon atau teks yang setara selain label kecil. | `src/components/dataset/dataset-explorer.tsx:712-755` |
| F-58 | Rendah | **`aria-label` hardcoded English** di komponen non-i18n (`Back to top`, `aria-label` close button). | `src/components/mhgsl/back-to-top.tsx:38` |

### 6.2 i18n

| ID | Severity | Temuan | Bukti |
|---|---|---|---|
| F-09 | Tinggi | **6 komponen inti sepenuhnya hardcoded Bahasa Indonesia** - total **4.402 baris** tanpa dukungan `useLang`: `dataset-explorer.tsx` (2.159), `oasis-dashboard.tsx` (1.116), `multi-channel-graph.tsx` (521), `fraud-ring.tsx` (411), `math-formulas.tsx` (272), `fraud-drilldown-modal.tsx` (243). | `grep -L useLang` atas 21 komponen; `multi-channel-graph.tsx:3-22` (tidak import `useLang`) |
| F-10 | Tinggi | **55 dari 148 key kamus mati** (37%): seluruh blok `graph*` (15 key), `ring*` (20 key), `math*` (7 key), `compare*` (13 key), `simSteps`, `heroStats`. Kamus itu sendiri **tidak sinkron** dengan komponen yang mengimplementasikan string tersebut secara manual. | `src/components/mhgsl/i18n.tsx:7-179` (interface `Dict`) vs pemakaian di `src/**` |
| F-11 | Tinggi | **English locale terputus di beberapa tempat**: `hero.tsx:209` memakai `HERO_STATS` dari `data.ts` sehingga label `t.heroStats` (`i18n.tsx:556-561`) tak pernah tampil; `problem-section.tsx:81,90` bercabang dengan **membandingkan string Inggris** `t.problemFraudSub === "of national total claim value"`. | `src/components/mhgsl/hero.tsx:7,209`; `src/components/mhgsl/problem-section.tsx:81,90` |
| F-12 | Sedang | **Kamus i18n ditulis manual, bukan `next-intl`** walau `next-intl` terpasang. Tidak ada routing locale, tidak ada message extraction, tidak ada deteksi locale dari `<html lang>`. | `src/components/mhgsl/i18n.tsx:877-909`; `package.json:63` |
| F-13 | Sedang | **Dokumentasi mengklaim "kamus bilingual penuh"** yang menyalakan "seluruh istilah antarmuka, terminologi medis, metrik evaluasi, dan narasi investigasi" - tidak berlaku untuk 6 komponen di atas. | `docs/user-guide/navigation.md:26-28` |

### 6.3 Error handling, loading, empty state

| ID | Severity | Temuan | Bukti |
|---|---|---|---|
| F-26 | Tinggi | **Tidak ada `error.tsx`, `loading.tsx`, `not-found.tsx`** di `src/app/`. Gunakan `Link`/navigasi client ke route yang bisa gagal; tidak ada fallback. | `src/app/` hanya berisi 6 file (lihat §2.1) |
| F-27 | Tinggi | **Tidak ada batas ukuran file/baris pada uploader.** `parseCSV` memecah seluruh file ke memori, `scoreRows` menjalankan loop O(n kuadrat) similarity (baris 105-117) di thread utama. File besar → freeze UI. | `src/components/mhgsl/data-uploader.tsx:60-77,105-117` |
| F-28 | Sedang | **Latensi palsu 700 ms** disisipkan untuk kesan proses; tidak ada pekerjaan nyata async. | `src/components/mhgsl/data-uploader.tsx:241` |
| F-29 | Sedang | **Penanganan file JSON tidak membedakan jenis galat.** Semua kegagalan parse → pesan generik "Gagal parse file…". Galat `JSON.parse` yang detail hilang. | `src/components/mhgsl/data-uploader.tsx:217-232` |
| F-30 | Sedang | **CSV parser tidak menangani field ter-quote.** `line.split(",")` merusak kolom yang mengandung koma di dalam tanda kutip (nama, narasi). | `src/components/mhgsl/data-uploader.tsx:65` |
| F-31 | Sedang | **Uploader tidak memvalidasi skema/kolom wajib.** Kolom hilang menghasilkan `undefined` → `Number(undefined)||0` = 0, sehingga baris tetap "berhasil" diskor dengan nilai nol. | `src/components/mhgsl/data-uploader.tsx:67-75,89-93` |
| F-32 | Rendah | **Empty state ada tapi minimal**: hanya 2 pesan "tidak ada yang cocok" + tombol reset; tidak ada panduan atau telemetri. | `src/components/dataset/dataset-explorer.tsx:1072-1081,1241-1249`; `src/components/oasis/oasis-dashboard.tsx:1118-1122` |
| F-33 | Rendah | **Tidak ada error boundary React** di root; kesalahan render komponen besar (`dataset-explorer` 2.159 baris) downed seluruh halaman. | `src/app/layout.tsx:60-78` |

### 6.4 Keamanan & XSS

| ID | Severity | Temuan | Bukti |
|---|---|---|---|
| F-34 | Sedang | **Satu-satunya `dangerouslySetInnerHTML`** ada di komponen shadcn `chart.tsx` untuk style SVG Recharts - isinya style statis, bukan input pengguna, sehingga **risiko XSS rendah**. Tidak ada `dangerouslySetInnerHTML` di komponen aplikasi. | `src/components/ui/chart.tsx:83` |
| F-35 | Sedang | **Tidak ada kontrol akses.** `next-auth` terpasang (`package.json:62`) tapi 0 importer; semua route publik, termasuk `/simulasi` yang menampilkan "verdict auditor" dan rekomendasi penangguhan klaim. | `src/app/simulasi/page.tsx:1-19`; `src/components/oasis/oasis-dashboard.tsx:415-425` |
| F-36 | Sedang | **Metadata memakai placeholder pihak ketiga** (`z.ai` / `chatglm.cn`), termasuk `openGraph.url` yang menunjuk domain yang bukan milik proyek. | `src/app/layout.tsx:37,43` |
| F-37 | Sedang | **`npm postinstall` menjalankan `prisma generate`** dan ada script `db:push --accept-data-loss` - tetapi tidak ada `prisma/migrations/`, dan `.env.example` hanya `DATABASE_URL="file:./db/custom.db"` (SQLite) yang tidak pernah dipakai. Risiko: developer menjalankan `db:push` tanpa menyadari dampaknya. | `package.json:10-14`; `.env.example:1-2` |
| F-38 | Rendah | **Tidak ada rate limit / validasi ukuran pada endpoint** API (meski endpoint-nya masih stub). | `src/app/api/route.ts:3-5` |
| F-39 | Rendah | **Data sintetis real (nama dokter/pasien, tanggal, nominal) dimuat penuh ke bundle klien.** Untuk demo sintetis ini tidak otomatis pelanggaran, tapi `i18n.tsx:523-524` mengklaim "dihasilkan via DP-CTGAN" yang **tidak sesuai sumber dataset** (dump Notion 300 baris, bukan DP-CTGAN) - pernyataan kepatuhan yang salah sasaran. | `src/components/mhgsl/i18n.tsx:523-524,870-871` vs `src/data/notion-datasets.ts:402` |

### 6.5 Performa

| ID | Severity | Temuan | Bukti |
|---|---|---|---|
| F-40 | Tinggi | **Bundle aplikasi memuat 9.401 baris dataset + 886 baris payload statis secara eager di client component.** `notion-datasets.ts` mengimpor seluruh 300 klaim + 33 riset ke bundle; `dataset-explorer.tsx` adalah `"use client"`. | `src/data/notion-datasets.ts:3,402`; `src/components/dataset/dataset-explorer.tsx:1-205` |
| F-41 | Sedang | **Entri riset dirender dua kali** pada halaman yang sama (`filteredResearch.map` di dua tempat) - pekerjaan render ganda untuk data yang sama. | `src/components/dataset/dataset-explorer.tsx:1534,1631` |
| F-42 | Sedang | **Animasi `whileInView` + `AnimatePresence` pada 12+ komponen** tanpa `prefers-reduced-motion` guard. | `src/components/mhgsl/architecture.tsx:30-33` (pola diulang di 10 file lain) |
| F-43 | Sedang | **Tidak ada `React.memo`/`useMemo` pada peta SVG 12 node & 15 node**; `nodeMap` di-memo, tetapi `MHGSL_EDGES.filter(...)` dipanggil **per node** saat render (O(V·E)). | `src/components/mhgsl/multi-channel-graph.tsx:453-454` |
| F-44 | Rendah | **`iframe` 750 px memuat HTML 150 KB** saat tab dibuka, tanpa lazy-mount. | `src/components/oasis/oasis-dashboard.tsx:1153-1159`; `public/dashboard-aegis-jkn.html` (150.741 B) |

### 6.6 Kode mati, dependensi, toolchain

| ID | Severity | Temuan | Bukti |
|---|---|---|---|
| F-45 | Sedang | **20 dari 66 dependensi produksi tidak pernah diimpor**: `@dnd-kit/core`, `@dnd-kit/sortable`, `@dnd-kit/utilities`, `@hookform/resolvers`, `@mdxeditor/editor`, `@reactuses/core`, `@tanstack/react-query`, `@tanstack/react-table`, `date-fns`, `next-auth`, `next-intl`, `react-markdown`, `react-syntax-highlighter`, `sharp`, `tailwindcss-animate`, `uuid`, `z-ai-web-dev-sdk`, `zod`, `zustand`. | `package.json:16-83` vs `grep` seluruh `src/` + `examples/` |
| F-46 | Sedang | **4 export mati di `data.ts`**: `RISK_PILLARS` (`:27`), `ROADMAP` (`:358`), `ROI_STATS` (`:390`), `DATASET_METRICS` (`:502`) - 0 referensi di luar file. `ROADMAP`/`ROI_STATS` menduplikasi isi `i18n.tsx:453-490` → **dua sumber kebenaran** untuk roadmap & ROI. | `src/components/mhgsl/data.ts:27,358,390,502` |
| F-47 | Tinggi | **`npx tsc --noEmit` menghasilkan 8 error, ditutup oleh `ignoreBuildErrors: true`.** 4 di antaranya error tipe nyata pada `Dict`: `mathTitle2b` tidak ada di interface (`:386`, `:734`), `roiTitle3`/`roiTitle4` tidak ada (`:71`) - artinya string itu **tidak pernah tampil** di UI: `roadmap.tsx:71` merender `undefined`. | `npx tsc --noEmit` → `i18n.tsx:386,734`, `roadmap.tsx:71`, `fraud-drilldown-modal.tsx:120` (unused `@ts-expect-error`), `simulation.tsx:337` (unused `@ts-expect-error`); `next.config.ts:5-7` |
| F-48 | Sedang | **`.sort()` dilakukan in-place pada array yang diimpor** dari `data.ts` - mutate shared module state, bisa mengubah urutan di render berikutnya. | `src/components/mhgsl/fraud-drilldown-modal.tsx:169-170` |
| F-49 | Sedang | **`reactStrictMode: false`** - double-render tidak terdeteksi, beberapa bug efek (mis. `simulation.tsx:56-70`) bisa lolos. | `next.config.ts:8` |
| F-50 | Rendah | **Tidak ada test framework.** `tests/` hanya berisi 3 shell script build runtime; tidak ada unit test, tidak ada `vitest`/`jest`, tidak ada `test` script di `package.json`. | `tests/*.sh`; `package.json:5-15` |
| F-51 | Rendah | **Tidak ada artefak ML di repo** (`configs/`, `data/`, `scripts/`, `experiments/`, `notebooks/` - semua tidak ada), padahal roadmap UI mengutip `configs/leakage.yaml` sebagai item Fase 0 "Berlangsung". | `data.ts:363`; `i18n.tsx:470`; `ls` repo root |
| F-52 | Rendah | **`z-ai-web-dev-sdk`** dipaketkan sebagai dependensi produksi - SDK generator situs pihak ketiga yang tidak relevan dengan produk. | `package.json:80` |

---

## 7. Apakah Simulator Benar-Benar Bisa Dijalankan?

**Ya sebagai antarmuka; tidak sebagai model.** Alur ini bisa dijalankan tanpa satu pun backend, inference, atau data nyata.

### 7.1 Alur yang berjalan

1. `simulation.tsx:44-46` menyimpan `stepIdx` (0..3) dan `playing`; `step = SIM_STEPS[stepIdx]`, `progress = CHANNEL_PROGRESS[stepIdx]`.
2. `simulation.tsx:49-54` - `next()`/`prev()`/`reset()` mengubah indeks; tidak ada komputasi.
3. `simulation.tsx:56-70` - autoplay memakai `setTimeout(..., 2200)` (bukan 3 detik seperti klaim dokumentasi `navigation.md:78`).
4. `simulation.tsx:207` `AnimatePresence mode="wait"` menganimasikan pergantian langkah; `simulation.tsx:333` menampilkan gauge `<Progress>`.
5. `simulation.tsx:349` - panel SHAP **hanya** tampil di langkah terakhir (`stepIdx === SIM_STEPS.length - 1`).
6. `simulation.tsx:120-133,405-414` - stepper dan progress bar dapat diklik; `178-199` tombol Reset/Prev/Auto-Play/Next dengan `disabled` sesuai batas.

### 7.2 Bukti bahwa tidak ada komputasi

| Aspek | Bukti | Verdict |
|---|---|---|
| Skor langkah | `data.ts:304-337` - `score: 0.32, 0.61, 0.84, 0.94` konstanta | Hardcode |
| Kontribusi kanal per langkah | `data.ts:350-355` - 4 baris konstanta (0.32/0.61/0.84/0.94) | Hardcode |
| Atribusi SHAP | `data.ts:340-346` - 5 nilai konstanta (0.41/0.28/0.19/0.12/−0.07) | Hardcode |
| Graf yang ditampilkan | `data.ts:87-137` - 12 node, 20 edge; label node & bobot edge tulis tangan | Hardcode |
| Perhitungan | **Tidak ada satu pun operasi aritmetika pada data di `simulation.tsx`** selain `stepIdx + 1` dan indeks array | **Tidak ada komputasi** |
| Data masukan | Nol baris dari `notion-datasets.ts` masuk ke `simulation.tsx` | **Tidak ada data nyata** |
| Koneksi model/backend | Nol pemanggilan `fetch`; `api/route.ts` adalah stub | **Tidak ada model** |
| Klaim ilustratif | `data.ts:310` "Cosine Similarity 0.92", `data.ts:322` "0.88" - angka yang di dalam graf adalah nilai yang sama, bukan yang dihitung | Konsisten secara internal, bukan hasil hitung |

**Kesimpulan.** Simulator adalah *state machine animasi* yang memutar 4 slide berangka tetap. Ia interaktif (Next/Prev/Reset/Auto-Play/stepper/panel SHAP), ia bisa dijalankan, tetapi **tidak menjalankan model apa pun**: tidak ada feature extraction, tidak ada GCN, tidak ada fusi late-fusion, tidak ada SHAP computation. Nilai yang ditampilkan identik dengan konstanta di `data.ts`. Satu-satunya komponen di seluruh aplikasi yang benar-benar menghitung adalah `data-uploader.tsx:79-148` - dan itu pun memakai heuristik string, bukan model (lihat §8).

Yang **berpisah** dari simulasi: `multi-channel-graph.tsx` benar-benar punya state (channel aktif `46`, visibilitas `47`, hover `48`, pilih `49`, metapath `50`) dan `fraud-ring.tsx` punya toggle highlight (`68`) dan mode message-passing (`69`, dipakai `406,414`) - interaksinya nyata, datanya tetap mock.

---

## 8. Roadmap UI vs Dokumen vs Realitas

### 8.1 Roadmap dalam UI

`roadmap.tsx:143-146` menetapkan status **berdasarkan indeks array**, bukan berdasarkan data:

```ts
const statusOrder: ("active" | "next" | "future")[] = ["active", "next", "future", "future"];
const status = statusOrder[i] ?? "future";
```

Efeknya: **Fase 0 selalu "Berlangsung"**, apa pun isi Fase 0. Status tidak pernah berubah, tidak pernah dihitung, dan tidak ada sumber status lain (`data.ts:358-387` punya field `status` sendiri yang justru **mati** - 0 referensi).

### 8.2 Tabel status roadmap

| Fase | Status di UI (`roadmap.tsx:144`) | Isi item (`i18n.tsx:465-490`) | Realitas di repo | Status sebenarnya |
|---|---|---|---|---|
| **Fase 0** - Fondasi & Audit Data v2.1 | "Berlangsung" (aktif) | "Dataset v2.1 (300 klaim, seed 20260707)" | **Ada** - `src/data/notion-datasets.ts:402`, 300 record, seed tidak stored di dalam record | ✅ Selesai (data) |
| | | "Blokir kolom leakage (`configs/leakage.yaml`)" | **Folder `configs/` tidak ada.** Tidak ada `leakage.yaml`, tidak ada `tests/test_leakage.py` | ❌ **Tidak ada** |
| | | "Evaluasi group-aware (GroupKFold & LOGO)" | **Tidak ada** skrip evaluasi, manifest, atau `experiment_manifest.json` di repo (`02-architecture.md:76-86` wajib) | ❌ **Tidak ada** |
| **Fase 1** - Baseline Tabular & ML | "Berikutnya" | "Baseline XGBoost + SMOTE & MLP PyTorch" | **Tidak ada** kode Python, notebook, atau `.pth`. `package.json` tak punya dependensi ML. | ❌ **Tidak ada** |
| | | "Rekayasa fitur agregat 30 hari & rasio tarif" | Tidak ada; kolom `alasan` di dataset berisi narasi, bukan nilai fitur terhitung | ❌ **Tidak ada** |
| | | "Benchmark awal AUPRC pada prevalensi 3–7%" | Angka AUPRC di UI berasal dari `data.ts:258-265` - konstanta, bukan benchmark. | ❌ **Fabrikasi** |
| **Fase 2** - Graf Heterogen & MHGSL | "Visi jangka panjang" | "Konstruksi PyG HeteroData (3 saluran paralel)" | **Tidak ada** PyG/HeteroData. Yang ada: SVG statis 12 node (`multi-channel-graph.tsx:255-460`). | ❌ **Tidak ada** (UI hanya visual, bukan model) |
| | | "Dual GCN (Channel-Specific & Shared-Parameter)" | **Tidak ada** implementasi GCN. | ❌ **Tidak ada** |
| | | "Modul XAI (SHAP per-saluran & TreeExplainer)" | **Tidak ada** TreeExplainer. `SHAP_ATTRS` (`data.ts:340-346`) adalah 5 konstanta. | ❌ **Fabrikasi** |
| **Fase 3** - Validasi Final & Pilot 5 FKRTL | "Visi jangka panjang" | "Late Fusion NLP teks & sentimen (γ = 0.10)" | γ hanya konstanta di teks LaTeX (`math-formulas.tsx:250`) & label roadmap. Tidak ada implementasi fusi teks. | ❌ **Tidak ada** |
| | | "Uji 9 sindikat (SYND-01 s.d. SYND-09)" | `/simulasi` hanya menguji **5** sindikat (`oasis-data.ts:100-110`); 9 sindikat ada di dataset tapi tanpa hit-rate. | ⚠️ **Separuh** |
| | | "Pilot operasional 5 FKRTL rujukan JKN" | **Tidak ada** - dan `05-decision-scope.md:63` menyatakan pengoperasian sistem produksi di luar lingkup. | ❌ **Di luar scope** |

**7 dari 12 item roadmap UI tidak punya artefak di repo. 1 item (Fase 3 pilot) justru di luar lingkup yang dideklarasikan dokumen sendiri.**

### 8.3 Roadmap vs `10-simulation-dataset.md:207-213`

Dokumen menyebut Fase 0 = "Dataset v2.1, leakage.yaml, unit test" (minggu 1) dan Fase 2 = "PyG HeteroData, MHGSL, SHAP per-saluran" (minggu 4-6). UI menampilkan rencana identik, tetapi **pada halaman yang sama** menampilkan hasil fase 2 dan 3 sebagai fait accompli (graf 3-saluran, SHAP per-saluran, 100% recall, badge "SESUAI"). Presentasi visual membangun ilusi hasil yang tidak didukung artefak mana pun.

---

## 9. Dokumentasi vs Kode

`docs/user-guide/navigation.md` (122 baris) - 12 klaim yang tidak sesuai dengan implementasi:

| # | Klaim di docs | Lokasi docs | Realitas kode | Dampak |
|---|---|---|---|---|
| 1 | "tombol uploader klaim" ada di Navbar | `navigation.md:12` | **Tidak ada.** `navbar.tsx:18-23` import Glossary/Shortcuts/Lang/Theme; `DataUploader` hanya di `comparison.tsx:92` | Pengguna tidak menemukan uploader; dokumentasi Navigasi utama salah |
| 2 | "Klik tombol **Uji Data Mandiri** … di Navbar atau bagian header" | `navigation.md:110` | Tombol tersebut tidak ada di Navbar. Label yang dipakai: `data-uploader.tsx:189` (`t_local.uploadHint`) | Jalur discoverability salah |
| 3 | "**Metode C**: Salin dan tempel data berformat teks CSV langsung ke area input" | `navigation.md:114` | **Tidak ada textarea/paste handler** di `data-uploader.tsx` (0 kemunculan `textarea`/`onPaste`). Hanya file input + drag-drop + tombol "Gunakan Contoh". | Metode yang didokumentasikan tidak ada |
| 4 | Auto-Play "dengan jeda **3 detik** per tahap" | `navigation.md:78` | `simulation.tsx:68` - `}, 2200)` | Selisih 800 ms |
| 5 | "Struktur antarmuka terdiri dari **8 seksi utama**" | `navigation.md:11-19` | Halaman `/` punya **10 seksi**: problem, architecture, graph, simulation, math, compare, ring, roadmap (+ hero, footer) - `page.tsx:91-99` | Dokumen tidak memuat Roadmap, Hero, maupun Footer |
| 6 | "Pilihan bahasa tersimpan di **state memori peramban** selama sesi aktif" | `navigation.md:29` | `i18n.tsx:893,898` - `localStorage` key `aegis-lang` (bertahan lintas sesi) | Deskripsi mekanisme salah |
| 7 | "Platform dilengkapi **sistem kamus bilingual penuh**… mengalihkan **seluruh istilah antarmuka, terminologi medis, metrik evaluasi, dan narasi investigasi**" | `navigation.md:26-28` | 6 komponen (4.402 baris) hardcoded ID; 55 key mati | Jaminan yang tidak terpenuhi |
| 8 | "Seluruh pintasan **diabaikan otomatis** saat verifikator mengetik di dalam formulir input teks" | `navigation.md:45` | Benar untuk INPUT/TEXTAREA/SELECT, tapi **tidak** untuk BUTTON/LINK (`use-keyboard-shortcuts.ts:26-33`) | Gangguan saat fokus di tombol |
| 9 | "**Dukungan Dwibahasa ID/EN**" + "tampilan bahasa Inggris" | `navigation.md:25-30` | Halaman `/dataset` dan `/simulasi` **tidak punya** toggle bahasa sama sekali (`grep useLang` → tidak ada) | Dua dari tiga route sepenuhnya monolingual |
| 10 | "Klik simpul **D₁**, **RS_A**, atau **P₁**" untuk membuka modal audit | `navigation.md:97` | Benar - `fraud-ring.tsx:16,19,21` punya `profileId`; tapi 12 dari 15 node **tidak punya** `profileId` (hanya 3 yang punya) | Sebagian sesuai |
| 11 | "**Bobot pembuktian matematis** dari kanal semantik, fitur, dan topologi" | `navigation.md:101` | Bobot hardcode (`data.ts:424-427`), tidak dihitung dari model | Istilah "matematis" menyesatkan |
| 12 | "**deviasi peer** ($+4.2\sigma$)" | `navigation.md:103` | Nilai konstanta `data.ts:439` | Angka karangan |

Tambahan: `docs/user-guide/navigation.md` **tidak menyebut** `/dataset` dan `/simulasi` sebagai route meski keduanya ada di `navbar.tsx:126-144`. `wiki/reference/component-catalog.md` dan `wiki/guides/custom-data-scoring.md` ada, tetapi `wiki/` bukan bagian dari deliverable terdokumentasi dan isinya tidak diverifikasi dalam audit ini.

---

## 10. Prisma / Audit Trail

### 10.1 Isi `prisma/schema.prisma` (32 baris)

```
generator client { provider = "prisma-client-js" }    // :7-9
datasource db { provider = "sqlite"; url = env("DATABASE_URL") } // :11-14

model User { id, email, name, createdAt, updatedAt }    // :16-22
model Post { id, title, content, published, authorId, createdAt } // :24-32
```

Dua model boilerplate Next.js starter. **Nol** model domain. Tidak ada `Claim`, `Patient`, `Practitioner`, `Organization`, `Condition`, `Procedure`, `Medication`, `Referral` (kontrak data `02-architecture.md:49-57`), tidak ada `AuditTrail`, `ModelVersion`, `Prediction`, `ReviewAction`, `Override`, `ReviewQueue`, `ExperimentManifest`, `SplitManifest`, `Rule`.

### 10.2 Jejak pemakaian

| Artefak | Bukti | Status |
|---|---|---|
| `src/lib/db.ts` | `src/lib/db.ts:7` export `db` (PrismaClient, singleton global) | **0 importer** di seluruh `src/` dan `examples/` - kode mati |
| Migrasi | `prisma/` berisi **hanya** `schema.prisma`; tidak ada `prisma/migrations/` | Tidak ada riwayat skema |
| `db:push` | `package.json:11` - `prisma db push --accept-data-loss` | Tersedia tapi tanpa alasan dipakai; tidak ada `db/` di repo |
| `DATABASE_URL` | `.env.example:1` - `file:./db/custom.db` (SQLite) | Tidak pernah dibaca; `db/` tidak ada di repo |
| `postinstall` | `package.json:10` - `prisma generate` | Dijalankan di setiap install, menghasilkan client yang tak terpakai |
| API | `src/app/api/route.ts:3-5` | Tidak menyentuh Prisma |

### 10.3 Penilaian terhadap klaim "audit trail"

Butir `01-proposal.md:60`: "Audit trail: merekam versi model, waktu prediksi, alasan, tindakan verifikator, dan perubahan keputusan."*
Butir `00-dashboard.md:55`: fitur inti MVP salah satunya "audit trail".
`05-decision-scope.md:58`: "log audit dan evaluasi yang dapat direproduksi" - in-scope.

**Tidak ada satu pun dari lima elemen yang terpenuhi:**

| Elemen audit trail | Ada? | Bukti |
|---|---|---|
| Versi model | ❌ | Tidak ada model `ModelVersion`; tidak ada nomor versi di UI mana pun (`i18n.tsx`/components) |
| Waktu prediksi | ❌ | Tidak ada kolom/waktu prediksi; `notion-datasets.ts` menyimpan `tanggal` klaim, bukan waktu inferensi |
| Alasan | ⚠️ | Alasan **terbaca** (`dataset-explorer.tsx:2168` `selectedClaim.alasan`) tapi **tidak direkam** |
| Tindakan verifikator | ❌ | Tidak ada kontrol review (`oasis-dashboard.tsx:798-830`; `dataset-explorer.tsx:1973-2170`) |
| Perubahan keputusan | ❌ | Tidak ada model `ReviewAction`/`Override`, tidak ada event, tidak ada log |
| Log audit yang dapat direproduksi | ❌ | `02-architecture.md:75-86` (10 artefak wajib per eksperimen) - **tidak ada satu pun** (`experiment_manifest.json`, checksum dataset, konfigurasi model, daftar fitur, ID split, prediksi per klaim, label pembanding, skrip metrik, log, analisis kesalahan, batasan interpretasi) |

**Kesimpulan.** Klaim "audit trail" pada proposal adalah klaim **yang belum didukung implementasi apa pun** - di database, di API, maupun di UI. Ini adalah kesenjangan paling material antara dokumen dan kode, karena menyangkut seluruh daftar in-scope `05-decision-scope.md:51-58` dan prinsip "ketertelusuran" `02-architecture.md:14`.

---

## 11. Rekomendasi Terurut

### P0 - Hilangkan klaim yang tidak dapat dipertanggungjawabkan (1-2 hari, edit teks saja)

1. **Hapus atau turunkan ke badge "simulasi"** angka `93%` (`oasis-dashboard.tsx:334`), `AUPRC 0.91` (`data.ts:264`), `ROC-AUC 0.95` (`data.ts:300`), `Precision 0.92` (`data.ts:295`), `Rp 1,2 M / Rp 14,4 M` (`fraud-ring.tsx:415`, `roadmap.tsx:34`). Tambahkan label wajib "simulasi sintetis, prevalensi oversampled" **pada kartu yang sama**, bukan di tab lain. *(F-03, F-04, F-02)*
2. **Matriks kepatuhan & badge "SESUAI"** (`oasis-dashboard.tsx:681,693,705,717`, `:198`) harus menampilkan status per-kriteria yang **dihitung dari data**, atau diberi label "sebelum validasi independen". Hapus field literal `status`/`ok` (`oasis-data.ts:95-96`). *(F-20)*
3. **Perbaiki satuan**: `Rp 3,53 M` → "Rp 3,53 Miliar" (`dataset-explorer.tsx:764`); dan selaraskan ID vs EN untuk penghematan (`i18n.tsx:443` vs `:791` - 1000×). *(F-04, F-25)*
4. **Hapus `data.ts:441` "Tangguhkan pre-authorization…"** (dirender lewat `fraud-drilldown-modal.tsx:240-243` "Rekomendasi Tindakan (HITL)") sebagai instruksi otomatis - `05-decision-scope.md:60-61` melarang penolakan/pemotongan otomatis. Ganti menjadi "usulan telaah". *(F-07)*
5. **Perbaiki disclaimer footer** `i18n.tsx:523-524` - dataset berasal dari dump Notion 300 baris, bukan DP-CTGAN. Klaim kepatuhan harus akurat. *(F-39)*

### P1 - Perbaiki penggabungan data (3-5 hari)

6. **Sambungkan `data.ts` ke `NOTION_CLAIMS_DATASET`** untuk graf, simulasi, dan fraud ring. Minimal: node/edge graf diturunkan dari klaim nyata (KLM001-003 untuk SYND-01), dan skor simulasi dihitung dari `skorFraud`/`kontribusiSaluran` yang sudah ada di record. Hapus `DATASET_METRICS` atau jadikan sumber tunggal. *(F-01, F-46)*
7. **Hapus atau hitung metrik benchmark dari artefak nyata.** Bila belum ada eksperimen, ganti label "AUPRC" dengan "Skor ilustratif" dan hapus graf tren epoch (`comparison.tsx:372-378`). *(F-02)*
8. **Terapkan `configs/leakage.yaml` + `tests/test_leakage.py` yang diklaim Fase 0**, atau ubah teks roadmap Fase 0 agar jujur. Hapus 4 export mati `data.ts:27,358,390,502` dan jadikan `i18n.tsx:465-490` satu-satunya sumber roadmap. *(F-46, F-51, F-19)*
9. **Perbaiki status roadmap agar berasal dari data** (`status` per fase di satu konstanta), bukan `statusOrder[i]`. *(F-19)*

### P2 - Tutup celah fungsional inti (1-2 minggu)

10. **Implementasikan minimal audit trail**: model `AuditEvent { id, claimId, modelVersion, threshold, predictedAt, reason, action, overrideReason, followUpStatus }` di `prisma/schema.prisma`, endpoint POST di `src/app/api/`, dan **7 field wajib `02-architecture.md:40-47` lengkap di sheet detail** `dataset-explorer.tsx:1973-2170` - terutama versi model & threshold, aturan terpicu, sumber & waktu data, dan tindakan reviewer + alasan override. *(F-05, F-07, F-08)*
11. **Pisahkan yang synthetic vs real secara tegas di UI**: `/simulasi` memakai dataset v1 (100 klaim) tetapi mempresentasikan diri "v2.1" - tambahkan badge versi dataset di header dan skew seluruh angka ke v2 (300 klaim) atau labeli eksplisit. *(F-20, F-25)*
12. **Aktifkan RBAC** (`next-auth` sudah terpasang) untuk `/simulasi` dan endpoint tulis. *(F-35)*

### P3 - Kualitas kode, a11y, i18n (2-3 minggu)

13. **Hapus `ignoreBuildErrors: true`** (`next.config.ts:5-7`) dan perbaiki 4 error `Dict` - `mathTitle2b` (`i18n.tsx:386,734`) dan `roiTitle3`/`roiTitle4` (`roadmap.tsx:71`, yang saat ini merender `undefined`). Set `reactStrictMode: true`. *(F-47, F-49)*
14. **Perbaiki a11y graf**: `role="button"` + `tabIndex={0}` + handler Enter/Space pada `<g>` (`multi-channel-graph.tsx:383-390`, `fraud-ring.tsx:207-213`), ubah baris antrean ke `<button>` (`oasis-dashboard.tsx:803-811`), tambahkan `aria-label` pada tombol tutup (`multi-channel-graph.tsx:485-490`), dan perbarui `<html lang>` saat `lang` berubah (`layout.tsx:61`). *(F-16, F-17, F-18, F-55)*
15. **Rampungkan i18n**: hapus 55 key mati, pindahkan 6 komponen hardcoded ke `useLang`, dan hapus `heroStats` duplikat (`hero.tsx:209` → pakai `t.heroStats`). Hapus `next-intl` bila i18n manual dipertahankan. *(F-09, F-10, F-11, F-45)*
16. **Perkuat uploader**: parser CSV yang menghormati quote (`data-uploader.tsx:65`), validasi kolom wajib, batas ukuran/baris, hapus latensi palsu 700 ms, dan ganti heuristik substring "semantik" (`data-uploader.tsx:121-125`) dengan label jujur ("heuristik lexical") supaya tidak disalahartikan sebagai saluran semantik MHGSL. *(F-27, F-28, F-30, F-31)*
17. **Tambahkan `error.tsx`, `loading.tsx`, `not-found.tsx`** di `src/app/` dan satu `error boundary` di root. *(F-26, F-33)*

### P4 - Kebersihan (bersamaan)

18. **Hapus 20 dependensi mati** (`package.json:16-83`) dan `z-ai-web-dev-sdk`; hapus `next.config.ts` override `ignoreBuildErrors`; hapus `public/logo.svg` yang tak dipakai (metadata masih menunjuk logo pihak ketiga - `layout.tsx:37,43`).
19. **Perbaiki `navigation.md`**: hapus "uploader di Navbar" (`:12`, `:110`), "Metode C tempel" (`:114`), ubah "3 detik" → "2,2 detik" (`:78`), "8 seksi" → 10 (`:11`), "state memori" → "localStorage" (`:29`), dan tambahkan route `/dataset` & `/simulasi`. *(§9)*
20. **Tambahkan test suite** minimal (`vitest`) untuk: parser CSV, `scoreRows` uploader, dan KPI `dataset-explorer.tsx:214-242` terhadap angka korpus (300/240/24/36/Rp 3.526.650.000). Dan sediakan `configs/leakage.yaml` + `tests/test_leakage.py` seperti dijanjikan `10-simulation-dataset.md:126-127`.

---

### Lampiran - Daftar Temuan (ID → severity)

| ID | Sev | Ringkas | Path:line utama |
|---|---|---|---|
| F-01 | Kritis | Route `/` tanpa data nyata | `data.ts:502-519`; `app/page.tsx:89-99` |
| F-02 | Kritis | Metrik benchmark difabrikasi | `data.ts:253,258-265,294-301`; `comparison.tsx:372-378` |
| F-03 | Kritis | Angka 93% sebagai KPI utama | `oasis-dashboard.tsx:334`; `oasis-data.ts:97` |
| F-04 | Kritis | Penghematan finansial sebagai hasil | `fraud-ring.tsx:415`; `roadmap.tsx:34-37` |
| F-05 | Kritis | Audit trail absen | `prisma/schema.prisma:16-32`; `lib/db.ts:7` |
| F-06 | Kritis | Tanpa backend | `api/route.ts:3-5` |
| F-07 | Kritis | Tidak ada review/override | `oasis-dashboard.tsx:798-830`; `dataset-explorer.tsx:1973-2170` |
| F-08 | Tinggi | 4 dari 7 field wajib §3.6 hilang | `dataset-explorer.tsx:2047-2168` |
| F-09 | Tinggi | 6 komponen tanpa i18n (4.402 baris) | `multi-channel-graph.tsx:3-22`; `fraud-ring.tsx`; `math-formulas.tsx`; `dataset-explorer.tsx`; `oasis-dashboard.tsx`; `fraud-drilldown-modal.tsx` |
| F-10 | Tinggi | 55 key i18n mati | `i18n.tsx:7-179` |
| F-11 | Tinggi | Locale EN terputus | `hero.tsx:209`; `problem-section.tsx:81,90` |
| F-12 | Sedang | i18n manual, `next-intl` menganggur | `i18n.tsx:877-909`; `package.json:63` |
| F-13 | Sedang | Docs klaim bilingual penuh | `docs/user-guide/navigation.md:26-28` |
| F-14 | Tinggi | "5 entitas" vs 8 node fraud | `multi-channel-graph.tsx:226`; `i18n.tsx:334,682`; `data.ts:87-109` |
| F-15 | Tinggi | "14 edge" vs 13 edge | `fraud-ring.tsx:275,280` vs `:36-45` |
| F-16 | Tinggi | Node SVG tidak keyboard-accessible | `multi-channel-graph.tsx:383-390`; `fraud-ring.tsx:207-213` |
| F-17 | Tinggi | Antrean `<div onClick>` | `oasis-dashboard.tsx:803-811` |
| F-18 | Tinggi | Tombol tutup tanpa `aria-label` | `multi-channel-graph.tsx:485-490` |
| F-19 | Tinggi | Roadmap status by-index; item Fase 0 tidak ada | `roadmap.tsx:144`; `i18n.tsx:470` |
| F-20 | Sedang | Badge "SESUAI" dari literal | `oasis-dashboard.tsx:198`; `oasis-data.ts:95-96` |
| F-55 | Sedang | `<html lang>` mati | `layout.tsx:61` |
| F-56 | Sedang | Teks 10-11px untuk data kritis | `roadmap.tsx:121`; `oasis-dashboard.tsx:336,347` |
| F-23 | Rendah | SVG tanpa title/aria-label | `multi-channel-graph.tsx:255`; `fraud-ring.tsx:150-160` |
| F-57 | Rendah | Kode warna tanpa teks setara | `dataset-explorer.tsx:712-755` |
| F-25 | Sedang | Diskon 1000× ID vs EN | `i18n.tsx:443` vs `:791` |
| F-26 | Tinggi | Tidak ada error/loading/not-found | `src/app/` (6 file) |
| F-27 | Tinggi | Uploader tanpa batas ukuran; O(n²) | `data-uploader.tsx:60-77,105-117` |
| F-28 | Sedang | Latensi palsu 700 ms | `data-uploader.tsx:241` |
| F-29 | Sedang | Galat JSON generik | `data-uploader.tsx:217-232` |
| F-30 | Sedang | CSV split(",") tanpa quote | `data-uploader.tsx:65` |
| F-31 | Sedang | Tanpa validasi kolom wajib | `data-uploader.tsx:67-75` |
| F-32 | Rendah | Empty state minimal | `dataset-explorer.tsx:1072-1081` |
| F-33 | Rendah | Tanpa error boundary | `layout.tsx:60-78` |
| F-34 | Sedang | `dangerouslySetInnerHTML` (risiko rendah) | `ui/chart.tsx:83` |
| F-35 | Sedang | Tanpa kontrol akses | `package.json:62`; `simulasi/page.tsx:1-19` |
| F-36 | Sedang | Metadata placeholder z.ai | `layout.tsx:37,43` |
| F-37 | Sedang | `db:push --accept-data-loss` tanpa konteks | `package.json:10-14`; `.env.example:1-2` |
| F-38 | Rendah | Endpoint tanpa validasi | `api/route.ts:3-5` |
| F-39 | Rendah | Data sintetis penuh di bundle klien; klaim DP-CTGAN tidak sesuai sumber | `i18n.tsx:523-524`; `notion-datasets.ts:402` |
| F-40 | Tinggi | Dataset 9.401 baris di bundle klien | `notion-datasets.ts:3,402`; `dataset-explorer.tsx:1-205` |
| F-41 | Sedang | Riset dirender dua kali | `dataset-explorer.tsx:1534,1631` |
| F-42 | Sedang | Animasi tanpa `prefers-reduced-motion` | `architecture.tsx:30-33` |
| F-43 | Sedang | Filter edge O(V·E) per render | `multi-channel-graph.tsx:453-454` |
| F-44 | Rendah | iframe 150 KB non-lazy | `oasis-dashboard.tsx:1153-1159` |
| F-45 | Sedang | 20 dependensi mati | `package.json:16-83` |
| F-46 | Sedang | 4 export mati; 2 sumber kebenaran | `data.ts:27,358,390,502` |
| F-47 | Tinggi | 8 error TS disembunyikan; `undefined` dirender | `i18n.tsx:386,734`; `roadmap.tsx:71`; `next.config.ts:5-7` |
| F-48 | Sedang | `.sort()` in-place pada impor | `fraud-drilldown-modal.tsx:169-170` |
| F-49 | Sedang | `reactStrictMode: false` | `next.config.ts:8` |
| F-50 | Rendah | Tanpa test suite | `tests/*.sh`; `package.json:5-15` |
| F-51 | Rendah | Artefak ML tidak ada di repo | `data.ts:363`; `i18n.tsx:470` |
| F-53 | Sedang | Shortcut global aktif di atas tombol/link | `use-keyboard-shortcuts.ts:26-33` |
| F-54 | Sedang | Shortcut panah andal pada teks tombol | `src/app/page.tsx:63-76` |
| F-58 | Rendah | `aria-label` hardcoded English | `back-to-top.tsx:38` |
| F-52 | Rendah | `z-ai-web-dev-sdk` sebagai dependensi produksi | `package.json:80` |

**Catatan verifikasi.** Semua hitungan di laporan ini dihitung ulang langsung dari berkas pada commit `f62b86d` (8 Oktober 2026 area kerja): `npx tsc --noEmit` (8 error), hitungan baris per berkas via `Get-Content | Measure-Object -Line`, hitungan konstanta via parser Node, hitungan key i18n via perbandingan interface `Dict` dengan seluruh pemakaian `t.*` di `src/`, hitungan dependensi mati via scanning `package.json` terhadap seluruh impor di `src/` + `examples/`, dan rekonsiliasi dataset 300-klaim terhadap `00-dashboard.md` §3 (300 record; 240/24/36; Rp 3.526.650.000; 9 sindikat; 12 kontradiksi narasi). Tidak ada berkas di `N:\HEALTHKATHON\Aegis-JKN\` yang dimodifikasi.
