---
title: Custom Data Scoring Guide
type: guide
tags: [uploader, csv, json, scoring, client-side, inference]
related:
  - "[[overview]]"
  - "[[concepts/mhgsl-architecture]]"
  - "[[reference/data-schema]]"
sources:
  - src/components/mhgsl/data-uploader.tsx
---

# Panduan Evaluasi & Scoring Data Klaim Pengguna

## Gambaran Fitur Data Uploader

Aegis-JKN menyertakan mesin inferensi lokal di dalam peramban (`src/components/mhgsl/data-uploader.tsx`) yang memungkinkan tim verifikator BPJS Kesehatan untuk mengunggah dataset klaim baru dalam format CSV atau JSON dan langsung memperoleh estimasi skor risiko MHGSL.

## Cara Mengakses Uploader

1. Pada halaman beranda, navigasi ke bagian **Komparasi Model & Metrik**.
2. Klik tombol **"Bandingkan Data" / "Compare Data"**.
3. Dialog modal uploader akan terbuka.

## Format Data yang Didukung

### Format CSV
Kolom wajib yang harus disertakan dalam file CSV:
```csv
claimId,patientId,doctorId,faskesId,los,cost,age,diagnosis,procedure
CLM-001,P01,D01,RS01,3,15000000,42,Dx-Ringan,S-Mahal
CLM-002,P02,D01,RS01,3,14800000,39,Dx-Ringan,S-Mahal
CLM-003,P03,D02,RS01,3,15200000,45,Dx-Ringan,S-Mahal
CLM-004,P04,D03,RS02,1,1200000,28,Dx-Ringan,S-Standar
```

### Format JSON
Array of objects dengan kunci yang sama:
```json
[
  {
    "claimId": "CLM-001",
    "patientId": "P01",
    "doctorId": "D01",
    "faskesId": "RS01",
    "los": 3,
    "cost": 15000000,
    "age": 42,
    "diagnosis": "Dx-Ringan",
    "procedure": "S-Mahal"
  }
]
```

## Algoritma Scoring di Peramban
Mesin `scoreRows` mengevaluasi setiap baris klaim:
1. **Skor Topologi ($S_{\text{topo}}$)**: Konsentrasi dokter dan faskes dalam dataset.
2. **Skor Fitur ($S_{\text{feat}}$)**: Rata-rata kemiripan kosinus dari vektor terstandarisasi $[\text{LOS}, \text{usia}, \text{biaya}]$.
3. **Skor Semantik ($S_{\text{sem}}$)**: Heuristik ketidaksesuaian diagnosis vs prosedur (misal: diagnosis ringan + tindakan mahal $= 0.9$).
4. **Skor Fusi Akhir**:
   $$\text{Fusion} = 0.38 \cdot S_{\text{feat}} + 0.41 \cdot S_{\text{sem}} - 0.12 \cdot S_{\text{topo}} + 0.30$$

Klaim dengan skor $\ge 0.75$ diberi label **High Risk (Merah)**, $0.50 - 0.74$ **Medium Risk (Kuning)**, dan $< 0.50$ **Low Risk (Hijau)**.
