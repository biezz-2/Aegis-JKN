import rawData from '@/data/klaim-aegis-jkn-dataset.json'
import type {
  ChannelContribution,
  Claim,
  ClinicalCode,
  RawClaim,
  RiskBadge,
  RiskLevel,
  ShapEvidence,
  TriageStatus,
} from '@/types/claims'

export const SOURCE_DATASET_HASH = '2b8c4113da2dd742075282865b9075eb14061a8eea81a2f3da0035cbbae79d9a'
export const SOURCE_RECORD_COUNT = 300

const CHANNEL_RE = /^\s*T\s+([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*·\s*F\s+([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*·\s*S\s+([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*$/i
const NO_DOMINANT_SHAP = 'tidak ada sinyal dominan'
const RISK_WEIGHT: Record<RiskLevel, number> = { low: 0, medium: 1, high: 2, fraud: 3 }

export interface ClaimFilters {
  risk?: RiskLevel | 'all'
  contradiction?: 'all' | 'yes' | 'no'
  syndrome?: 'all' | 'yes'
  query?: string
}

function parsePerson(display: string) {
  const match = /^([^\s]+)\s*\((.+)\)$/.exec(display.trim())
  return match ? { pseudonymId: match[1], display } : { display }
}

function parseCode(raw: string): ClinicalCode | undefined {
  if (!raw || raw.trim() === '—') return undefined
  const [code, ...label] = raw.split(' - ')
  return { raw, code: code.trim(), label: label.join(' - ').trim() || undefined }
}

export function parseChannelContribution(raw: unknown): ChannelContribution | undefined {
  if (typeof raw !== 'string') return undefined
  const match = CHANNEL_RE.exec(raw)
  if (!match) return undefined
  const [topology, feature, semantic] = match.slice(1).map(Number)
  if (![topology, feature, semantic].every(Number.isFinite)) return undefined
  return { topology, feature, semantic }
}

export function parseShapEvidence(raw: unknown): ShapEvidence {
  const value = typeof raw === 'string' ? raw.trim() : ''
  if (!value || value.toLocaleLowerCase('id-ID') === NO_DOMINANT_SHAP) {
    return { raw: value, hasDominantSignal: false, clauses: [] }
  }
  return {
    raw: value,
    hasDominantSignal: true,
    clauses: value.split(/\s*;\s*/).map((item) => item.trim()).filter(Boolean),
  }
}

export function normalizeClaim(raw: RawClaim): Claim {
  return {
    id: raw.Name,
    date: raw.Tanggal,
    triageStatus: raw.Status,
    risk: raw.Risiko,
    fraudScore: raw['Skor Fraud'],
    mode: raw.Modus || undefined,
    syndromeId: raw.Sindikat || undefined,
    hospital: raw.Faskes,
    service: raw.Layanan,
    patient: parsePerson(raw.Pasien),
    doctor: parsePerson(raw.Dokter),
    icd10Diagnosis: parseCode(raw['Diagnosis ICD-10']) ?? { raw: raw['Diagnosis ICD-10'] },
    icd9cmProcedure: parseCode(raw['Prosedur ICD-9-CM']),
    claimedAmount: raw['Biaya Rp'],
    lengthOfStayDays: raw['LOS hari'],
    medication: raw.Obat,
    referral: raw.Rujukan,
    visitReason: raw['Alasan Berobat'],
    clinicalNarrative: raw['Narasi Rekam Medis'],
    narrativeContradiction: raw['Kontradiksi Narasi'],
    patientFeedback: raw['Umpan Balik Pasien'],
    sentiment: raw.Sentimen,
    sentimentScore: raw['Skor Sentimen'],
    shapEvidence: parseShapEvidence(raw['Sinyal SHAP']),
    channelContribution: parseChannelContribution(raw['Kontribusi Saluran']),
    channelContributionRaw: raw['Kontribusi Saluran'],
    reason: raw.Alasan,
    notes: raw.Catatan,
    provenanceId: raw['Notion ID'],
  }
}

export const claims = (rawData as RawClaim[]).map(normalizeClaim)

export function validateSource(records: RawClaim[]): string[] {
  const errors: string[] = []
  if (records.length !== SOURCE_RECORD_COUNT) errors.push(`Expected ${SOURCE_RECORD_COUNT} records, received ${records.length}.`)
  for (const [index, record] of records.entries()) {
    if (!record.Name || !Number.isFinite(record['Skor Fraud']) || !Number.isFinite(record['Biaya Rp'])) {
      errors.push(`Invalid required claim fields at index ${index}.`)
    }
  }
  return errors
}

export function filterClaims(items: Claim[], filters: ClaimFilters): Claim[] {
  const query = filters.query?.trim().toLocaleLowerCase('id-ID')
  return items.filter((claim) => {
    if (filters.risk && filters.risk !== 'all' && claim.risk !== filters.risk) return false
    if (filters.contradiction === 'yes' && !claim.narrativeContradiction) return false
    if (filters.contradiction === 'no' && claim.narrativeContradiction) return false
    if (filters.syndrome === 'yes' && !claim.syndromeId) return false
    if (!query) return true
    return [claim.id, claim.patient.display, claim.doctor.display, claim.hospital, claim.icd10Diagnosis.raw, claim.icd9cmProcedure?.raw, claim.mode, claim.syndromeId]
      .filter(Boolean)
      .join(' ')
      .toLocaleLowerCase('id-ID')
      .includes(query)
  })
}

export function sortByPriority(items: Claim[]): Claim[] {
  return [...items].sort((a, b) => b.fraudScore - a.fraudScore || RISK_WEIGHT[b.risk] - RISK_WEIGHT[a.risk] || a.id.localeCompare(b.id))
}

export function deriveRiskBadge(claim: Claim): RiskBadge {
  if (claim.syndromeId) return 'Syndicate'
  if (claim.triageStatus === 'escalate') return 'Escalate'
  if (claim.triageStatus === 'review') return 'Review'
  return 'Safe'
}

export function labelTriage(status: TriageStatus) {
  return { auto_clear: 'Auto-clear (rekomendasi)', review: 'Telaah (rekomendasi)', escalate: 'Eskalasi (rekomendasi)' }[status]
}

export function formatCurrency(value: number) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(value)
}

export function relatedSyndicateClaims(claim: Claim): Claim[] {
  return claim.syndromeId ? claims.filter((item) => item.syndromeId === claim.syndromeId) : []
}
