/**
 * Audit Log Types for Aegis-JKN Fraud Investigation
 * Immutable log viewer with cryptographic hash chain verification
 */

export type AuditEventType = 'CREATED' | 'SCORED' | 'REVIEWED' | 'DECISION';
export type AuditDecision = 'APPROVED' | 'DENIED' | 'FLAGGED' | 'PENDING';

export interface AuditLogEntry {
  id: string;
  timestamp: string; // ISO8601
  claimId: string;
  eventType: AuditEventType;
  payload: Record<string, unknown>;
  userId: string;
  providerId: string;
  decision?: AuditDecision;
  previousHash: string;
  hash: string;
}

export interface AuditFilters {
  dateRange?: { from: Date; to: Date };
  claimId?: string;
  providerId?: string;
  userId?: string;
  decision?: AuditDecision;
  eventType?: AuditEventType;
}

export interface AuditPagination {
  page: number;
  pageSize: number;
  total: number;
}

export interface AuditLogResponse {
  entries: AuditLogEntry[];
  pagination: AuditPagination;
}

export interface MerkleProof {
  leafIndex: number;
  leafHash: string;
  siblings: string[];
  root: string;
}

export interface ExportOptions {
  format: 'csv' | 'pdf';
  includeSignature: boolean;
  filters: AuditFilters;
  dateRange: { from: Date; to: Date };
}

export interface DigitalSignature {
  algorithm: 'RSA-SHA256' | 'HMAC-SHA256';
  signature: string;
  publicKey: string;
  signedAt: string;
  dataHash: string;
}

export const EVENT_TYPE_LABELS: Record<AuditEventType, string> = {
  CREATED: 'Claim Created',
  SCORED: 'Risk Scored',
  REVIEWED: 'Manual Review',
  DECISION: 'Decision Made',
};

export const EVENT_TYPE_COLORS: Record<AuditEventType, string> = {
  CREATED: 'bg-blue-500',
  SCORED: 'bg-yellow-500',
  REVIEWED: 'bg-purple-500',
  DECISION: 'bg-green-500',
};

export const DECISION_COLORS: Record<AuditDecision, string> = {
  APPROVED: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  DENIED: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  FLAGGED: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  PENDING: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
};