---
title: Multi-Channel Heterogeneous Graphs
type: concept
tags: [graph, topology, feature-graph, semantic-graph, metapaths, nodes, edges]
related:
  - "[[concepts/mhgsl-architecture]]"
  - "[[concepts/fraud-rings]]"
  - "[[reference/data-schema]]"
sources:
  - src/components/mhgsl/multi-channel-graph.tsx
  - src/components/mhgsl/data.ts
---

# Multi-Channel Heterogeneous Graphs

## Ringkasan Konsep

Konsep dasar MHGSL dalam Aegis-JKN bertumpu pada dekomposisi data klaim ke dalam tiga representasi saluran graf heterogen. Setiap saluran menyoroti dimensi relasi yang berbeda dari ekosistem layanan kesehatan.

## Tipe Entitas (Nodes)

Dalam graf Aegis-JKN, terdapat 5 kelas entitas yang ditandai dengan kode warna dan ikon semantik:

| Tipe Node | Label | Warna UI | Keterangan |
| :--- | :--- | :--- | :--- |
| **Pasien** | $P_1, P_2, \dots$ | Emerald (`oklch(0.55 0.14 165)`) | Peserta penerima manfaat JKN yang menerima pelayanan medis. |
| **Dokter** | $D_1, D_2, \dots$ | Sky/Teal (`oklch(0.62 0.13 200)`) | Tenaga medis profesional penanggung jawab pelayanan (DPJP). |
| **Faskes** | $RS_A, RS_B, \dots$ | Amber (`oklch(0.7 0.16 70)`) | Fasilitas Kesehatan Rujukan Tingkat Lanjutan / Puskesmas. |
| **Prosedur** | $S_{\text{mahal}}, S_{\text{std}}$ | Rose (`oklch(0.62 0.22 20)`) | Tindakan medis berdasarkan kodifikasi ICD-9-CM. |
| **Diagnosis** | $Dx_{\text{ringan}}, Dx_{\text{berat}}$ | Violet (`oklch(0.5 0.13 280)`) | Kodifikasi penyakit berdasarkan ICD-10. |

## Tiga Saluran Graf

### 1. Saluran Topologi (Topology Channel)
- **Tujuan**: Menangkap riwayat interaksi klaim konvensional (siapa berobat ke siapa dan di mana).
- **Garis Edge**: Garis solid teal dengan panah penunjuk.
- **Kelemahan jika berdiri sendiri**: Rentan terhadap teknik kamuflase, di mana pelaku fraud dengan sengaja membatasi interaksi langsung antar entitas agar derajat node terlihat seperti pengguna normal.

### 2. Saluran Fitur (Feature Channel)
- **Tujuan**: Memetakan kemiripan profil atribut (Length of Stay / LOS, umur pasien, biaya klaim INA-CBG).
- **Garis Edge**: Garis putus-putus (*dashed line*) oranye/amber dengan bobot kosinus $S_{ij}$.
- **Kelebihan**: Mengungkap kelompok pasien yang memiliki pola rawat inap identik yang tidak wajar (misal: selalu tepat 3 hari dengan biaya mendekati batas tarif tertinggi).

### 3. Saluran Semantik (Semantic Channel)
- **Tujuan**: Menelusuri rantai korelasi klinis berbasis metapath.
- **Garis Edge**: Garis lengkung ungu/rose (*metapath flow*) dengan anotasi simbol $\mathcal{M}$.
- **Kelebihan**: Mendeteksi anomali klinis seperti dokter yang secara konsisten meresepkan prosedur bedah mahal ($S_{\text{mahal}}$) untuk diagnosis penyakit umum bergejala ringan ($Dx_{\text{ringan}}$).

## Representasi Interaktif pada UI

Komponen `multi-channel-graph.tsx` mengimplementasikan kanvas SVG interaktif yang mendukung:
- Toggle visualisasi per saluran (Topologi, Fitur, Semantik).
- Toggle jalur *metapath flow* dengan animasi pulsa edge (*flow dash*).
- Pemeriksaan node saat diklik atau di-hover, menampilkan atribut klinis dan label risiko fraud.

## Kode Terkait

- `src/components/mhgsl/multi-channel-graph.tsx` - Komponen SVG graf multi-saluran.
- `src/components/mhgsl/data.ts:68-135` - Definisi koordinat node, daftar edge, dan metadata risiko.
