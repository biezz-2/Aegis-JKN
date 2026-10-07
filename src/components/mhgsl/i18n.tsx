"use client";

import * as React from "react";

export type Lang = "id" | "en";

export interface Dict {
  // Navbar
  navBrand: string;
  navTagline: string;
  navCta: string;
  navItems: { id: string; label: string }[];
  navOpenMenu: string;
  navQuickNav: string;

  // Hero
  heroBadge: string;
  heroTitle1: string;
  heroTitle2: string;
  heroSubtitleTopologi: string;
  heroSubtitleFitur: string;
  heroSubtitleSemantik: string;
  heroSubtitleEnd: string;
  heroCta1: string;
  heroCta2: string;
  heroMiniBadge: string;
  heroStats: { value: string; label: string }[];
  heroTrust: [string, string][];
  heroScroll: string;

  // Problem
  problemBadge: string;
  problemTitle1: string;
  problemTitle2: string;
  problemDesc1: string;
  problemDesc2: string;
  problemDesc3: string;
  problemVolumeLabel: string;
  problemVerifierLabel: string;
  problemFraudLabel: string;
  problemFraudSub: string;
  problemPillars: { title: string; subtitle: string; modus: string[]; approach: string; focus?: boolean }[];
  problemFocus: string;
  problemApproachLabel: string;

  // Architecture
  archBadge: string;
  archTitle1: string;
  archTitle2: string;
  archTitle3: string;
  archDesc: string;
  archPipeline: { step: string; title: string; subtitle: string; desc: string }[];
  archDataSourcesTitle: string;
  archDataSources: { name: string; desc: string }[];
  archPrivacyTitle: string;
  archPrivacy: { name: string; desc: string }[];
  archOpsTitle: string;
  archOps: { name: string; desc: string }[];

  // Multi-channel graph
  graphBadge: string;
  graphTitle1: string;
  graphTitle2: string;
  graphDesc: string;
  graphChannelsLabel: string;
  graphMode: string;
  graphLegend: string;
  graphRiskLabel: string;
  graphHeader: string;
  graphClickHint: string;
  graphMetapathBtn: string;
  graphNodeDetail: { type: string; inDegree: string; outDegree: string; edge: string };

  // Simulation
  simBadge: string;
  simTitle1: string;
  simTitle2: string;
  simDesc: string;
  simSteps: { title: string; desc: string; insight: string }[];
  simStagesLabel: string;
  simControlsLabel: string;
  simReset: string;
  simPrev: string;
  simNext: string;
  simAutoPlay: string;
  simPause: string;
  simScoreLabel: string;
  simInsightLabel: string;
  simProbLabel: string;
  simScaleSafe: string;
  simScaleReview: string;
  simScaleEscalate: string;
  simShapTitle: string;
  simVerdict: string;

  // Math
  mathBadge: string;
  mathTitle1: string;
  mathTitle2: string;
  mathDesc: string;
  mathCopy: string;
  mathCopied: string;
  mathGlossary: string;

  // Comparison
  compareBadge: string;
  compareTitle1: string;
  compareTitle2: string;
  compareDesc: string;
  compareTabAuprc: string;
  compareTabRadar: string;
  compareTabMetrics: string;
  compareTabMatrix: string;
  compareAuprcTitle: string;
  compareAuprcDesc: string;
  compareDeltaLabel: string;
  compareRadarTitle: string;
  compareRadarDesc: string;
  compareMetricsTitle: string;
  compareMetricsDesc: string;
  compareMetricCol: string;
  compareMatrixCol: string;

  // Fraud ring
  ringBadge: string;
  ringTitle1: string;
  ringTitle2: string;
  ringDesc1: string;
  ringDesc2: string;
  ringClickHint: string;
  ringHeader: string;
  ringHideHl: string;
  ringShowHl: string;
  ringDense: string;
  ringDenseSub: string;
  ringHealthy: string;
  ringHealthySub: string;
  ringMsgPassing: string;
  ringMsgPassingSteps: string[];
  ringCamouflageTitle: string;
  ringCamouflage: string[];
  ringQuickAccess: string;
  ringVerdictBtn: string;
  ringVerdictText: string;
  ringVerdictTextHidden: string;

  // Roadmap
  roiBadge: string;
  roiTitle1: string;
  roiTitle2: string;
  roiDesc: string;
  roiStats: { before: string; after: string; label: string }[];
  roiSavingsTitle: string;
  roiSavingsSub: string;
  roiSavingsDesc: string;
  roadmapBadge: string;
  roadmapTitle: string;
  roadmapPhases: { phase: string; period: string; title: string; items: string[] }[];

  // Footer
  footerTagline: string;
  footerDesc: string;
  footerPrivacyBadge: string;
  footerHitlBadge: string;
  footerModulViz: string;
  footerSumber: string;
  footerEco: string;
  footerModulItems: { label: string; href: string }[];
  footerSumberItems: { label: string; href: string }[];
  footerEcoItems: { label: string; href: string }[];
  footerCopyright: string;
  footerBackTop: string;
  footerSource: string;
  footerDisclaimer: string;

  // Theme toggle
  themeDark: string;
  themeLight: string;
}

const id: Dict = {
  navBrand: "Aegis-JKN",
  navTagline: "MHGSL · Fraud Intelligence",
  navCta: "Coba Demo",
  navOpenMenu: "Buka menu navigasi",
  navQuickNav: "Navigasi Cepat",
  navItems: [
    { id: "problem", label: "Taksonomi Risiko" },
    { id: "architecture", label: "Arsitektur" },
    { id: "graph", label: "Multi-Channel Graph" },
    { id: "simulation", label: "Simulasi" },
    { id: "math", label: "Formulasi" },
    { id: "compare", label: "Perbandingan" },
    { id: "ring", label: "Fraud Ring" },
  ],
  heroBadge: "Healthkathon BPJS Kesehatan 2026 · Detect Smarter, Protect JKN",
  heroTitle1: "Visualisasi Interaktif",
  heroTitle2: "untuk Deteksi Fraud Ekosistem JKN",
  heroSubtitleTopologi: "topologi",
  heroSubtitleFitur: "fitur",
  heroSubtitleSemantik: "semantik",
  heroSubtitleEnd:
    "untak menembus kamuflase sindikat kecurangan klaim asuransi kesehatan nasional.",
  heroCta1: "Mulai Simulasi Deteksi",
  heroCta2: "Jelajah Arsitektur MHGSL",
  heroMiniBadge: "3 graf heterogen · 1 ekosistem · deteksi sindikat kolusi",
  heroStats: [
    { value: "2.000.000+", label: "Klaim harian diproses sistem BPJS" },
    { value: "±1.000", label: "Verifikator manual yang tersedia" },
    { value: "3", label: "Saluran graf heterogen MHGSL" },
    { value: "+20%", label: "Lonjakan AUPRC pada arsitektur hibrida" },
  ],
  heroTrust: [
    ["HL7", "FHIR R4"],
    ["SATUSEHAT", "Permenkes 24/2022"],
    ["V-Claim", "BPJS Middleware"],
    ["UU PDP", "No. 27/2022"],
    ["SHAP", "Explainable AI"],
  ],
  heroScroll: "Scroll untuk eksplorasi",

  problemBadge: "Taksonomi Risiko Ekosistem JKN",
  problemTitle1: "Tiga Pilar Risiko yang Harus Didekati",
  problemTitle2: "Presisi Tinggi",
  problemDesc1:
    "Hindari 'super app' yang mengklaim menyelesaikan semua masalah. Fokus pada use case bernilai tinggi—deteksi",
  problemDesc2: "upcoding & phantom billing pada FKRTL",
  problemDesc3:
    "—memberikan presisi terukur yang dihargai dewan juri.",
  problemVolumeLabel: "Volume Klaim Harian",
  problemVerifierLabel: "Verifikator Manual",
  problemFraudLabel: "Estimasi Potensi Fraud",
  problemFraudSub: "dari total nilai klaim nasional",
  problemPillars: [
    {
      title: "Risiko Fasilitas Kesehatan",
      subtitle: "Area dengan potensi kebocoran finansial terbesar",
      modus: ["Phantom Billing", "Upcoding", "Unbundling", "Prolonged Stay", "Cloning Rekam Medis"],
      approach:
        "Analisis anomali frekuensi kunjungan pasien, deteksi inkonsistensi diagnosis (ICD-10) vs tindakan (ICD-9-CM), serta pemodelan jaringan dokter–pasien.",
      focus: true,
    },
    {
      title: "Risiko Peserta JKN",
      subtitle: "Manipulasi identitas & penyalahgunaan hak layanan",
      modus: [
        "Peminjaman kartu kepesertaan",
        "Kolusi surat keterangan sakit fiktif",
        "Drug diversion (penumpukan obat)",
      ],
      approach:
        "Autentikasi biometrik, analisis pola pergerakan geografis klaim, dan clustering pengambilan obat kronis yang melebihi dosis rasional.",
    },
    {
      title: "Risiko Pemberi Kerja",
      subtitle: "Manipulasi administratif korporasi",
      modus: ["Under-reporting upah", "Penahanan setoran iuran", "Misklasifikasi hubungan kerja"],
      approach:
        "Ekstraksi dokumen penggajian (OCR/NLP), pemodelan silang data perpajakan, dan deteksi anomali tren pembayaran iuran bulanan.",
    },
  ],
  problemFocus: "Fokus Solusi",
  problemApproachLabel: "Pendekatan Solusi AI",

  archBadge: "Arsitektur Teknis & Data Pipeline",
  archTitle1: "Dari",
  archTitle2: "hingga",
  archTitle3: "Skor Fraud + SHAP",
  archDesc:
    "Solusi AI bertindak sebagai middleware antara SIMRS faskes dan server penagihan BPJS. Berkas berisiko rendah diproses otomatis; berkas berisiko tinggi masuk antrean investigasi verifikator.",
  archPipeline: [
    {
      step: "01",
      title: "Ingestasi FHIR",
      subtitle: "SATUSEHAT HL7 FHIR R4 · V-Claim",
      desc: "Encounter, Condition (ICD-10), MedicationRequest, Composition diparse menjadi entitas graf heterogen.",
    },
    {
      step: "02",
      title: "Konstruksi 3 Graf",
      subtitle: "Multi-channel adjacency",
      desc: "Dibangun matriks A⁽ᵗᵒᵖ⁾, A⁽ᶠᵉᵃᵗ⁾, A⁽ˢᵉᵐ⁾ yang merepresentasikan tiga pandangan ekosistem secara paralel.",
    },
    {
      step: "03",
      title: "Channel-Specific GCN",
      subtitle: "Ekstraksi karakteristik unik",
      desc: "GCN independen W⁽ᵏ⁾ untuk tiap saluran mempelajari pola khas topologi/fitur/semantik.",
    },
    {
      step: "04",
      title: "Shared-Parameter GCN",
      subtitle: "Komonalitas lintas-saluran",
      desc: "W⁽ˢʰᵃʳᵉᵈ⁾ yang sama memaksa ekstraksi representasi umum lintas ketiga graf.",
    },
    {
      step: "05",
      title: "Fusion & Classifier",
      subtitle: "Skor fraud & SHAP",
      desc: "Embedding digabung lalu diproyeksikan ke Sigmoid menghasilkan probabilitas kecurangan + atribusi SHAP.",
    },
  ],
  archDataSourcesTitle: "Sumber Data (FHIR R4)",
  archDataSources: [
    { name: "Encounter", desc: "episode kunjungan/admisi" },
    { name: "Condition", desc: "diagnosis ICD-10" },
    { name: "MedicationRequest/Dispense", desc: "" },
    { name: "Composition", desc: "resume medis elektronik" },
  ],
  archPrivacyTitle: "Tata Kelola Privasi",
  archPrivacy: [
    { name: "UU PDP No. 27/2022", desc: "data kesehatan = spesifik" },
    { name: "DP-CTGAN", desc: "data sintetis privacy-by-design" },
    { name: "Federated Learning", desc: "data tidak meninggalkan faskes" },
    { name: "DPO", desc: "+ pelaporan 3×24 jam" },
  ],
  archOpsTitle: "Operasionalisasi",
  archOps: [
    { name: "Human-in-the-Loop", desc: "keputusan akhir = auditor" },
    { name: "Active Learning + DPO", desc: "feedback verifikator" },
    { name: "Tokenomics Gemini", desc: "Flash (batch) + Pro (kasus kritis)" },
    { name: "ROI", desc: "20 mnt → 3 mnt per berkas" },
  ],

  graphBadge: "Multi-Channel Graph Visualization",
  graphTitle1: "Satu Ekosistem,",
  graphTitle2: "Tiga Perspektif Graf",
  graphDesc:
    "Toggle antar saluran untuk melihat bagaimana topologi fisik, kemiripan fitur, dan hubungan semantik metapath menyaring informasi berbeda—dan bagaimana gabungannya menembus kamuflase sindikat.",
  graphChannelsLabel: "Tampilan Saluran",
  graphMode: "Mode",
  graphLegend: "Legenda Simpul",
  graphRiskLabel: "Tingkat Risiko",
  graphHeader: "Sindikat D01–D02 · RS_A (SYND-01) · 5 entitas berisiko fraud",
  graphClickHint: "Klik simpul untuk detail klinis & klaim",
  graphMetapathBtn: "Metapath ℳ",
  graphNodeDetail: { type: "Tipe", inDegree: "In-degree", outDegree: "Out-degree", edge: "edge" },

  simBadge: "Simulasi Kasus · Upcoding Terselubung (SYND-01)",
  simTitle1: "Menelusuri",
  simTitle2: "di RS Aegis Medika A",
  simDesc:
    "Skenario: tiga pasien PBPU (P01 Agus Raharjo, P02 Bunga Lestari, P03 Candra Wijaya) dirujuk ke dr. Adnan Prakoso (D01) & dr. Barli Soemarno (D02) di RS_A untuk tindakan PCI 00.66 (Rp 58 jt), namun diagnosis primer hanya K29.7 Gastritis (Rp 3,2 jt). Topologi tampak wajar—fitur & semantik yang mengungkap kecurangan.",
  simSteps: [
    {
      title: "Klaim masuk (KLM001–003)",
      desc: "Tiga pasien (P01, P02, P03) dirujuk ke RS_A oleh D01 & D02 untuk prosedur PCI 00.66. Diagnosis primer tercatat sebagai K29.7 Gastritis ringan.",
      insight: "Pada graf topologi, jalur P → D → RS_A → PCI terlihat sebagai rujukan medis formal yang valid & wajar.",
    },
    {
      title: "Analisis graf fitur (A⁽ᶠᵉᵃᵗ⁾)",
      desc: "Vektor atribut P01, P02, P03 dievaluasi: Length of Stay identik (3 hari), diagnosis K29.7 identik, biaya berhimpitan Rp 58 juta dengan Cosine Similarity 0.92 melampaui ambang θ_feat = 0.85.",
      insight: "Cosine similarity P01–P02 = 0.92 dan P02–P03 = 0.88, jauh di atas θ_feat. Muncul subgraf padat berisiko tinggi.",
    },
    {
      title: "Analisis graf semantik (A⁽ˢᵉᵐ⁾)",
      desc: "Metapath Dokter → Diagnosis → Prosedur → Faskes (D01/D02 → K29.7 → 00.66 → RS_A) menunjukkan pola berulang sistematis: diagnosis gastritis ringan dipasangkan dengan bedah stent PCI di RS_A.",
      insight: "Pola metapath berulang = upcoding terselubung. Kamuflase rujukan terdeteksi melalui kesamaan semantik tinggi.",
    },
    {
      title: "Fusion & klasifikasi akhir",
      desc: "Embedding 3 saluran + shared digabung dengan Late Fusion (γ = 0.10). Sigmoid menghasilkan skor akhir 0.94. SHAP mengatribusi kontribusi tiap saluran & fitur.",
      insight: "Skor fraud 0.94 (KLM001). Kontribusi: semantic graph +41%, feature graph +38%, topology −12% (kamuflase operasional).",
    },
  ],
  simStagesLabel: "Tahapan Analisis",
  simControlsLabel: "Kontrol",
  simReset: "Reset",
  simPrev: "Prev",
  simNext: "Next",
  simAutoPlay: "Auto-play",
  simPause: "Pause",
  simScoreLabel: "Skor Fraud",
  simInsightLabel: "Insight terdeteksi",
  simProbLabel: "Probabilitas kecurangan",
  simScaleSafe: "Aman (≥3 mnt telaah)",
  simScaleReview: "Tinjau manual",
  simScaleEscalate: "Eskalasi",
  simShapTitle: "Atribusi SHAP (Explainable AI)",
  simVerdict:
    "Verdict: Skor fraud 0.94 → klaim KLM001–003 masuk antrean prioritas investigasi verifikator. Topology berkontribusi negatif (kamuflase) → ciri khas sindikat upcoding.",

  mathBadge: "Formulasi Matematis",
  mathTitle1: "Dari",
  mathTitle2: "Konvolusi Graf",
  mathTitle2b: "hingga Prediksi",
  mathDesc:
    "Empat persamaan inti MHGSL: konstruksi adjasensi fitur (cosine), konvolusi spesifik-saluran, GCN parameter-bersama, dan fusion + klasifikasi akhir.",
  mathCopy: "Salin LaTeX",
  mathCopied: "Tersalin",
  mathGlossary: "Glosarium simbol",

  compareBadge: "Benchmark Metode Deteksi",
  compareTitle1: "MHGSL vs",
  compareTitle2: "XGBoost / GNN / Hybrid",
  compareDesc:
    "Tiga saluran graf heterogen + parameter bersama secara konsisten mendominasi AUPRC pada dataset asuransi finansial & kesehatan.",
  compareTabAuprc: "AUPRC",
  compareTabRadar: "Radar Multi-Metrik",
  compareTabMetrics: "Metrik Detail",
  compareTabMatrix: "Matriks",
  compareAuprcTitle: "Area Under Precision-Recall Curve (AUPRC)",
  compareAuprcDesc: "Skor relatif (0–1) · semakin tinggi = lebih sedikit false negatives",
  compareDeltaLabel: "Δ MHGSL vs XGBoost",
  compareRadarTitle: "Radar Multi-Metrik",
  compareRadarDesc: "5 metrik kinerja: Precision · Recall · F1 · AUPRC · Specificity",
  compareMetricsTitle: "Metrik Detail",
  compareMetricsDesc: "Tabel rinci per metrik + tren konvergensi AUPRC",
  compareMetricCol: "Metrik",
  compareMatrixCol: "Metrik",

  ringBadge: "Fraud Ring Detection · Sindikat Kolusi",
  ringTitle1: "Pesan Berjalan,",
  ringTitle2: "Sindikat Tersingkap",
  ringDesc1:
    "Model tabular memeriksa tiap klaim secara terisolasi—pelaku sindikat memanfaatkan celah dengan membagi peran. Melalui",
  ringDesc2:
    "pada graf heterogen, MHGSL mengidentifikasi subgraf padat anomali sebagai collusive communities.",
  ringClickHint: "Klik simpul berisiko fraud (P01 / D01 / RS_A) untuk lihat detail investigasi klinis",
  ringHeader: "Komunitas pasien–dokter–faskes (SYND-01)",
  ringHideHl: "Sembunyikan highlight",
  ringShowHl: "Tampilkan subgraf padat",
  ringDense: "Subgraf padat",
  ringDenseSub: "14 edge berlebih",
  ringHealthy: "Komunitas sehat",
  ringHealthySub: "7 edge tersebar",
  ringMsgPassing: "Mekanisme Message Passing",
  ringMsgPassingSteps: [
    "Tiap simpul mengagregasi fitur dari semua tetangga melalui bobot adjasensi ternormalisasi.",
    "Pada sindikat, simpul-simpul bertukar pesan intensif karena derajat keterhubungan sangat tinggi.",
    "Embedding simpul dalam klaster padat terdorong ke arah vektor risiko fraud setelah beberapa lapisan.",
    "Klasifikator mendeteksi collusive community sebagai satu unit anomali terstruktur—bukan klaim individual.",
  ],
  ringCamouflageTitle: "Mengapa Sindikat Berkamuflase Gagal",
  ringCamouflage: [
    "Klaim individu tampak valid → lolos seleksi tabular, tetapi pola agregat metapath tidak konsisten dengan praktik medis normal.",
    "Penambahan feature graph menangkap kemiripan tidak wajar antar-pasien (LOS identik, biaya berhimpitan).",
    "Shared-parameter GCN memaksa konsistensi representasi lintas-saluran → kamuflase pada satu saluran terbongkar oleh dua saluran lain.",
  ],
  ringQuickAccess: "Akses Cepat Profil Investigasi",
  ringVerdictBtn: "Verdict auditor",
  ringVerdictText:
    "Sindikat D01–D02 di RS_A (SYND-01) → klaim KLM001–003 upcoding ditarik ke antrean investigasi. Total penghematan estimasi Rp 1,2 M / bulan (Rp 14,4 M / tahun).",
  ringVerdictTextHidden: "Klik untuk melihat rekomendasi yang dihasilkan sistem...",

  roiBadge: "Kelayakan Ekonomi & ROI",
  roiTitle1: "Dari",
  roiTitle2: "20 menit",
  roiTitle3: "3 menit",
  roiTitle4: "per berkas",
  roiDesc:
    "Biaya komputasi API beberapa sen dolar per klaim terjustifikasi jika mencegah satu klaim fiktif bernilai jutaan–puluhan juta rupiah.",
  roiStats: [
    { before: "20 mnt", after: "3 mnt", label: "Telaah per berkas klaim" },
    { before: "1.000", after: "~6.700", label: "Kapasitas verifikator (efektif)" },
    { before: "≤ 3x24 jam", after: "Realtime", label: "Pelaporan kebocoran (UU PDP)" },
    { before: "Manual", after: "XAI + HITL", label: "Mode keputusan akhir" },
  ],
  roiSavingsTitle: "Estimasi penghematan tahunan",
  roiSavingsSub: "/ FKRTL pilot",
  roiSavingsDesc:
    "Asumsi 3% tingkat fraud pada tagihan operasi bedah; basis 5 FKRTL rujukan.",
  roadmapBadge: "Cetak Biru Implementasi",
  roadmapTitle: "Roadmap Empat Fase (v2.1)",
  roadmapPhases: [
    {
      phase: "Fase 0",
      period: "Minggu 1",
      title: "Fondasi & Audit Data v2.1",
      items: ["Dataset v2.1 (300 klaim, seed 20260707)", "Blokir kolom leakage (configs/leakage.yaml)", "Evaluasi group-aware (GroupKFold & LOGO)"],
    },
    {
      phase: "Fase 1",
      period: "Minggu 2–3",
      title: "Baseline Tabular & ML",
      items: ["Baseline XGBoost + SMOTE & MLP PyTorch", "Rekayasa fitur agregat 30 hari & rasio tarif", "Benchmark awal AUPRC pada prevalensi 3–7%"],
    },
    {
      phase: "Fase 2",
      period: "Minggu 4–6",
      title: "Graf Heterogen & MHGSL",
      items: ["Konstruksi PyG HeteroData (3 saluran paralel)", "Dual GCN (Channel-Specific & Shared-Parameter)", "Modul XAI (SHAP per-saluran & TreeExplainer)"],
    },
    {
      phase: "Fase 3",
      period: "Minggu 7–8",
      title: "Validasi Final & Pilot 5 FKRTL",
      items: ["Late Fusion NLP teks & sentimen (γ = 0.10)", "Uji 9 sindikat kecurangan (SYND-01 s.d. SYND-09)", "Pilot operasional 5 FKRTL rujukan JKN"],
    },
  ],

  footerTagline: "MHGSL · Fraud Intelligence",
  footerDesc:
    "Visualisasi interaktif pendekatan Multi-channel Heterogeneous Graph Structure Learning & Graph Neural Networks untuk deteksi kecurangan ekosistem Jaminan Kesehatan Nasional.",
  footerPrivacyBadge: "Privacy-by-design",
  footerHitlBadge: "Human-in-the-loop",
  footerModulViz: "Modul Visualisasi",
  footerSumber: "Sumber Pengetahuan",
  footerEco: "Ekosistem Rujukan",
  footerModulItems: [
    { label: "Taksonomi Risiko", href: "#problem" },
    { label: "Arsitektur Pipeline", href: "#architecture" },
    { label: "Multi-Channel Graph", href: "#graph" },
    { label: "Simulasi Upcoding", href: "#simulation" },
  ],
  footerSumberItems: [
    { label: "Hasil Simulasi Oasis (v2.1)", href: "/simulasi" },
    { label: "Dataset Notion (300 Klaim)", href: "/dataset" },
    { label: "Formulasi Matematis", href: "#math" },
    { label: "Benchmark Metode", href: "#compare" },
    { label: "Fraud Ring Detection", href: "#ring" },
    { label: "Roadmap & ROI", href: "#top" },
  ],
  footerEcoItems: [
    { label: "SATUSEHAT FHIR R4", href: "https://satusehat.kemkes.go.id" },
    { label: "BPJS Kesehatan V-Claim", href: "https://vclaim.bpjs-kesehatan.go.id" },
    { label: "UU PDP No. 27/2022", href: "https://jdih.kominfo.go.id" },
    { label: "Healthkathon BPJS 2026", href: "#" },
  ],
  footerCopyright: "© 2026 Aegis-JKN · Healthkathon BPJS Kesehatan",
  footerBackTop: "Kembali ke atas ↑",
  footerSource: "Sumber kode",
  footerDisclaimer:
    "Seluruh data yang divisualisasikan adalah data sintetis yang dihasilkan via DP-CTGAN untuk tujuan edukasi & purwarupa—bukan data peserta riil, sesuai kepatuhan UU PDP No. 27/2022.",

  themeDark: "Aktifkan mode gelap",
  themeLight: "Aktifkan mode terang",
};

const en: Dict = {
  navBrand: "Aegis-JKN",
  navTagline: "MHGSL · Fraud Intelligence",
  navCta: "Try Demo",
  navOpenMenu: "Open navigation menu",
  navQuickNav: "Quick Navigation",
  navItems: [
    { id: "problem", label: "Risk Taxonomy" },
    { id: "architecture", label: "Architecture" },
    { id: "graph", label: "Multi-Channel Graph" },
    { id: "simulation", label: "Simulation" },
    { id: "math", label: "Formulas" },
    { id: "compare", label: "Benchmark" },
    { id: "ring", label: "Fraud Ring" },
  ],
  heroBadge: "Healthkathon BPJS 2026 · Detect Smarter, Protect JKN",
  heroTitle1: "Interactive Visualization of",
  heroTitle2: "for JKN Ecosystem Fraud Detection",
  heroSubtitleTopologi: "topology",
  heroSubtitleFitur: "feature",
  heroSubtitleSemantik: "semantic",
  heroSubtitleEnd:
    "to break through the camouflage of health-insurance claim fraud syndicates.",
  heroCta1: "Start Detection Simulation",
  heroCta2: "Explore MHGSL Architecture",
  heroMiniBadge: "3 heterogeneous graphs · 1 ecosystem · syndicate collusion detection",
  heroStats: [
    { value: "2,000,000+", label: "Daily claims processed by BPJS" },
    { value: "≈1,000", label: "Manual verifiers available" },
    { value: "3", label: "MHGSL heterogeneous graph channels" },
    { value: "+20%", label: "AUPRC lift on hybrid architecture" },
  ],
  heroTrust: [
    ["HL7", "FHIR R4"],
    ["SATUSEHAT", "Permenkes 24/2022"],
    ["V-Claim", "BPJS Middleware"],
    ["PDP Law", "No. 27/2022"],
    ["SHAP", "Explainable AI"],
  ],
  heroScroll: "Scroll to explore",

  problemBadge: "JKN Ecosystem Risk Taxonomy",
  problemTitle1: "Three Risk Pillars to Approach with",
  problemTitle2: "High Precision",
  problemDesc1:
    "Avoid a 'super app' that claims to solve everything. Focus on a high-value use case—detecting",
  problemDesc2: "upcoding & phantom billing at FKRTL",
  problemDesc3: "—delivering measurable precision that judges value.",
  problemVolumeLabel: "Daily Claim Volume",
  problemVerifierLabel: "Manual Verifiers",
  problemFraudLabel: "Estimated Fraud Potential",
  problemFraudSub: "of national total claim value",
  problemPillars: [
    {
      title: "Health Facility Risk",
      subtitle: "Largest potential financial leakage area",
      modus: ["Phantom Billing", "Upcoding", "Unbundling", "Prolonged Stay", "Medical Record Cloning"],
      approach:
        "Anomaly analysis of patient visit frequency, ICD-10 vs ICD-9-CM inconsistency detection, and doctor–patient network modeling.",
      focus: true,
    },
    {
      title: "JKN Member Risk",
      subtitle: "Identity manipulation & benefit abuse",
      modus: [
        "Membership card lending",
        "Fictitious sick-leave collusion",
        "Drug diversion (medication hoarding)",
      ],
      approach:
        "Biometric authentication, geographic claim pattern analysis, and clustering of chronic-medication pickups exceeding rational doses.",
    },
    {
      title: "Employer Risk",
      subtitle: "Corporate administrative manipulation",
      modus: ["Wage under-reporting", "Contribution withholding", "Employment-status misclassification"],
      approach:
        "Payroll document extraction (OCR/NLP), tax-data cross modeling, and monthly contribution trend anomaly detection.",
    },
  ],
  problemFocus: "Solution Focus",
  problemApproachLabel: "AI Solution Approach",

  archBadge: "Technical Architecture & Data Pipeline",
  archTitle1: "From",
  archTitle2: "to",
  archTitle3: "Fraud Score + SHAP",
  archDesc:
    "The AI sits as middleware between facility SIMRS and BPJS billing servers. Low-risk claims auto-pass; high-risk claims queue for verifier investigation.",
  archPipeline: [
    {
      step: "01",
      title: "FHIR Ingestion",
      subtitle: "SATUSEHAT HL7 FHIR R4 · V-Claim",
      desc: "Encounter, Condition (ICD-10), MedicationRequest, Composition parsed into heterogeneous graph entities.",
    },
    {
      step: "02",
      title: "3-Graph Construction",
      subtitle: "Multi-channel adjacency",
      desc: "Build matrices A⁽ᵗᵒᵖ⁾, A⁽ᶠᵉᵃᵗ⁾, A⁽ˢᵉᵐ⁾ representing three parallel ecosystem views.",
    },
    {
      step: "03",
      title: "Channel-Specific GCN",
      subtitle: "Unique characteristic extraction",
      desc: "Independent GCN W⁽ᵏ⁾ per channel learns topology/feature/semantic-specific patterns.",
    },
    {
      step: "04",
      title: "Shared-Parameter GCN",
      subtitle: "Cross-channel commonalities",
      desc: "Same W⁽ˢʰᵃʳᵉᵈ⁾ forces extraction of common representations across all three graphs.",
    },
    {
      step: "05",
      title: "Fusion & Classifier",
      subtitle: "Fraud score & SHAP",
      desc: "Embeddings fused then projected via Sigmoid producing fraud probability + SHAP attributions.",
    },
  ],
  archDataSourcesTitle: "Data Sources (FHIR R4)",
  archDataSources: [
    { name: "Encounter", desc: "visit/admission episode" },
    { name: "Condition", desc: "ICD-10 diagnosis" },
    { name: "MedicationRequest/Dispense", desc: "" },
    { name: "Composition", desc: "electronic medical resume" },
  ],
  archPrivacyTitle: "Privacy Governance",
  archPrivacy: [
    { name: "PDP Law No. 27/2022", desc: "health data = specific" },
    { name: "DP-CTGAN", desc: "privacy-by-design synthetic data" },
    { name: "Federated Learning", desc: "data never leaves facility" },
    { name: "DPO", desc: "+ 3×24h breach reporting" },
  ],
  archOpsTitle: "Operationalization",
  archOps: [
    { name: "Human-in-the-Loop", desc: "final decision = auditor" },
    { name: "Active Learning + DPO", desc: "verifier feedback" },
    { name: "Gemini Tokenomics", desc: "Flash (batch) + Pro (critical)" },
    { name: "ROI", desc: "20 min → 3 min per claim" },
  ],

  graphBadge: "Multi-Channel Graph Visualization",
  graphTitle1: "One Ecosystem,",
  graphTitle2: "Three Graph Perspectives",
  graphDesc:
    "Toggle channels to see how physical topology, feature similarity, and metapath semantic relations filter different information—and how their fusion breaks syndicate camouflage.",
  graphChannelsLabel: "Channel View",
  graphMode: "Mode",
  graphLegend: "Node Legend",
  graphRiskLabel: "Risk Level",
  graphHeader: "Syndicate D01–D02 · RS_A (SYND-01) · 5 fraud-flagged entities",
  graphClickHint: "Click nodes for clinical & claim details",
  graphMetapathBtn: "Metapath ℳ",
  graphNodeDetail: { type: "Type", inDegree: "In-degree", outDegree: "Out-degree", edge: "edge" },

  simBadge: "Case Simulation · Hidden Upcoding (SYND-01)",
  simTitle1: "Tracing",
  simTitle2: "Syndicate at RS Aegis Medika A",
  simDesc:
    "Scenario: three PBPU patients (P01 Agus Raharjo, P02 Bunga Lestari, P03 Candra Wijaya) referred to dr. Adnan Prakoso (D01) & dr. Barli Soemarno (D02) at RS_A for procedure PCI 00.66 (Rp 58M), yet primary diagnosis is only K29.7 Gastritis (Rp 3.2M). Topology looks normal—features & semantics expose the fraud.",
  simSteps: [
    {
      title: "Claim intake (KLM001–003)",
      desc: "Three patients (P01, P02, P03) referred to RS_A by D01 & D02 for procedure PCI 00.66. Primary diagnosis recorded as mild K29.7 Gastritis.",
      insight: "On the topology graph, the path P → D → RS_A → PCI looks like a valid & reasonable medical referral.",
    },
    {
      title: "Feature graph analysis (A⁽ᶠᵉᵃᵗ⁾)",
      desc: "P01, P02, P03 attribute vectors evaluated: identical Length of Stay (3 days), identical K29.7 diagnosis, cost ratios overlapping Rp 58M with Cosine Similarity 0.92 exceeding threshold θ_feat = 0.85.",
      insight: "Cosine similarity P01–P02 = 0.92 and P02–P03 = 0.88, well above θ_feat. A dense high-risk node cluster emerges.",
    },
    {
      title: "Semantic graph analysis (A⁽ˢᵉᵐ⁾)",
      desc: "Metapath Doctor → Diagnosis → Procedure → Facility (D01/D02 → K29.7 → 00.66 → RS_A) shows consistent systematic pairing: mild gastritis diagnosis paired with expensive coronary stent surgery at RS_A.",
      insight: "Repeated metapath pattern = hidden upcoding. Camouflage exposed through high semantic similarity.",
    },
    {
      title: "Fusion & final classification",
      desc: "Embeddings from 3 channels + shared are fused via Late Fusion (γ = 0.10). Sigmoid yields final score 0.94. SHAP attributes contribution per channel & clinical feature.",
      insight: "Fraud score 0.94 (KLM001). Contributions: semantic graph +41%, feature graph +38%, topology −12% (operational camouflage).",
    },
  ],
  simStagesLabel: "Analysis Stages",
  simControlsLabel: "Controls",
  simReset: "Reset",
  simPrev: "Prev",
  simNext: "Next",
  simAutoPlay: "Auto-play",
  simPause: "Pause",
  simScoreLabel: "Fraud Score",
  simInsightLabel: "Detected insight",
  simProbLabel: "Fraud probability",
  simScaleSafe: "Safe (≥3 min review)",
  simScaleReview: "Manual review",
  simScaleEscalate: "Escalate",
  simShapTitle: "SHAP Attribution (Explainable AI)",
  simVerdict:
    "Verdict: Fraud score 0.94 → claims KLM001–003 enter priority verifier investigation queue. Topology contributes negatively (camouflage) → hallmark of upcoding syndicate.",

  mathBadge: "Mathematical Formulation",
  mathTitle1: "From",
  mathTitle2: "Graph Convolution",
  mathTitle2b: "to Prediction",
  mathDesc:
    "Four core MHGSL equations: feature adjacency (cosine), channel-specific convolution, shared-parameter GCN, and final fusion + classification.",
  mathCopy: "Copy LaTeX",
  mathCopied: "Copied",
  mathGlossary: "Symbol glossary",

  compareBadge: "Detection Method Benchmark",
  compareTitle1: "MHGSL vs",
  compareTitle2: "XGBoost / GNN / Hybrid",
  compareDesc:
    "Three heterogeneous graph channels + shared parameters consistently dominate AUPRC on financial & health-insurance datasets.",
  compareTabAuprc: "AUPRC",
  compareTabRadar: "Multi-Metric Radar",
  compareTabMetrics: "Metric Detail",
  compareTabMatrix: "Matrix",
  compareAuprcTitle: "Area Under Precision-Recall Curve (AUPRC)",
  compareAuprcDesc: "Relative score (0–1) · higher = fewer false negatives",
  compareDeltaLabel: "Δ MHGSL vs XGBoost",
  compareRadarTitle: "Multi-Metric Radar",
  compareRadarDesc: "5 performance metrics: Precision · Recall · F1 · AUPRC · Specificity",
  compareMetricsTitle: "Metric Detail",
  compareMetricsDesc: "Per-metric table + AUPRC convergence trend",
  compareMetricCol: "Metric",
  compareMatrixCol: "Metric",

  ringBadge: "Fraud Ring Detection · Collusion Syndicate",
  ringTitle1: "Messages Walk,",
  ringTitle2: "Syndicate Exposed",
  ringDesc1:
    "Tabular models inspect each claim in isolation—syndicate actors exploit this by splitting roles. Through",
  ringDesc2:
    "on heterogeneous graphs, MHGSL identifies dense anomalous subgraphs as collusive communities.",
  ringClickHint: "Click fraud-risk nodes (P01 / D01 / RS_A) for clinical investigation details",
  ringHeader: "Patient–doctor–facility community (SYND-01)",
  ringHideHl: "Hide highlight",
  ringShowHl: "Show dense subgraph",
  ringDense: "Dense subgraph",
  ringDenseSub: "14 excess edges",
  ringHealthy: "Healthy community",
  ringHealthySub: "7 scattered edges",
  ringMsgPassing: "Message-Passing Mechanism",
  ringMsgPassingSteps: [
    "Each node aggregates features from all neighbors via normalized adjacency weights.",
    "In syndicates, nodes exchange messages intensively due to very high connectivity degree.",
    "Embeddings of nodes in dense clusters drift toward the fraud-risk vector after several layers.",
    "Classifier detects the collusive community as one structured anomaly unit—not individual claims.",
  ],
  ringCamouflageTitle: "Why Syndicate Camouflage Fails",
  ringCamouflage: [
    "Individual claims look valid → pass tabular selection, but aggregate metapath patterns are inconsistent with normal medical practice.",
    "Adding the feature graph captures unusual similarity between patients (identical LOS, overlapping costs).",
    "Shared-parameter GCN forces cross-channel representation consistency → camouflage in one channel is exposed by the other two.",
  ],
  ringQuickAccess: "Quick Investigation Profile Access",
  ringVerdictBtn: "Auditor verdict",
  ringVerdictText:
    "Syndicate D01–D02 at RS_A (SYND-01) → claims KLM001–003 upcoding pulled into investigation queue. Total estimated savings Rp 1.2 B / month (Rp 14.4 B / year).",
  ringVerdictTextHidden: "Click to see system-generated recommendation...",

  roiBadge: "Economic Feasibility & ROI",
  roiTitle1: "From",
  roiTitle2: "20 minutes",
  roiTitle3: "3 minutes",
  roiTitle4: "per claim file",
  roiDesc:
    "API compute cost of a few cents per claim is justified if it prevents a single fictitious claim worth millions of rupiah.",
  roiStats: [
    { before: "20 min", after: "3 min", label: "Per-claim file review" },
    { before: "1,000", after: "~6,700", label: "Effective verifier capacity" },
    { before: "≤ 3×24h", after: "Realtime", label: "Breach reporting (PDP Law)" },
    { before: "Manual", after: "XAI + HITL", label: "Final decision mode" },
  ],
  roiSavingsTitle: "Estimated annual savings",
  roiSavingsSub: "/ pilot FKRTL",
  roiSavingsDesc: "Assumes 3% fraud rate on surgery billing; basis 5 referral FKRTL.",
  roadmapBadge: "Implementation Blueprint",
  roadmapTitle: "Four-Phase Roadmap (v2.1)",
  roadmapPhases: [
    {
      phase: "Phase 0",
      period: "Week 1",
      title: "Data Foundation & Audit v2.1",
      items: ["Dataset v2.1 (300 claims, seed 20260707)", "Block leakage columns (configs/leakage.yaml)", "Group-aware evaluation (GroupKFold & LOGO)"],
    },
    {
      phase: "Phase 1",
      period: "Weeks 2–3",
      title: "Tabular & ML Baselines",
      items: ["XGBoost + SMOTE & PyTorch MLP baselines", "Feature engineering (30-day aggregate & tariff ratios)", "Initial AUPRC benchmark at 3–7% prevalence"],
    },
    {
      phase: "Phase 2",
      period: "Weeks 4–6",
      title: "Heterogeneous Graph & MHGSL",
      items: ["PyG HeteroData construction (3 parallel channels)", "Dual GCN (Channel-Specific & Shared-Parameter)", "Per-channel SHAP module & TreeExplainer"],
    },
    {
      phase: "Phase 3",
      period: "Weeks 7–8",
      title: "Final Validation & 5-FKRTL Pilot",
      items: ["Text & sentiment Late Fusion (γ = 0.10)", "9 fraud syndicate benchmark (SYND-01 to SYND-09)", "Operational pilot across 5 JKN referral facilities"],
    },
  ],

  footerTagline: "MHGSL · Fraud Intelligence",
  footerDesc:
    "Interactive visualization of Multi-channel Heterogeneous Graph Structure Learning & Graph Neural Networks for fraud detection in Indonesia's National Health Insurance ecosystem.",
  footerPrivacyBadge: "Privacy-by-design",
  footerHitlBadge: "Human-in-the-loop",
  footerModulViz: "Visualization Modules",
  footerSumber: "Knowledge Sources",
  footerEco: "Reference Ecosystem",
  footerModulItems: [
    { label: "Risk Taxonomy", href: "#problem" },
    { label: "Architecture Pipeline", href: "#architecture" },
    { label: "Multi-Channel Graph", href: "#graph" },
    { label: "Upcoding Simulation", href: "#simulation" },
  ],
  footerSumberItems: [
    { label: "Oasis Simulation Results (v2.1)", href: "/simulasi" },
    { label: "Notion Dataset (300 Claims)", href: "/dataset" },
    { label: "Mathematical Formulation", href: "#math" },
    { label: "Method Benchmark", href: "#compare" },
    { label: "Fraud Ring Detection", href: "#ring" },
    { label: "Roadmap & ROI", href: "#top" },
  ],
  footerEcoItems: [
    { label: "SATUSEHAT FHIR R4", href: "https://satusehat.kemkes.go.id" },
    { label: "BPJS Health V-Claim", href: "https://vclaim.bpjs-kesehatan.go.id" },
    { label: "PDP Law No. 27/2022", href: "https://jdih.kominfo.go.id" },
    { label: "Healthkathon BPJS 2026", href: "#" },
  ],
  footerCopyright: "© 2026 Aegis-JKN · Healthkathon BPJS Health",
  footerBackTop: "Back to top ↑",
  footerSource: "Source code",
  footerDisclaimer:
    "All visualized data is synthetic generated via DP-CTGAN for educational & prototype purposes—not real member data, per PDP Law No. 27/2022 compliance.",

  themeDark: "Switch to dark mode",
  themeLight: "Switch to light mode",
};

export const DICTS: Record<Lang, Dict> = { id, en };

// ----- React context -----
const LangContext = React.createContext<{
  lang: Lang;
  setLang: (l: Lang) => void;
  t: Dict;
}>({
  lang: "id",
  setLang: () => {},
  t: id,
});

export function LangProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLangState] = React.useState<Lang>("id");
  React.useEffect(() => {
    const stored = (typeof window !== "undefined" && localStorage.getItem("aegis-lang")) as Lang | null;
    if (stored === "id" || stored === "en") setLangState(stored);
  }, []);
  const setLang = (l: Lang) => {
    setLangState(l);
    if (typeof window !== "undefined") localStorage.setItem("aegis-lang", l);
  };
  return (
    <LangContext.Provider value={{ lang, setLang, t: DICTS[lang] }}>
      {children}
    </LangContext.Provider>
  );
}

export function useLang() {
  return React.useContext(LangContext);
}
