---
title: Component Catalog
type: reference
tags: [components, react, nextjs, shadcn, ui, framer-motion]
related:
  - "[[overview]]"
  - "[[guides/getting-started]]"
sources:
  - src/components/mhgsl/
---

# Katalog Komponen Aegis-JKN

Daftar komponen modular dalam arsitektur antarmuka `src/components/mhgsl/`:

| Nama Komponen | File Path | Fungsi Utama |
| :--- | :--- | :--- |
| **Navbar** | `navbar.tsx` | Navigasi sticky glassmorphism dengan scrollspy IntersectionObserver, drawer mobile, kontrol tema, tombol bahasa, dan shortcut hints. |
| **Hero** | `hero.tsx` | Bagian pembuka dengan animasi counter angka (*count-up*), ringkasan metrik volume klaim, dan CTA demo. |
| **ProblemSection** | `problem-section.tsx` | Visualisasi rasio kontras 2M klaim vs 1K verifikator serta 3 kartu pilar risiko (Faskes, Peserta, Pemberi Kerja). |
| **Architecture** | `architecture.tsx` | Diagram 5 tahapan pipeline MHGSL dari SATUSEHAT FHIR hingga Attention Fusion dan SHAP. |
| **MultiChannelGraph** | `multi-channel-graph.tsx` | Kanvas SVG interaktif graf heterogen 3 saluran dengan animasi edge pulse dan metapath flow. |
| **Simulation** | `simulation.tsx` | Simulasi interaktif 4 langkah deteksi upcoding dengan visualisasi penumpukan kontribusi saluran dan grafik waterfall SHAP. |
| **MathFormulas** | `math-formulas.tsx` | Penampil tab rumus matematis (Cosine Adjacency, GCN, Weight Sharing, Attention Fusion) disertai glosarium simbol. |
| **Comparison** | `comparison.tsx` | Evaluasi komparatif multi-tab: Bar chart AUPRC, Radar Chart 5 metrik, tabel komparasi detail, dan pemicu Data Uploader. |
| **FraudRing** | `fraud-ring.tsx` | Kanvas visualisasi graf perbandingan komunitas kolusif padat vs komunitas normal dengan tombol buka modal profil. |
| **FraudDrilldownModal**| `fraud-drilldown-modal.tsx`| Dialog modal rincian profil audit entitas tersangka ($D_1$, $RS_A$, $P_1$) dengan timeline dan usulan tindakan. |
| **DataUploader** | `data-uploader.tsx` | Parser file CSV/JSON dengan mesin scoring MHGSL lokal peramban. |
| **Roadmap** | `roadmap.tsx` | Estimasi ROI penghematan dana kesehatan (Rp 14,4 Miliar) dan 3 fase implementasi operasional. |
| **Footer** | `footer.tsx` | Footer 4 kolom dengan tautan dokumentasi, privasi data SATUSEHAT, dan hak cipta. |
| **ThemeToggle** | `theme-toggle.tsx` | Tombol animasi transisi mode gelap/terang (Sun/Moon rotasi Framer Motion). |
| **LangToggle** | `lang-toggle.tsx` | Pengalih dwibahasa Bahasa Indonesia (ID) dan English (EN). |
| **ShortcutsHint** | `shortcuts-hint.tsx` | Popover pop-up daftar pintasan keyboard global. |
| **BackToTop** | `back-to-top.tsx` | Tombol melayang untuk kembali ke bagian atas halaman secara mulus. |
