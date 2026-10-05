---
title: MHGSL Architecture
type: concept
tags: [architecture, mhgsl, gnn, gcn, attention-fusion, pipeline]
related:
  - "[[overview]]"
  - "[[concepts/multi-channel-graphs]]"
  - "[[concepts/shap-camouflage-detection]]"
  - "[[reference/mathematical-formulations]]"
sources:
  - src/components/mhgsl/architecture.tsx
  - src/components/mhgsl/math-formulas.tsx
  - src/components/mhgsl/data.ts
---

# Multi-channel Heterogeneous Graph Structure Learning (MHGSL)

## Ringkasan Konsep

MHGSL adalah metodologi mutakhir dalam pembelajaran representasi graf heterogen (*Heterogeneous Information Networks / HIN*). Model ini dirancang khusus untuk memecahkan kelemahan algoritma GNN tradisional ketika berhadapan dengan data transaksi medis yang dipalsukan (*adversarial camouflage*).

Dalam kasus penipuan klaim asuransi kesehatan, sindikat penipu sering kali menyebarkan pasien fiktif ke berbagai dokter atau menggunakan rekam medis yang terlihat terisolasi secara topologis agar tidak memicu alarm sistem berbasis aturan (*rule-based*) atau analisis derajat node (*node degree*).

## Arsitektur Pipeline 5 Tahap

```
[SATUSEHAT FHIR R4 Ingestion]
             │
             ▼
[3-Channel Graph Construction]
 ├── Saluran 1: Topologi (Adjacency Historis)
 ├── Saluran 2: Fitur (Cosine Similarity Atribut)
 └── Saluran 3: Semantik (Metapath Klinis D-Dx-S-RS)
             │
             ▼
[Channel-Specific GCN Layers]
 ├── GCN_Topo(A_topo, H_0)
 ├── GCN_Feat(A_feat, H_0)
 └── GCN_Sem(A_sem, H_0)
             │
             ▼
[Shared-Parameter GCN (Weight Sharing)]
 └── Cross-channel Invariant Representation
             │
             ▼
[Adaptive Attention Fusion & Sigmoid Classification]
 └── Skor Probabilitas Fraud (0.00 - 1.00) + Penjelasan SHAP
```

## Komponen Kunci

### 1. Saluran Graf Topologi ($A_{\text{topo}}$)
Mewakili interaksi langsung dalam transaksi riil: pasien terdaftar mengunjungi dokter, dokter berpraktik di faskes, prosedur ditagihkan oleh faskes. Saluran ini mencerminkan struktur operasional aktual.

### 2. Saluran Graf Fitur ($A_{\text{feat}}$)
Dibangun menggunakan matriks kedekatan kosinus (*Cosine Adjacency*) antar entitas berdasarkan vektor fitur intrinsik numerik dan kategorial:
$$S_{ij} = \frac{x_i \cdot x_j}{\|x_i\| \|x_j\|}$$
Edge dibentuk jika nilai kemiripan melampaui ambang batas tertentu $\epsilon$. Saluran ini menghubungkan entitas yang memiliki pola perilaku medis serupa meski tidak terhubung langsung dalam riwayat klaim.

### 3. Saluran Graf Semantik ($A_{\text{sem}}$)
Menggunakan skema metapath terpandu domain medis, seperti skema $\mathcal{M} = \text{Dokter} \xrightarrow{\text{merawat}} \text{Diagnosis} \xrightarrow{\text{memerlukan}} \text{Tindakan} \xrightarrow{\text{dilakukan di}} \text{Faskes}$. Saluran ini menangkap anomali klinis semantik seperti ketidakwajaran tindakan mahal untuk diagnosis ringan.

### 4. Attention Fusion Mechanism
Setiap saluran menghasilkan representasi node $Z_c \in \mathbb{R}^{N \times d}$. Modul atensi menghitung bobot kepentingan dinamis $\alpha_c$ untuk setiap saluran $c$:
$$Z = \sum_{c \in \{\text{topo}, \text{feat}, \text{sem}\}} \alpha_c Z_c$$
Hasil fusi kemudian diproyeksikan melalui MLP dengan aktivasi Sigmoid untuk menghasilkan probabilitas fraud akhir.

## Kode Terkait

- `src/components/mhgsl/architecture.tsx` - Komponen visualisasi 5 tahapan pipeline.
- `src/components/mhgsl/math-formulas.tsx` - Implementasi penampil rumus matematis dan LaTeX interaktif.
- `src/components/mhgsl/data.ts:167` - Definisi metadata pipeline dan matriks scoring.
