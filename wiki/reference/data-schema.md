---
title: Data Schema & Entity Specifications
type: reference
tags: [schema, entities, prisma, typescript, fhir, nodes, edges]
related:
  - "[[overview]]"
  - "[[concepts/multi-channel-graphs]]"
sources:
  - src/components/mhgsl/data.ts
  - prisma/schema.prisma
---

# Spesifikasi Skema Data & Kontrak Entitas

## 1. Definisi Tipe TypeScript (Client Data Model)

Sumber: `src/components/mhgsl/data.ts`

### Tipe Node dan Level Risiko
```typescript
export type NodeType = "patient" | "doctor" | "faskes" | "procedure" | "diagnosis";
export type RiskLevel = "low" | "medium" | "high" | "fraud";
```

### Antarmuka Node Graf Heterogen
```typescript
export interface GraphNode {
  id: string;              // Pengenal unik (misal: "p1", "d1", "rs_a")
  type: NodeType;          // Kategori entitas graf
  label: string;           // Label tampilan di kanvas (misal: "P₁", "D₁")
  x: number;               // Koordinat X kanvas SVG (viewBox 700x460)
  y: number;               // Koordinat Y kanvas SVG
  risk?: RiskLevel;        // Label klasifikasi risiko
  note?: string;           // Informasi klinis / catatan audit ringkas
  profileId?: string;      // ID profil investigasi detail (jika tersedia)
}
```

### Antarmuka Edge Multi-Saluran
```typescript
export interface GraphEdge {
  from: string;                                    // ID node asal
  to: string;                                      // ID node tujuan
  kind: "topology" | "feature" | "semantic";       // Saluran graf
  weight?: number;                                 // Bobot kemiripan atau keterkaitan
  dashed?: boolean;                                // Gaya visual garis pada UI
}
```

### Antarmuka Profil Investigasi Lengkap
```typescript
export interface FraudProfile {
  id: string;
  name: string;
  role: string;
  type: NodeType;
  riskScore: number;           // Rentang 0.00 - 1.00
  summary: string;
  evidence: Array<{
    channel: "topology" | "feature" | "semantic";
    metric: string;
    value: string;
    impact: "positive" | "negative";
  }>;
  timeline: Array<{
    date: string;
    event: string;
    flag: boolean;
  }>;
  metrics: Array<{
    label: string;
    value: string;
    badge?: string;
  }>;
  recommendedAction: string;
}
```

## 2. Pemetaan Kode Klinis Standar

- **ICD-10**: Kodifikasi Diagnosis Utama dan Sekunder (Kemenkes RI).
- **ICD-9-CM**: Kodifikasi Prosedur Medis dan Pembedahan.
- **INA-CBG**: Indonesian Case Base Groups, sistem tarif paket layanan berbasis tarif acuan nasional.
- **FHIR R4**: Format pertukaran data standar SATUSEHAT (Resource: `Claim`, `Encounter`, `Condition`, `Procedure`, `Practitioner`, `Organization`).
