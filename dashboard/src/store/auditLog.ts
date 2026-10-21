import { writable } from 'svelte/store'
import { SOURCE_DATASET_HASH } from '@/lib/claims'
import type { AuditAction, AuditLogEntry } from '@/types/claims'

const STORAGE_KEY = `aegis-jkn:audit:${SOURCE_DATASET_HASH}`

/** localStorage is absent during SSR and in non-browser test environments. */
const hasStorage = typeof localStorage !== 'undefined'

export function createAuditEntry(
  claimId: string,
  action: AuditAction,
  note: string,
  aiScore: number,
): AuditLogEntry | undefined {
  const trimmedNote = note.trim()
  if (!trimmedNote) return undefined

  return {
    id: crypto.randomUUID(),
    timestamp: new Date().toISOString(),
    claimId,
    action,
    note: trimmedNote,
    aiScore,
  }
}

function loadEntries(): AuditLogEntry[] {
  if (!hasStorage) return []
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? (JSON.parse(saved) as AuditLogEntry[]) : []
  } catch {
    return []
  }
}

export const auditLog = writable<AuditLogEntry[]>(loadEntries())

if (hasStorage) {
  auditLog.subscribe((entries) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries))
  })
}

/** Appends a decision. Returns false when the verifier note is empty. */
export function recordAudit(claimId: string, action: AuditAction, note: string, aiScore: number): boolean {
  const entry = createAuditEntry(claimId, action, note, aiScore)
  if (!entry) return false
  auditLog.update((current) => [...current, entry])
  return true
}
