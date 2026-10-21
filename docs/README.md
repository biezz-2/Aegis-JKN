# Dokumentasi Proyek Aegis-JKN (BPJS Kesehatan Healthkathon 2026)

> **Sumber Ruang Kerja Notion:** [HEALTHKATHON 2026 — Aegis-JKN](https://app.notion.com/p/HEALTHKATHON-3f23e6031ab7808db2cbfe92cd62391d)  
> **ID Halaman Induk:** `3f23e603-1ab7-808d-b2cb-fe92cd62391d`  
> **Slogan:** *« Detect Smarter. Protect JKN. »*  
> **Purwarupa Aplikasi:** [aegisjkn.vercel.app](http://aegisjkn.vercel.app)

---

## 📌 Daftar Isi Dokumentasi

Koleksi berkas di dalam folder `docs/` ini telah disusun secara modular dan terstruktur sesuai hierarki dokumen pada ruang kerja Notion:

### 1. Perencanaan & Konsep Ide
- **[01-kandidat-ide-hackathon-bpjs.md](./01-kandidat-ide-hackathon-bpjs.md)**  
  Analisis dan komparasi 3 kandidat ide solusi penanganan kebocoran dana BPJS Kesehatan:
  - *Kandidat 1 (Pilihan Utama):* Anomali Diagnosa Jantung & Saraf (Upcoding & Unbundling) via NLP / Local LLM.
  - *Kandidat 2:* Sindikat Joki Pasien (Penyalahgunaan Identitas) via PWA Facial Recognition.
  - *Kandidat 3 (Cadangan):* Manipulasi Gaji Pekerja (Under-reporting Upah) via Cross-match DJP & Whistleblowing.

### 2. Proposal Resmi
- **[02-proposal-lengkap-aegis-jkn.md](./02-proposal-lengkap-aegis-jkn.md)**  
  Naskah proposal inovasi lengkap dan formal untuk BPJS Kesehatan Healthkathon 2026 (~82.000 karakter):
  - Lembar Pernyataan Orisinalitas & Pengesahan.
  - Executive Summary & Latar Belakang Finansial DJS.
  - Arsitektur Solusi MHGSL (*Multi-Hop Graph Structure Learning*) & Multimodal Simulation.
  - Interoperabilitas SATUSEHAT FHIR & BPJS V-Claim.
  - Explainable AI (XAI) & SHAP Decision Support.
  - Kepatuhan Hukum (UU PDP No. 27/2022 & Permenkes No. 24/2022).
  - Analisis Finansial, Proyeksi ROI, Timeline Implementasi, dan Susunan Tim Inovator.

### 3. Arsitektur Teknis & Kerangka Presentasi
- **[03-arsitektur-dan-strategi-pengembangan.md](./03-arsitektur-dan-strategi-pengembangan.md)**  
  Dokumen teknis komprehensif mengenai analisis kelayakan sistem, pemodelan multi-dimensi (MHGSL + XAI/SHAP), mitigasi alert fatigue, dan kerangka proposal 20 slide presentasi pitch deck.

### 4. Strategi AI, XAI, dan Model Fraud
- **[STRATEGI_AI_XAI_DAN_MODEL_FRAUD.md](./STRATEGI_AI_XAI_DAN_MODEL_FRAUD.md)**  
  Keputusan arsitektur untuk XAI/Grok sebagai copilot bahasa, model tabular sebagai fraud scorer, roadmap MHGSL, dan batas keputusan *human-in-the-loop*.

### 5. Riset Investigasi & Analisis LLM
- **[04-deep-research/README.md](./04-deep-research/README.md)**  
  Laporan investigasi kasus fraud klaim BPJS tahun 2024 (3 RS swasta, kerugian Rp25 miliar, modus phantom billing & upcoding) serta identifikasi 5 celah sistemik.
- **[04-deep-research/large-language-model-hallucination.md](./04-deep-research/large-language-model-hallucination.md)**  
  Kajian teknis mengenai halusinasi LLM pada domain medis, 6 tahap siklus model, serta metrik tolok ukur mitigasi halusinasi pada pembacaan narasi EMR.

### 5. Desain UI/UX & Analisis Masalah
- **[05-figma-dan-fishbone-diagram.md](./05-figma-dan-fishbone-diagram.md)**  
  Dokumentasi desain dan tautan langsung ke papan kerja Figma/FigJam:
  - *FigJam Board:* [Fishbone Diagram 6M — Kebocoran Finansial Klaim JKN Aegis](https://www.figma.com/board/ePv0sbUCNU9iOgRiTMwH8E/Fishbone-Diagram-6M---Kebocoran-Finansial-Klaim-JKN-Aegis?node-id=0-1&p=f&t=pYR0GTGzXi53K7Hq-0).
  - Dekonstruksi akar masalah menggunakan kerangka 6M (*Man, Machine, Method, Material, Measurement, Milieu*).

### 6. Dataset Riset & Data Simulasi
Folder **[datasets/](./datasets/README.md)** menyediakan data terstruktur dan dataset sintetis berorientasi privasi:
- **[01-dataset-riset-fraud-jkn.md](./datasets/01-dataset-riset-fraud-jkn.md)**  
  Katalog 33 referensi riset, regulasi, dan teknologi AI.
  - Data Mentah: `dataset-riset-fraud-jkn.csv` | `dataset-riset-fraud-jkn.json`
- **[02-dataset-simulasi-100-klaim.md](./datasets/02-dataset-simulasi-100-klaim.md)**  
  Metodologi pembentukan 100 klaim sintetis berbasis DP-CTGAN (*Differential Privacy Conditional GAN*).
- **[03-klaim-aegis-jkn-100-baris.md](./datasets/03-klaim-aegis-jkn-100-baris.md)**  
  Tabel 100 klaim sintetis dengan 27 parameter verifikasi (skor fraud, diagnosis ICD-10, prosedur ICD-9-CM, narasi EMR, kontradiksi klinis, sentimen pasien, rujukan, dsb).
  - Data Mentah: `klaim-aegis-jkn-100-baris.csv` | `klaim-aegis-jkn-100-baris.json`

---

## 🛠️ Informasi Teknis Ekstraksi
- **Tooling:** Composio MCP (`composio execute NOTION_GET_PAGE_MARKDOWN`, `NOTION_FETCH_ALL_BLOCK_CONTENTS`, `NOTION_QUERY_DATABASE`).
- **Tanggal Ekstraksi:** 20 Oktober 2026.
- **Standar Output:** GitHub Flavored Markdown (GFM), RFC 4180 CSV, dan JSON UTF-8.
