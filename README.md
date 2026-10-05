# Aegis-JKN · MHGSL Fraud Intelligence Platform

### Multi-Channel Heterogeneous Graph Structure Learning for JKN/BPJS Healthkathon 2026

[![Next.js](https://img.shields.io/badge/Next.js-16.1.1-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.0.0-blue?style=flat-square&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4.0-38bdf8?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![Vercel Ready](https://img.shields.io/badge/Vercel-Deployment_Ready-black?style=flat-square&logo=vercel)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=flat-square)](LICENSE)

---

## Executive Summary

Program Jaminan Kesehatan Nasional (JKN) yang dikelola oleh BPJS Kesehatan memproses lebih dari 2.000.000 klaim pelayanan kesehatan setiap hari kerja. Skala operasional masif ini dihadapkan pada keterbatasan kapasitas verifikasi manual yang hanya didukung oleh sekitar 1.000 personel verifikator di seluruh Indonesia. Rasio beban kerja 2.000:1 menciptakan celah operasional yang rentan dieksploitasi oleh modus kecurangan (fraud) layanan kesehatan sistematis.

Modus kecurangan modern tidak lagi berbentuk anomali kasual pada klaim tunggal, melainkan sindikat terorganisir yang mencakup:
- **Phantom Billing**: Klaim fiktif untuk layanan, kunjungan, atau obat yang tidak pernah diberikan.
- **Upcoding & Unbundling**: Penggelembungan kode diagnosis (ICD-10) atau tindakan (ICD-9-CM) ke kelompok INA-CBG berbiaya tinggi, serta pemecahan satu paket tindakan menjadi klaim terpisah.
- **Prolonged Stay & Readmisi Terencana**: Perpanjangan lama rawat inap (Length of Stay/LOS) yang tidak didasarkan pada indikasi medis demi memaksimalkan plafon klaim.
- **Sindikat Kolusi Multi-Pihak**: Kolusi lintas entitas antara dokter penanggung jawab pelayanan (DPJP), faskes rujukan (FKRTL), dan rekam medis pasien yang dikloning.

Tantangan utama sistem deteksi konvensional (seperti algoritma tabular XGBoost maupun Graph Neural Networks homogen) adalah **Topological Camouflage**. Pelaku kejahatan sengaja merekayasa alur rujukan fisik agar menyerupai prosedur medis standar. Model tabular gagal karena mengevaluasi setiap klaim secara terisolasi tanpa konteks relasional. Model GNN standar gagal karena graf rujukan yang dikamuflasekan mencemari proses agregasi tetangga (*neighborhood aggregation*).

**Aegis-JKN** menghadirkan terobosan berbasis **Multi-Channel Heterogeneous Graph Structure Learning (MHGSL)**. Sistem memproyeksikan ekosistem klaim ke dalam tiga saluran graf independen:
1. **Topological Channel** ($A^{(top)}$): Memetakan interaksi rujukan fisik aktual.
2. **Feature Channel** ($A^{(feat)}$): Memetakan kedekatan atribut laten antar-entitas berbasis kemiripan kosinus (*cosine similarity*).
3. **Semantic Channel** ($A^{(sem)}$): Mengekstraksi pola perilaku berulang tingkat tinggi melalui jalur relasi meta (*metapaths*).

Melalui kombinasi konvolusi graf spesifik-saluran, representasi umum berparameter bersama (*shared-parameter* GCN), dan fusi atensi dengan atribusi SHAP, Aegis-JKN mampu menembus kamuflase topologi dan mengungkap sindikat kolusi dengan skor **AUPRC 0.91** (lonjakan +20% dibandingkan model tabular dasar).

---

## Core Architecture & Pipeline

Aegis-JKN mengimplementasikan alur pemrosesan end-to-end dalam 5 tahapan terstruktur:

```
+-----------------------------------------------------------------------------------+
|                        AEGIS-JKN 5-STAGE MHGSL PIPELINE                          |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| Stage 01: Standardized Health Data Ingestion                                      |
| SATUSEHAT HL7 FHIR R4 & BPJS V-Claim API (Encounter, Condition, Procedure, Meds) |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| Stage 02: Heterogeneous Multi-Channel Graph Construction                          |
| - Channel 1: Topology Adjacency A(top) [Physical Referrals & Service Chains]      |
| - Channel 2: Feature Adjacency A(feat) [Attribute Cosine Similarity > theta_feat]  |
| - Channel 3: Semantic Adjacency A(sem) [Metapath Co-occurrence Doctor-Dx-Proc-RS] |
+-----------------------------------------------------------------------------------+
                                          |
                     +--------------------+--------------------+
                     |                                         |
                     v                                         v
+------------------------------------------+ +--------------------------------------+
| Stage 03: Channel-Specific GCN Layers    | | Stage 04: Shared-Parameter GCN Layer |
| H(k) = sigma( D_k^(-1/2) A_k D_k^(-1/2)  | | H(shared,k) = sigma( D_k^(-1/2) A_k  |
|              * X * W(k) )                | |              * D_k^(-1/2) * X        |
| Ekstraksi fitur khas per saluran (top,   | |              * W(shared) )           |
| feat, sem)                               | | Menangkap komonalitas lintas saluran |
+------------------------------------------+ +--------------------------------------+
                     |                                         |
                     +--------------------+--------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| Stage 05: Multi-Channel Attention Fusion & SHAP Explainability                    |
| - H(final) = Concat( H(top), H(feat), H(sem), H(shared) )                        |
| - y_hat = Sigmoid( H(final) * W_cls + b )                                        |
| - SHAP Attribution: Mengungkap kontribusi tiap kanal (Misal: Kamuflase Topologi)  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| Human-in-the-Loop (HITL) Dashboard & Verifier Audit Action                        |
+-----------------------------------------------------------------------------------+
```

### Rincian 5 Tahapan Pipeline
1. **Ingestasi FHIR & V-Claim**: Ekstraksi terstandarisasi dari SATUSEHAT HL7 FHIR R4 (`Encounter`, `Condition` ICD-10, `Procedure` ICD-9-CM, `MedicationRequest`, `Composition`) dan format klaim BPJS V-Claim menjadi entitas graf heterogen: Pasien ($P$), Dokter ($D$), Fasilitas Kesehatan ($RS$), Prosedur ($S$), dan Diagnosis ($Dx$).
2. **Konstruksi 3 Kanal Graf**:
   - $A^{(top)}$: Matriks ketetanggaan fisik dari interaksi pelayanan medis nyata.
   - $A^{(feat)}$: Matriks kemiripan fitur atribut simpul berdasarkan threshold kosinus $\theta_{feat}$ (menghubungkan pasien dengan profil Length of Stay, usia, dan pola biaya yang identik).
   - $A^{(sem)}$: Graf semantik tingkat tinggi berbasis metapath $\mathcal{M} = D \to Dx \to S \to RS$ untuk menangkap perulangan pola diagnosis ringan yang dipasangkan dengan prosedur berbiaya mahal.
3. **Channel-Specific GCN**: Tiga model GCN independen dengan matriks bobot $W^{(top)}$, $W^{(feat)}$, dan $W^{(sem)}$ mempelajari karakteristik khusus masing-masing kanal secara terisolasi.
4. **Shared-Parameter GCN**: Konvolusi graf dengan matriks bobot bersama $W^{(shared)}$ diaplikasikan serentak ke ketiga kanal, memaksa representasi laten menangkap komonalitas struktural antar-kanal.
5. **Attention Fusion & SHAP Explainability**: Seluruh representasi digabungkan ($H^{(final)}$) dan diproyeksikan ke klasifikasi probabilitas fraud. Algoritma SHAP memecah skor risiko ke atribusi per-kanal, membuktikan adanya kamuflase topologi (nilai SHAP topologi negatif) yang dibongkar oleh saluran fitur dan semantik.

---

## Key Modules & Visualizations

Aegis-JKN dilengkapi dengan modul eksplorasi interaktif berbasis web untuk verifikator dan auditor:

### 1. Multi-Channel Interactive Graph Explorer
- Visualisasi graf heterogen interaktif berbasis Canvas dan SVG.
- Filter kanal dinamis: Toggle mandiri antara $A^{(top)}$, $A^{(feat)}$, dan $A^{(sem)}$ untuk mengamati struktur jaringan dari perspektif fisik, kesamaan fitur, maupun jalur semantik.
- Tombol penelusuran metapath untuk menyorot jalur relasi anomali Dokter-Diagnosis-Prosedur-Faskes.
- Tooltip dan inspeksi simpul komprehensif (in-degree, out-degree, tipe entitas, tingkat risiko).

### 2. 4-Step Upcoding Simulation with Camouflage Detection
Simulasi interaktif 4 fase yang membedah bagaimana pelaku kejahatan mengaburkan jejak dan bagaimana MHGSL menembusnya:
- **Langkah 01 (Klaim Masuk)**: Pada saluran topologi $A^{(top)}$, berkas rujukan $P_1, P_2, P_3 \to D_1, D_2 \to RS_A \to S_{mahal}$ tampak sebagai rujukan klinis yang normal dan wajar (skor awal 0.32).
- **Langkah 02 (Analisis Graf Fitur)**: Saluran $A^{(feat)}$ mendeteksi kemiripan kosinus $P_1-P_2 = 0.92$ dengan Length of Stay identik 3 hari dan rasio biaya klaster upcoding (skor meningkat ke 0.61).
- **Langkah 03 (Analisis Graf Semantik)**: Saluran $A^{(sem)}$ membongkar metapath berulang di mana dokter secara konsisten memadukan diagnosis primer ringan dengan prosedur bedah kompleks (skor meningkat ke 0.84).
- **Langkah 04 (Fusion & Klasifikasi SHAP)**: Fusi multi-kanal menghasilkan probabilitas fraud 0.94 dengan dekomposisi SHAP:
  - Kanal Semantik: $+41\%$ kontribusi risiko.
  - Kanal Fitur: $+38\%$ kontribusi risiko.
  - Kanal Topologi: $-12\%$ kontribusi risiko (**bukti tanda tangan kamuflase topologi**).

### 3. Syndicate Collusion Ring & Audit Drilldown
- Pemodelan subgraf komunitas padat (*dense collusive ring*) yang membandingkan komunitas sindikat dengan jaringan rujukan normal.
- Visualisasi penyebaran risiko melalui *message passing*.
- Modal investigasi audit (*Drilldown Modal*) mendalam untuk setiap entitas sindikat:
  - **D1 (Dr. A. Wijaya)**: Dokter spesialis bedah dengan 14 klaim upcoding repetitif, deviasi peer $+4.2\sigma$.
  - **RS_A (RS Sentosa Medika)**: Faskes rujukan dengan lonjakan klaim tindakan bedah mahal $+320\%$ yang terkonsentrasi pada 3 dokter spesialis.
  - **P1 (Pasien #JKN-2026-0451)**: Pasien dengan 3 episode rawat inap terpisah berjarak singkat dengan profil fitur kloning.

### 4. Benchmark Comparison Suite
- Evaluasi komparatif multi-metrik: AUPRC, ROC-AUC, Precision, Recall, Specificity, dan F1-Score.
- Visualisasi kurva dan Radar Chart interaktif membandingkan 6 metodologi:
  - Rule-Based / Thresholding (AUPRC: 0.58)
  - Logistic Regression (AUPRC: 0.62)
  - XGBoost Baseline (AUPRC: 0.71)
  - Homogeneous GCN (AUPRC: 0.78)
  - Hybrid GNN + XGBoost (AUPRC: 0.85)
  - **Aegis-JKN MHGSL (AUPRC: 0.91)**

### 5. Self-Service Data Uploader
- Fasilitas pengujian mandiri berkas klaim berbasis browser melalui file CSV atau JSON.
- Parser otomatis skema klaim (`patient_id`, `doctor_id`, `faskes`, `procedure`, `diagnosis`, `los`, `cost`, `age`).
- Mesin inferensi klien untuk kalkulasi skor topologi, fitur, dan semantik serta label risiko akhir (*Low*, *Medium*, *High*, *Fraud*).
- Dilengkapi template data klaim sintetis siap pakai untuk demonstrasi langsung.

---

## Mathematical Formulations Summary

### 1. Feature Channel Adjacency Matrix ($A^{(feat)}$)
Matriks ketetanggaan fitur menghubungkan pasangan simpul $i$ dan $j$ apabila kemiripan kosinus vektor atribut fitur $\mathbf{x}_i$ dan $\mathbf{x}_j$ melampaui ambang batas $\theta_{feat}$:

$$
A^{(feat)}_{ij} = \begin{cases} 
\frac{\mathbf{x}_i \cdot \mathbf{x}_j}{\|\mathbf{x}_i\| \|\mathbf{x}_j\|}, & \text{jika } \cos(\mathbf{x}_i, \mathbf{x}_j) > \theta_{feat} \\ 
0, & \text{lainnya} 
\end{cases}
$$

### 2. Channel-Specific Graph Convolution ($H^{(k)}$)
Operasi konvolusi graf spektral tingkat pertama untuk setiap saluran $k \in \{top, feat, sem\}$ dengan normalisasi derajat simetri:

$$
\mathbf{H}^{(k)} = \sigma \left( \tilde{\mathbf{D}}^{-\frac{1}{2}}_{(k)} \tilde{\mathbf{A}}^{(k)} \tilde{\mathbf{D}}^{-\frac{1}{2}}_{(k)} \mathbf{X} \mathbf{W}^{(k)} \right)
$$

Di mana $\tilde{\mathbf{A}}^{(k)} = \mathbf{A}^{(k)} + \mathbf{I}_N$ adalah matriks ketetanggaan dengan *self-loops*, $\tilde{\mathbf{D}}^{(k)}_{ii} = \sum_j \tilde{\mathbf{A}}^{(k)}_{ij}$ adalah matriks derajat terkait, dan $\sigma(\cdot)$ adalah fungsi aktivasi non-linier (ReLU/LeakyReLU).

### 3. Shared-Parameter Graph Convolution ($H^{(shared, k)}$)
Konvolusi graf menggunakan bobot bersama $\mathbf{W}^{(shared)}$ untuk menangkap representasi invarian lintas ketiga saluran:

$$
\mathbf{H}^{(shared,\, k)} = \sigma \left( \tilde{\mathbf{D}}^{-\frac{1}{2}}_{(k)} \tilde{\mathbf{A}}^{(k)} \tilde{\mathbf{D}}^{-\frac{1}{2}}_{(k)} \mathbf{X} \mathbf{W}^{(shared)} \right)
$$

### 4. Attention-Based Multi-Channel Fusion & Classification
Penggabungan representasi laten multi-kanal diikuti proyeksi klasifikasi akhir:

$$
\mathbf{H}^{(final)} = \text{Concat}\left( \mathbf{H}^{(top)}, \mathbf{H}^{(feat)}, \mathbf{H}^{(sem)}, \mathbf{H}^{(shared)} \right)
$$

$$
\hat{y}_i = \text{Sigmoid}\left( \mathbf{H}^{(final)}_i \mathbf{W}_{cls} + b \right)
$$

---

## Tech Stack & Dependencies

| Lapisan | Teknologi | Versi | Peran |
|---|---|---|---|
| **Framework** | Next.js (App Router) | 16.1.1 | Server-Side Rendering, Static Optimization, API Handlers |
| **Runtime** | Bun / Node.js | >= 20.0 | High-performance JavaScript/TypeScript Runtime |
| **UI Library** | React | 19.0.0 | Declarative Component Architecture |
| **Language** | TypeScript | 5.x | Strict Type Safety & Data Contracts |
| **CSS & Design** | Tailwind CSS | 4.0 | Modern utility-first styling dengan OKLCH token engine |
| **Primitives** | Radix UI | Latest | Accessible unstyled primitives (Dialog, Tabs, Accordion) |
| **Animation** | Framer Motion | 12.23.2 | Smooth orchestrated physics animations |
| **Data Viz** | Recharts & HTML5 Canvas | 2.15.4 | Radar charts, bar metrics, interactive graph layouts |
| **Icons** | Lucide React | 0.525.0 | Clean, accessible vector icons |
| **Forms & Validation** | React Hook Form & Zod | 7.60 / 4.0 | Robust form validation & CSV schema enforcement |
| **Theme & i18n** | next-themes & Aegis-i18n | Built-in | Bilingual (ID/EN) and Dark/Light Mode switching |

---

## Repository Structure

```
N:\HEALTHKATHON\
├── src\
│   ├── app\
│   │   ├── api\
│   │   │   └── route.ts              # API health check and scoring endpoint
│   │   ├── globals.css               # Tailwind CSS v4 variables & OKLCH color definitions
│   │   ├── layout.tsx                # Root layout with ThemeProvider and toaster
│   │   └── page.tsx                  # Main single-page dashboard container
│   ├── components\
│   │   ├── mhgsl\
│   │   │   ├── architecture.tsx      # 5-stage pipeline and system architecture
│   │   │   ├── back-to-top.tsx       # Smooth scroll to top trigger
│   │   │   ├── comparison.tsx        # Benchmark comparison suite (AUPRC, Radar, Table)
│   │   │   ├── data.ts               # Synthetic datasets, graph nodes/edges, and profiles
│   │   │   ├── data-uploader.tsx     # Client-side custom claim scoring engine modal
│   │   │   ├── footer.tsx            # Compliance footer and quick navigation links
│   │   │   ├── fraud-drilldown-modal.tsx # Deep investigative entity audit modal
│   │   │   ├── fraud-ring.tsx        # Syndicate collusion ring graph and message passing
│   │   │   ├── glossary.tsx          # Health economics & machine learning glossary
│   │   │   ├── hero.tsx              # Hero header with dynamic counter statistics
│   │   │   ├── i18n.tsx              # Bilingual dictionary context (Indonesian / English)
│   │   │   ├── lang-toggle.tsx       # Language switcher component
│   │   │   ├── math-formulas.tsx     # Mathematical formulations interactive explorer
│   │   │   ├── multi-channel-graph.tsx # Interactive 3-channel graph visualizer
│   │   │   ├── navbar.tsx            # Sticky navigation bar with quick anchors
│   │   │   ├── problem-section.tsx   # BPJS problem statement and 3 fraud risk pillars
│   │   │   ├── roadmap.tsx           # Multi-phase implementation roadmap and ROI analysis
│   │   │   ├── shortcuts-hint.tsx    # Keyboard shortcut cheat sheet trigger
│   │   │   ├── simulation.tsx        # 4-stage upcoding simulation with SHAP breakdown
│   │   │   ├── theme-toggle.tsx      # Dark / Light theme toggle
│   │   │   ├── use-count-up.ts       # Animated integer count-up hook
│   │   │   └── use-keyboard-shortcuts.ts # Global accessible keyboard listener
│   │   └── ui\                       # 40+ atomic Shadcn UI / Radix components
│   └── lib\
│       ├── db.ts                     # Database connection utility
│       └── utils.ts                  # Class merger utility (clsx + twMerge)
├── docs\                             # Comprehensive Technical Documentation Suite
│   ├── architecture\
│   │   └── system-design.md          # End-to-end system design & FHIR mapping
│   ├── algorithms\
│   │   └── mhgsl-theory.md           # Mathematical theory of MHGSL & camouflage detection
│   ├── deployment\
│   │   └── vercel.md                 # Production deployment guide for Vercel
│   ├── user-guide\
│   │   └── navigation.md             # Verifier manual, simulation, and keyboard navigation
│   └── api\
│       └── data-contracts.md         # Data contracts, JSON/CSV schemas, and scoring weights
├── public\                           # Static assets, SVG diagrams, robots.txt
├── next.config.ts                    # Next.js configuration (standalone output)
├── package.json                      # Dependency manifests and scripts
├── tsconfig.json                     # TypeScript compiler configuration
└── README.md                         # Project documentation entry point
```

---

## Getting Started / Local Development

### Prerequisites
- Node.js version 20.x or higher (LTS recommended)
- Alternatively, Bun version 1.1 or higher
- Git for version control

### 1. Clone the Repository
```bash
git clone https://github.com/biezz-2/aegis-jkn-mhgsl.git
cd aegis-jkn-mhgsl
```

### 2. Install Dependencies
Using Bun (preferred for optimal speed):
```bash
bun install
```
Atau menggunakan npm:
```bash
npm install
```

### 3. Start Development Server
```bash
bun dev
```
Atau:
```bash
npm run dev
```

Buka peramban web pada alamat `http://localhost:3000` untuk mengakses aplikasi Aegis-JKN.

### 4. Build for Production
```bash
bun run build
```
Atau:
```bash
npm run build
```

Jalankan server produksi lokal:
```bash
bun start
# atau
npm start
```

---

## Vercel Deployment Guide

Aegis-JKN dirancang secara native agar sepenuhnya kompatibel dengan infrastruktur Vercel Serverless & Edge.

### 1-Click Deploy via Vercel CLI
Pastikan Vercel CLI telah terinstal pada mesin lokal:
```bash
npm i -g vercel
```

Jalankan perintah deploy dari root repositori:
```bash
vercel
```

Untuk rilis produksi:
```bash
vercel --prod
```

### Konfigurasi Vercel Dashboard
Saat mengimpor proyek melalui Vercel Web Dashboard:
- **Framework Preset**: Next.js
- **Root Directory**: `./`
- **Build Command**: `next build`
- **Output Directory**: `.next`
- **Install Command**: `bun install` atau `npm install`

Lihat panduan lengkap di [docs/deployment/vercel.md](docs/deployment/vercel.md) untuk detail optimasi bundle dan konfigurasi CDN.

---

## Keyboard Shortcuts & Accessibility

Aegis-JKN dirancang dengan standar aksesibilitas tinggi untuk memfasilitasi alur kerja verifikator yang cepat:

| Tombol Pintas | Aksi | Keterangan |
|---|---|---|
| `t` | **Toggle Theme** | Beralih antara Dark Mode dan Light Mode |
| `p` | **Print / Export PDF** | Membuka dialog cetak laporan audit terformat |
| `g` | **Scroll ke Graf** | Navigasi cepat ke Multi-Channel Graph Explorer |
| `s` | **Scroll ke Simulasi** | Navigasi cepat ke 4-Step Upcoding Simulation |
| `→` (*Arrow Right*) | **Langkah Berikutnya** | Menjalankan tahap simulasi selanjutnya |
| `←` (*Arrow Left*) | **Langkah Sebelumnya** | Kembali ke tahap simulasi sebelumnya |

### Fitur Aksesibilitas Tambahan
- **Dukungan Bilingual (ID/EN)**: Seluruh label antarmuka, deskripsi medis, dan analisis risiko tersedia dalam Bahasa Indonesia dan Bahasa Inggris secara terpadu melalui toggle `[ID] / [EN]`.
- **Palet Warna OKLCH Ramah Pengguna**: Kontras teks dan grafika memenuhi rasio WCAG 2.1 AA di seluruh skema warna terang dan gelap.
- **Screen Reader Friendly**: Elemen grafis dilengkapi dengan label semantik, ARIA tags, dan visualisasi alternatif.

---

## Documentation Suite

Dokumentasi teknis mendalam tersedia dalam folder `docs/`:

1. [System Architecture & Design](docs/architecture/system-design.md): Struktur modular, hirarki komponen, dan pemetaan data SATUSEHAT FHIR R4 ke graf.
2. [MHGSL Mathematical & Algorithmic Theory](docs/algorithms/mhgsl-theory.md): Formulasi matematika lengkap, matriks kosinus, konvolusi graf multi-kanal, dan SHAP.
3. [Vercel Deployment Guide](docs/deployment/vercel.md): Prosedur deployment, pengaturan caching, dan optimasi performa Next.js 16.
4. [User Guide & Navigation Manual](docs/user-guide/navigation.md): Panduan verifikator untuk penggunaan simulasi, drilldown modal, dan upload berkas mandiri.
5. [Data Contracts & API Specifications](docs/api/data-contracts.md): Skema JSON/CSV klaim, model simpul/tepi graf, serta matriks bobot penilaian risiko.

---

## License & Attribution

Proyek ini dirilis di bawah lisensi [MIT License](LICENSE).

Dikembangkan sebagai proposal inovasi teknologi kecerdasan buatan untuk **BPJS Kesehatan Healthkathon 2026**.
Seluruh data pasien, dokter, dan rumah sakit yang ditampilkan dalam platform ini merupakan data sintetis untuk keperluan demonstrasi metodologi ilmiah.
