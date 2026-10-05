# Aegis-JKN Data Contracts & API Specifications

### Schema Definitions, Graph Models, and Scoring Matrix Contracts

---

## 1. Overview & Data Architecture

Dokumentasi ini mendefinisikan kontrak data formal (*data contracts*) yang mengatur pertukaran informasi pada Aegis-JKN:
- **Ingestion Schema**: Format berkas CSV dan payload JSON untuk berkas klaim raw pelayanan kesehatan.
- **Graph Structural Models**: Definisi antarmuka TypeScript untuk simpul (*nodes*), sisi (*edges*), dan properti kanal graf heterogen.
- **Audit Entity Profile Contract**: Model data untuk modal investigasi forensik sindikat kolusi.
- **Scoring Weight Matrices**: Bobot parameter fusi multi-kanal dan formula kalibrasi risiko.
- **REST API Endpoints**: Spesifikasi antarmuka pemrograman aplikasi berbasis Next.js App Router (`/api`).

---

## 2. Claim Data Contracts (CSV & JSON)

### 2.1. Standard CSV Header Specification
Setiap berkas CSV yang diunggah ke sistem atau dipertukarkan antar-layanan wajib menyertakan kolom-kolom berikut:

| Kolom Header | Tipe Data | Wajib | Rentang / Nilai Contoh | Keterangan |
|---|---|---|---|---|
| `patient_id` | `string` | Ya | `P001`, `JKN-002931` | Token anonim identitas pasien (UU PDP) |
| `doctor_id` | `string` | Ya | `D01`, `DR-78190` | Nomor registrasi dokter penanggung jawab (DPJP) |
| `faskes` | `string` | Ya | `RS_A`, `FKRTL-317101` | Kode fasilitas kesehatan tingkat lanjut rujukan |
| `procedure` | `string` | Ya | `S_mahal`, `01.24` | Nama tindakan medis atau kode ICD-9-CM |
| `diagnosis` | `string` | Ya | `Dx_ringan`, `J03.9` | Nama diagnosis primer atau kode ICD-10 |
| `los` | `number` | Ya | `1` hingga `60` | Length of Stay (lama rawat inap dalam hari) |
| `cost` | `number` | Ya | `100000` hingga `500000000` | Nilai total klaim diajukan (dalam Rupiah) |
| `age` | `number` | Ya | `0` hingga `120` | Usia pasien pada saat pelayanan |

#### Contoh Baris CSV Standar:
```csv
patient_id,doctor_id,faskes,procedure,diagnosis,los,cost,age
P001,D01,RS_A,S_mahal,Dx_ringan,3,42000000,42
P002,D01,RS_A,S_mahal,Dx_ringan,3,41500000,39
P003,D02,RS_A,S_mahal,Dx_ringan,3,41800000,45
P004,D03,RS_B,S_std,Dx_normal,2,3500000,28
```

### 2.2. JSON Schema for Ingestion Payload
Kontrak JSON schema untuk payload pengiriman klaim batch via REST API:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ClaimIngestionPayload",
  "type": "object",
  "required": ["claims"],
  "properties": {
    "batch_id": {
      "type": "string",
      "format": "uuid"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "claims": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "patient_id",
          "doctor_id",
          "faskes",
          "procedure",
          "diagnosis",
          "los",
          "cost",
          "age"
        ],
        "properties": {
          "patient_id": { "type": "string", "minLength": 1 },
          "doctor_id": { "type": "string", "minLength": 1 },
          "faskes": { "type": "string", "minLength": 1 },
          "procedure": { "type": "string", "minLength": 1 },
          "diagnosis": { "type": "string", "minLength": 1 },
          "los": { "type": "number", "minimum": 0 },
          "cost": { "type": "number", "minimum": 0 },
          "age": { "type": "number", "minimum": 0, "maximum": 150 }
        }
      }
    }
  }
}
```

---

## 3. Graph Node & Edge Models (TypeScript Interfaces)

Model data internal aplikasi yang digunakan oleh kanvas visualisasi dan engine inferensi:

```typescript
// Tipe Entitas Simpul Heterogen
export type NodeType = "patient" | "doctor" | "faskes" | "procedure" | "diagnosis";

// Tingkat Klasifikasi Risiko
export type RiskLevel = "low" | "medium" | "high" | "fraud";

// Definisi Simpul Graf (Node)
export interface GraphNode {
  id: string;             // Identifier unik simpul (misal: "p1", "d1", "rs")
  type: NodeType;         // Kategori entitas
  label: string;          // Label singkatan yang dirender di kanvas (misal: "P₁", "D₁")
  x: number;              // Koordinat X pada sistem kanvas viewBox (0..700 / 0..800)
  y: number;              // Koordinat Y pada sistem kanvas viewBox (0..420 / 0..460)
  risk?: RiskLevel;       // Estimasi tingkat keparahan risiko
  note?: string;          // Keterangan klinis atau diagnostik tambahan
  profileId?: string;     // Relasi kunci asing ke profil audit forensik
}

// Tipe Saluran Kanal Graf
export type ChannelKind = "topology" | "feature" | "semantic";

// Definisi Sisi Graf (Edge)
export interface GraphEdge {
  from: string;           // ID simpul asal
  to: string;             // ID simpul tujuan
  kind: ChannelKind;      // Saluran graf yang memiliki relasi ini
  weight?: number;        // Bobot relasi (0.00 s/d 1.00)
  dashed?: boolean;       // Rendering garis putus-putus untuk relasi laten
}
```

---

## 4. Scored Claim Output Contract

Format hasil penilaian evaluasi yang dipancarkan setelah inferensi multi-kanal selesai:

```typescript
export interface ScoredClaimOutput {
  patient_id: string;
  doctor_id: string;
  faskes: string;
  procedure: string;
  diagnosis: string;
  los: number;
  cost: number;
  age: number;
  
  // MHGSL Per-Channel Scores (0.00 - 1.00)
  topologyScore: number;  // Skor konsentrasi rujukan fisik
  featureScore: number;   // Skor kemiripan atribut kosinus terhadap klaster anomali
  semanticScore: number;  // Skor deviasi metapath diagnosis vs tindakan

  // Fusion & Classification Result
  fusionScore: number;    // Probabilitas akhir kecurangan (0.00 - 1.00)
  riskLabel: RiskLevel;   // "low" | "medium" | "high" | "fraud"
  
  // Audit Signature
  camouflageDetected: boolean; // True jika topologyScore rendah tetapi feature/semantic tinggi
}
```

---

## 5. Audit Entity Profile Contract

Kontrak data untuk modal investigasi mendalam (*Drilldown Modal*):

```typescript
export interface FraudEvidenceItem {
  source: "topology" | "feature" | "semantic";
  text: string;           // Deskripsi temuan forensik
  weight: number;         // Bobot pembuktian matematis (0.00 - 1.00)
}

export interface IncidentTimelineEvent {
  date: string;           // Format ISO Date: YYYY-MM-DD
  event: string;          // Kronologi peristiwa klaim anomali
}

export interface ForensicMetricItem {
  label: string;          // Nama metrik pemeriksaan
  value: string;          // Nilai terukur
  flag?: boolean;         // Indikator peringatan merah (anomali)
}

export interface FraudEntityProfile {
  id: string;             // Identifier entitas (misal: "d1", "rs", "p1")
  label: string;          // Nama publik entitas (misal: "D₁ · Dr. A. Wijaya")
  type: NodeType;
  role: "Pasien" | "Dokter" | "Faskes" | "Prosedur" | "Diagnosis";
  riskScore: number;      // Skor probabilitas gabungan (0.00 - 1.00)
  riskLevel: RiskLevel;
  summary: string;        // Ringkasan temuan investigasi forensik
  evidence: FraudEvidenceItem[];
  timeline: IncidentTimelineEvent[];
  metrics: ForensicMetricItem[];
  recommendedAction: string; // Instruksi tindakan verifikator/auditor P2PK
}
```

---

## 6. Scoring Weights & Fusion Matrix Configuration

Tabel berikut mendefinisikan matriks bobot yang digunakan oleh mesin fusi MHGSL pada rilis `v0.2.1`:

| Parameter | Simbol | Nilai Default | Rasionalisasi & Perilaku |
|---|---|---|---|
| **Feature Weight** | $W_{feat}$ | $+0.38$ | Memberikan penalti tinggi pada kesamaan atribut abnormal (LOS, tarif klaster) |
| **Semantic Weight** | $W_{sem}$ | $+0.41$ | Bobot tertinggi; membongkar ketidaksesuaian kode diagnosis vs tindakan |
| **Topology Weight** | $W_{top}$ | $-0.12$ | **Bobot Negatif**: Mengompensasi kamuflase rujukan fisik yang direkayasa |
| **Base Offset** | $b_0$ | $+0.30$ | Kalibrasi probabilitas dasar populasi klaim rawat inap |
| **Feature Threshold** | $\theta_{feat}$ | $0.75$ | Batas minimum kemiripan kosinus untuk membentuk tepi saluran fitur |
| **High Risk Bound** | $\tau_{high}$ | $0.65$ | Batas ambang eskalasi ke pemeriksaan berkas manual |
| **Fraud Confirmed Bound**| $\tau_{fraud}$ | $0.85$ | Batas ambang rekomendasi penolakan / audit khusus P2PK |

### Persamaan Fusi Evaluator:
$$
\text{FusionScore} = \max\left(0, \min\left(1, S_{feat} \times 0.38 + S_{sem} \times 0.41 + S_{top} \times (-0.12) + 0.30\right)\right)
$$

---

## 7. REST API Endpoints Specification

### 7.1. Health & Metadata Endpoint
- **URL**: `/api`
- **Method**: `GET`
- **Deskripsi**: Memeriksa status kesehatan server dan versi build aplikasi.
- **Respons (200 OK)**:
```json
{
  "status": "online",
  "service": "aegis-jkn-mhgsl-intelligence",
  "version": "0.2.1",
  "timestamp": "2026-10-05T15:30:00.000Z"
}
```

### 7.2. Batch Scoring Endpoint
- **URL**: `/api`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**: Sesuai dengan skema `ClaimIngestionPayload` di Seksi 2.2.
- **Respons (200 OK)**:
```json
{
  "batch_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "total_claims": 6,
  "flagged_fraud": 3,
  "flagged_high_risk": 0,
  "scored_claims": [
    {
      "patient_id": "P001",
      "doctor_id": "D01",
      "faskes": "RS_A",
      "topologyScore": 1.0,
      "featureScore": 0.82,
      "semanticScore": 0.90,
      "fusionScore": 0.88,
      "riskLabel": "fraud",
      "camouflageDetected": true
    }
  ]
}
```
