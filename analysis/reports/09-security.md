# 09 - Audit Keamanan & Privasi Aegis-JKN

| Aspek | Nilai |
|---|---|
| Objek audit | `N:\HEALTHKATHON\Aegis-JKN\` (133 file terlacak, commit `232ce79`, branch `main`) |
| Dokumentasi acuan | `analysis/corpus/00-dashboard.md`, `01-proposal.md`, `02-architecture.md`, `03-dataset-registry.md`, `07-dataset-v2-catalog.md`, `10-simulation-dataset.md` |
| Metodologi | STRIDE per aset; audit OWASP API Top 10 pada kode nyata; grep PII/telemetry/secrets; `npm audit --json`; `git ls-files`; verifikasi manual path:line terhadap file sumber |
| Tanggal audit | 22 Oktober 2026 |
| Status kode | Read-only. Tidak ada file di `Aegis-JKN/` yang dimodifikasi. |
| Batasan | Tautan `507.370.000` **tidak ada** di dalam kode (grep 0 hit). Verifikasi tabrakan nama faskes dengan dunia nyata **gagal** karena mesin pencari tidak stabil (lihat SEC-13, ditandai TIDAK TERVERIFIKASI, bukan fakta). |

---

## 1. Ringkasan Eksekutif

Repositori Aegis-JKN adalah purwarupa **tanpa data pasien riil**: nol temuan nomor peserta, NIK, nomor KK, tanggal lahir, alamat, atau nomor HP di seluruh `src/` dan `public/`. Klaim "privacy-by-design" pada `10-simulation-dataset.md:3` **terdukung** dari sisi tidak adanya data riil, tetapi **tidak** berarti sistem sudah privacy-compliant, karena tidak ada kontrol akses, audit trail, RBAC, maupun retensi yang diimplementasikan.

Temuan paling berbahaya bukan eksploitasi teknis, melainkan **risiko reputasi dan hukum untuk BPJS**: aplikasi mempublikasikan angka finansial dan prevalensi **tanpa kualifikasi "sintetis/simulasi"** di area yang paling terlihat, sementara `00-dashboard.md:46-52` secara eksplisit menyatakan angka tersebut belum boleh disebut tervalidasi. Rantai "3-7% dari total nilai klaim nasional" dan "penghematan Rp 14,4 M/tahun" dibaca peserta hackathon sebagai temuan nyata. Ini temuan SATU-SATUNYA pada tingkat KRITIS, karena dampaknya menimpa kredibilitas penerbit, bukan sekadar kualitas kode.

Tiga temuan TINGGI lain: (1) nol header keamanan di `next.config.ts`/`vercel.json`; (2) `Caddyfile.txt` meneruskan ke port hulu yang dipilih **parameter kueri klien** tanpa autentikasi; (3) API publik adalah stub `GET {message:"Hello, world!"}` tanpa auth, rate limit, validasi, atau batas body, sementara `docs/api/data-contracts.md:222-265` menjanjikan endpoint `POST /api` untuk batch scoring yang tidak ada. Selain itu, ground truth label dan titik data sintetis dipublikasikan sebagai aset statis, dan 14 kerentanan npm (10 HIGH) tidak pernah dipindai karena tidak ada pipeline CI sama sekali.

Sebaliknya, beberapa hal yang lazim dikritik justru **bersih dan harus dinyatakan sebagai fact**: tidak ada telemetry pihak ketiga di HEAD, tidak ada secret di git, tidak ada `console.log` di `src/`, tidak ada panggilan LLM di kode (jadi prompt injection **belum dapat dieksploitasi**), dan tidak ada jalur unggah server-side (jadi path traversal dan SSRF **tidak berlaku**).

### Tabel severity

| Severity | Jumlah | Cakupan singkat |
|---|---|---|
| KRITIS | 1 | Angka finansial & prevalensi tanpa kualifikasi (pembaca dapat menyalahartikan sebagai temuan nyata atas nama BPJS) |
| TINGGI | 6 | Nol header keamanan; proxy Caddy ke port klien; API tanpa kontrol & kontrak tidak cocok; ground truth + sink `innerHTML`; 10 CVE HIGH tanpa CI; `.env` polos tidak di-ignore |
| SEDANG | 15 | Query log Prisma; robots allow-all; ekspor tanpa banner & memuat kolom terblokir; disclaimer hanya di beranda; quasi-identifier sintetis; nama faskes (belum terverifikasi); blokir leakage tidak diimplementasikan; uploader tanpa batas; O(n^2); sanitasi LLM belum ada; RBAC/audit trail/retensi absen; contoh websocket CORS `*`; drift versi lockfile; `ignoreBuildErrors`; dependensi tak terpakai |
| RINGAN | 7 | Inkonsistensi "Miliar"/"M"; wording verdict; bobot hardcoded; ikon CDN pihak ketiga; `dangerouslySetInnerHTML` chart; Prisma boilerplate; "undefined" pada ekspor |
| **Total** | **29** | |

---

## 2. Threat Model STRIDE

### 2.1 Aset 1 - Pengunggah Data (Self-Service Data Uploader)

| Aset | Vektor | Dampak | Kontrol ada? | Gap |
|---|---|---|---|---|
| Parser CSV/JSON sisi klien (`src/components/mhgsl/data-uploader.tsx:60-77`, `:210-235`) | Berkas CSV/JSON raksasa (puluhan MB) diparse penuh di memori browser | DoS peramban, kehilangan tab, bukan kompromi server | Sebagian: `parseCSV` guarded `lines.length < 2` (`:62`) | Tidak ada batas ukuran berkas, batas jumlah baris, atau batas waktu parse. `JSON.parse` pada input sewenang-wenang (`:216`) |
| Parser CSV naif `line.split(",")` (`:65`) | Nilai berkoma di dalam tanda kutip menghasilkan pergeseran kolom | Kolom `pasien`/`faskes` bergeser, nilai pseudo-identifier tidak sinkron dengan label | Tidak | Tidak ada dukungan quoting RFC4180; tidak ada validasi skema kolom |
| Kolom bebas pada baris (teks `alasanBerobat`, `narasiRekamMedis`) | Teks arbitrer dari berkas, nanti diekspor ke CSV | CSV formula injection bila diimpor ke Excel/Sheets | Ya di jalur ekspor dataset (`src/components/dataset/dataset-explorer.tsx:415-423` menetralkan `^[=+\-@\t\r]`) | Jalur uploader sendiri tidak punya kontrol formula; tidak ada sanitasi HTML bila teks nanti dirender |
| Skor fusion menentukan label UI `fraud`/`high` (`:128-137`) | Persepsi lokal: file berisi baris yang dirancang menghasilkan skor >= 0.85 | Persepsi lokal bahwa "fraud" adalah temuan | Tidak | Skor bersifat deterministik dan hanya ditampilkan di klien (`:377` merender `rows.slice(0, 6)`), jadi belum ada poisoning ke model tersimpan. Tidak ada tanda "simulasi" pada label (`:199-203`) |
| O(n^2) similarity (`:103-117`) | 10.000 baris | 10^8 perbandingan, freeze UI | Tidak | Kompleksitas kuadratik tanpa paginasi |

### 2.2 Aset 2 - API Publik

| Aset | Vektor | Dampak | Kontrol ada? | Gap |
|---|---|---|---|---|
| `GET /api` (`src/app/api/route.ts:1-5`) | Anonim, tanpa rate limit | Penebusan bandwidth, enumerasi | Tidak | Tanpa autentikasi, tanpa rate limit, tanpa header keamanan |
| Kontrak `POST /api` batch scoring (`docs/api/data-contracts.md:222-265`) | Klien integrasi mengirim payload klaim ke endpoint yang tidak ada | Kehilangan integrasi; tekanan untuk mengimplementasikan tanpa kontrol | Tidak | Route tidak ada. Hanya satu `route.ts` di seluruh `src/app` |
| Body/isi respons | `NextResponse.json({message})` | Tidak ada data sensitif yang dikembalikan saat ini | Ya (konsekuensi) | Tidak ada `Content-Type`/size guard, tidak ada skema Zod meski `zod` terpasang (`package.json:81`) |
| `zod` terpasang tapi nol pemakaian | Validasi input tidak pernah dipakai | Kebergantungan pada model saja | Tidak | Validasi harus jadi kode, bukan ketergantungan |

### 2.3 Aset 3 - Dashboard Triase & Ekspor

| Aset | Vektor | Dampak | Kontrol ada? | Gap |
|---|---|---|---|---|
| Halaman `/dataset` (`src/app/dataset/page.tsx:7,23,29-31`) | Tidak ada `<Footer>`, sehingga disclaimer sintetis tidak pernah dirender | Pembaca `/dataset` dan `/simulasi` tidak melihat bantalan "data sintetis" | Tidak | `<Footer />` hanya di `src/app/page.tsx:101` |
| Tombol ekspor (`:645-690`) | Ekspor CSV/JSON 27 kolom tanpa banner peringatan | File keluar dari sistem tanpa penanda "sintetis" | Tidak | `handleExportClaimsCSV` (`:414`), `handleExportClaimsJSON` (`:499`), `handleExportResearchCSV` (`:512`), `handleExportResearchJSON` (`:562`) tanpa banner |
| Kolom terblokir anti-leakage ikut terekspor (`:441-451`) | `Skor Fraud`, `Risiko`, `Status`, `Modus`, `Sindikat`, `Sinyal SHAP`, `Kontribusi Saluran`, `Alasan Audit` | Dataset hasil ekspor rawan dipakai ulang sebagai latih ulang sehingga label bocor | Tidak | Aturan `03-dataset-registry.md:84` hanya naratif, tidak ada allowlist saat ekspor |
| `public/dashboard-aegis-jkn.html:1172,1190,1199` | `innerHTML` dengan escaping tidak seragam | XSS bila data yang dirender berasal dari sumber tak dipercaya | Sebagian | `esc()` ada di `:1073`, tapi `${q.id}` (`:1172`) dan `${item.claim}` (`:1199`) diinterpolasi mentah |
| `public/payload-aegis-jkn.json` | `gtSent`, `syndHit`, `sentiment_gt` (48 kemunculan) bocor | Kunci jawaban ground truth dipublikasikan | Tidak | Menggagalkan evaluasi dan memungkinkan pencocokan output model |

### 2.4 Aset 4 - Model ML / Kanal Teks

| Aset | Vektor | Dampak | Dampak | Gap |
|---|---|---|---|---|
| Konfigurasi fitur model (diklaim ada di `configs/leakage.yaml`) | Artefak tidak ada di repositori | Fitur turunan label bocor ke latih ulang, hasil validasi tidak dapat direproduksi | Tidak ada kontrol | `03-dataset-registry.md:84-85`, `10-simulation-dataset.md:126,152-154`, `src/components/mhgsl/data.ts:363`, `src/components/mhgsl/i18n.tsx:470,817` menyebutnya sebagai done, direktori `configs/` tidak ada |
| Kanal teks LLM (Gemini, `10-simulation-dataset.md:171-173`) | Teks baris mentah masuk prompt eksternal | Eksfiltrasi data kesehatan + prompt injection | Tidak ada di kode | Belum ada panggilan LLM apa pun di `src/` (nol `fetch(`/`axios`/`openai`/`generativeai`), jadi **belum dapat dieksploitasi**, tetapi juga belum ada sanitasi, allowlist kolom, ataupto redaksi |
| Bobot & ambang fusion | Hardcoded di UI, tanpa versi | Hasil berubah diam-diam saat kode berubah, tidak dapat direproduksi | Parsial | `src/components/mhgsl/data-uploader.tsx:128-137`, `src/components/mhgsl/i18n.tsx:363` |
| Artifact bobot model (`.pt`, `.pkl`, `.onnx`) | Tidak ada di repositori | Model extraction tidak mungkin saat ini | Ya (konsekuensi) | Tidak ada model tersimpan; seluruh "model" adalah heuristik deterministik di frontend |

### 2.5 Aset 5 - Ekspor Laporan & Klaim Finansial

| Aset | Vektor | Dampak | Kontrol ada? | Gap |
|---|---|---|---|---|
| Angka "3-7% dari total nilai klaim nasional" (`src/components/mhgsl/i18n.tsx:232-233`, `src/components/mhgsl/problem-section.tsx:97`) | Interpretasi sebagai temuan nyata | Risiko hukum dan reputasi untuk BPJS | Tidak | Tidak ada label "estimasi literatur/sintetis"; `00-dashboard.md:39` menyatakan angka overcharge `507.370.000` **tidak dapat direproduksi** dan `03-dataset-registry.md:100` menyatakan 12% adalah distribusi skenario sintetis |
| Angka penghematan "Rp 1,2 M/bulan (Rp 14,4 M/tahun)" (`i18n.tsx:442-443`, `src/components/mhgsl/fraud-ring.tsx:415`, `src/components/mhgsl/roadmap.tsx:33-34`) | Disepal sebagai saving BPJS | Klaim performa fiktif | Sebagian | Asumsi "3% tingkat fraud ... basis 5 FKRTL" ada di `i18n.tsx:461`, tetapi tidak ada catatan "belum tervalidasi" |
| Metrik "AUPRC 0.91 / +20%" (`src/components/mhgsl/data.ts:23,253,264,297-299`, `README.md:31,133`) | Disepal sebagai hasil tervalidasi | Klaim performa fiktif | Tidak | `00-dashboard.md:46-47` secara eksplisit classifies AUPRC 0,9142 sebagai "belum boleh disebut hasil tervalidasi" |
| Narasi pasien sintetis dengan nama, umur, kota (`src/data/notion-datasets.ts:2871,4641`) | Nama sintetis bisa sama dengan pasien nyata | Salah-identitas dan kebocoran identitas | Tidak | 40 pasien dengan nama, umur, jenis kelamin, kota, dan segmen BPJS; `02-architecture.md:53` mensyaratkan "nama fiktif diberi penanda" |

---

## 3. Audit API (`src/app/api/route.ts`)

Berkas lengkap hanya 5 baris:

```ts
1  import { NextResponse } from "next/server";
2
3  export async function GET() {
4    return NextResponse.json({ message: "Hello, world!" });
5  }
```

| Aspek audit | Hasil | Bukti |
|---|---|---|
| Metode HTTP | Hanya `GET`. Tidak ada `POST`/`PUT`/`DELETE`. Hanya satu route di seluruh `src/app` | `src/app/api/route.ts:3`; `find src/app -name "route.ts"` menghasilkan 1 file |
| Autentikasi | Tidak ada. Tidak ada `middleware.ts`, tidak ada `src/auth.ts`, tidak ada `src/middleware.ts`, tidak ada handler auth | `ls middleware.ts src/middleware.ts src/auth.ts` -&gt; tidak ada |
| Otorisasi (RBAC) | Tidak ada. Tidak ada pemeriksaan peran di mana pun | grep `role|permission` pada `src/` nihil selain teks UI |
| Rate limiting | Tidak ada. Nol dependensi rate limit, nol implementasi | grep `rateLimit|rate-limit|ratelimit` pada `src/` -&gt; 0 hit |
| Validasi input | Tidak ada skema request, tidak ada `zod` schema Zod meski `zod@^4.0.2` terpasang | `package.json:81`; nol pemakaian `zod` di `src/` |
| Batas ukuran body | Tidak ada | `src/app/api/route.ts:1-5` |
| CORS | Tidak ada header CORS, juga tidak ada handler OPTIONS | `src/app/api/route.ts:1-5` |
| Data sensitif pada respons | Tidak ada. Respons hanya `{message:"Hello, world!"}` | `src/app/api/route.ts:4` |
| SSRF | **Tidak berlaku saat ini.** Nol `fetch(`/`axios`/klien HTTP keluar di `src/` | grep `fetch\(|axios|openai|generativeai|googleapis` pada `src/` -&gt; hanya URL dokumentasi di `src/data/notion-datasets.ts:130` dan label UI `i18n.tsx:321,669` |
| Path traversal pada unggah | **Tidak berlaku saat ini.** Unggah sepenuhnya sisi klien (`FileReader.readAsText`), tidak ada `fs`, `path`, atau penulisan berkas di server | `src/components/mhgsl/data-uploader.tsx:235`; nol `fs`/`path` di `src/` |
| Kontrak terdokumentasi vs implementasi | **Selisih.** `docs/api/data-contracts.md:222-234` menjanjikan `GET /api` -&gt; `{status:"online", service:"aegis-jkn-mhgsl-intelligence", version:"0.2.1", timestamp}`; `:239-265` menjanjikan `POST /api` batch scoring dengan `ClaimIngestionPayload` (skema `:43-89`). Keduanya tidak sesuai kode | `src/app/api/route.ts:4` vs `docs/api/data-contracts.md:222-265` |
| Version drift pada kontrak | Kontrak/API menyebut versi `0.2.1`, `package.json` menyebut `1.1.0` | `docs/api/data-contracts.md:229`, `package.json:3` |
| Query log database | Prisma mencatat seluruh query | `src/lib/db.ts:10` (`log: ['query']`) |

**Catatan penting soal SSRF/path traversal.** Pemeriksaan yang diminta berpotensi menemukan keduanya, tetapi keduanya **tidak dapat dieksploitasi pada kode saat ini** karena tidak ada jalur server-side untuk menerima berkas dan tidak ada klien HTTP keluar. Saya melaporkannya sebagai "tidak berlaku + belum ada kontrol", bukan sebagai kerentanan. Yang akan berubah adalah begitu `POST /api` diimplementasikan sesuai kontrak: ia akan menerima payload klaim tanpa auth, tanpa rate limit, tanpa batas body, dan tanpa validasi.

---

## 4. Audit Privasi & Kepatuhan Regulasi

### 4.1 Klaim vs realitas

| Klaim (sumber) | Realitas terverifikasi | Status |
|---|---|---|
| "privacy-by-design - bukan data peserta riil, aman menurut Permenkes 24/2022 & UU PDP No. 27/2022" (`10-simulation-dataset.md:3`) | Nol data peserta riil: grep `PSTV`, `PNK0`, `FKL0`, `NIK`, "nomor kartu keluarga", "tanggal lahir", "nomor peserta" pada `src/` dan `public/` -&gt; **0 hit**. Satu-satunya `process.env` di `src/` adalah `src/lib/db.ts:13` (`NODE_ENV`), jadi **tidak ada "Default Mode" data nyata tersembunyi** | **TERDUKUNG** untuk poin "bukan data riil". **TIDAK TERDUKUNG** untuk poin "aman/patuh": kepatuhan tidak dapat disimpulkan dari ketiadaan data di demo |
| "Seluruh data yang divisualisasikan adalah data sintetis ... sesuai kepatuhan UU PDP No. 27/2022" (`src/components/mhgsl/i18n.tsx:523-524`) | Banner hanya dirender di beranda (`src/app/page.tsx:101`). `/dataset` dan `/simulasi` tidak merender `<Footer>` (`src/app/dataset/page.tsx:29-31`, `src/app/simulasi/page.tsx:19-21`). `/simulasi` punya banner kejujuran amber sendiri (`src/components/oasis/oasis-dashboard.tsx:246-262`), `/dataset` hanya menyebut "sintetis" di hero (`:640`) | **TERBATAS**: disclaimer tidak berlaku di semua halaman |
| "Generator DP-CTGAN dengan privasi diferensial" (`i18n.tsx:313`, `src/components/dataset/dataset-explorer.tsx:1420,1761`, `src/components/mhgsl/glossary.tsx:175-178`) | Tidak ada kode generator, epsilon, laporan privasi diferensial, atau artefak DP di repositori. Data tampak sebagai template hardcode di `src/data/notion-datasets.ts` (300 objek, 9.403 baris) | **TIDAK TERDUKUNG** |
| "Nama fiktif diberi penanda" (`02-architecture.md:53`) | Nama faskes seperti "RS Aegis Medika A" (Jakarta Selatan, kelas B, 412 TT), "RSUD Harapan D" (Bandung), "RSUD Giri Menang F" (Yogyakarta) memuat kota, kelas, dan jumlah tempat tidur realistis, tanpa penanda "fiktif" | **TIDAK TERDUKUNG** (lihat SEC-13) |
| "Blokir kolom leakage (configs/leakage.yaml)" dan "Unit test (tests/test_leakage.py)" sebagai deliverable Fase 0 (`10-simulation-dataset.md:126,152-154,182-195`; `src/components/mhgsl/data.ts:363`; `i18n.tsx:470,817`) | Direktori `configs/`, `data/`, dan `tests/test_leakage.py` **tidak ada**. `tests/` hanya berisi 3 skrip build runtime | **TIDAK TERDUKUNG** |
| "Prinsip privasi: pseudonymization bukan anonimisasi sempurna" (`01-proposal.md`) | Tidak ada implementasi kontrol privasi apa pun di kode: nol RBAC, nol audit trail, nol retensi, nol log akses | **TIDAK TERDUKUNG** (SEC-18) |
| "Dataset v2.1 punya 6 kolom tambahan" (`10-simulation-dataset.md:117-121`) | `pasien_id`, `faskes_id`, `dokter_id`, `seed`, `version`, `timestamp` tidak ada sebagai kolom; ID hanya berupa prefiks di dalam rich text. Konfirmasi: `04-data-quality.md` menemukan 6 dari 6 kolom nihil | **TIDAK TERDUKUNG** |

### 4.2 Apakah nama sintetis faskes bisa menyiratkan identitas faskes nyata?

Nama yang dipakai: RS Aegis Medika A, RS Bakti Husada B, RS Cendana Medika C,WZEE.mdadz Harap D, RS Bahari Medika E, RSUD Giri Menang F (`10-simulation-dataset.md:22-27`; `src/components/mhgsl/data.ts:101,445`; `src/data/oasis-data.ts`).

- **Tidak terverifikasi.** Upaya verifikasi tabrakan nama dengan mesin pencari (SearXNG, beberapa engine) gagal: brave/duckduckgo/google CSE tersuspensi atau timeout, dan engine yang aktif hanya mengembalikan hasil tidak relevan (RS Components). Upaya `"RSUD Giri Menang"` pada 4 engine mengembalikan "No results found" yang tidak dapat dibedakan dari kebuntuan indexasi.
- Karena itu saya **tidak menyatakan** ada atau tidak tabrakan nama. Yang dapat dinyatakan sebagai fakta: pola penamaan memakai sufiks huruf (`A`..`J`) pada nama generik berbahasa Indonesia tanpa penanda fiktif, digabung dengan atribut realistis (kelas, TT, kota), sehingga **risiko kebingungan dengan faskes nyata tidak dapat dibantah** dan harus ditutup secara administratif, bukan diasumsikan aman.
- Dampak bila tabrakan terjadi: platform yang memuat nama, kelas, jumlah TT, kota, skor 0,95, dan label `fraud` pada faskes dengan nama yang mirip nyata dapat disalahartikan sebagai tuduhan. Karena itu, penandaan eksplisit "fiktif" pada setiap entitas faskes adalah kontrol yang wajib.

### 4.3 Apakah dataset survei risiko ter-re-identifiable?

`07-dataset-v2-catalog.md` menginventarisasi file D01 `DM_kepesertaan.dta` yang memuat `PSTV01` nomor peserta dan `PSTV03` tanggal lahir (`:9`, `:18-20`), serta `PNK02` ID kunjungan (`:11`, `:47`). Re-identifikasi terhadap data kepesertaan adalah **nyata secara desain** (pengenal langsung + tanggal lahir + provinsi/kabupaten). Yang penting: **baris D01-D03 tidak ada di dalam aplikasi** (nol `PSTV`/`PNK` di `src/` dan `public/`), dan katalog sendiri sudah menegakkan aturan "jangan dijadikan fitur model" (`:44-45`, `:87-88`). Jadi risiko re-identifikasi dataset DM **terkelola di tingkat dokumen**, tetapi tidak ada pengaman teknis di kode.

### 4.4 "Alasan" dan data governance lain

| Aspek | Hasil |
|---|---|
| Apakah kolom `Alasan` memuat data pribadi? | **Tidak.** 300 dari 300 baris punya `alasan` (`src/data/notion-datasets.ts`), 1 baris kosong (cocok dengan `03-dataset-registry.md:79`). Isi `alasan` adalah rasional klinis ("dx K80.2 ditindaki 51.23 - pasangan klinis standar; biaya Rp15.000.000 ~ tarif paket (rasio 1.03); LOS 4 hari ...", `notion-datasets.ts:430`). 35 baris menyebut entitas generik ("pasien", "dokter", "faskes") atau ID sintetis; contoh yang menyebut ID: `"FRAUD (Drug Diversion): 24 pen insulin per episode mengikuti pola pasien P16 ..."` (1 baris). Tidak ada nomor HP, alamat, NIK, atau tanggal lahir |
| Apakah data kuotatif ada di `Alasan`? | Ya, nilai rupiah dan rasio tarif, misalnya "biaya Rp58.000.000 ~ tarif paket (rasio 1.00)". Ini membocorkan informasi tarif internal BPJS ke file yang bisa dibagikan |
| Apakah ada "Default Mode" data pasien nyata? | **Tidak.** Satu-satunya `process.env` di `src/` adalah `src/lib/db.ts:13`. Tidak ada toggle, tidak ada feature flag, tidak ada variabel DM |
| Log akses / audit trail | **Tidak ada.** Requirement `01-proposal.md:60` (rekam versi model, waktu prediksi, alasan, tindakan verifikator, perubahan keputusan) tidak diimplementasikan. Yang ada hanya array timeline statis di `src/components/mhgsl/data.ts:432` |
| Retensi data | **Tidak ada.** `02-architecture.md:93` mensyaratkan log akses, retensi, dan prosedur insiden |
| Hashing vs privasi | Tidak ada hashing di kode; pernyataan `02-architecture.md:94` ("hindari menjadikan hash biasa sebagai pengganti kontrol privasi") terpenuhi secara vakum |

---

## 5. Audit Data Governance, Telemetry & Logging

| Item yang diperiksa | Hasil | Bukti |
|---|---|---|
| Sentry | Nol | grep `sentry` pada `src/`, `public/`, `package.json` -&gt; 0 hit |
| PostHog / Mixpanel / Amplitude / Hotjar / Clarity / Datadog / Segment / GA (`gtag`) | Nol | grep yang sama -&gt; 0 hit |
| `console.log` / `console.warn` / `console.error` di `src/` | **Nol** | grep `console\.` pada `src/` -&gt; 0 hit |
| `localStorage` / `sessionStorage` | Hanya preferensi bahasa `aegis-lang`, tanpa data klaim | `src/components/mhgsl/i18n.tsx:893,898` |
| Cookie | Nol di `src/` | grep `document.cookie` -&gt; 0 hit |
| Pengiriman data ke pihak ketiga | Tidak ada di HEAD. `src/app/layout.tsx:37` memuat ikon dari CDN pihak ketiga (`z-cdn.chatglm.cn`), dan `layout.tsx:43` menulis `openGraph.url` ke `https://chat.z.ai` yang **tidak terkait** dengan proyek | `src/app/layout.tsx:36-44` |
| **Vercel Web Analytics (komit belum merged)** | Commit `f13b4a3` "Install Vercel Web Analytics with latest docs" authored `Vercel <vercel[bot]@github.com>` ada di branch `origin/vercel/install-vercel-web-analytics-w-hgxwtt` dan **BUKAN ancestor HEAD** (`git merge-base --is-ancestor f13b4a3 HEAD` -&gt; NO). Komit menambah `@vercel/analytics@^2.0.1` (`package.json` versi komit `:53`), `import { Analytics } from "@vercel/analytics/next"` (`src/app/layout.tsx:7` versi komit) dan `<Analytics />` (`src/app/layout.tsx:77` versi komit) | `git show f13b4a3` |
| Query log database | Aktif: `new PrismaClient({ log: ['query'] })`. Pada fase integrasi nyata, log ini berisi payload klaim INCLUDING narasi rekam medis | `src/lib/db.ts:10` |
| Log di contoh websocket | `console.log` setiap pesan pengguna | `examples/websocket/server.ts:92` |
| Skema audit di DB | `prisma/schema.prisma` hanya punya model `User` dan `Post` boilerplate. Tidak ada model klaim, audit trail, atau reviewer action | `prisma/schema.prisma:16-32` |

**Catatan risiko telemetry (belum terjadi).** Bila branch Vercel Analytics di-merge, aplikasi health-sector akan mengirim page-view ke pihak ketiga. Itu menuntut review: konfirmasi bahwa `/dataset` dan `/simulasi` tidak ikut terlacak, ada opt-out, dan ada dasar pemrosesan yang terdokumentasi. Saat ini **belum terjadi** dan saya tidak melaporkannya sebagai temuan aktif.

---

## 6. Audit Dependensi, Konfigurasi & Secrets

### 6.1 Dependensi

`npm audit --json` (eksekusi di repo, berkas sementara dihapus):

| Severity | Jumlah | Paket | Langsung? | Remediasi |
|---|---|---|---|---|
| Critical | 0 | - | - | - |
| High | 10 | `sharp@^0.34.3` (`package.json:74`) | Ya | `sharp` 0.35.5 (perubahan mayor) |
| High | 10 | `prisma@^6.11.1` (`package.json:65`) | Ya | fix tersedia |
| High | 10 | `eslint-config-next@^16.1.1` (`package.json:90`) | Ya | fix ke 14.2.35 (turunan major) |
| High | 10 | `@next/eslint-plugin-next`, `@prisma/config`, `braces`, `deepmerge-ts`, `fast-glob`, `js-yaml`, `micromatch` | Transitif | Ikuti rantai `npm audit fix` |
| Moderate | 4 | `@mdxeditor/editor@^3.39.1` (`package.json:21`) | Ya | advisory `js-yaml` |
| Moderate | 4 | `react-syntax-highlighter@^15.6.1` (`package.json:72`) | Ya | `prismjs` DOM Clobbering + `refractor` |
| Low | 0 | - | - | - |

Dependensi langsung yang **tidak diimpor sekali pun** di `src/` (permukaan serang yang tidak perlu): `next-auth@^4.24.11` (`:62`), `zod@^4.0.2` (`:81`), `uuid@^11.1.0` (`:78`), `next-intl@^4.3.4` (`:63`), `@tanstack/react-query@^5.82.0` (`:51`), `@hookform/resolvers@^5.1.1` (`:20`), `z-ai-web-dev-sdk@^0.0.18` (`:80`), `react-syntax-highlighter` (`:72`), `@mdxeditor/editor` (`:21`).

`prisma@^6.11.1` dan `sharp@^0.34.3` adalah dependensi **build/runtime** yang tidak dipakai: `sharp` tidak needed karena nol pemakaian `next/image` (nol `next/image` di `src/`), `prisma` hanya menyisakan boilerplate `User`/`Post` yang tidak dipakai.

### 6.2 Konfigurasi

| Berkas | Temuan | Bukti |
|---|---|---|
| `next.config.ts` | **Nol header keamanan.** Tidak ada blok `headers()`: tanpa CSP, HSTS, `X-Frame-Options`/`frame-ancestors`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`. `typescript.ignoreBuildErrors: true` dan `reactStrictMode: false` | `next.config.ts:3-9` (seluruh konfigurasi) |
| `next.config.ts` | Tidak ada `images.remotePatterns`. Tidak relevan saat ini karena nol `next/image`, tetapi akan menggoda penambahan remote image tanpa allowlist | `next.config.ts:3-9` |
| `vercel.json` | Hanya `framework: "nextjs"`. Tidak ada `headers`, `regions`, `functions`, `security` | `vercel.json:1-4` |
| `Caddyfile.txt` | Reverse proxy **meneruskan ke port yang dipilih klien** lewat query param, tanpa autentikasi, tanpa TLS. Port default 3000 | `Caddyfile.txt:1-13`, default `:15-22` |
| `examples/websocket/frontend.tsx` | Komentar mengarahkan pemakaian pola `XTransformPort` | `examples/websocket/frontend.tsx:34-36` |
| `.env.example` | **Tidak ada secret terekspos.** Hanya `DATABASE_URL="file:./db/custom.db"` dan `NODE_ENV="development"` | `.env.example:1-5` |
| `.gitignore` | Mengabaikan `.env*.local`, `.env.local`, `.env.development.local`, `.env.test.local`, `.env.production.local`. **Tidak mengabaikan `.env` polos** | `.gitignore:31-35` |
| `package.json` / `package-lock.json` | Versi melenceng: `package.json:3` = `1.1.0`, `package-lock.json:3,9` = `0.2.1`. Dua lockfile dilacak (`bun.lock` dan `package-lock.json`) | `package.json:3`, `package-lock.json:3` |
| CI/CD | **Tidak ada sama sekali.** Tidak ada `.github/`, `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile`, `azure-pipelines.yml` | `ls -d .github .gitlab-ci.yml .circleci Jenkinsfile azure-pipelines.yml` -&gt; semua tidak ada |
| `prisma/schema.prisma` | Provider sqlite, `env("DATABASE_URL")`, model `User`/`Post` boilerplate tidak terpakai, tidak ada model audit | `prisma/schema.prisma:11-32` |
| `public/robots.txt` | `Allow: /` eksplisit untuk Googlebot, Bingbot, **Twitterbot**, **facebookexternalhit**, dan `User-agent: *` | `public/robots.txt:1-14` |

### 6.3 Hasil `git ls-files` (rahasia di repositori)

```
git ls-files | grep -iE "\.env|secret|credential|\.pem$|\.key$|cert|\.db$|token"
.env.example
```

Total file terlacak: **133**. Hanya `.env.example` yang cocok, dan isinya tidak memuat kredensial. **Tidak ada `.env`, `.pem`, `.key`, `*.db`, atau token yang ter-commit.** Ini hasil yang bersih; yang perlu diperbaiki hanya cakupan `.gitignore` (lihat SEC-07) dan konfirmasi bahwa `AGENTS.md` (untracked, dibuat otomatis `next dev`) tidak pernah ikut ter-commit.

Catatan topologi: repositori luar `N:/HEALTHKATHON` dan repositori dalam `N:/HEALTHKATHON/Aegis-JKN` adalah dua repo terpisah. `analysis/` tidak terlacak di repo luar, sehingga laporan ini tidak masuk riwayat publik.

---

## 7. Keamanan ML / LLM

### 7.1 Prompt injection lewat kolom teks

Kanal teks dirancang pada `10-simulation-dataset.md:100-108` (Narasi Rekam Medis, Umpan Balik Pasien, Kontradiksi Narasi, sentiment GT) dan Calls `Gemini API (toggle via configs/text.yaml)` pada `:171-173`.

| Pertanyaan | Jawaban terverifikasi |
|---|---|
| Apakah ada input yang mencapai LLM tanpa sanitasi? | **Belum ada LLM sama sekali.** grep `fetch(`/`axios`/`openai`/`generativeai`/`googleapis` pada `src/` -&gt; hanya satu URL dokumentasi (`src/data/notion-datasets.ts:130`) dan dua label UI (`i18n.tsx:321,669`). Tidak ada client Gemini, tidak ada key, tidak ada endpoint server |
| Apakah prompt injection sekarang bisa dieksploitasi? | **Tidak.** Tidak ada jalur eksekusi. Melaporkan ini sebagai kerentanan aktif akan salah |
| Apakah jalur siap bila kanal teks diaktifkan? | **Tidak.** Teks yang akan dikirim sudah tersedia di repo pada `src/data/notion-datasets.ts` (`narasiRekamMedis`, `alasanBerobat`, `umpanBalikPasien`) dan diekspor mentah ke CSV/JSON (`src/components/dataset/dataset-explorer.tsx:438-451`, `:469-475`). Tidak ada allowlist kolom, redaksi, atau sanitasi. `07-dataset-v2-catalog.md:4` sendiri sudah memperingatkan "jangan memasukkan baris mentah ke prompt AI eksternal" - peringatan itu benar, tetapi tidak ditegakkan di kode |
| Apakah ada risiko eksfiltrasi lewat prompt? | Ya, ketika kanal teks aktif: tidak ada filter sebelum `POST` ke API Gemini. Perlu allowlist kolom, scrub PII, dan larangan eksplisit field `pasien`/`dokter` |

### 7.2 Dataset poisoning lewat uploader

| Aspek | Status | Bukti |
|---|---|---|
| Batas ukuran/jumlah baris | Tidak ada | `src/components/mhgsl/data-uploader.tsx:307-315` (`<input type="file" accept=".csv,.json">` tanpa attr batas), `:221-224` (`setRows(parsed)` tanpa validasi jumlah) |
| Validasi skema | Tidak ada. Header CSV dipakai langsung sebagai kunci objek, nilai non-numerik jadi `0` | `src/components/mhgsl/data-uploader.tsx:60-77` |
| headed sanitasi | Tidak ada | `src/components/mhgsl/data-uploader.tsx:60-77` |
| Dampak poisoning | Saat ini **terbatas lokal**: tidak ada unggah ke server, tidak ada penyimpanan, skor hanya ditampilkan (`:377` merender 6 baris pertama). Tidak ada model yang dilatih dari unggahan ini | `src/components/mhgsl/data-uploader.tsx:206-236` |
| Risiko ketika pipeline ML ditambahkan | Tinggi: baris yang dirancang/skoring- minded bisa menggeser ambang dan label | Direkomendasikan: batas ukuran/jumlah baris, validasi skema whitelist, tolak baris dengan ID duplikat, dan cap pada jumlah baris yang boleh diekspor |

### 7.3 Model extraction, anti-leakage, dan poisoning label

| Aspek | Status | Bukti |
|---|---|---|
| Model extraction | **Tidak berlaku saat ini.** Tidak ada artefak bobot (`.pt`/`.pkl`/`.onnx`) di repositori; seluruh skor adalah heuristik determinisitik yang kodenya sudah terbuka di bundel klien | `src/components/mhgsl/data-uploader.tsx:119-137` |
|-Blokir anti-leakage | **Diklaim, tidak diimplementasikan.** `configs/leakage.yaml` dan `tests/test_leakage.py` tidak ada; `tests/` hanya berisi 3 skrip build | `10-simulation-dataset.md:126,152-154,182-195`; `src/components/mhgsl/data.ts:363`; `src/components/mhgsl/i18n.tsx:470,817` |
| Ground truth bocor | **Aktif.** `public/payload-aegis-jkn.json` memuat `gtSent`, `syndHit`, dan 48 kemunculan `sentiment_gt`; `public/dashboard-aegis-jkn.html:1071` menyematkan objek `D` penuh | `public/payload-aegis-jkn.json`; `public/dashboard-aegis-jkn.html:1071` |
| Ekspor memuat kolom terblokir | **Aktif.** 27 kolom termasuk `Skor Fraud`, `Risiko`, `Status`, `Modus`, `Sindikat`, `Sinyal SHAP`, `Kontribusi Saluran`, `Alasan Audit` | `src/components/dataset/dataset-explorer.tsx:441-451` |
| Round-trip poisoning yang sama: ekspor -> impor -> ekspor dapat digunakan untuk menyuntikkan label | `src/components/dataset/dataset-explorer.tsx:499` + `src/components/mhgsl/data-uploader.tsx:216` |
| Group-aware evaluation | **Tidak ada.** `GroupKFold`/`LOGO` disebut sebagai deliverable Fase 0, tapi tidak ada kode, split manifest, atau ID kelompok | `src/components/mhgsl/data.ts:363`; `src/components/mhgsl/i18n.tsx:470` |

---

## 8. Risiko Misinterpretasi (Angka Finansial Tanpa Kualifikasi)

### 8.1 Angka `507.370.000` sendiri

Angka tersebut **tidak ada** di dalam repositori (grep `507.370.000` pada `src/`, `public/`, `docs/`, `README.md` -&gt; 0 hit). Jadi risiko spesifik "Rp507.370.000 overcharge tampil di UI" **tidak terjadi pada kode ini**. Yang tersisa adalah risikonya sendiri: `00-dashboard.md:39` menyatakan angka itu tidak dapat direproduksi per klaim karena tarif pembanding, formula, dan status validasi tidak tercatat. Karena angka itu tidak ada di kode, temuan ini saya laporkan sebagai **tidak berlaku pada UI**, bukan sebagai temuan.

### 8.2 Angka lain tanpa kualifikasi (risiko yang sebenarnya ada)

| Angka / klaim | Lokasi | Kualifikasi yang tampil? | Risiko |
|---|---|---|---|
| "3-7%" + "Estimasi Potensi Fraud" + "dari total nilai klaim nasional" | `src/components/mhgsl/i18n.tsx:232-233`; render di `src/components/mhgsl/problem-section.tsx:95-100` | **Tidak.** Tidak ada catatan "estimasi literatur" | **KRITIS.** Sintesis: 3-7% adalah estimasi literatur, 12% adalah distribusi skenario sintetis (`03-dataset-registry.md:100`, `10-simulation-dataset.md:10,179-181`). Menampilkannya sebagai "dari total nilai klaim nasional" mengarahkan pembaca pada klaim national |
| "Total penghematan estimasi Rp 1,2 M / bulan (Rp 14,4 M / tahun)" | `src/components/mhgsl/i18n.tsx:442-443`; `src/components/mhgsl/fraud-ring.tsx:411-416` | Sebagian: ada asumsi "3% tingkat fraud ... basis 5 FKRTL" di `i18n.tsx:459-461` | **TINGGI.** `00-dashboard.md:50` menyatakan penghematan yang dihitung dari dataset "belum boleh disebut hasil tervalidasi" |
| Counter "Rp 14,4 M" | `src/components/mhgsl/roadmap.tsx:33-34,113-121` | Sebagian | **TINGGI.** Angka yang sama dengan label "Estimasi penghematan tahunan" (`:459`) |
| "AUPRC 0.91" dan "+20% lonjakan" | `src/components/mhgsl/data.ts:23,253,264,297-299`; `README.md:31,133` | **Tidak** | **TINGGI.** `00-dashboard.md:47` menyatakan AUPRC 0,9142 belum boleh disebut tervalidasi. Label "+20% lonjakan AUPRC" adalah klaim performa |
| "300 berkas klaim sintetis ... (senilai Rp 3,53 Miliar)" / KPI "Rp 3,53 M" | `src/components/dataset/dataset-explorer.tsx:640,764`; metadata `src/app/dataset/page.tsx:7,23` | "sintetis" ada di hero (`:640`) | **SEDANG.** Nominal sintetis tanpa catatan "bukan kerugian BPJS" |
| "Fraud Terdeteksi 14/14, det_rate 100%" | `src/components/oasis/oasis-dashboard.tsx:286-298`; `public/payload-aegis-jkn.json` (`kpi.det_rate`) | Ya, banner kejujuran amber di `:246-262` | **SEDANG** |
| "Accuracy 93,0%" | `public/payload-aegis-jkn.json` (`kpi.accuracy: 93`) | Sebagian (banner `:246-262`) | **SEDANG** (`00-dashboard.md:47`) |
| "Estimasi Potensi Fraud" dalam bahasa Inggris: "of national total claim value" | `src/components/mhgsl/i18n.tsx:580-581` | Tidak | **TINGGI** (versi EN untuk audiens internasional, risiko dan kebingungan) |

### 8.3 Adanya pemisahan "simulasi" vs "keputusan nyata" di UI

Kriteria MVP `02-architecture.md:104` menuntut UI membedakan skor, dugaan anomali, dan keputusan verifikator, dan `:106` menuntut dokumentasi menyatakan data sintetis.

| Kebutuhan | Realitas |
|---|---|
| Skor vs dugaan vs keputusan verifikator | **Parsial.** UI menampilkan skor, risiko, status, modus, sindikat, dan "Alasan". Namun keputusan verifikator **tidak ada**: nol kontrol override, nol aksi review, nol audit trail. `src/components/mhgsl/fraud-drilldown-modal.tsx:251` hanya menampilkan label "verifikator (Human-in-the-Loop)". `02-architecture.md:40-47` mensyaratkan "tindakan reviewer, alasan override, dan status tindak lanjut" - nol dari ketiganya ada |
| Banner kualifikasi | **Tidak seragam.** Home punya `footerDisclaimer` (`i18n.tsx:523-524`, render `src/app/page.tsx:101`). `/dataset` dan `/simulasi` tidak punya Footer. `/simulasi` punya banner amber sendiri. `/dataset` tidak punya banner pada area ekspor (`dataset-explorer.tsx:645-690`) |
| Istilah "fraud" untuk data simulasi | **Berlebihan.** `src/components/mhgsl/data-uploader.tsx:201` "skor >= 0.85 menandakan kemungkinan fraud", `src/components/dataset/dataset-explorer.tsx:1920` "Auto-Clear (Klaim Normal / Sah)", dan label "fraud" dipakai sebagai nilai enum tanpa prefiks "skenario" |

---

## 9. Daftar Temuan per Severity dengan Remediasi

### KRITIS

| ID | Temuan | Bukti | Remediasi |
|---|---|---|---|
| SEC-01 | Angka prevalensi dan finansial disajikan tanpa kualifikasi "sintetis/simulasi/estimasi literatur", padahal `00-dashboard.md:46-52` menyatakan angka sejenis belum boleh disebut tervalidasi. Risiko hukum dan reputasi untuk BPJS | `src/components/mhgsl/i18n.tsx:232-233`, `:442-443`, `:459-461`, `:580-581`; `src/components/mhgsl/problem-section.tsx:95-100`; `src/components/mhgsl/fraud-ring.tsx:411-416`; `src/components/mhgsl/roadmap.tsx:33-34,113-121`; `src/components/mhgsl/data.ts:23,253,264,297-299`; `README.md:31,133`; `src/components/dataset/dataset-explorer.tsx:640,764` | 1) Ubah `problemFraudLabel` menjadi "Estimasi literatur (bukan hasil model)" dan `problemFraudSub` menjadi "prevalensi skenario simulasi, bukan data nasional". 2) Tambah kalimat kualifikasi wajib pada setiap blok angka: "Angka simulasi sintetis. Bukan temuan, bukan estimasi kerugian BPJS." 3) Ubah "Estimasi penghematan tahunan" menjadi "Skenario penghematan (asumsi demonstrasi)". 4) Tandai AUPRC/+20% dengan "benchmark internal, belum tervalidasi" sesuai `00-dashboard.md:47`. 5) Taruh disclaimer yang sama di Footer `/dataset` dan `/simulasi`, bukan hanya beranda |

### TINGGI

| ID | Temuan | Bukti | Remediasi |
|---|---|---|---|
| SEC-02 | Nol header keamanan: tanpa CSP, HSTS, X-Frame-Options/frame-ancestors, X-Content-Type-Options, Referrer-Policy | `next.config.ts:3-9` (tidak ada blok `headers()`); `vercel.json:1-4` | Tambahkan `headers()` di `next.config.ts` dan/atau `headers` di `vercel.json`: `Content-Security-Policy` (default-src 'self'; batasi `img-src` ke origin sendiri), `Strict-Transport-Security` (max-age 31536000; includeSubDomains), `X-Frame-Options: DENY` + `frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` |
| SEC-03 | Reverse proxy meneruskan ke port hulu yang dipilih **parameter kueri klien**, tanpa autentikasi dan tanpa TLS | `Caddyfile.txt:1-13` (`reverse_proxy localhost:{query.XTransformPort}`), default `:15-22`; `examples/websocket/frontend.tsx:34-36` | Hapus blok `@transform_port_query` dari Caddyfile produksi. Jika tetap diperlukan, batasi ke allowlist port tetap (matcher eksplisit, bukan placeholder mentah), pesan "unknown" untuk nilai di luar daftar, dan pasang TLS. Jangan pernah membiarkan port berasal dari input klien |
| SEC-04 | API publik tanpa autentikasi, otorisasi, rate limit, validasi input, batas ukuran body, maupun CORS; dan kontrak terdokumentasi (`POST /api` batch scoring) tidak ada di kode sehingga tim terdorong mengimplementasikan tanpa kontrol | `src/app/api/route.ts:1-5`; `docs/api/data-contracts.md:43-89`, `:222-265`; nol `middleware.ts`; `zod` terpasang tapi tak terpakai (`package.json:81`) | 1) Tambahkan `middleware.ts` dengan rate limit (Token bucket per IP/role) untuk `/api/*`. 2) Saat `POST /api` diimplementasikan, wajibkan skema Zod, `Content-Length` maksimum, dan `Content-Type` JSON; kembalikan 400/413/429. 3) Perbarui `docs/api/data-contracts.md` agar cocok dengan implementasi, atau tandai eksplisit "planned, not implemented". 4) Sinkronkan nomor versi di `:229` dengan `package.json:3` |
| SEC-05 | Ground truth dipublikasikan sebagai aset statis (`gtSent`, `syndHit`, 48 x `sentiment_gt`) dan HTML dashboard memakai `innerHTML` dengan escaping tidak seragam (`${q.id}` dan `${item.claim}` diinterpolasi mentah) | `public/payload-aegis-jkn.json`; `public/dashboard-aegis-jkn.html:1071`, `:1073`, `:1172`, `:1190`, `:1199` | 1) Hapus `gtSent`/`syndHit`/`sentiment_gt` dari payload yang dilayani publik, atau pindahkan ke direktori privat yang tidak ikut ter-deploy. 2) Terapkan `esc()` pada `${q.id}` (`:1172`) dan `${item.claim}` (`:1199`), atau ganti `innerHTML` dengan `textContent`/template yang aman. 3) Tambahkan header CSP `script-src 'self'` agar injeksi HTML tidak dapat mengeksekusi skrip |
| SEC-06 | 14 kerentanan npm (10 HIGH, 4 MODERATE), termasuk 3 dependensi langsung, tanpa pipeline CI yang memindainya | `npm audit --json`; `package.json:74` (`sharp`), `:65` (`prisma`), `:90` (`eslint-config-next`), `:21` (`@mdxeditor/editor`), `:72` (`react-syntax-highlighter`); nol `.github/`, `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile` | 1) `npm audit fix` untuk yang non-major, dan renaikkan `sharp` ke 0.35.5 serta `eslint-config-next` ke jalur yang sudah dipatch dengan uji build. 2) Buang dependensi tak terpakai (§6.1) termasuk `sharp` dan `prisma` bila tidak dipakai. 3) Tambahkan CI minimal: `npm ci`, `npm run lint`, `npm run build`, `npm audit --audit-level=high`, plus `gitleaks` untuk deteksi secret |
| SEC-07 | `.gitignore` tidak mengabaikan `.env` polos, sehingga `DATABASE_URL` atau API key dapat ter-commit | `.gitignore:31-35` | Tambahkan baris `.env` dan `.env.*` (dengan pengecualian `!.env.example`) di `.gitignore`; jalankan `gitleaks` di CI |

### SEDANG

| ID | Temuan | Bukti | Remediasi |
|---|---|---|---|
| SEC-08 | Query log Prisma aktif; pada integrasi nyata log akan memuat payload klaim termasuk narasi rekam medis | `src/lib/db.ts:10` | Batasi ke `log: process.env.NODE_ENV === 'development' ? ['query'] : ['error']`, arahkan ke sink terstruktur dengan retensi dan akses terbatas |
| SEC-09 | `robots.txt` mengizinkan semua crawler secara eksplisit (termasuk Twitterbot dan facebookexternalhit) sementara aset statis publik memuat narasi, ground truth, dan data faskes yang disimulasikan | `public/robots.txt:1-14`; `public/payload-aegis-jkn.json`; `public/dashboard-aegis-jkn.html` | Batasi crawler: `Disallow` untuk bot media sosial pada path data, atau pindahkan dataset ke subdomain non-crawlable dengan autentikasi. Jangan andalkan `robots.txt` sebagai kontrol keamanan, hanya sebagai hygiene |
| SEC-10 | Ekspor 27 kolom tanpa banner kualifikasi dan memuat seluruh kolom yang harus diblokir anti-leakage | `src/components/dataset/dataset-explorer.tsx:414-423`, `:426-452`, `:499`, `:512`, `:562`, `:645-690` | Tambahkan allowlist kolom ekspor (hapus `Skor Fraud`, `Risiko`, `Status`, `Modus`, `Sindikat`, `Sinyal SHAP`, `Kontribusi Saluran`, `Alasan Audit` dari ekspor "publik"), atau pisahkan tombol "Ekspor untuk evaluasi" dari "Ekspor demo". Tambahkan baris header file "DATA SINTETIS - BUKAN DATA PESERTA JKN" pada setiap file ekspor |
| SEC-11 | Disclaimer "data sintetis" hanya dirender di beranda | `src/app/page.tsx:101`; `src/app/dataset/page.tsx:29-31`; `src/app/simulasi/page.tsx:19-21`; `src/components/mhgsl/i18n.tsx:523-524` | Render `<Footer />` (atau komponen disclaimer yang sama) di `/dataset` dan `/simulasi`, plus banner melekat pada setiap area ekspor |
| SEC-12 | Quasi-identifier sintetis yang lengkap untuk 40 pasien: nama, umur, jenis kelamin, kota, dan segmen BPJS. Nama sintetis dapat sama dengan nama orang nyata, sehingga rekaman dapat disalah-attribusikan | `10-simulation-dataset.md:43-63`; `src/data/notion-datasets.ts:2871,4641` ("P01 (Agus Raharjo)"), `:1490,4040` ("D01 (dr. Adnan Prakoso, Sp.BTKV)") | 1) Ganti nama dengan inisial/anonim berurutan (`PASIEN-001`) dan simpan nama lengkap hanya di corpus internal. 2) Hapus atau bucket-bucketkan kota dan segmen. 3) Tandai setiap entitas dengan penanda "fiktif" sesuai `02-architecture.md:53` |
| SEC-13 | Nama faskes memakai pola generik+sufiks huruf dengan kota, kelas, dan jumlah TT realistis, **tanpa** penanda fiktif. Tabrakan dengan faskes nyata **belum dapat diverifikasi** (mesin pencari tidak stabil: brave/duckduckgo/google CSE tersuspensi, hasil yang ada tidak relevan) | `10-simulation-dataset.md:22-27`; `src/components/mhgsl/data.ts:101,445`; `src/data/oasis-data.ts` | 1) Verifikasi satu kali terhadap daftar faskes resmi (SIRS/SARS) untuk keenam nama; hasilnya didokumentasikan sebagai bukti. 2) Sampai terverifikasi, ganti nama dengan prefiks eksplisit non-ambigu ("FASKES-SINT-A (fiktif)") di seluruh UI dan ekspor. 3) Tambahkan field `isSynthetic: true` pada entitas faskes |
| SEC-14 | Blokir anti-leakage dan unit test yang diklaim sebagai deliverable Fase 0 tidak ada di repositori | `10-simulation-dataset.md:126,152-154,182-195`; `src/components/mhgsl/data.ts:363`; `src/components/mhgsl/i18n.tsx:470,817`; direktori `configs/`, `data/` tidak ada | Buat `configs/leakage.yaml` dan `tests/test_leakage.py` (gagal keras bila kolom terlarang masuk fitur), jalankan di CI, dan hapus UI yang menyatakan Phase 0 selesai sampai artefaknya benar-benar ada |
| SEC-15 | Uploader menerima berkas tanpa batas ukuran, tanpa batas jumlah baris, tanpa validasi skema; CSV dipecah naif dan JSON di-parse tanpa whitelist | `src/components/mhgsl/data-uploader.tsx:60-77`, `:210-236`, `:307-315` | Tambahkan batas 5 MB dan 5.000 baris, validasi header terhadap daftar putih, parser CSV yang menghormati tanda kutip, dan pesan error yang informatif |
| SEC-16 | Similarity O(n^2) pada data uploader dengan baris tak terbatas | `src/components/mhgsl/data-uploader.tsx:103-117`, `:221-224` | Batasi baris (lihat SEC-15) atau ganti dengan indeks hash/bucket pada kunci `(dokter, faskes)` |
| SEC-17 | Kanal teks LLM direncanakan tanpa sanitasi, allowlist kolom, atau redaksi, sementara teks yang akan dikirim sudah tersedia dan diekspor mentah | `10-simulation-dataset.md:171-173`; `07-dataset-v2-catalog.md:4`; `src/components/dataset/dataset-explorer.tsx:438-451`, `:469-475`; `src/components/mhgsl/i18n.tsx:321,669` | Buat allowlist kolom (hanya `dx`, `prosedur`, `LOS`, sentimen), redaksi PII, larangan eksplisit `pasien`/`dokter`/`faskes`, dan pemanggil LLM hanya di server dengan kunci di env.-blocklist siap sebelum kanal diaktifkan |
| SEC-18 | RBAC, audit trail, log akses, dan retensi tidak diimplementasikan meski menjadi syarat arsitektur | `01-proposal.md:60`; `02-architecture.md:90,93`; `src/components/mhgsl/fraud-drilldown-modal.tsx:251` (label saja); `prisma/schema.prisma:16-32` | Tambahkan model audit (`AuditEvent`: claim_id, model_version, threshold_version, skor, alasan, aksi_reviewer, timestamp) dan aturan retensi, plus RBAC minimal untuk aksi review/escalate |
| SEC-19 | Contoh server websocket: CORS `*`, tanpa autentikasi, mempercayai `username` dan `content` dari klien, menyiarkan ke semua klien, dan mencatat setiap pesan | `examples/websocket/server.ts:9`, `:62`, `:85-93`, `:92` | Batasi CORS ke origin tepercaya, wajibkan token, server yang mengarang nama, jangan log isi pesan, dan keluarkan dari repo bila tidak dipakai. Catatan: `socket.io` tidak ada di `package.json`, jadi contoh ini tidak berjalan di build apa pun |
| SEC-20 | Drift versi: `package.json` 1.1.0 vs `package-lock.json` 0.2.1, dan dua lockfile dilacak (`bun.lock` + `package-lock.json`) | `package.json:3`; `package-lock.json:3,9` | Sinkronkan versi, pilih satu package manager, dan hapus lockfile yang tidak dipakai |
| SEC-21 | `typescript.ignoreBuildErrors: true` dan `reactStrictMode: false` melemahkan deteksi masalah saat build | `next.config.ts:5-8` | Set `ignoreBuildErrors: false` dan `reactStrictMode: true`; perbaiki error yang muncul |
| SEC-22 | Sembilan dependensi langsung tidak pernah diimpor, memperbesar permukaan serang tanpa manfaat (`next-auth`, `zod`, `uuid`, `next-intl`, `@tanstack/react-query`, `@hookform/resolvers`, `z-ai-web-dev-sdk`, `react-syntax-highlighter`, `@mdxeditor/editor`) | `package.json:20,21,51,62,63,72,78,80,81`; nol impor di `src/` | Hapus seluruh dependensi tersebut. Jika `zod` akan dipakai untuk validasi API (SEC-04), pertahankan hanya `zod` |

### RINGAN

| ID | Temuan | Bukti | Remediasi |
|---|---|---|---|
| SEC-23 | Inkonsistensi satuan: "Rp 3,53 Miliar" di hero vs "Rp 3,53 M" di KPI "Nilai Klaim" pada komponen yang sama | `src/components/dataset/dataset-explorer.tsx:640` vs `:764` | Gunakan satu formatter (`formatRupiah`, sudah dipakai di `:767`) untuk kedua tempat |
| SEC-24 | Verdict uploader menyebut "kemungkinan fraud" tanpa penanda bahwa ini simulasi deterministik | `src/components/mhgsl/data-uploader.tsx:199-203` | Tambahkan "Simulasi heuristik, bukan model tervalidasi" pada label verdict |
| SEC-25 | Bobot fusion, ambang skor, dan formula ditulis hardcoded di komponen UI, tanpa versi atau konfigurasi | `src/components/mhgsl/data-uploader.tsx:128-137`, `:203`; `src/components/mhgsl/i18n.tsx:363` | Pindahkan ke satu berkas konfigurasi berversi (`configs/scoring.yaml`) yang dirujuk UI dan displayed versinya |
| SEC-26 | Ikon situs dimuat dari CDN pihak ketiga (`z-cdn.chatglm.cn`) dan `openGraph.url` menunjuk ke domain yang tidak terkait dengan proyek (`chat.z.ai`) | `src/app/layout.tsx:36-37`, `:39-44` | Ganti ikon ke `/public/logo.svg` (nihil permintaan ke pihak ketiga) dan set `openGraph.url` ke domain proyek yang sebenarnya |
| SEC-27 | Satu `dangerouslySetInnerHTML` pada komponen chart | `src/components/ui/chart.tsx:83` | Pola Recharts yang umum; pastikan input originates dari data internal, bukan input pengguna |
| SEC-28 | Model Prisma `User`/`Post` boilerplate dengan `email @unique`, tidak terpakai, dan tidak ada model klaim/audit | `prisma/schema.prisma:16-32` | Hapus boilerplate atau ganti dengan model domain + audit (§SEC-18) |
| SEC-29 | 28 baris data ekspor memuat literal `"undefined · RJ-2026-..."` pada kolom Rujukan; nomor versi pada kontrak API (`0.2.1`) tidak cocok dengan `package.json` (`1.1.0`) | `src/data/notion-datasets.ts` (28 match `"rujukan": "undefined`); `docs/api/data-contracts.md:229`; `package.json:3` | Perbaiki generator rujukan agar tidak menghasilkan `undefined`, dan sinkronkan nomor versi |

---

## Lampiran A - Perintah Replikasi

```
cd "N:/HEALTHKATHON/Aegis-JKN"

# API dan konfigurasi
cat -n src/app/api/route.ts
cat -n next.config.ts vercel.json .env.example prisma/schema.prisma src/lib/db.ts
find src/app -name "route.ts"
ls middleware.ts src/middleware.ts src/auth.ts

# Kontrol yang tidak ada
grep -rn "rateLimit\|rate-limit" src/
grep -rn "console\." src/
grep -rniE "sentry|posthog|mixpanel|datadog|amplitude|hotjar|gtag" src/ public/ package.json
grep -rniE "PSTV|PNK0|FKL0|nik|tanggal lahir|nomor kartu|alamat" src/ public/
grep -rniE "fetch\(|axios|openai|generativeai|googleapis" src/

# Rahasia
git ls-files | grep -iE "\.env|secret|credential|\.pem$|\.key$|cert|\.db$|token"
git merge-base --is-ancestor f13b4a3 HEAD && echo YES || echo NO
git show f13b4a3 --stat

# Dependensi
npm audit --json > ./audit-tmp.json && node -e "console.log(require('./audit-tmp.json').metadata.vulnerabilities)"; rm -f ./audit-tmp.json

# Artefak yang diklaim tapi tidak ada
ls -d configs data scripts; ls tests
```

## Lampiran B - Yang Dicek dan Turns Out BERSIH

Dinyatakan eksplisit agar tidak disalahartikan sebagai temuan:

1. Tidak ada secret di git. `git ls-files` hanya memuat `.env.example` yang isinya bukan kredensial.
2. Tidak ada telemetry pihak ketiga di HEAD (Sentry, PostHog, GA, Mixpanel, Datadog, Hotjar: nol). Commit Vercel Analytics `f13b4a3` ada di branch terpisah, **tidak** di HEAD.
3. Tidak ada `console.log` di `src/`.
4. Tidak ada PII: nomor peserta, NIK, nomor KK, tanggal lahir, alamat, nomor HP, `PSTV*`, `PNK*`: nol di `src/` dan `public/`.
5. Tidak ada "Default Mode" data pasien nyata. Satu-satunya `process.env` di `src/` adalah `src/lib/db.ts:13`.
6. Tidak ada panggilan LLM di kode, sehingga prompt injection **belum dapat dieksploitasi**.
7. Tidak ada jalur unggah ke server, sehingga path traversal dan SSRF **tidak berlaku** saat ini.
8. `escapeCSV` di `src/components/dataset/dataset-explorer.tsx:415-423` sudah menetralkan formula injection spreadsheet (`^[=+\-@\t\r]`).
9. `src/components/oasis/oasis-dashboard.tsx:1105` merender `{item.text}` lewat React (auto-escape), bukan `innerHTML`.
10. `git ls-files` menunjukkan tidak ada `.pem`/`.key`/`.db` yang terlacak.
