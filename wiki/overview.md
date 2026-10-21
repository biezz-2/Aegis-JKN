---
title: Aegis-JKN Overview
type: overview
tags: [overview, healthkathon, mhgsl, gnn, bpjs-kesehatan, fraud-detection, synthetic-data, verifier-dashboard]
related:
  - "[[concepts/mhgsl-architecture]]"
  - "[[concepts/multi-channel-graphs]]"
  - "[[concepts/fraud-rings]]"
  - "[[concepts/dataset-contract]]"
  - "[[concepts/verifier-dashboard]]"
  - "[[guides/getting-started]]"
  - "[[guides/dashboard-development]]"
  - "[[reference/component-catalog]]"
  - "[[reference/academic-paper]]"
sources:
  - src/app/page.tsx
  - src/components/mhgsl/data.ts
  - dashboard/src/
  - docs/DATA_SCHEMA.md
---

# Aegis-JKN · Sistem Intelijen Deteksi Fraud Klaim BPJS Kesehatan

Aegis-JKN adalah platform analitik dan visualisasi interaktif untuk mendeteksi kecurangan klaim layanan kesehatan di ekosistem Program Jaminan Kesehatan Nasional (JKN) yang dikelola oleh BPJS Kesehatan Indonesia. Platform ini memvisualisasikan implementasi **Multi-channel Heterogeneous Graph Structure Learning (MHGSL)** yang digabungkan dengan **Graph Neural Networks (GNN)** untuk mengidentifikasi sindikat penipuan yang menyamarkan polanya (*camouflage fraud*).

Repositori ini memuat dua bagian yang saling melengkapi:

1. **Showcase MHGSL** (Next.js, di root) — visualisasi interaktif arsitektur 3 kanal, simulasi upcoding, dan analisis fraud ring.
2. **Dashboard Verifikator Aegis-JKN** (SvelteKit, di `dashboard/`) — prototipe *decision support* client-side untuk menelaah dataset klaim sintetis.

## Tantangan Nyata Ekosistem JKN

1. **Volume Klaim Masif**: Lebih dari 2.000.000 klaim diproses setiap hari kerja dari ribuan fasilitas kesehatan (FKTP dan FKRTL) di seluruh Indonesia.
2. **Keterbatasan Verifikator Manusia**: Tersedia sekitar 1.000 verifikator klaim manual, menghasilkan rasio beban verifikasi hingga 2.000 klaim per verifikator per hari.
3. **Kebocoran Dana Kesehatan**: Estimasi global estimasi fraud berkisar antara 3% hingga 7% dari total realisasi klaim tahunan.
4. **Kamuflase Canggih**: Sindikat kejahatan memanipulasi topologi klaim sehingga terlihat normal bila diaudit satu per satu dengan pendekatan rule-based tradisional atau machine learning konvensional (XGBoost, Regresi Logistik).

## Arsitektur 5-Tahap Aegis-JKN

1. **Ingest SATUSEHAT FHIR**: Standardisasi data transaksi klaim klinis menggunakan standar interoperabilitas Kementerian Kesehatan Republik Indonesia (FHIR R4).
2. **Konstruksi 3 Saluran Graf Heterogen**: Memetakan entitas (Pasien, Dokter, Faskes, Prosedur, Diagnosis) ke dalam 3 saluran independen:
   - *Saluran Topologi*: Relasi historis kunjungan dan rujukan.
   - *Saluran Fitur*: Kemiripan atribut numerik/kategorikal (Length of Stay, usia, total biaya).
   - *Saluran Semantik*: Jalur metapath klinis (Dokter $\to$ Diagnosis $\to$ Tindakan $\to$ RS).
3. **Channel-Specific GCN**: Ekstraksi representasi embedding dari masing-masing saluran graf secara terisolasi.
4. **Shared-Parameter GCN**: Pertukaran bobot parameter untuk mengekstraksi representasi invarian lintas domain relasional.
5. **Attention Fusion & SHAP Explainability**: Penimbangan adaptif saluran graf dan penjelas kontribusi fitur (*explainable AI*) yang mampu mendeteksi sindrom kamuflase (misal: saluran topologi berkontribusi negatif sementara saluran semantik bernilai ekstrem).

## Modul Utama pada Aplikasi

- **Multi-Channel Graph Viewer** (`src/components/mhgsl/multi-channel-graph.tsx`): Kanvas SVG graf dinamis dengan pemfilteran saluran, deteksi node berisiko, serta tracing *metapath flow*.
- **Interactive Simulation Engine** (`src/components/mhgsl/simulation.tsx`): Demo 4 langkah audit kasus upcoding dengan akumulasi bobot fusi dan waterfall atribusi SHAP.
- **Fraud Ring Visualizer & Drilldown Modal** (`src/components/mhgsl/fraud-ring.tsx` & `src/components/mhgsl/fraud-drilldown-modal.tsx`): Perbandingan topologi komunitas kolusif padat vs normal serta investigasi profil mendalam.
- **Benchmark & Radar Chart** (`src/components/mhgsl/comparison.tsx`): Evaluasi AUPRC (MHGSL mencapai 0.91 vs GNN 0.81 dan XGBoost 0.74).
- **Self-Service Claim Data Uploader** (`src/components/mhgsl/data-uploader.tsx`): Mesin inferensi lokal peramban untuk scoring dataset CSV/JSON pengguna.
- **Mathematical Formulations Viewer** (`src/components/mhgsl/math-formulas.tsx`): Katalog persamaan matematis lengkap.

## Dashboard Verifikator

Dashboard Verifikator Aegis-JKN adalah prototipe *clinical decision support* yang berjalan sepenuhnya di peramban. Ia menampilkan bukti pra-komputasi dari **dataset sintetis** dan tidak pernah otomatis menyetujui, menolak, atau menaikkan klaim — keputusan akhir tetap pada verifikator.

- Rute `/` adalah landing page publik; seluruh CTA mengarah ke `/demo`.
- Rute `/demo` adalah ruang kerja verifikator: antrean klaim dengan filter/pencarian, panel EMR, panel bukti AI, pengelompokan sindikat, dan tindakan HITL yang mewajibkan catatan.
- Sumber kanonik dataset adalah `docs/datasets/klaim-aegis-jkn-dataset.json` (300 klaim sintetis); salinan di `dashboard/src/data/` harus byte-identik.
- Dataset tidak memuat tarif INA-CBG pembanding, graph edge produksi, maupun nilai SHAP numerik per fitur — UI tidak boleh mengarang nilai-nilai tersebut.
- Audit keputusan disimpan di `localStorage` browser untuk demonstrasi; itu **bukan** rekam audit produksi.

## Panduan Navigasi Wiki

- [[concepts/mhgsl-architecture]] - Detail arsitektur model dan mekanisme 3 saluran.
- [[concepts/multi-channel-graphs]] - Representasi entitas, node, dan edge heterogen.
- [[concepts/fraud-rings]] - Pola sindikat kolusi faskes-dokter-pasien dan analisis komunitas graf.
- [[concepts/shap-camouflage-detection]] - Metodologi pembuktian kamuflase menggunakan SHAP.
- [[concepts/dataset-contract]] - Kontrak dataset sintetis 300 klaim dan batas data.
- [[concepts/verifier-dashboard]] - Rute, aliran data, dan batas aman dashboard verifikator.
- [[guides/getting-started]] - Panduan instalasi dan menjalankan proyek secara lokal.
- [[guides/vercel-deployment]] - Panduan deployment aplikasi ke platform Vercel.
- [[guides/dashboard-development]] - Perintah, port 5175, deployment PM2, dan konvensi Svelte 5.
- [[reference/data-schema]] - Struktur tipe data, metadata node, dan format klaim FHIR.
- [[reference/component-catalog]] - Katalog komponen React dan peruntukannya.
- [[reference/academic-paper]] - Status bukti makalah dan catatan sitasi.
