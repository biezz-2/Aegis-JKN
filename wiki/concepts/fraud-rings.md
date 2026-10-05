---
title: Fraud Rings & Collusion Communities
type: concept
tags: [fraud-ring, collusion, syndicates, community-detection, audit, drilldown]
related:
  - "[[concepts/mhgsl-architecture]]"
  - "[[concepts/multi-channel-graphs]]"
  - "[[reference/component-catalog]]"
sources:
  - src/components/mhgsl/fraud-ring.tsx
  - src/components/mhgsl/fraud-drilldown-modal.tsx
  - src/components/mhgsl/data.ts
---

# Fraud Rings & Sindikat Kolusi Layanan Kesehatan

## Ringkasan Konsep

Penipuan klaim layanan kesehatan skala besar jarang dilakukan oleh pelaku tunggal secara acak. Sebagian besar kerugian finansial yang dialami BPJS Kesehatan diakibatkan oleh sindikat terorganisir (*fraud ring* / sindikat kolusi) yang melibatkan koordinasi antar faskes korup, oknum dokter rujukan, dan kelompok pasien terkoordinasi (atau kartu identitas JKN yang disalahgunakan).

## Karakteristik Komunitas Kolusif vs Komunitas Normal

Aegis-JKN membandingkan dua topologi komunitas secara berdampingan:

| Indikator | Komunitas Kolusif (Fraud Ring) | Komunitas Sehat / Normal |
| :--- | :--- | :--- |
| **Kepadatan Edge (Graph Density)** | Sangat tinggi (misal: 14 edge untuk 6 node). | Normal/renggang (misal: 7 edge untuk 6 node). |
| **Pola Rujukan** | Sirkular dan tertutup (pasien selalu dirujuk bolak-balik antara dokter tertentu dan faskes yang sama). | Terbuka dan terdistribusi wajar sesuai zonasi dan kompetensi faskes. |
| **Inkonsistensi Klinis** | Rasio peresepan obat atau tindakan mahal melebihi 85% untuk kasus ringan. | Mengikuti pedoman klinis (Clinical Pathway) dan Formularium Nasional. |
| **Distribusi Waktu** | Lonjakan klaim dalam batch teratur (misal: akhir bulan) dengan Length of Stay identik. | Kedatangan pasien acak mengikuti distribusi Poisson alami. |

## Modul Investigasi Mandiri: Fraud Drilldown

Aegis-JKN menyediakan antarmuka audit investigasi mendalam melalui komponen `fraud-drilldown-modal.tsx`. Fitur ini memungkinkan auditor BPJS Kesehatan untuk membuka rekam jejak entitas yang dicurigai:

1. **Profil Dokter $D_1$ (Dr. A. Wijaya)**:
   - Skor Risiko: **0.94 (Tinggi / Sindikat)**
   - Temuan Kunci: Upcoding repetitif pada 87% klaim, rasio rujukan sirkular ke Faskes $RS_A$ mencapai 92%.
   - Atribusi Saluran: Fitur (+0.38), Semantik (+0.41), Topologi (-0.12).
   
2. **Profil Fasilitas Kesehatan $RS_A$ (RS Sentosa Medika)**:
   - Skor Risiko: **0.89 (Tinggi)**
   - Temuan Kunci: Rasio tagihan tindakan berbiaya tinggi ($S_{\text{mahal}}$) tidak sebanding dengan kelas rumah sakit dan populasi diagnosis masuk.

3. **Profil Pasien $P_1$ (Pasien #JKN-2026-0451)**:
   - Skor Risiko: **0.78 (Sedang-Tinggi)**
   - Temuan Kunci: Dugaan peminjaman kartu BPJS atau *phantom billing*, di mana Length of Stay tercatat selalu 3 hari secara persis dalam 4 kunjungan berturut-turut.

## Tindakan Remediasi yang Direkomendasikan
Sistem secara otomatis mengusulkan aksi operasional:
- Penangguhan sementara pencairan klaim (*provisional hold*).
- Pemeriksaan rekam medis fisik (*on-site audit*).
- Pemanggilan komite medik dan verifikator internal faskes.

## Kode Terkait
- `src/components/mhgsl/fraud-ring.tsx` - Komponen visualisasi perbandingan komunitas.
- `src/components/mhgsl/fraud-drilldown-modal.tsx` - Dialog modal profil audit dan timeline kejadian.
- `src/components/mhgsl/data.ts:250-320` - Profil data sintetis investigasi.
