# Aegis-JKN System Architecture & Design

### Technical Specification & Component Hierarchy

---

## 1. Architectural Vision & Operational Context

Aegis-JKN dirancang sebagai sistem pendukung keputusan (*Clinical Decision Support System - CDSS*) bagi verifikator klaim dan auditor P2PK (Pencegahan dan Penanganan Kecurangan) di lingkungan BPJS Kesehatan. Sistem ini menjembatani kesenjangan skala antara volume klaim harian yang masif (>2.000.000 klaim) dengan keterbatasan tenaga manusia (~1.000 verifikator manual).

Arsitektur sistem dibangun di atas prinsip **Hybrid Intelligence**:
1. **Automated Structural Learning**: MHGSL memproses miliaran relasi antar-entitas untuk menyaring dan memberikan skor anomali.
2. **Explainable AI (XAI)**: Atribusi SHAP (*SHapley Additive exPlanations*) mendekomposisi risiko ke setiap kanal graf dan atribut klinis.
3. **Human-in-the-Loop (HITL)**: Keputusan akhir terkait penolakan klaim atau audit lapangan tetap berada di tangan verifikator berwenang.

---

## 2. End-to-End Data Flow: From FHIR to Multi-Channel Graph

```
+---------------------------------------------------------------------------------------+
| SATUSEHAT Ecosystem / RS SIMRS / BPJS V-Claim API                                    |
+---------------------------------------------------------------------------------------+
    |               |                       |                     |
    | Encounter     | Condition (ICD-10)    | Procedure (ICD-9)   | MedicationRequest
    v               v                       v                     v
+---------------------------------------------------------------------------------------+
| FHIR Ingestion & Normalization Worker (ETL Engine)                                    |
| - JSON Extraction & Schema Validation                                                 |
| - Privacy Tokenization: NIK / No. JKN -> Anonymized Hash (UU PDP No. 27/2022)         |
| - Entity Disambiguation: Dokter (SIP), RS (Kode Faskes), Diagnosis (ICD), Proc (ICD)  |
+---------------------------------------------------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
| Heterogeneous Graph Builder                                                           |
| Nodes: V = {V_patient, V_doctor, V_faskes, V_procedure, V_diagnosis}                 |
| Features: X = [LOS, Normalized_Cost, Age_Group, Tariff_Deviation, Charlson_Index]     |
+---------------------------------------------------------------------------------------+
            |                               |                              |
            v                               v                              v
+------------------------+      +-----------------------+     +-------------------------+
| Channel 1: Topology    |      | Channel 2: Feature     |     | Channel 3: Semantic     |
| A(top)                 |      | A(feat)               |     | A(sem)                  |
| Physical referrals     |      | Cosine similarity     |     | Metapath patterns       |
| & clinical encounters  |      | thresholding          |     | D -> Dx -> S -> RS      |
+------------------------+      +-----------------------+     +-------------------------+
            |                               |                              |
            +-------------------------------+------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
| GCN Neural Representation Engine                                                      |
| - Parallel Channel-Specific GCN Layers: W(top), W(feat), W(sem)                       |
| - Inter-Channel Shared-Parameter GCN Layer: W(shared)                                 |
+---------------------------------------------------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
| Attention-Based Fusion & Multi-Head Classification Layer                              |
| - Concatenation: H(final) = Concat( H(top), H(feat), H(sem), H(shared) )              |
| - Risk Scoring: y_hat = Sigmoid( H(final) * W_cls + b )                               |
| - Explainer Engine: Per-Channel SHAP Attribution                                      |
+---------------------------------------------------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
| Interactive Audit Presentation Layer (Next.js 16 Client & Verifier UI)                |
+---------------------------------------------------------------------------------------+
```

### Pemetaan Spesifikasi SATUSEHAT HL7 FHIR R4
Sistem mengonsumsi standar interoperabilitas kesehatan nasional yang mencakup 5 *FHIR Resources*:
1. **Encounter**:
   - `Encounter.subject`: Dipetakan menjadi simpul Pasien ($P$).
   - `Encounter.participant.individual`: Dipetakan menjadi simpul Dokter ($D$).
   - `Encounter.serviceProvider`: Dipetakan menjadi simpul Faskes ($RS$).
   - `Encounter.period`: Diekstrak untuk menghitung *Length of Stay* (LOS) dalam hari.
2. **Condition**:
   - `Condition.code.coding`: Dipetakan menjadi simpul Diagnosis ($Dx$) berbasis kode ICD-10.
   - `Condition.rank`: Menentukan diagnosis primer versus diagnosis sekunder/komorbiditas.
3. **Procedure**:
   - `Procedure.code.coding`: Dipetakan menjadi simpul Prosedur/Tindakan ($S$) berbasis kode ICD-9-CM.
   - `Procedure.performedDateTime`: Menentukan kronologi tindakan bedah atau diagnostik.
4. **MedicationRequest**:
   - `MedicationRequest.medicationCodeableConcept`: Dievaluasi untuk mendeteksi *drug diversion* dan duplikasi terapi obat kronis.
5. **Coverage / Claim (V-Claim)**:
   - `Claim.item.revenue` & `Claim.total`: Memetakan besaran rupiah klaim tarif INA-CBG yang diajukan.

---

## 3. The 5-Stage MHGSL Pipeline Breakdown

### Stage 1: Ingestion & Privacy-Preserving Tokenization
- Mengonsumsi aliran data klaim baik secara batch (rekonsiliasi harian) maupun streaming melalui antarmuka REST API.
- Menjamin kepatuhan terhadap **Undang-Undang Perlindungan Data Pribadi (UU PDP No. 27/2022)** dengan menerapkan enkripsi satu arah (*salted SHA-256 tokenization*) pada nomor identitas kependudukan (NIK) dan nomor kepesertaan BPJS sebelum pembentukan graf.

### Stage 2: Multi-Channel Graph Construction
Graf heterogen didefinisikan sebagai $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{T}_v, \mathcal{T}_e)$ dengan $\mathcal{T}_v = \{Pasien, Dokter, Faskes, Prosedur, Diagnosis\}$. Tiga kanal relasi dikonstruksi secara simultan:
1. **Topology Graph ($A^{(top)}$)**:
   Relasi rujukan operasional:
   - Tepi $(P_i, D_j) \in \mathcal{E}^{(top)}$ jika dokter $j$ memeriksa pasien $i$.
   - Tepi $(D_j, RS_k) \in \mathcal{E}^{(top)}$ jika dokter $j$ berpraktik di fasilitas kesehatan $k$.
   - Tepi $(RS_k, S_m) \in \mathcal{E}^{(top)}$ jika fasilitas $k$ menagihkan prosedur $m$.
2. **Feature Graph ($A^{(feat)}$)**:
   Membangun tepi sintetis antar-simpul bertipe sejenis yang memiliki kemiripan profil atribut di atas threshold $\theta_{feat} = 0.75$:
   - Menghubungkan pasien yang memiliki kesamaan LOS, rentang usia, dan pola biaya INA-CBG.
   - Mengungkap sindikat kloning rekam medis meskipun rujukan fisik sengaja disebarkan ke dokter berbeda.
3. **Semantic Graph ($A^{(sem)}$)**:
   Memproyeksikan graf melalui skema metapath tingkat tinggi $\mathcal{M} = D \to Dx \to S \to RS$.
   - Menghubungkan dokter dengan diagnosis dan tindakan spesifik untuk mengukur ko-okurensi anomali.
   - Membongkar pola di mana dokter tertentu memiliki rasio tidak rasional dalam memasangkan diagnosis ringan dengan tindakan bedah invasif.

### Stage 3: Channel-Specific Graph Convolutional Network (GCN)
Setiap kanal memiliki matriks bobot yang dapat dilatih secara independen ($W^{(k)}$) untuk mempelajari struktur relasi lokal:

$$
\mathbf{H}^{(top)} = \text{ReLU}\left( \tilde{\mathbf{D}}_{top}^{-\frac{1}{2}} \tilde{\mathbf{A}}^{(top)} \tilde{\mathbf{D}}_{top}^{-\frac{1}{2}} \mathbf{X} \mathbf{W}^{(top)} \right)
$$

$$
\mathbf{H}^{(feat)} = \text{ReLU}\left( \tilde{\mathbf{D}}_{feat}^{-\frac{1}{2}} \tilde{\mathbf{A}}^{(feat)} \tilde{\mathbf{D}}_{feat}^{-\frac{1}{2}} \mathbf{X} \mathbf{W}^{(feat)} \right)
$$

$$
\mathbf{H}^{(sem)} = \text{ReLU}\left( \tilde{\mathbf{D}}_{sem}^{-\frac{1}{2}} \tilde{\mathbf{A}}^{(sem)} \tilde{\mathbf{D}}_{sem}^{-\frac{1}{2}} \mathbf{X} \mathbf{W}^{(sem)} \right)
$$

### Stage 4: Cross-Channel Shared-Parameter GCN
Untuk mencegah *overfitting* pada kanal tertentu dan mengekstraksi invariant structural representations, lapisan konvolusi kedua menggunakan matriks parameter bersama $W^{(shared)}$:

$$
\mathbf{H}^{(shared,\, k)} = \text{ReLU}\left( \tilde{\mathbf{D}}_{k}^{-\frac{1}{2}} \tilde{\mathbf{A}}^{(k)} \tilde{\mathbf{D}}_{k}^{-\frac{1}{2}} \mathbf{X} \mathbf{W}^{(shared)} \right)
$$

Representasi bersama ini diagregasikan:

$$
\mathbf{H}^{(shared)} = \frac{1}{3} \sum_{k \in \{top, feat, sem\}} \mathbf{H}^{(shared,\, k)}
$$

### Stage 5: Multi-Channel Attention Fusion & SHAP Explainability
Representasi laten digabungkan melalui konkatenasi dan diproyeksikan ke classifier:

$$
\mathbf{H}^{(final)} = \left[ \mathbf{H}^{(top)} \,\|\, \mathbf{H}^{(feat)} \,\|\, \mathbf{H}^{(sem)} \,\|\, \mathbf{H}^{(shared)} \right]
$$

$$
\hat{y} = \text{Sigmoid}\left( \mathbf{H}^{(final)} \mathbf{W}_{cls} + \mathbf{b} \right)
$$

Model SHAP kemudian mengurai $\hat{y}$ menjadi kontribusi aditif:

$$
\hat{y}_i = \phi_0 + \phi_i^{(top)} + \phi_i^{(feat)} + \phi_i^{(sem)} + \sum_{m} \phi_i^{(feature\_m)}
$$

Ketika $\phi_i^{(top)} < 0$ sementara $\phi_i^{(feat)} \gg 0$ dan $\phi_i^{(sem)} \gg 0$, sistem memicu tanda bahaya **Topological Camouflage Signature**.

---

## 4. Frontend Component Hierarchy & State Architecture

Aplikasi antarmuka verifikator dibangun menggunakan Next.js 16 App Router dengan arsitektur reaktif:

```
src/app/layout.tsx (Root Layout)
│
├── ThemeProvider (next-themes: Dark / Light Mode)
│
└── src/app/page.tsx (Single Page Interactive Console)
    │
    ├── Navbar (Sticky Brand, Navigation Anchors, Language & Theme Toggles)
    │
    ├── Hero (Interactive Title, Live Claim Counters, Value Metrics)
    │
    ├── ProblemSection (BPJS Workload 2M:1K, 3 Fraud Pillars: Faskes/Peserta/Badan Usaha)
    │
    ├── Architecture (5-Stage Pipeline, SATUSEHAT Data Sources, Privacy Compliance)
    │
    ├── MultiChannelGraph (Interactive Graph Canvas, Channel Switcher, Node Tooltip)
    │
    ├── Simulation (4-Step Upcoding Scenario, Progressive Radar/Bar, SHAP Decomposition)
    │
    ├── MathFormulas (Interactive Mathematical Formulation Explorer with LaTeX Display)
    │
    ├── Comparison (AUPRC Benchmark Bars, Radar Chart 5-Metric, Evaluation Matrix)
    │
    ├── FraudRing (Syndicate Graph, Message-Passing Animation, Dense Halo Toggle)
    │   └── FraudDrilldownModal (Deep Audit Modal: Doctor / Hospital / Patient Profiles)
    │
    ├── Roadmap (Implementation Horizons, ROI Metrics, HITL Cost Savings)
    │
    ├── DataUploader (Dialog: Custom CSV/JSON Scoring Engine, Client-side MHGSL Inference)
    │
    ├── Footer (Compliance Badges, Documentation Anchors, Disclaimer)
    │
    └── BackToTop (Smooth Scroll Controller)
```

---

## 5. Security & Regulatory Compliance

1. **Undang-Undang Perlindungan Data Pribadi (UU PDP No. 27/2022)**:
   - Data rekam medis sensitif tidak pernah meninggalkan perimeter server BPJS Kesehatan.
   - PII (*Personally Identifiable Information*) diubah menjadi token kriptografis sebelum proses graph embedding.
2. **Kepatuhan Standar HL7 FHIR R4 & Kementerian Kesehatan**:
   - Struktur entitas graf sepenuhnya selaras dengan ontologi data interoperabilitas SATUSEHAT.
3. **Audit Trail Immutability**:
   - Seluruh hasil inferensi model dan rekomendasi tindakan verifikator disimpan dalam log audit terstruktur untuk verifikasi pasca-klaim.
