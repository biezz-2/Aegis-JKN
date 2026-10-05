---
title: SHAP Camouflage Detection
type: concept
tags: [shap, camouflage, explainability, xai, attribution, simulation]
related:
  - "[[concepts/mhgsl-architecture]]"
  - "[[concepts/multi-channel-graphs]]"
  - "[[reference/mathematical-formulations]]"
sources:
  - src/components/mhgsl/simulation.tsx
  - src/components/mhgsl/data.ts
---

# Deteksi Kamuflase Fraud Menggunakan Nilai SHAP

## Masalah Kamuflase Adversarial (*Camouflage Fraud*)

Dalam sistem deteksi berbasis kecerdasan buatan, pelaku kejahatan (*adversary*) yang cerdas sering kali mempelajari cara kerja algoritma. Salah satu teknik penyamaran yang sering digunakan pada transaksi klaim asuransi kesehatan adalah **Topological Camouflage**:
- Oknum dokter atau fasilitas kesehatan menjaga pola kunjungan pasien agar terlihat normal dan tidak memicu deteksi anomali topologi sederhana.
- Frekuensi pertemuan pasien dengan dokter dijaga tetap wajar.
- Akibatnya, pada saluran graf topologi tradisional, klaim ini diberi skor anomali yang sangat rendah atau bahkan dinilai "sehat" (nilai kontribusi negatif terhadap kecurigaan).

## Solusi MHGSL: Penguraian Saluran Multi-Dimensi

MHGSL mengatasi penyamaran ini dengan memisahkan representasi graf ke dalam 3 saluran mandiri dan mengagregasikannya dengan mekanisme *Attention Fusion*.

Ketika dievaluasi dengan SHAP (*SHapley Additive exPlanations*), tanda tangan penyamaran (*camouflage signature*) terlihat secara jelas:

$$\text{Fraud Probability} = \sigma\left(\phi_0 + \sum_{i} \phi_i\right)$$

Di mana $\phi_i$ adalah nilai kontribusi SHAP untuk masing-masing saluran:

| Saluran / Komponen Fitur | Nilai SHAP ($\phi_i$) | Interpretasi AI |
| :--- | :--- | :--- |
| **Saluran Topologi** | **-0.12** | *Penyamaran Aktif*: Struktur kunjungan sengaja disamarkan agar terlihat wajar. |
| **Saluran Fitur** | **+0.38** | *Anomali Atribut*: Length of Stay (LOS) dan keseragaman tarif mencurigakan. |
| **Saluran Semantik** | **+0.41** | *Inkonsistensi Klinis*: Diagnosis ringan dipasangkan dengan tindakan berbiaya mahal. |
| **Base / Bias Intercept** | **+0.27** | Bobot probabilitas dasar populasi klaim. |
| **Skor Probabilitas Fusi Akhir** | **0.94** | **Vonis: FRAUD TINGGI (Sindikat Upcoding Terorganisir)** |

## Visualisasi Waterfall SHAP pada Simulasi

Komponen `simulation.tsx` menyediakan visualisasi *waterfall chart* interaktif pada langkah ke-4 simulasi:
- Baris warna hijau/teal mengindikasikan faktor yang menekan risiko (kamuflase topologi).
- Baris warna rose/merah mengindikasikan faktor pendorong risiko kecurangan (anomali fitur dan inkonsistensi semantik).
- Penjelasan ini memberikan justifikasi hukum dan klinis yang transparan bagi verifikator BPJS Kesehatan sebelum membekukan klaim faskes terkait.

## Kode Terkait

- `src/components/mhgsl/simulation.tsx` - Komponen simulasi 4 langkah dan grafik waterfall SHAP.
- `src/components/mhgsl/data.ts:180-240` - Data tahapan narasi kasus upcoding dan kontribusi bobot SHAP per langkah.
