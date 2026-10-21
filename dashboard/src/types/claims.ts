export type RiskLevel = 'low' | 'medium' | 'high' | 'fraud'
export type TriageStatus = 'auto_clear' | 'review' | 'escalate'
export type Channel = 'topology' | 'feature' | 'semantic'

export interface RawClaim {
  Name: string
  Tanggal: string
  Status: TriageStatus
  Risiko: RiskLevel
  'Skor Fraud': number
  Modus: string
  Sindikat: string
  Faskes: string
  Layanan: string
  Pasien: string
  Dokter: string
  'Diagnosis ICD-10': string
  'Prosedur ICD-9-CM': string
  'Biaya Rp': number
  'LOS hari': number
  Obat: string
  Rujukan: string
  'Alasan Berobat': string
  'Narasi Rekam Medis': string
  'Kontradiksi Narasi': boolean
  'Umpan Balik Pasien': string
  Sentimen: string
  'Skor Sentimen': number
  'Sinyal SHAP': string
  'Kontribusi Saluran': string
  Alasan: string
  Catatan: string
  'Notion ID': string
}

export interface Person {
  display: string
  pseudonymId?: string
}

export interface ClinicalCode {
  raw: string
  code?: string
  label?: string
}

export interface ChannelContribution {
  topology: number
  feature: number
  semantic: number
}

export interface ShapEvidence {
  raw: string
  hasDominantSignal: boolean
  clauses: string[]
}

export interface Claim {
  id: string
  date: string
  triageStatus: TriageStatus
  risk: RiskLevel
  fraudScore: number
  mode?: string
  syndromeId?: string
  hospital: string
  service: string
  patient: Person
  doctor: Person
  icd10Diagnosis: ClinicalCode
  icd9cmProcedure?: ClinicalCode
  claimedAmount: number
  lengthOfStayDays: number
  medication: string
  referral: string
  visitReason: string
  clinicalNarrative: string
  narrativeContradiction: boolean
  patientFeedback: string
  sentiment: string
  sentimentScore: number
  shapEvidence: ShapEvidence
  channelContribution?: ChannelContribution
  channelContributionRaw: string
  reason: string
  notes: string
  provenanceId: string
}

export type RiskBadge = 'Safe' | 'Review' | 'Escalate' | 'Syndicate'
export type AuditAction = 'approve' | 'request_confirmation' | 'reject'

export interface AuditLogEntry {
  id: string
  timestamp: string
  claimId: string
  action: AuditAction
  note: string
  aiScore: number
}
