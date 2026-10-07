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
  // Patients (Notion-docs simulation_full.md & claims_db_parsed.json)
  { id: "p1", type: "patient", label: "P01", x: 110, y: 90, risk: "fraud", note: "Agus Raharjo (58 th, PBPU Jakarta) · K29.7 Gastritis · LOS 3 hr · KLM001" },
  { id: "p2", type: "patient", label: "P02", x: 110, y: 230, risk: "fraud", note: "Bunga Lestari (63 th, PBPU Jakarta) · K29.7 Gastritis · LOS 3 hr · KLM002" },
  { id: "p3", type: "patient", label: "P03", x: 110, y: 370, risk: "fraud", note: "Candra Wijaya (55 th, PBPU Jakarta) · K29.7 Gastritis · LOS 3 hr · KLM003" },
  { id: "p4", type: "patient", label: "P04", x: 560, y: 100, risk: "low", note: "Dewi Anggraeni (34 th, PBI Bogor) · Kontrol Rawat Jalan · Normal" },
  { id: "p5", type: "patient", label: "P06", x: 560, y: 360, risk: "low", note: "Fajar Nugroho (71 th, PBI Surabaya) · Kontrol Rawat Jalan · Normal" },

  // Doctors (syndicate SYND-01)
  { id: "d1", type: "doctor", label: "D01", x: 270, y: 160, risk: "fraud", note: "dr. Adnan Prakoso, Sp.BTKV · RS_A · Upcoding PCI 00.66" },
  { id: "d2", type: "doctor", label: "D02", x: 270, y: 300, risk: "fraud", note: "dr. Barli Soemarno, Sp.B · RS_A · Bedah Kolusi SYND-01" },
  { id: "d3", type: "doctor", label: "D06", x: 430, y: 100, risk: "low", note: "dr. Fitri Handayani, Sp.A · RS_B · Praktik Wajar (Kontrol Normal)" },

  // Faskes (RS_A Aegis Medika A)
  { id: "rs", type: "faskes", label: "RS_A", x: 410, y: 230, risk: "fraud", note: "RS Aegis Medika A (Kelas B, 412 TT, Jakarta Selatan, Skor 0.95)" },

  // Procedures (ICD-9-CM)
  { id: "sExpensive", type: "procedure", label: "00.66", x: 590, y: 230, risk: "fraud", note: "Angioplasti Koroner PCI + Stent · INA-CBG Rp 58 jt" },
  { id: "sStd", type: "procedure", label: "44.13", x: 250, y: 400, risk: "low", note: "Gastroskopi Standar Non-Bedah · INA-CBG Rp 3,2 jt" },

  // Diagnosis (ICD-10)
  { id: "dxMild", type: "diagnosis", label: "K29.7", x: 410, y: 400, risk: "fraud", note: "Gastritis Akut Tanpa Perdarahan (Ringan) · Ditagih PCI" },
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
  {
    id: "late-fusion",
    title: "Late Fusion (NLP & Social Media Signal)",
    legend: "p_fused",
    desc: "Late Fusion memadukan probabilitas graf (p_graph) dengan sinyal sentimen teks media sosial (f_text) berbobot γ = 0.10.",
    latex: "p_{\\text{fused}} = p_{\\text{graph}} + \\gamma \\cdot f_{\\text{text}} \\cdot (1 - p_{\\text{graph}}), \\quad \\gamma = 0.10",
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

// ----- Simulation steps (Berdasarkan skenario SYND-01 pada simulation_full.md) -----
export const SIM_STEPS = [
  {
    id: 0,
    title: "Klaim masuk (KLM001–003)",
    desc: "Tiga pasien (P01 Agus Raharjo, P02 Bunga Lestari, P03 Candra Wijaya) dirujuk ke RS Aegis Medika A oleh dr. Adnan Prakoso (D01) dan dr. Barli Soemarno (D02) untuk prosedur PCI 00.66, dengan diagnosis primer K29.7 (Gastritis).",
    channel: "topology" as const,
    insight: "Pada graf topologi, jalur P → D → RS_A → PCI tampak sebagai rujukan medis formal yang valid.",
    score: 0.32,
  },
  {
    id: 1,
    title: "Analisis graf fitur (A⁽ᶠᵉᵃᵗ⁾)",
    desc: "Vektor atribut P01, P02, P03 dievaluasi: Length of Stay identik (3 hari), diagnosis K29.7 identik, rasio biaya berhimpitan Rp 58 juta dengan Cosine Similarity 0.92 melampaui ambang θ_feat = 0.85.",
    channel: "feature" as const,
    insight: "Cosine similarity P01–P02 = 0.92 dan P02–P03 = 0.88 mengungkap subgraf kemiripan yang mencurigakan.",
    score: 0.61,
  },
  {
    id: 2,
    title: "Analisis graf semantik (A⁽ˢᵉᵐ⁾)",
    desc: "Metapath Dokter → Diagnosis → Prosedur → Faskes (D01/D02 → K29.7 → 00.66 → RS_A) menunjukkan pola upcoding sistematis: diagnosis gastritis ringan dipasangkan dengan bedah stent mahal di faskes yang sama.",
    channel: "semantic" as const,
    insight: "Pola metapath berulang berfrekuensi tinggi = upcoding terselubung. Kamuflase rujukan terbongkar.",
    score: 0.84,
  },
  {
    id: 3,
    title: "Fusion & klasifikasi akhir",
    desc: "Embedding 3 saluran + parameter bersama digabungkan. Late Fusion formula p_fused = p_graph + 0.10 * f_text * (1 - p_graph) menghasilkan probabilitas 0.94. SHAP mengatribusi kontribusi tiap saluran.",
    channel: "fusion" as const,
    insight: "Skor fraud 0.94 (KLM001). Kontribusi: semantik +41%, fitur +38%, topologi −12% (kamuflase rujukan).",
    score: 0.94,
  },
];

// ----- SHAP attribution -----
export const SHAP_ATTRS = [
  { feature: "Metapath K29.7 (Gastritis) → 00.66 (PCI)", shap: 0.41, channel: "semantic" as const },
  { feature: "Cosine similarity P01–P02 (LOS 3 hr, Rp 58 jt)", shap: 0.28, channel: "feature" as const },
  { feature: "Frekuensi kolusi D01–D02 di RS_A", shap: 0.19, channel: "semantic" as const },
  { feature: "Rasio biaya klaim vs INA-CBG gastritis standar", shap: 0.12, channel: "feature" as const },
  { feature: "Topologi jalur rujukan RS_A (kamuflase)", shap: -0.07, channel: "topology" as const },
];

// Progressive channel contribution per simulation step (grows toward final score)
// stepIdx 0 = topology only (initial), 1 = +feature, 2 = +semantic, 3 = final fusion
export const CHANNEL_PROGRESS = [
  { step: 0, topology: 0.32, feature: 0.0, semantic: 0.0, fusion: 0.32 },
  { step: 1, topology: 0.30, feature: 0.45, semantic: 0.0, fusion: 0.61 },
  { step: 2, topology: 0.28, feature: 0.42, semantic: 0.55, fusion: 0.84 },
  { step: 3, topology: -0.12, feature: 0.38, semantic: 0.41, fusion: 0.94 },
];

// ----- Roadmap phases v2.1 (8 Minggu / 4 Fase sesuai architecture_full.md) -----
export const ROADMAP = [
  {
    phase: "Fase 0",
    period: "Minggu 1",
    title: "Fondasi & Audit Data v2.1",
    items: ["Dataset v2.1 (300 klaim, seed 20260707)", "Blokir kolom leakage (configs/leakage.yaml)", "Evaluasi group-aware (GroupKFold & LOGO)"],
    status: "active",
  },
  {
    phase: "Fase 1",
    period: "Minggu 2–3",
    title: "Baseline Tabular & ML",
    items: ["Baseline XGBoost + SMOTE & MLP PyTorch", "Rekayasa fitur agregat 30 hari & rasio tarif", "Benchmark awal AUPRC pada prevalensi 3–7%"],
    status: "next",
  },
  {
    phase: "Fase 2",
    period: "Minggu 4–6",
    title: "Graf Heterogen & MHGSL",
    items: ["Konstruksi PyG HeteroData (3 saluran paralel)", "Dual GCN (Channel-Specific & Shared-Parameter)", "Modul XAI (SHAP per-saluran & TreeExplainer)"],
    status: "future",
  },
  {
    phase: "Fase 3",
    period: "Minggu 7–8",
    title: "Validasi Final & Pilot 5 FKRTL",
    items: ["Late Fusion NLP teks & sentimen (γ = 0.10)", "Uji 9 sindikat kecurangan (SYND-01 s.d. SYND-09)", "Pilot operasional 5 FKRTL rujukan JKN"],
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

// ----- Fraud ring drilldown profiles (Berdasarkan simulation_full.md) -----
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
    label: "D01 · dr. Adnan Prakoso, Sp.BTKV",
    type: "doctor",
    role: "Dokter",
    riskScore: 0.94,
    riskLevel: "fraud",
    summary:
      "Spesialis Bedah Toraks & Kardiovaskular di RS Aegis Medika A (RS_A) yang terdeteksi memasangkan diagnosis gastritis ringan (ICD-10 K29.7) dengan prosedur PCI kardiovaskular kompleks (ICD-9-CM 00.66) berulang pada klaim KLM001–002 bersama D02.",
    evidence: [
      { source: "semantic", text: "Metapath D01 → K29.7 → 00.66 (PCI) → RS_A berulang pada klaim KLM001–002 (ina-cbg Rp 58 jt vs tarif gastritis Rp 3,2 jt)", weight: 0.41 },
      { source: "feature", text: "Vektor atribut klaim D01 berhimpitan 0.79 dengan D02 (kolusi sindikat upcoding SYND-01)", weight: 0.23 },
      { source: "topology", text: "Semua pasien rujukan D01 dirujuk langsung ke RS_A untuk tindakan bedah mahal tanpa riwayat FKTP", weight: 0.18 },
      { source: "feature", text: "Rata-rata tagihan tindakan 4.2× di atas peer dokter spesialis regional", weight: 0.14 },
    ],
    timeline: [
      { date: "2026-08-12", event: "Klaim KLM001 diajukan untuk P01 Agus Raharjo (K29.7 ditagih PCI Rp 58 jt)" },
      { date: "2026-08-19", event: "Klaim KLM002 diajukan untuk P02 Bunga Lestari dengan pola LOS 3 hari identik" },
      { date: "2026-09-02", event: "Metapath semantik D01–D02 terdeteksi berulang oleh MHGSL" },
      { date: "2026-09-15", event: "Skor fraud 0.94 → eskalasi prioritas investigasi verifikator" },
    ],
    metrics: [
      { label: "Total klaim terindikasi", value: "2 klaim (SYND-01)", flag: true },
      { label: "Rasio K29.7 → PCI", value: "100%", flag: true },
      { label: "Tagihan per klaim", value: "Rp 58.000.000", flag: true },
      { label: "Deviasi peer group", value: "+4.2σ", flag: true },
    ],
    recommendedAction:
      "Tangguhkan pre-authorization tindakan PCI 00.66 untuk kasus gastritis K29.7. Audit rekam medis elektronik (Composition) KLM001–002. Eskalasi ke Tim Pencegahan Kecurangan JKN (P2PK).",
  },
  {
    id: "rs",
    label: "RS_A · RS Aegis Medika A",
    type: "faskes",
    role: "Faskes",
    riskScore: 0.95,
    riskLevel: "fraud",
    summary:
      "FKRTL Swasta Kelas B di Jakarta Selatan (412 Tempat Tidur) dengan 19 klaim, skor fraud tertinggi 0.95. Konsentrasi 78% tagihan bedah mahal berasal dari dokter D01 & D02 pada klaster sindikat SYND-01.",
    evidence: [
      { source: "feature", text: "Volume klaim PCI (00.66) mencapai 4.2× baseline historik faskes kelas B sejenis", weight: 0.36 },
      { source: "semantic", text: "Metapath padat D → K29.7 → 00.66 → RS_A terkonsentrasi di RS_A dibanding 5 FKRTL peer (RS_B s.d. RS_F)", weight: 0.31 },
      { source: "topology", text: "Konsentrasi rujukan bedah tertutup antara D01 dan D02 (78% tagihan PCI)", weight: 0.21 },
    ],
    timeline: [
      { date: "2026-07", event: "Baseline volume PCI RS_A tercatat 8 klaim/bulan" },
      { date: "2026-08", event: "Lonjakan klaim PCI gastritis ke 19 klaim (+137%)" },
      { date: "2026-09", event: "Deteksi anomali kolusi D01–D02 di modul MHGSL" },
    ],
    metrics: [
      { label: "Total klaim di RS_A", value: "19 klaim", flag: true },
      { label: "Skoring fraud maks", value: "0.95 (fraud)", flag: true },
      { label: "Tempat tidur", value: "412 TT (Kelas B)", flag: false },
      { label: "Deviasi klaim bedah", value: "+3.8σ", flag: true },
    ],
    recommendedAction:
      "Pemeriksaan lapangan terpadu oleh Tim Pertimbangan Klinis BPJS. Audit retrospektif 19 klaim. Uji kesesuaian log tindakan kateterisasi jantung vs resume medis pasien.",
  },
  {
    id: "p1",
    label: "P01 · Agus Raharjo (58 th)",
    type: "patient",
    role: "Pasien",
    riskScore: 0.94,
    riskLevel: "fraud",
    summary:
      "Peserta PBPU Jakarta Selatan (58 tahun) dengan klaim KLM001 dirawat inap 3 hari dengan diagnosis Gastritis K29.7 namun ditagih tindakan PCI 00.66 senilai Rp 58.000.000, memiliki vektor fitur identik sempurna dengan P02 Bunga Lestari & P03 Candra Wijaya.",
    evidence: [
      { source: "feature", text: "Cosine similarity atribut (LOS=3, biaya=Rp 58 jt) dengan P02 = 0.92, dengan P03 = 0.85 (ambang batas θ_feat = 0.85)", weight: 0.38 },
      { source: "semantic", text: "Kombinasi diagnosis K29.7 dan prosedur 00.66 identik dengan pola upcoding SYND-01", weight: 0.31 },
      { source: "topology", text: "Ditangani dokter D01 di RS_A tanpa rujukan riwayat poli spesialis primer", weight: 0.22 },
    ],
    timeline: [
      { date: "2026-08-12", event: "Klaim KLM001 diajukan untuk rawat inap 3 hari di RS_A" },
      { date: "2026-08-20", event: "Teridentifikasi kemiripan profil tinggi dengan klaim KLM002 (P02)" },
      { date: "2026-09-10", event: "Kontradiksi narasi: resume klinis mengonfirmasi tidak ada tindakan kateterisasi" },
    ],
    metrics: [
      { label: "Nomor klaim", value: "KLM001", flag: true },
      { label: "Tagihan INA-CBG", value: "Rp 58.000.000", flag: true },
      { label: "Length of Stay (LOS)", value: "3 hari", flag: false },
      { label: "Cosine sim. rerata", value: "0.89", flag: true },
    ],
    recommendedAction:
      "Verifikasi faktual ke peserta terkait pelaksanaan tindakan kateterisasi. Klarifikasi surat rujukan FKTP. Sinkronisasi log fingerprint dan resume medis elektronik.",
  },
];

// ----- Official Dataset Metrics (Notion-docs & Colab Execution) -----
export const DATASET_METRICS = {
  claimsV2: 300,
  claimsV1: 100,
  patients: 40,
  doctors: 20,
  faskes: 10,
  syndicates: 9,
  groundTruthSyndicates: 5,
  fraudClaimsV1: 14,
  fraudClaimsV2: 36,
  anomalyClaimsV2: 60,
  normalClaimsV2: 240,
  featureEdges: 4563,
  textContradictions: 8,
  oasisSteps: 300,
  socialPosts: 48,
  syndicateHitRate: 100,
};
