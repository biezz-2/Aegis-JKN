import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { AuditLogEntry, Claim, HitlAction } from "$lib/types";

// In Vite/SvelteKit, client public environment variables can come from import.meta.env
const supabaseUrl = (typeof import.meta !== "undefined" && import.meta.env?.PUBLIC_SUPABASE_URL) || "";
const supabaseAnonKey = (typeof import.meta !== "undefined" && import.meta.env?.PUBLIC_SUPABASE_ANON_KEY) || "";

export const isSupabaseConfigured = Boolean(supabaseUrl && supabaseAnonKey);

export const supabase: SupabaseClient | null = isSupabaseConfigured
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export interface SupabaseSyncStatus {
  configured: boolean;
  connected: boolean;
  endpoint: string;
  lastSyncTime: string | null;
  pendingCount: number;
  isSyncing: boolean;
  error?: string;
}

export interface QueueItem {
  id: string;
  type: "audit_log" | "claim_decision" | "graph_node";
  payload: Record<string, unknown>;
  timestamp: number;
  retryCount: number;
}

const QUEUE_STORAGE_KEY = "aegis_supabase_sync_queue";
const MAX_RETRIES = 5;
const PING_INTERVAL_MS = 20_000;

type SyncListener = (status: SupabaseSyncStatus) => void;
const syncListeners = new Set<SyncListener>();

export const syncState: SupabaseSyncStatus = {
  configured: isSupabaseConfigured,
  connected: false,
  endpoint: supabaseUrl || "http://localhost:8000 (Self-Hosted Demo)",
  lastSyncTime: null,
  pendingCount: 0,
  isSyncing: false,
};

function notifyListeners(): void {
  for (const listener of syncListeners) {
    try {
      listener({ ...syncState });
    } catch (err) {
      console.error("Error in syncListener:", err);
    }
  }
}

export function onSyncStateChange(callback: SyncListener): () => void {
  syncListeners.add(callback);
  callback({ ...syncState });
  return () => syncListeners.delete(callback);
}

// Local Storage Sync Queue Helpers
function loadQueue(): QueueItem[] {
  if (typeof window === "undefined" || !window.localStorage) return [];
  try {
    const raw = localStorage.getItem(QUEUE_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as QueueItem[]) : [];
  } catch (e) {
    console.warn("Failed reading sync queue from localStorage:", e);
    return [];
  }
}

function saveQueue(queue: QueueItem[]): void {
  if (typeof window === "undefined" || !window.localStorage) return;
  try {
    localStorage.setItem(QUEUE_STORAGE_KEY, JSON.stringify(queue));
    syncState.pendingCount = queue.length;
    notifyListeners();
  } catch (e) {
    console.warn("Failed saving sync queue to localStorage:", e);
  }
}

export function enqueueSyncItem(type: QueueItem["type"], payload: Record<string, unknown>): void {
  const queue = loadQueue();
  const newItem: QueueItem = {
    id: typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : `item-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    type,
    payload,
    timestamp: Date.now(),
    retryCount: 0,
  };
  queue.push(newItem);
  saveQueue(queue);
}

export function getPendingQueueCount(): number {
  return loadQueue().length;
}

export async function checkSupabaseConnection(): Promise<boolean> {
  if (!supabase) {
    syncState.connected = false;
    notifyListeners();
    return false;
  }
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    const { error } = await supabase.from("claims").select("count", { count: "exact", head: true }).abortSignal(controller.signal);
    clearTimeout(timeoutId);

    const wasConnected = syncState.connected;
    syncState.connected = !error;
    if (!error) {
      syncState.lastSyncTime = new Date().toLocaleTimeString("id-ID");
      syncState.error = undefined;
      // Flush pending queue automatically upon becoming online
      if (!wasConnected || syncState.pendingCount > 0) {
        void flushSyncQueue();
      }
    } else {
      syncState.error = error.message;
    }
    notifyListeners();
    return !error;
  } catch (err) {
    syncState.connected = false;
    syncState.error = err instanceof Error ? err.message : "Connection failed";
    notifyListeners();
    return false;
  }
}

export async function flushSyncQueue(): Promise<{ processed: number; remaining: number }> {
  if (!supabase || syncState.isSyncing) {
    return { processed: 0, remaining: getPendingQueueCount() };
  }

  const queue = loadQueue();
  if (queue.length === 0) {
    syncState.pendingCount = 0;
    notifyListeners();
    return { processed: 0, remaining: 0 };
  }

  syncState.isSyncing = true;
  notifyListeners();

  const remainingQueue: QueueItem[] = [];
  let processed = 0;

  for (const item of queue) {
    let success = false;
    try {
      if (item.type === "audit_log") {
        const { error } = await supabase.from("audit_logs").insert([item.payload]);
        if (!error) success = true;
      } else if (item.type === "claim_decision") {
        const { claim_id, ...updateFields } = item.payload;
        const { error } = await supabase.from("claims").update(updateFields).eq("claim_id", claim_id);
        if (!error) success = true;
      } else if (item.type === "graph_node") {
        const { error } = await supabase.from("graph_nodes").upsert([item.payload], { onConflict: "id" });
        if (!error) success = true;
      }
    } catch (err) {
      console.warn(`Error syncing item ${item.id}:`, err);
      success = false;
    }

    if (success) {
      processed++;
    } else {
      item.retryCount += 1;
      if (item.retryCount < MAX_RETRIES) {
        remainingQueue.push(item);
      } else {
        console.error(`Item ${item.id} exceeded max retries (${MAX_RETRIES}), dropped from sync queue.`);
      }
    }
  }

  saveQueue(remainingQueue);
  syncState.isSyncing = false;
  syncState.lastSyncTime = new Date().toLocaleTimeString("id-ID");
  notifyListeners();

  return { processed, remaining: remainingQueue.length };
}

export async function saveAuditLogToSupabase(entry: AuditLogEntry): Promise<{ success: boolean; queued?: boolean; error?: string }> {
  const record: Record<string, unknown> = {
    id: entry.id,
    timestamp: entry.timestamp,
    claim_id: entry.claimId || entry.targetClaimId,
    action: entry.action,
    verifier_id: entry.verifierId || entry.actor,
    note: entry.note,
    ai_score: entry.aiScore,
    modus: entry.modus,
    syndicate: entry.syndicate,
    sha256_hash: entry.hash,
    prev_hash: entry.prevHash,
    signature: entry.signature,
  };

  if (!supabase || !syncState.connected) {
    enqueueSyncItem("audit_log", record);
    return { success: true, queued: true };
  }

  try {
    const { error } = await supabase.from("audit_logs").insert([record]);
    if (error) {
      enqueueSyncItem("audit_log", record);
      return { success: true, queued: true, error: error.message };
    }
    syncState.lastSyncTime = new Date().toLocaleTimeString("id-ID");
    notifyListeners();
    return { success: true };
  } catch (err) {
    enqueueSyncItem("audit_log", record);
    const message = err instanceof Error ? err.message : "Error jaringan, disimpan ke antrean offline";
    return { success: true, queued: true, error: message };
  }
}

export async function syncClaimDecisionToSupabase(
  claimId: string,
  action: HitlAction,
  verifierNote: string
): Promise<{ success: boolean; queued?: boolean; error?: string }> {
  const payload: Record<string, unknown> = {
    claim_id: claimId,
    verified_status: action,
    verifier_note: verifierNote,
    verified_at: new Date().toISOString(),
  };

  if (!supabase || !syncState.connected) {
    enqueueSyncItem("claim_decision", payload);
    return { success: true, queued: true };
  }

  try {
    const { error } = await supabase
      .from("claims")
      .update({
        verified_status: payload.verified_status,
        verifier_note: payload.verifier_note,
        verified_at: payload.verified_at,
      })
      .eq("claim_id", claimId);

    if (error) {
      enqueueSyncItem("claim_decision", payload);
      return { success: true, queued: true, error: error.message };
    }
    return { success: true };
  } catch (err) {
    enqueueSyncItem("claim_decision", payload);
    const message = err instanceof Error ? err.message : "Error jaringan, disimpan ke antrean offline";
    return { success: true, queued: true, error: message };
  }
}

export async function syncGraphNodeToSupabase(
  node: { id: string; label: string; type: string; risk?: string; detail?: string; metadata?: Record<string, unknown> }
): Promise<{ success: boolean; queued?: boolean; error?: string }> {
  const payload: Record<string, unknown> = {
    id: node.id,
    label: node.label,
    type: node.type,
    risk: node.risk || null,
    detail: node.detail || null,
    metadata: node.metadata || {},
    updated_at: new Date().toISOString(),
  };

  if (!supabase || !syncState.connected) {
    enqueueSyncItem("graph_node", payload);
    return { success: true, queued: true };
  }

  try {
    const { error } = await supabase.from("graph_nodes").upsert([payload], { onConflict: "id" });
    if (error) {
      enqueueSyncItem("graph_node", payload);
      return { success: true, queued: true, error: error.message };
    }
    return { success: true };
  } catch (err) {
    enqueueSyncItem("graph_node", payload);
    const message = err instanceof Error ? err.message : "Error jaringan, disimpan ke antrean offline";
    return { success: true, queued: true, error: message };
  }
}

// Inisialisasi status antrean & periodik ping
type TimerHandle = number | NodeJS.Timeout;
let pingTimer: TimerHandle | undefined;

export function startPeriodicPing(intervalMs = PING_INTERVAL_MS): void {
  if (typeof window === "undefined") return;
  clearInterval(pingTimer);
  syncState.pendingCount = getPendingQueueCount();
  void checkSupabaseConnection();

  // Event listener browser online/offline
  window.addEventListener("online", () => {
    void checkSupabaseConnection();
    void flushSyncQueue();
  });
  window.addEventListener("offline", () => {
    syncState.connected = false;
    notifyListeners();
  });

  pingTimer = setInterval(() => {
    void checkSupabaseConnection();
  }, intervalMs);
}

export function stopPeriodicPing(): void {
  clearInterval(pingTimer);
  pingTimer = undefined;
}

// Jalankan ping periodik otomatis di lingkungan browser
if (typeof window !== "undefined") {
  startPeriodicPing();
}

/**
 * ============================================================================
 * DOKUMENTASI SKEMA MIGRASI SQL SUPABASE / POSTGRESQL SELF-HOSTED
 * ============================================================================
 * Simpan ke direktori migrasi (misal: migrations/20261025_supabase_schema.sql)
 *
 * ```sql
 * -- 1. TABEL CLAIMS
 * CREATE TABLE IF NOT EXISTS public.claims (
 *     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 *     claim_id VARCHAR(100) UNIQUE NOT NULL,
 *     patient_id VARCHAR(100),
 *     provider_id VARCHAR(100),
 *     patient_name VARCHAR(255),
 *     hospital_name VARCHAR(255),
 *     doctor_name VARCHAR(255),
 *     diagnosis_icd10 VARCHAR(50),
 *     procedure_icd9 VARCHAR(50),
 *     service_type VARCHAR(50),
 *     amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
 *     risk_score FLOAT DEFAULT 0.0,
 *     risk_level VARCHAR(50),
 *     modus VARCHAR(255),
 *     syndicate VARCHAR(100),
 *     verified_status VARCHAR(50),      -- 'APPROVE' | 'CLARIFY_RS' | 'ESCALATE_P2PK'
 *     verifier_note TEXT,
 *     verified_at TIMESTAMP WITH TIME ZONE,
 *     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
 *     updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
 * );
 *
 * CREATE INDEX IF NOT EXISTS idx_claims_claim_id ON public.claims(claim_id);
 * CREATE INDEX IF NOT EXISTS idx_claims_verified_status ON public.claims(verified_status);
 * CREATE INDEX IF NOT EXISTS idx_claims_risk_level ON public.claims(risk_level);
 *
 * -- 2. TABEL AUDIT LOGS (Append-Only Cryptographic Log)
 * CREATE TABLE IF NOT EXISTS public.audit_logs (
 *     id VARCHAR(100) PRIMARY KEY,
 *     timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
 *     claim_id VARCHAR(100),
 *     action VARCHAR(100) NOT NULL,
 *     verifier_id VARCHAR(100),
 *     note TEXT,
 *     ai_score FLOAT,
 *     modus VARCHAR(255),
 *     syndicate VARCHAR(100),
 *     sha256_hash VARCHAR(64) NOT NULL,
 *     prev_hash VARCHAR(64),
 *     signature TEXT,
 *     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
 * );
 *
 * CREATE INDEX IF NOT EXISTS idx_audit_logs_claim_id ON public.audit_logs(claim_id);
 * CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON public.audit_logs(timestamp);
 * CREATE INDEX IF NOT EXISTS idx_audit_logs_hash ON public.audit_logs(sha256_hash);
 *
 * -- 3. TABEL GRAPH NODES (Graphiti Bi-temporal / MiroFish Topology)
 * CREATE TABLE IF NOT EXISTS public.graph_nodes (
 *     id VARCHAR(100) PRIMARY KEY,
 *     label VARCHAR(255) NOT NULL,
 *     type VARCHAR(50) NOT NULL,       -- 'patient' | 'doctor' | 'hospital' | 'diagnosis' | 'procedure'
 *     risk VARCHAR(50),                -- 'fraud' | 'high' | 'medium' | 'low'
 *     detail TEXT,
 *     metadata JSONB DEFAULT '{}'::jsonb,
 *     valid_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
 *     invalid_at TIMESTAMP WITH TIME ZONE,
 *     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
 *     updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
 * );
 *
 * CREATE INDEX IF NOT EXISTS idx_graph_nodes_type ON public.graph_nodes(type);
 * CREATE INDEX IF NOT EXISTS idx_graph_nodes_risk ON public.graph_nodes(risk);
 * CREATE INDEX IF NOT EXISTS idx_graph_nodes_metadata ON public.graph_nodes USING GIN(metadata);
 *
 * -- Row Level Security (RLS) Policies
 * ALTER TABLE public.claims ENABLE ROW LEVEL SECURITY;
 * ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
 * ALTER TABLE public.graph_nodes ENABLE ROW LEVEL SECURITY;
 *
 * CREATE POLICY "Allow read/write for authenticated users" ON public.claims
 *     FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');
 * CREATE POLICY "Allow read/write for authenticated users" ON public.audit_logs
 *     FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');
 * CREATE POLICY "Allow read/write for authenticated users" ON public.graph_nodes
 *     FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');
 * ```
 * ============================================================================
 */
