// Centralized data for the MHGSL/GNN fraud-detection visualization demo.
// All data here is illustrative/synthetic for educational visualization.

export type NodeType = "patient" | "doctor" | "faskes" | "procedure" | "diagnosis";
export type RiskLevel = "low" | "medium" | "high" | "fraud";

export const NODE_TYPE_META: Record<
  NodeType,
  { label: string; color: string; ring: string; icon: string }
> = {
  patient: { label: "Pasien", color: "oklch(0.55 0.14 165)", ring: "oklch(0.55 0.14 165 / 0.25)", icon: "User" },
  doctor: { label: "Dokter", color: "oklch(0.62 0.13 200)", ring: "oklch(0.62 0.13 200 / 0.25)", icon: "Stethoscope" },
  faskes: { label: "Faskes", color: "oklch(0.7 0.16 70)", ring: "oklch(0.7 0.16 70 / 0.25)", icon: "Hospital" },
  procedure: { label: "Prosedur", color: "oklch(0.62 0.22 20)", ring: "oklch(0.62 0.22 20 / 0.25)", icon: "Syringe" },
  diagnosis: { label: "Diagnosis", color: "oklch(0.5 0.13 280)", ring: "oklch(0.5 0.13 280 / 0.25)", icon: "ClipboardList" },
};

// ----- Hero stats -----
export const HERO_STATS = [
  { value: "2.000.000+", numericValue: 2000000, prefix: "", suffix: "+", label: "Klaim harian diproses sistem BPJS", accent: "primary" },
  { value: "±1.000", numericValue: 1000, prefix: "±", suffix: "", label: "Verifikator manual yang tersedia", accent: "rose" },
  { value: "3", numericValue: 3, prefix: "", suffix: "", label: "Saluran graf heterogen MHGSL", accent: "amber" },
  { value: "+20%", numericValue: 20, prefix: "+", suffix: "%", label: "Lonjakan AUPRC pada arsitektur hibrida", accent: "teal" },
];

// ----- Risk taxonomy -----
export const RISK_PILLARS = [
  {
    id: "faskes",
    title: "Risiko Fasilitas Kesehatan",
    subtitle: "Area dengan potensi kebocoran finansial terbesar",
    icon: "Hospital",
    accent: "rose",
    modus: ["Phantom Billing", "Upcoding", "Unbundling", "Prolonged Stay", "Cloning Rekam Medis"],
    approach:
      "Analisis anomali frekuensi kunjungan pasien, deteksi inkonsistensi diagnosis (ICD-10) vs tindakan (ICD-9-CM), serta pemodelan jaringan dokter–pasien.",
    focus: true,
  },
  {
    id: "peserta",
    title: "Risiko Peserta JKN",
    subtitle: "Manipulasi identitas & penyalahgunaan hak layanan",
    icon: "User",
    accent: "amber",
    modus: [
      "Peminjaman kartu kepesertaan",
      "Kolusi surat keterangan sakit fiktif",
      "Drug diversion (penumpukan obat)",
    ],
    approach:
      "Autentikasi biometrik, analisis pola pergerakan geografis klaim, dan clustering pengambilan obat kronis yang melebihi dosis rasional.",
    focus: false,
  },
  {
    id: "pemberi-kerja",
    title: "Risiko Pemberi Kerja",
    subtitle: "Manipulasi administratif korporasi",
    icon: "Building2",
    accent: "teal",
    modus: ["Under-reporting upah", "Penahanan setoran iuran", "Misklasifikasi hubungan kerja"],
    approach:
      "Ekstraksi dokumen penggajian (OCR/NLP), pemodelan silang data perpajakan, dan deteksi anomali tren pembayaran iuran bulanan.",
    focus: false,
  },
];

// ----- MHGSL multi-channel graph definition -----
export interface GraphNode {
  id: string;
  type: NodeType;
  label: string;
  x: number;
  y: number;
  risk?: RiskLevel;
  note?: string;
}

export interface GraphEdge {
  from: string;
  to: string;
  kind: "topology" | "feature" | "semantic";
  weight?: number;
  dashed?: boolean;
}

// Layout: 700x460 viewBox
export const MHGSL_NODES: GraphNode[] = [
  // Patients
  { id: "p1", type: "patient", label: "P₁", x: 110, y: 90, risk: "fraud", note: "LOS 3 hari · usia 42" },
  { id: "p2", type: "patient", label: "P₂", x: 110, y: 230, risk: "fraud", note: "LOS 3 hari · usia 39" },
  { id: "p3", type: "patient", label: "P₃", x: 110, y: 370, risk: "fraud", note: "LOS 3 hari · usia 45" },
  { id: "p4", type: "patient", label: "P₄", x: 560, y: 100, risk: "low", note: "Klaim normal" },
  { id: "p5", type: "patient", label: "P₅", x: 560, y: 360, risk: "low", note: "Klaim normal" },

  // Doctors (syndicate)
  { id: "d1", type: "doctor", label: "D₁", x: 270, y: 160, risk: "fraud", note: "Upcoding repetitif" },
  { id: "d2", type: "doctor", label: "D₂", x: 270, y: 300, risk: "fraud", note: "Kolusi resep" },
  { id: "d3", type: "doctor", label: "D₃", x: 430, y: 100, risk: "low", note: "Praktik wajar" },

  // Faskes
  { id: "rs", type: "faskes", label: "RS_A", x: 410, y: 230, risk: "high", note: "FKRTL Rujukan" },

  // Procedures
  { id: "sExpensive", type: "procedure", label: "S_mahal", x: 590, y: 230, risk: "fraud", note: "Bedah kompleks · INA-CBG tinggi" },
  { id: "sStd", type: "procedure", label: "S_standar", x: 250, y: 400, risk: "low", note: "Tindakan ringan" },

  // Diagnosis
  { id: "dxMild", type: "diagnosis", label: "Dx ringan", x: 410, y: 400, risk: "fraud", note: "ICD-10 tidak sesuai S_mahal" },
];

export const MHGSL_EDGES: GraphEdge[] = [
  // Topology (real interactions)
  { from: "p1", to: "d1", kind: "topology" },
  { from: "p2", to: "d1", kind: "topology" },
  { from: "p2", to: "d2", kind: "topology" },
  { from: "p3", to: "d2", kind: "topology" },
  { from: "d1", to: "rs", kind: "topology" },
  { from: "d2", to: "rs", kind: "topology" },
  { from: "d3", to: "rs", kind: "topology" },
  { from: "p4", to: "d3", kind: "topology" },
  { from: "p5", to: "d3", kind: "topology" },
  { from: "rs", to: "sExpensive", kind: "topology" },
  { from: "rs", to: "sStd", kind: "topology" },
  { from: "sStd", to: "dxMild", kind: "topology" },

  // Feature (similarity of attributes)
  { from: "p1", to: "p2", kind: "feature", dashed: true, weight: 0.92 },
  { from: "p2", to: "p3", kind: "feature", dashed: true, weight: 0.88 },
  { from: "p1", to: "p3", kind: "feature", dashed: true, weight: 0.85 },
  { from: "d1", to: "d2", kind: "feature", dashed: true, weight: 0.79 },

  // Semantic (metapath Doctor -> Diagnosis -> Procedure -> Faskes)
  { from: "d1", to: "dxMild", kind: "semantic", dashed: true, weight: 0.81 },
  { from: "d2", to: "dxMild", kind: "semantic", dashed: true, weight: 0.83 },
  { from: "dxMild", to: "sExpensive", kind: "semantic", dashed: true, weight: 0.94 },
  { from: "sExpensive", to: "rs", kind: "semantic", dashed: true, weight: 0.71 },
];

// ----- Channel metadata -----
export const CHANNELS = [
  {
    id: "topology",
    title: "Topology Graph",
    sub: "A⁽ᵗᵒᵖ⁾",
    color: "oklch(0.55 0.14 165)",
    description:
      "Struktur jaringan fisik asli antar-entitas. Pasien → Dokter → Faskes → Tindakan. Menangkap rujukan & interaksi operasional langsung.",
    formula: "A_ij ∈ {0,1} dari graf asli G = (V, E)",
  },
  {
    id: "feature",
    title: "Feature Graph",
    sub: "A⁽ᶠᵉᵃᵗ⁾",
    color: "oklch(0.62 0.13 200)",
    description:
      "Kemiripan vektor atribut antar-simpul di ruang fitur (LOS, usia, rasio biaya). Mengungkap pasien/prosedur dengan profil sangat mirip.",
    formula: "A_ij = cos(xᵢ, xⱼ) jika > θ_feat",
  },
  {
    id: "semantic",
    title: "Semantic Graph",
    sub: "A⁽ˢᵉᵐ⁾",
    color: "oklch(0.7 0.16 70)",
    description:
      "Hubungan semantik tingkat tinggi berbasis metapath (Dokter → Diagnosis → Prosedur → Faskes). Menangkap pola perilaku berulang mencurigakan.",
    formula: "A_ij = Sim_ℳ(vᵢ, vⱼ) via metapath ℳ",
  },
];

// ----- Pipeline stages -----
export const PIPELINE = [
  {
    step: "01",
    title: "Ingestasi FHIR",
    subtitle: "SATUSEHAT HL7 FHIR R4 · V-Claim",
    desc: "Encounter, Condition (ICD-10), MedicationRequest, Composition diparse menjadi entitas graf heterogen.",
    icon: "Database",
  },
  {
    step: "02",
    title: "Konstruksi 3 Graf",
    subtitle: "Multi-channel adjacency",
    desc: "Dibangun matriks A⁽ᵗᵒᵖ⁾, A⁽ᶠᵉᵃᵗ⁾, A⁽ˢᵉᵐ⁾ yang merepresentasikan tiga pandangan ekosistem secara paralel.",
    icon: "Share2",
  },
  {
    step: "03",
    title: "Channel-Specific GCN",
    subtitle: "Ekstraksi karakteristik unik",
    desc: "GCN independen W⁽ᵏ⁾ untuk tiap saluran mempelajari pola khas topologi/fitur/semantik.",
    icon: "GitBranch",
  },
  {
    step: "04",
    title: "Shared-Parameter GCN",
    subtitle: "Komonalitas lintas-saluran",
    desc: "W⁽ˢʰᵃʳᵉᵈ⁾ yang sama memaksa ekstraksi representasi umum lintas ketiga graf.",
    icon: "Merge",
  },
  {
    step: "05",
    title: "Fusion & Classifier",
    subtitle: "Skor fraud & SHAP",
    desc: "Embedding digabung lalu diproyeksikan ke Sigmoid menghasilkan probabilitas kecurangan + atribusi SHAP.",
    icon: "ShieldAlert",
  },
];

// ----- Math formulas -----
export const FORMULAS = [
  {
    id: "feat",
    title: "Feature Adjacency (Cosine Similarity)",
    legend: "A⁽ᶠᵉᵃᵗ⁾",
    desc: "Menghubungkan simpul dengan vektor fitur sangat mirip. θ_feat adalah ambang batas kemiripan.",
    latex: "A^{(feat)}_{ij} = \\begin{cases} \\frac{\\mathbf{x}_i \\cdot \\mathbf{x}_j}{\\|\\mathbf{x}_i\\| \\|\\mathbf{x}_j\\|}, & \\text{jika } \\cos(\\mathbf{x}_i, \\mathbf{x}_j) > \\theta_{feat} \\\\ 0, & \\text{lainnya} \\end{cases}",
  },
  {
    id: "gcn",
    title: "Channel-Specific GCN",
    legend: "H⁽ᵏ⁾",
    desc: "Konvolusi graf per saluran k ∈ {top, feat, sem}. Bobot W⁽ᵏ⁾ spesifik per saluran.",
    latex: "\\mathbf{H}^{(k)} = \\sigma \\left( \\tilde{\\mathbf{D}}^{-\\frac{1}{2}}_{(k)} \\tilde{\\mathbf{A}}^{(k)} \\tilde{\\mathbf{D}}^{-\\frac{1}{2}}_{(k)} \\mathbf{X} \\mathbf{W}^{(k)} \\right)",
  },
  {
    id: "shared",
    title: "Shared-Parameter GCN",
    legend: "H⁽ˢʰᵃʳᵉᵈ, ᵏ⁾",
    desc: "W⁽ˢʰᵃʳᵉᵈ⁾ bernilai sama untuk ketiga saluran, memaksa ekstraksi representasi umum.",
    latex: "\\mathbf{H}^{(shared,\\, k)} = \\sigma \\left( \\tilde{\\mathbf{D}}^{-\\frac{1}{2}}_{(k)} \\tilde{\\mathbf{A}}^{(k)} \\tilde{\\mathbf{D}}^{-\\frac{1}{2}}_{(k)} \\mathbf{X} \\mathbf{W}^{(shared)} \\right)",
  },
  {
    id: "fusion",
    title: "Multi-Channel Fusion & Prediction",
    legend: "ŷᵢ",
    desc: "Concat lalu proyeksi linier dengan Sigmoid menghasilkan probabilitas fraud per klaim.",
    latex: "\\mathbf{H}^{(final)} = \\text{Concat}\\!\\left( \\mathbf{H}^{(top)}, \\mathbf{H}^{(feat)}, \\mathbf{H}^{(sem)}, \\mathbf{H}^{(shared)} \\right) \\\\ \\hat{y}_i = \\sigma\\!\\left( \\mathbf{H}^{(final)}_i \\mathbf{W}_{cls} + b \\right)",
  },
];

// ----- Method comparison -----
export const COMPARISON_ROWS = [
  { metric: "Fokus Analisis Data", xgboost: "Atribut baris independen", gnn: "Relasi & topologi", hybrid: "Tabular + spasial graf", mhgsl: "3 saluran (topologi+fitur+semantik)" },
  { metric: "Deteksi Sindikat (Fraud Ring)", xgboost: "Lemah", gnn: "Kuat", hybrid: "Kuat", mhgsl: "Sangat kuat (klaster padat)" },
  { metric: "Penembusan Kamuflase", xgboost: "Rendah", gnn: "Sedang", hybrid: "Tinggi", mhgsl: "Sangat tinggi (lintas-saluran)" },
  { metric: "AUPRC (relatif)", xgboost: "0.71", gnn: "0.78", hybrid: "0.85", mhgsl: "0.91" },
  { metric: "Explainability (SHAP)", xgboost: "Bawaan", gnn: "Terbatas", hybrid: "Bawaan", mhgsl: "Atribusi per-saluran" },
  { metric: "Komputasi", xgboost: "Cepat", gnn: "Sedang", hybrid: "Sedang–Tinggi", mhgsl: "Tinggi" },
];

export const AUPRC_DATA = [
  { method: "Rule-based", auprc: 0.58, color: "oklch(0.6 0.05 0)" },
  { method: "Logistic Reg.", auprc: 0.62, color: "oklch(0.55 0.08 280)" },
  { method: "XGBoost", auprc: 0.71, color: "oklch(0.62 0.13 200)" },
  { method: "GNN", auprc: 0.78, color: "oklch(0.55 0.14 165)" },
  { method: "Hybrid GNN+XGB", auprc: 0.85, color: "oklch(0.5 0.16 70)" },
  { method: "MHGSL", auprc: 0.91, color: "oklch(0.62 0.22 20)" },
];

// Multi-metric benchmark for radar chart (Precision / Recall / F1 / AUPRC / Specificity)
export const RADAR_METRICS = ["Precision", "Recall", "F1-Score", "AUPRC", "Specificity"];

export const RADAR_DATA = [
  {
    method: "XGBoost",
    color: "oklch(0.62 0.13 200)",
    values: { Precision: 0.74, Recall: 0.68, "F1-Score": 0.71, AUPRC: 0.71, Specificity: 0.89 },
  },
  {
    method: "GNN",
    color: "oklch(0.55 0.14 165)",
    values: { Precision: 0.80, Recall: 0.76, "F1-Score": 0.78, AUPRC: 0.78, Specificity: 0.91 },
  },
  {
    method: "Hybrid",
    color: "oklch(0.5 0.16 70)",
    values: { Precision: 0.86, Recall: 0.84, "F1-Score": 0.85, AUPRC: 0.85, Specificity: 0.94 },
  },
  {
    method: "MHGSL",
    color: "oklch(0.62 0.22 20)",
    values: { Precision: 0.92, Recall: 0.90, "F1-Score": 0.91, AUPRC: 0.91, Specificity: 0.96 },
  },
];

// Per-metric detailed comparison (for the metrics table tab)
export const METRIC_DETAIL = [
  { metric: "Precision", xgboost: 0.74, gnn: 0.80, hybrid: 0.86, mhgsl: 0.92, desc: "TP / (TP + FP) — minimasi alarm palsu" },
  { metric: "Recall", xgboost: 0.68, gnn: 0.76, hybrid: 0.84, mhgsl: 0.90, desc: "TP / (TP + FN) — minimasi fraud lolos" },
  { metric: "F1-Score", xgboost: 0.71, gnn: 0.78, hybrid: 0.85, mhgsl: 0.91, desc: "Harmonic mean precision × recall" },
  { metric: "AUPRC", xgboost: 0.71, gnn: 0.78, hybrid: 0.85, mhgsl: 0.91, desc: "Area di bawah kurva Precision-Recall" },
  { metric: "Specificity", xgboost: 0.89, gnn: 0.91, hybrid: 0.94, mhgsl: 0.96, desc: "TN / (TN + FP) — akurasi klaim valid" },
  { metric: "ROC-AUC", xgboost: 0.83, gnn: 0.88, hybrid: 0.92, mhgsl: 0.95, desc: "Area di bawah kurva ROC" },
];

// ----- Simulation steps -----
export const SIM_STEPS = [
  {
    id: 0,
    title: "Klaim masuk",
    desc: "Tiga pasien (P₁, P₂, P₃) dirujuk ke RS_A oleh D₁ & D₂ untuk prosedur S_mahal. Diagnosis primer tercatat sebagai 'Dx ringan'.",
    channel: "topology" as const,
    insight: "Pada graf topologi, jalur P → D → RS → S terlihat sebagai rujukan medis yang valid & wajar.",
    score: 0.32,
  },
  {
    id: 1,
    title: "Analisis graf fitur",
    desc: "Vektor atribut P₁, P₂, P₃ dibandingkan: Length of Stay identik (3 hari), usia berdekatan (39–45), rasio biaya berhimpitan dengan klaster upcoding historis.",
    channel: "feature" as const,
    insight: "Cosine similarity antar P₁–P₂ = 0.92, jauh di atas θ_feat. Muncul simpul padat berisiko tinggi.",
    score: 0.61,
  },
  {
    id: 2,
    title: "Analisis graf semantik",
    desc: "Metapath Dokter → Diagnosis → Prosedur → Faskes menunjukkan D₁ & D₂ secara konsisten memasangkan Dx ringan dengan S_mahal di RS_A untuk kelompok pasien serupa.",
    channel: "semantic" as const,
    insight: "Pola metapath berulang = upcoding terselubung. Kamuflase terdeteksi melalui kesamaan semantik tinggi.",
    score: 0.84,
  },
  {
    id: 3,
    title: "Fusion & klasifikasi",
    desc: "Embedding 3 saluran + shared digabung. Sigmoid menghasilkan skor akhir. SHAP mengatribusi kontribusi tiap saluran & fitur.",
    channel: "fusion" as const,
    insight: "Skor fraud 0.94. Kontribusi: feature graph +38%, semantic graph +41%, topology −12% (kamuflase).",
    score: 0.94,
  },
];

// ----- SHAP attribution -----
export const SHAP_ATTRS = [
  { feature: "Metapath Dx ringan → S_mahal", shap: 0.41, channel: "semantic" as const },
  { feature: "Cosine similarity P₁–P₂ (LOS)", shap: 0.28, channel: "feature" as const },
  { feature: "Frekuensi pasangan D₁–D₂", shap: 0.19, channel: "semantic" as const },
  { feature: "Rasio biaya vs INA-CBG regional", shap: 0.12, channel: "feature" as const },
  { feature: "Topology jalur rujukan (normal)", shap: -0.07, channel: "topology" as const },
];

// Progressive channel contribution per simulation step (grows toward final score)
// stepIdx 0 = topology only (initial), 1 = +feature, 2 = +semantic, 3 = final fusion
export const CHANNEL_PROGRESS = [
  { step: 0, topology: 0.32, feature: 0.0, semantic: 0.0, fusion: 0.32 },
  { step: 1, topology: 0.30, feature: 0.45, semantic: 0.0, fusion: 0.61 },
  { step: 2, topology: 0.28, feature: 0.42, semantic: 0.55, fusion: 0.84 },
  { step: 3, topology: -0.12, feature: 0.38, semantic: 0.41, fusion: 0.94 },
];

// ----- Roadmap phases -----
export const ROADMAP = [
  {
    phase: "Fase 1",
    period: "0–3 bulan",
    title: "Fondasi Data & Baseline",
    items: ["Generator DP-CTGAN (privacy-by-design)", "Baseline XGBoost + SMOTE", "Skema FHIR R4 ingestion"],
    status: "active",
  },
  {
    phase: "Fase 2",
    period: "3–6 bulan",
    title: "XAI & Integrasi",
    items: ["Modul SHAP per-saluran", "Integrasi V-Claim middleware", "UAT dengan verifikator"],
    status: "next",
  },
  {
    phase: "Fase 3",
    period: ">6 bulan",
    title: "Pilot MHGSL & HITL",
    items: ["Pilot project 5 FKRTL", "MHGSL + Active Learning (DPO)", "Federated learning bayangan"],
    status: "future",
  },
];

// ----- ROI -----
export const ROI_STATS = [
  { before: "20 mnt", after: "3 mnt", label: "Telaah per berkas klaim" },
  { before: "1.000", after: "~6.700", label: "Kapasitas verifikator (efektif)" },
  { before: "≤ 3x24 jam", after: "Realtime", label: "Pelaporan kebocoran (UU PDP)" },
  { before: "Manual", after: "XAI + HITL", label: "Mode keputusan akhir" },
];

// ----- Fraud ring drilldown profiles -----
export interface FraudEntityProfile {
  id: string;
  label: string;
  type: NodeType;
  role: "Pasien" | "Dokter" | "Faskes" | "Prosedur" | "Diagnosis";
  riskScore: number;
  riskLevel: RiskLevel;
  summary: string;
  evidence: { source: "topology" | "feature" | "semantic"; text: string; weight: number }[];
  timeline: { date: string; event: string }[];
  metrics: { label: string; value: string; flag?: boolean }[];
  recommendedAction: string;
}

export const FRAUD_PROFILES: FraudEntityProfile[] = [
  {
    id: "d1",
    label: "D₁ · Dr. A. Wijaya",
    type: "doctor",
    role: "Dokter",
    riskScore: 0.96,
    riskLevel: "fraud",
    summary:
      "Spesialis bedah yang terdeteksi memasangkan diagnosis primer ringan (ICD-10 J03.9) dengan prosedur bedah kompleks (ICD-9-CM 01.24) secara berulang pada 14 klaim dalam 30 hari.",
    evidence: [
      { source: "semantic", text: "Metapath D₁ → Dx ringan → S_mahal → RS_A berulang 14× (normal: ≤2×)", weight: 0.41 },
      { source: "feature", text: "Vektor atribut klaim D₁ mirip 0.79 dengan D₂ (kolusi sindikat)", weight: 0.23 },
      { source: "topology", text: "Out-degree 8 pasien → 100% dirujuk ke RS_A (konsentrasi tidak wajar)", weight: 0.18 },
      { source: "feature", text: "Rata-rata biaya klaim 4.2× dari peer dokter bedah regional", weight: 0.14 },
    ],
    timeline: [
      { date: "2026-08-12", event: "Klaim awal S_mahal + Dx ringan #1" },
      { date: "2026-08-19", event: "Klaim serupa #3 — flag awal feature graph" },
      { date: "2026-09-02", event: "Metapath semantic terdeteksi berulang" },
      { date: "2026-09-15", event: "Skor fraud > 0.90 → eskalasi investigasi" },
    ],
    metrics: [
      { label: "Total klaim 30 hari", value: "14", flag: true },
      { label: "Rasio Dx ringan → S_mahal", value: "100%", flag: true },
      { label: "Rata-rata biaya/klaim", value: "Rp 42,3 jt", flag: true },
      { label: "Peer deviation", value: "+4.2σ", flag: true },
    ],
    recommendedAction:
      "Tangguhkan pre-authorization prosedur S_mahal. Audit retrospektif 14 klaim. Eskalasi ke tim investigasi BPJS P2PK.",
  },
  {
    id: "rs",
    label: "RS_A · RS Sentosa Medika",
    type: "faskes",
    role: "Faskes",
    riskScore: 0.88,
    riskLevel: "high",
    summary:
      "FKRTL Tingkat Lanjut dengan lonjakan 320% klaim bedah kompleks dibanding periode sebelumnya. Tiga dokter bertanggung jawab atas 78% tagihan S_mahal.",
    evidence: [
      { source: "feature", text: "Volume klaim S_mahal 4.2× baseline historik RS_A", weight: 0.36 },
      { source: "semantic", text: "Metapath D → Dx → S → RS_A padat di RS_A dibanding 12 FKRTL peer", weight: 0.31 },
      { source: "topology", text: "Konsentrasi 3 dokter → 78% tagihan (normal: ≤35%)", weight: 0.21 },
    ],
    timeline: [
      { date: "2026-07", event: "Baseline volume S_mahal: 8/bln" },
      { date: "2026-08", event: "Lonjakan ke 25/bln (+212%)" },
      { date: "2026-09", event: "Eskalasi ke 34/bln (+320%)" },
    ],
    metrics: [
      { label: "Volume S_mahal/bln", value: "34", flag: true },
      { label: "Konsentrasi 3 dokter", value: "78%", flag: true },
      { label: "Rata-rata LOS", value: "3,0 hari", flag: false },
      { label: "Peer deviation", value: "+3.1σ", flag: true },
    ],
    recommendedAction:
      "Verifikasi lapangan terjadwal. Sample audit 30% klaim S_mahal 30 hari terakhir. Koordinasi dengan Dinas Kesehatan Provinsi.",
  },
  {
    id: "p1",
    label: "P₁ · Pasien #JKN-2026-0451",
    type: "patient",
    role: "Pasien",
    riskScore: 0.91,
    riskLevel: "fraud",
    summary:
      "Pasien laki-laki 42 tahun dengan 3 episode rawat inap terpisah dalam 30 hari, semua dengan profil fitur identik (LOS, biaya, diagnosis) bersama P₂ & P₃.",
    evidence: [
      { source: "feature", text: "Cosine similarity P₁–P₂ = 0.92, P₁–P₃ = 0.85 (threshold 0.75)", weight: 0.38 },
      { source: "semantic", text: "Pola metapath identik dengan klaster upcoding historis", weight: 0.31 },
      { source: "topology", text: "Selalu dirujuk D₁ → RS_A → S_mahal (tidak ada rujukan tingkat primer)", weight: 0.22 },
    ],
    timeline: [
      { date: "2026-08-15", event: "Episode #1 rawat inap 3 hari" },
      { date: "2026-08-28", event: "Episode #2 rawat inap 3 hari" },
      { date: "2026-09-10", event: "Episode #3 rawat inap 3 hari" },
    ],
    metrics: [
      { label: "Episode 30 hari", value: "3", flag: true },
      { label: "LOS identik", value: "3,0 hari", flag: true },
      { label: "Total tagihan", value: "Rp 126,9 jt", flag: true },
      { label: "Cosine sim. rerata", value: "0.89", flag: true },
    ],
    recommendedAction:
      "Verifikasi identitas biometrik. Cek riwayat rujukan primer. Wawancara pasien terkait 3 episode.",
  },
];
