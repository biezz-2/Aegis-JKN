import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import rawData from '@/data/klaim-aegis-jkn-dataset.json'
import { claims, deriveRiskBadge, filterClaims, normalizeClaim, parseChannelContribution, parseShapEvidence, SOURCE_DATASET_HASH, sortByPriority, validateSource } from '@/lib/claims'
import { createAuditEntry } from '@/store/auditLog'
import type { RawClaim } from '@/types/claims'

describe('synthetic claim dataset contract', () => {
  it('keeps the canonical source hash, 300 records, and 28 fields', () => {
    const source = readFileSync(resolve(import.meta.dirname, '../../../docs/datasets/klaim-aegis-jkn-dataset.json'))
    expect(createHash('sha256').update(source).digest('hex')).toBe(SOURCE_DATASET_HASH)
    expect(rawData).toHaveLength(300)
    expect(Object.keys(rawData[0] ?? {})).toHaveLength(28)
    expect(validateSource(rawData as RawClaim[])).toEqual([])
  })

  it('normalizes empty syndrome and unavailable procedure without mutating raw data', () => {
    const raw = { ...(rawData as RawClaim[]).find((item) => item['Prosedur ICD-9-CM'] === '—')! }
    const original = structuredClone(raw)
    const claim = normalizeClaim(raw)
    expect(claim.icd9cmProcedure).toBeUndefined()
    expect(raw).toEqual(original)
  })

  it('parses three source channels but preserves SHAP prose as evidence', () => {
    expect(parseChannelContribution('T 0.31 · F 0.32 · S 0.31')).toEqual({ topology: 0.31, feature: 0.32, semantic: 0.31 })
    expect(parseChannelContribution('wrong')).toBeUndefined()
    expect(parseShapEvidence('tidak ada sinyal dominan').hasDominantSignal).toBe(false)
    expect(parseShapEvidence('sinyal satu; sinyal dua').clauses).toEqual(['sinyal satu', 'sinyal dua'])
  })

  it('filters and prioritizes claims deterministically', () => {
    const contradictions = filterClaims(claims, { contradiction: 'yes' })
    expect(contradictions).toHaveLength(12)
    const syndicates = filterClaims(claims, { syndrome: 'yes' })
    expect(syndicates).toHaveLength(36)
    const ordered = sortByPriority(claims)
    expect(ordered[0]?.fraudScore).toBeGreaterThanOrEqual(ordered[1]?.fraudScore ?? 0)
    expect(deriveRiskBadge(syndicates[0]!)).toBe('Syndicate')
  })

  it('requires a verifier note and creates an immutable decision record', () => {
    expect(createAuditEntry('KLM001', 'reject', '   ', 0.98)).toBeUndefined()
    const entry = createAuditEntry('KLM001', 'request_confirmation', '  Cek berkas pendukung.  ', 0.98)
    expect(entry).toMatchObject({
      claimId: 'KLM001',
      action: 'request_confirmation',
      note: 'Cek berkas pendukung.',
      aiScore: 0.98,
    })
    expect(entry?.id).toEqual(expect.any(String))
    expect(entry?.timestamp).toEqual(expect.any(String))
  })
})
