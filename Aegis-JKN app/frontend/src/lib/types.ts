export type RiskLevel = "fraud" | "high" | "medium" | "low";
export type ClaimStatus = "escalate" | "review" | "auto_clear";
export type ServiceType = "rawat inap" | "rawat jalan";
export type HitlAction = "APPROVE" | "CLARIFY_RS" | "ESCALATE_P2PK";
export type LayoutMode = "dual" | "full-queue" | "full-detail";
export type DetailTab = "emr" | "ai" | "flow" | "graphiti" | "audit";
export type DatasetSource = "synthetic" | "bpjs-real";

export interface RawClaim {
  Name: string;
  Tanggal: string;
  Status: string;
  Risiko: string;
  "Skor Fraud": number;
  Modus: string | null;
  Sindikat: string | null;
  Faskes: string;
  Layanan: string;
  Pasien: string;
  Dokter: string;
  "Diagnosis ICD-10": string;
  "Prosedur ICD-9-CM": string;
  "Biaya Rp": number;
  "LOS hari": number;
  Obat: string;
  Rujukan: string;
  "Alasan Berobat": string;
  "Narasi Rekam Medis": string;
  "Kontradiksi Narasi": boolean;
  "Umpan Balik Pasien": string;
  Sentimen: string;
  "Skor Sentimen": number;
  "Sinyal SHAP": string;
  "Kontribusi Saluran": string;
  Alasan: string;
  Catatan: string;
  "Notion ID"?: string;
}

export interface ThreeChannelScore {
  topology: number;
  feature: number;
  semantic: number;
  rawString: string;
}

export interface Claim {
  id: string; // e.g. "KLM001"
  date: string;
  status: ClaimStatus;
  risk: RiskLevel;
  fraudScore: number;
  modus: string | null;
  syndicate: string | null;
  hospital: string;
  serviceType: ServiceType;
  patient: string;
  doctor: string;
  diagnosisIcd10: string;
  procedureIcd9: string;
  costRp: number;
  losDays: number;
  drugs: string;
  referral: string;
  chiefComplaint: string;
  clinicalNarrative: string;
  hasContradiction: boolean;
  patientFeedback: string;
  sentiment: string;
  sentimentScore: number;
  shapSignal: string;
  channelContribution: ThreeChannelScore;
  aiReasoning: string;
  notes: string;
  notionId?: string;
  verifiedStatus?: HitlAction | null;
}

export interface AuditLogEntry {
  id: string;
  timestamp: string;
  timestampIso?: string;
  claimId?: string;
  targetClaimId?: string;
  action: HitlAction | string;
  verifierId?: string;
  actor?: string;
  note?: string;
  aiScore?: number;
  modus?: string | null;
  syndicate?: string | null;
  hash: string;
  prevHash: string;
  signature: string;
  verified?: boolean;
}

export type SentimentType = "positif" | "netral" | "negatif";

export interface ClaimRecord {
  id: string;
  notionId: string;
  tanggal: string;
  pasien: string;
  dokter: string;
  faskes: string;
  layanan: "rawat inap" | "rawat jalan";
  rujukan: string;
  alasanBerobat: string;
  diagnosisIcd10: string;
  prosedurIcd9: string;
  obat: string;
  losHari: number;
  biayaRp: number;
  narasiRekamMedis: string;
  umpanBalikPasien: string;
  sentimen: SentimentType;
  skorSentimen: number;
  skorFraud: number;
  risiko: RiskLevel;
  status: ClaimStatus;
  modus: string | null;
  sindikat: string | null;
  sinyalShap: string;
  kontribusiSaluran: string;
  kontradiksiNarasi: boolean;
  alasan: string;
  catatan: string;
}

export type ResearchCategory =
  | "Teknologi AI"
  | "Metrik & Validasi"
  | "Regulasi & Kepatuhan"
  | "Roadmap & Operasional"
  | "Ekonomi & ROI"
  | "Sumber Data & Interoperabilitas"
  | "Modus Fraud"
  | "Konteks & Statistik";

export type RelevanceLevel = "Kritis" | "Tinggi" | "Pendukung";
export type VerificationStatus = "Terverifikasi" | "Perlu Verifikasi" | "Sebagian Terverifikasi";

export interface ResearchRecord {
  id: string;
  item: string;
  kategori: ResearchCategory;
  relevansi: RelevanceLevel;
  statusVerifikasi: VerificationStatus;
  sumberRiset: string | null;
  deskripsi: string;
  pendekatanTeknis: string;
  catatanRiset: string;
  notionUrl: string;
}

export interface FilterOptions {
  search: string;
  risk: string; // "all" | RiskLevel
  status: string; // "all" | ClaimStatus
  modus: string; // "all" | modus string
  syndicate: string; // "all" | "SYND-01" etc
  serviceType: string; // "all" | ServiceType
  contradictionOnly: boolean;
  sortBy: "score-desc" | "score-asc" | "cost-desc" | "cost-asc" | "date-desc";
}

export interface GraphitiNode {
  id: string;
  label: string;
  type: "patient" | "doctor" | "hospital" | "diagnosis" | "procedure";
  risk?: RiskLevel;
  detail?: string;
}

export interface GraphitiEdge {
  source: string;
  target: string;
  label: string;
  channel: "topology" | "feature" | "semantic";
  weight?: number;
}
