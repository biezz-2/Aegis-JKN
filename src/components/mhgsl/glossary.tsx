"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { BookOpen, Search, X } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useLang } from "./i18n";

interface Term {
  key: string;
  category: "data" | "method" | "metric" | "regulation" | "system";
  term_id: string;
  term_en: string;
  short_id: string;
  short_en: string;
  long_id: string;
  long_en: string;
}

const TERMS: Term[] = [
  {
    key: "fhir",
    category: "data",
    term_id: "HL7 FHIR R4",
    term_en: "HL7 FHIR R4",
    short_id: "Standar pertukaran data medis elektronik internasional.",
    short_en: "International electronic medical data exchange standard.",
    long_id:
      "Fast Healthcare Interoperability Resources Release 4 — protokol HL7 yang dipakai SATUSEHAT untuk merepresentasikan Encounter, Condition (ICD-10), MedicationRequest, Composition sebagai resource JSON yang saling tertaut.",
    long_en:
      "Fast Healthcare Interoperability Resources Release 4 — HL7 protocol used by SATUSEHAT to represent Encounter, Condition (ICD-10), MedicationRequest, Composition as interlinked JSON resources.",
  },
  {
    key: "icd10",
    category: "data",
    term_id: "ICD-10",
    term_en: "ICD-10",
    short_id: "Kode diagnosis medis WHO (10th revision).",
    short_en: "WHO medical diagnosis codes (10th revision).",
    long_id:
      "International Classification of Diseases v10 — sistem koding diagnosis yang dipakai seluruh faskes Indonesia. Pada upcoding, diagnosis ringan (mis. J03.9 tonsilitis) diklaim sebagai diagnosis berat agar tarif INA-CBG lebih tinggi.",
    long_en:
      "International Classification of Diseases v10 — diagnosis coding system used across all Indonesian facilities. In upcoding, mild diagnoses (e.g. J03.9 tonsillitis) are billed as severe to inflate INA-CBG tariff.",
  },
  {
    key: "icd9cm",
    category: "data",
    term_id: "ICD-9-CM",
    term_en: "ICD-9-CM",
    short_id: "Kode tindakan/prosedur medis.",
    short_en: "Medical procedure/action codes.",
    long_id:
      "International Classification of Diseases, 9th Revision, Clinical Modification — kode tindakan medis (operasi, prosedur diagnostik). Inkonsistensi antara ICD-10 diagnosis dan ICD-9-CM tindakan adalah sinyal kuat upcoding.",
    long_en:
      "International Classification of Diseases, 9th Revision, Clinical Modification — medical procedure codes (surgery, diagnostic procedures). Inconsistency between ICD-10 diagnosis and ICD-9-CM procedure is a strong upcoding signal.",
  },
  {
    key: "inacbg",
    category: "system",
    term_id: "INA-CBG",
    term_en: "INA-CBG",
    short_id: "Sistem pembayaran kapitasi berbasis kasus (case-mix).",
    short_en: "Case-based capitation payment system.",
    long_id:
      "Indonesia Case Base Groups — skema pembayaran JKN berbasis tingkat keparahan diagnosis. Tarif ditentukan oleh kode CBG. Upcoding meningkatkan tarif dengan menggeser kode ke severity lebih tinggi.",
    long_en:
      "Indonesia Case Base Groups — JKN payment scheme based on diagnosis severity. Tariff is set by CBG code. Upcoding increases tariff by shifting code to higher severity.",
  },
  {
    key: "shap",
    category: "method",
    term_id: "SHAP",
    term_en: "SHAP",
    short_id: "Explainable AI: kontribusi marjinal tiap fitur.",
    short_en: "Explainable AI: marginal contribution per feature.",
    long_id:
      "SHapley Additive exPlanations — metode game-theoretic yang menghitung kontribusi tiap variabel input terhadap prediksi model. Mengatasi alert fatigue dengan menunjukkan *mengapa* sebuah klaim ditandai fraud.",
    long_en:
      "SHapley Additive exPlanations — game-theoretic method computing each input variable's contribution to a model prediction. Solves alert fatigue by showing *why* a claim was flagged as fraud.",
  },
  {
    key: "xgboost",
    category: "method",
    term_id: "XGBoost",
    term_en: "XGBoost",
    short_id: "Baseline ML untuk klasifikasi data tabular.",
    short_en: "Baseline ML for tabular classification.",
    long_id:
      "Extreme Gradient Boosting — ansambel pohon keputusan sekuensial yang mengoreksi residual prediksi sebelumnya. Standar industri untuk data tabular; memproses tiap baris secara independen tanpa relasi antar-entitas.",
    long_en:
      "Extreme Gradient Boosting — sequential decision-tree ensemble correcting previous prediction residuals. Industry standard for tabular data; processes each row independently without inter-entity relations.",
  },
  {
    key: "gnn",
    category: "method",
    term_id: "GNN",
    term_en: "GNN",
    short_id: "Neural network yang beroperasi pada graf.",
    short_en: "Neural network operating on graphs.",
    long_id:
      "Graph Neural Network — arsitektur yang mempelajari representasi simpul via message-passing antar-tetangga. Mendeteksi fraud rings & sindikat kolusi yang tidak terlihat di model tabular.",
    long_en:
      "Graph Neural Network — architecture learning node representations via message-passing among neighbors. Detects fraud rings & collusion syndicates invisible to tabular models.",
  },
  {
    key: "mhgsl",
    category: "method",
    term_id: "MHGSL",
    term_en: "MHGSL",
    short_id: "Multi-channel Heterogeneous Graph Structure Learning.",
    short_en: "Multi-channel Heterogeneous Graph Structure Learning.",
    long_id:
      "Metode GNN yang membangun 3 saluran graf paralel (topologi, fitur, semantik) + GCN parameter bersama. Mendominasi AUPRC pada dataset fraud asuransi dengan menangkap pola lintas-perspektif.",
    long_en:
      "GNN method building 3 parallel graph channels (topology, feature, semantic) + shared-parameter GCN. Dominates AUPRC on insurance fraud datasets by capturing cross-perspective patterns.",
  },
  {
    key: "metapath",
    category: "method",
    term_id: "Metapath ℳ",
    term_en: "Metapath ℳ",
    short_id: "Jalur relasi berurutan antar tipe simpul.",
    short_en: "Sequential relation path between node types.",
    long_id:
      "Contoh: Dokter → Diagnosis → Prosedur → Faskes. Pola metapath berulang pada subgraf padat mengindikasikan kolusi terstruktur—jauh lebih kuat dari sekadar inspeksi edge tunggal.",
    long_en:
      "Example: Doctor → Diagnosis → Procedure → Facility. Repeated metapath patterns in dense subgraphs indicate structured collusion—far stronger than inspecting single edges.",
  },
  {
    key: "auprc",
    category: "metric",
    term_id: "AUPRC",
    term_en: "AUPRC",
    short_id: "Area Under Precision-Recall Curve.",
    short_en: "Area Under Precision-Recall Curve.",
    long_id:
      "Metrik utama untuk dataset tidak seimbang (fraud ≪ non-fraud). AUPRC tinggi = sedikit false negatives (fraud lolos) dan false positives (alarm palsu). MHGSL mencapai 0.91 vs XGBoost 0.71.",
    long_en:
      "Primary metric for imbalanced datasets (fraud ≪ non-fraud). High AUPRC = few false negatives (missed fraud) and false positives (false alarms). MHGSL achieves 0.91 vs XGBoost 0.71.",
  },
  {
    key: "f1",
    category: "metric",
    term_id: "F1-Score",
    term_en: "F1-Score",
    short_id: "Harmonic mean Precision × Recall.",
    short_en: "Harmonic mean of Precision × Recall.",
    long_id:
      "F1 = 2·(P·R)/(P+R). Menyeimbangkan minimasi alarm palsu (Precision) dan fraud lolos (Recall). Cocok saat kelas fraud minoritas dan kedua jenis error sama-sama merugikan.",
    long_en:
      "F1 = 2·(P·R)/(P+R). Balances false alarms (Precision) and missed fraud (Recall). Suitable when fraud class is minority and both error types are costly.",
  },
  {
    key: "uupdp",
    category: "regulation",
    term_id: "UU PDP No. 27/2022",
    term_en: "PDP Law No. 27/2022",
    short_id: "Undang-Undang Perlindungan Data Pribadi.",
    short_en: "Personal Data Protection Law.",
    long_id:
      "Pasal 4(2): data kesehatan, biometrik, genetika = 'Data Pribadi Spesifik' dengan standar kepatuhan tertinggi: persetujuan eksplipit, enkripsi, DPO, pelaporan kebocoran 3×24 jam. Pelanggaran: pidana 5–6 tahun + denda miliaran rupiah.",
    long_en:
      "Article 4(2): health, biometric, genetic data = 'Specific Personal Data' with highest compliance standards: explicit consent, encryption, DPO, 3×24h breach reporting. Violations: 5–6 years imprisonment + billion-rupiah fines.",
  },
  {
    key: "dpctgan",
    category: "method",
    term_id: "DP-CTGAN",
    term_en: "DP-CTGAN",
    short_id: "Generator data sintetis privacy-by-design.",
    short_en: "Privacy-by-design synthetic data generator.",
    long_id:
      "Differential Private Conditional Tabular GAN — model generatif yang mempelajari distribusi statistik historis dan menghasilkan jutaan baris rekam medis sintetis yang valid secara matematis namun mustahil direverse-engineer untuk melacak identitas pasien asli.",
    long_en:
      "Differential Private Conditional Tabular GAN — generative model learning historical statistical distributions and producing millions of synthetic medical records valid mathematically but impossible to reverse-engineer for original patient identity.",
  },
  {
    key: "hitl",
    category: "system",
    term_id: "Human-in-the-Loop (HITL)",
    term_en: "Human-in-the-Loop (HITL)",
    short_id: "AI sebagai augmentasi auditor, bukan pengganti.",
    short_en: "AI as auditor augmentation, not replacement.",
    long_id:
      "Paradigma di mana AI melakukan pra-penyaringan 100% volume klaim dan mengeskalasi anomali ke verifikator manusia. Keputusan akhir (konfirmasi fraud / penolakan alarm palsu) tetap di tangan auditor—kepatuhan etis & hukum.",
    long_en:
      "Paradigm where AI pre-screens 100% of claim volume and escalates anomalies to human verifiers. Final decision (confirm fraud / dismiss false alarm) stays with the auditor—ethical & legal compliance.",
  },
  {
    key: "fornas",
    category: "system",
    term_id: "FORNAS",
    term_en: "FORNAS",
    short_id: "Formularium Nasional daftar obat essensial.",
    short_en: "National Formulary essential drug list.",
    long_id:
      "Formularium Nasional — daftar obat essensial yang ditanggung JKN. Validasi peresepan terhadap FORNAS mendeteksi drug diversion (penumpukan obat kronis untuk dijual kembali).",
    long_en:
      "National Formulary — list of essential drugs covered by JKN. Validating prescriptions against FORNAS detects drug diversion (hoarding chronic meds for resale).",
  },
  {
    key: "fkrtl",
    category: "system",
    term_id: "FKRTL",
    term_en: "FKRTL",
    short_id: "Fasilitas Kesehatan Rujukan Tingkat Lanjut.",
    short_en: "Advanced Referral Health Facility.",
    long_id:
      "Rumah sakit dan klinik rujukan tingkat lanjut. Area dengan potensi kebocoran finansial JKN terbesar (Phantom Billing, Upcoding, Unbundling, Prolonged Stay). Fokus utama solusi Aegis-JKN.",
    long_en:
      "Hospitals and advanced referral clinics. The largest JKN financial leakage area (Phantom Billing, Upcoding, Unbundling, Prolonged Stay). Primary focus of Aegis-JKN solution.",
  },
];

const categoryColor: Record<Term["category"], string> = {
  data: "oklch(0.55 0.14 165)",
  method: "oklch(0.62 0.13 200)",
  metric: "oklch(0.7 0.16 70)",
  regulation: "oklch(0.62 0.22 20)",
  system: "oklch(0.5 0.13 280)",
};

const categoryLabel: Record<Term["category"], { id: string; en: string }> = {
  data: { id: "Data", en: "Data" },
  method: { id: "Metode", en: "Method" },
  metric: { id: "Metrik", en: "Metric" },
  regulation: { id: "Regulasi", en: "Regulation" },
  system: { id: "Sistem", en: "System" },
};

export function GlossaryButton() {
  const { lang } = useLang();
  const [open, setOpen] = React.useState(false);
  const [query, setQuery] = React.useState("");
  const [activeCategory, setActiveCategory] = React.useState<Term["category"] | "all">("all");

  const filtered = React.useMemo(() => {
    const q = query.toLowerCase().trim();
    return TERMS.filter((t) => {
      const matchesCat = activeCategory === "all" || t.category === activeCategory;
      const term = lang === "id" ? t.term_id : t.term_en;
      const short = lang === "id" ? t.short_id : t.short_en;
      const long = lang === "id" ? t.long_id : t.long_en;
      const matchesQuery =
        !q ||
        term.toLowerCase().includes(q) ||
        short.toLowerCase().includes(q) ||
        long.toLowerCase().includes(q) ||
        t.key.toLowerCase().includes(q);
      return matchesCat && matchesQuery;
    });
  }, [query, activeCategory, lang]);

  const tl = {
    title: lang === "id" ? "Glosarium Istilah" : "Term Glossary",
    desc:
      lang === "id"
        ? "Definisi istilah teknis di domain MHGSL & deteksi fraud JKN."
        : "Technical term definitions in the MHGSL & JKN fraud detection domain.",
    trigger: lang === "id" ? "Glosarium" : "Glossary",
    search: lang === "id" ? "Cari istilah..." : "Search terms...",
    all: lang === "id" ? "Semua" : "All",
    noResults: lang === "id" ? "Tidak ada istilah cocok." : "No matching terms.",
    resultsCount: (n: number) => `${n} ${lang === "id" ? "istilah" : "terms"}`,
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <button
          className="inline-flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/5 px-3 py-1.5 text-xs font-medium text-primary hover:bg-primary/10 transition-colors"
          title={tl.trigger}
        >
          <BookOpen className="h-3.5 w-3.5" />
          {tl.trigger}
        </button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto scrollbar-thin p-0 gap-0">
        <DialogHeader className="px-5 pt-5 pb-3 border-b border-border sticky top-0 bg-card z-10">
          <DialogTitle className="flex items-center gap-2 text-base">
            <span
              className="flex h-8 w-8 items-center justify-center rounded-lg shrink-0"
              style={{ background: "linear-gradient(135deg, var(--primary), var(--chart-2))" }}
            >
              <BookOpen className="h-4 w-4 text-white" />
            </span>
            <span>{tl.title}</span>
          </DialogTitle>
          <DialogDescription className="text-xs">{tl.desc}</DialogDescription>
          {/* Search + filters */}
          <div className="mt-3 space-y-2">
            <div className="relative">
              <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground pointer-events-none" />
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={tl.search}
                className="h-8 pl-8 text-xs"
              />
              {query && (
                <button
                  onClick={() => setQuery("")}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  <X className="h-3 w-3" />
                </button>
              )}
            </div>
            <div className="flex flex-wrap gap-1">
              <button
                onClick={() => setActiveCategory("all")}
                className={`rounded-full px-2.5 py-0.5 text-[10px] font-medium transition-colors ${
                  activeCategory === "all"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-muted-foreground hover:bg-accent"
                }`}
              >
                {tl.all}
              </button>
              {(Object.keys(categoryLabel) as Term["category"][]).map((cat) => {
                const isActive = activeCategory === cat;
                const color = categoryColor[cat];
                return (
                  <button
                    key={cat}
                    onClick={() => setActiveCategory(cat)}
                    className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[10px] font-medium transition-colors border"
                    style={
                      isActive
                        ? { background: color, color: "white", borderColor: color }
                        : { background: "transparent", color: color, borderColor: `${color}40` }
                    }
                  >
                    <span
                      className="h-1.5 w-1.5 rounded-full"
                      style={{ background: isActive ? "white" : color }}
                    />
                    {categoryLabel[cat][lang]}
                  </button>
                );
              })}
            </div>
          </div>
        </DialogHeader>

        <div className="p-4 space-y-2">
          <div className="text-[10px] text-muted-foreground uppercase tracking-wide">
            {tl.resultsCount(filtered.length)}
          </div>
          {filtered.length === 0 ? (
            <div className="text-center py-8 text-xs text-muted-foreground">
              {tl.noResults}
            </div>
          ) : (
            <AnimatePresence>
              {filtered.map((t, i) => {
                const color = categoryColor[t.category];
                const term = lang === "id" ? t.term_id : t.term_en;
                const short = lang === "id" ? t.short_id : t.short_en;
                const long = lang === "id" ? t.long_id : t.long_en;
                return (
                  <motion.div
                    key={t.key}
                    layout
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.2, delay: Math.min(i * 0.02, 0.2) }}
                    className="rounded-xl border-l-4 bg-card p-3 shadow-sm"
                    style={{ borderColor: color }}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <h3 className="text-sm font-bold">{term}</h3>
                          <Badge
                            variant="outline"
                            className="text-[9px] font-semibold uppercase"
                            style={{ color, borderColor: `${color}40` }}
                          >
                            {categoryLabel[t.category][lang]}
                          </Badge>
                        </div>
                        <p className="mt-1 text-xs text-foreground/80">{short}</p>
                        <p className="mt-1.5 text-[11px] leading-relaxed text-muted-foreground">
                          {long}
                        </p>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
