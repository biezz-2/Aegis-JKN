export type RiskLevel = "low" | "medium" | "high" | "fraud";
export type ClaimStatus = "auto_clear" | "review" | "escalate";
export type SentimentType = "positif" | "netral" | "negatif";

export interface ClaimRecord {
  id: string; // e.g. KLM001 - KLM300
  notionId: string;
  tanggal: string; // YYYY-MM-DD
  pasien: string;
  dokter: string;
  faskes: string;
  layanan: "rawat inap" | "rawat jalan" | string;
  rujukan: string;
  alasanBerobat: string;
  diagnosisIcd10: string;
  prosedurIcd9: string;
  obat: string;
  losHari: number;
  biayaRp: number;
  narasiRekamMedis: string;
  umpanBalikPasien: string;
  sentimen: SentimentType | string;
  skorSentimen: number;
  skorFraud: number;
  risiko: RiskLevel | string;
  status: ClaimStatus | string;
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
  | "Konteks & Statistik"
  | string;

export type RelevanceLevel = "Kritis" | "Tinggi" | "Pendukung" | string;
export type VerificationStatus = "Terverifikasi" | "Perlu Verifikasi" | "Sebagian Terverifikasi" | string;

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
