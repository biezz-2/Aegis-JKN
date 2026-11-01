import { INITIAL_CLAIMS, BPJS_REAL_CLAIMS, filterClaims, normalizeClaim } from "$lib/claims";
import type { Claim, RawClaim, HitlAction, LayoutMode, DetailTab, FilterOptions, AuditLogEntry, DatasetSource } from "$lib/types";
import { saveAuditLogToSupabase, syncClaimDecisionToSupabase } from "$lib/supabase";

export async function sha256(text: string): Promise<string> {
  if (typeof crypto !== "undefined" && crypto.subtle) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  // Fallback simple hash for non-crypto environments
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = (hash << 5) - hash + text.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash).toString(16).padStart(64, "0");
}

export function buildAuditPayload(params: {
  prevHash: string;
  timestamp: string;
  claimId: string;
  action: string;
  verifierId: string;
  note: string;
  fraudScore: number;
}): string {
  return `${params.prevHash}|${params.timestamp}|${params.claimId}|${params.action}|${params.verifierId}|${params.note}|${params.fraudScore}`;
}

export async function verifyAuditChain(logs: AuditLogEntry[]): Promise<{
  valid: boolean;
  brokenIndex?: number;
  reason?: string;
}> {
  if (!logs || logs.length === 0) {
    return { valid: true };
  }

  const GENESIS_PREV_HASH = "0000000000000000000000000000000000000000000000000000000000000000";

  for (let i = 0; i < logs.length; i++) {
    const entry = logs[i];

    // 1. Verifikasi kesinambungan rantai (prevHash -> currHash)
    if (i === 0) {
      if (entry.prevHash !== GENESIS_PREV_HASH) {
        return {
          valid: false,
          brokenIndex: 0,
          reason: `Genesis block prevHash tidak valid: diharapkan ${GENESIS_PREV_HASH}, ditemukan ${entry.prevHash}`,
        };
      }
    } else {
      const prevEntry = logs[i - 1];
      if (entry.prevHash !== prevEntry.hash) {
        return {
          valid: false,
          brokenIndex: i,
          reason: `Rantai hash terputus pada entri #${i} (${entry.id}): prevHash (${entry.prevHash}) tidak cocok dengan hash entri sebelumnya (${prevEntry.hash})`,
        };
      }
    }

    // 2. Verifikasi pencegahan manipulasi isi payload jika timestampIso tersedia
    if (entry.timestampIso && entry.claimId && entry.action && entry.verifierId && entry.note !== undefined && entry.aiScore !== undefined) {
      const expectedPayload = buildAuditPayload({
        prevHash: entry.prevHash,
        timestamp: entry.timestampIso,
        claimId: entry.claimId,
        action: entry.action,
        verifierId: entry.verifierId,
        note: entry.note,
        fraudScore: entry.aiScore,
      });
      const expectedHash = await sha256(expectedPayload);
      if (entry.hash !== expectedHash) {
        return {
          valid: false,
          brokenIndex: i,
          reason: `Manipulasi payload terdeteksi pada entri #${i} (${entry.id}): hash tercatat (${entry.hash}) tidak cocok dengan rekalkulasi SHA-256 payload (${expectedHash})`,
        };
      }
    }
  }

  return { valid: true };
}

export class DashboardStore {

  activeDatasetSource = $state<DatasetSource>("synthetic");
  private syntheticClaims: Claim[] = INITIAL_CLAIMS;
  private realBpjsClaims: Claim[] | null = null;
  isLoadingDataset = $state<boolean>(false);

  claims = $state<Claim[]>(INITIAL_CLAIMS);
  selectedClaimId = $state<string>("KLM001");
  layoutMode = $state<LayoutMode>("dual");
  leftPanelWidth = $state<number>(38); // percentage width for left queue
  activeDetailTab = $state<DetailTab>("emr");

  filters = $state<FilterOptions>({
    search: "",
    risk: "all",
    status: "all",
    modus: "all",
    syndicate: "all",
    serviceType: "all",
    contradictionOnly: false,
    sortBy: "score-desc",
  });

  auditLogs = $state<AuditLogEntry[]>([]);
  verifierId = $state<string>("VERIF-JKN-0891");

  get selectedClaim(): Claim | undefined {
    return this.claims.find((c) => c.id === this.selectedClaimId) || this.claims[0];
  }

  get filteredClaims(): Claim[] {
    return filterClaims(this.claims, this.filters);
  }

  get kpi() {
    return {
      total: this.claims.length,
      escalateCount: this.claims.filter((c) => c.status === "escalate" || c.risk === "fraud").length,
      highRiskCount: this.claims.filter((c) => c.risk === "high").length,
      reviewCount: this.claims.filter((c) => c.status === "review" && c.risk !== "fraud").length,
      autoClearCount: this.claims.filter((c) => c.status === "auto_clear").length,
      contradictionCount: this.claims.filter((c) => c.hasContradiction).length,
      totalCostRp: this.claims.reduce((acc, c) => acc + c.costRp, 0),
      preventedCostRp: this.claims
        .filter((c) => c.verifiedStatus === "ESCALATE_P2PK" || (c.status === "escalate" && !c.verifiedStatus))
        .reduce((acc, c) => acc + c.costRp, 0),
      approvedCostRp: this.claims
        .filter((c) => c.verifiedStatus === "APPROVE" || c.status === "auto_clear")
        .reduce((acc, c) => acc + c.costRp, 0),
    };
  }

  init() {
    if (typeof window !== "undefined") {
      // Load saved verified claims
      try {
        const savedDecisions = localStorage.getItem("aegis_decisions");
        if (savedDecisions) {
          const map = JSON.parse(savedDecisions) as Record<string, HitlAction>;
          this.applyDecisionsMap(map);
        }

        const savedLogs = localStorage.getItem("aegis_audit_logs");
        if (savedLogs) {
          this.auditLogs = JSON.parse(savedLogs);
        }
      } catch (e) {
        console.error("Gagal memuat state dari localStorage:", e);
      }
    }
  }

  private applyDecisionsMap(map: Record<string, HitlAction>) {
    this.claims = this.claims.map((c) => ({
      ...c,
      verifiedStatus: map[c.id] || c.verifiedStatus || null,
    }));
  }

  async switchDatasetSource(source: DatasetSource) {
    if (this.activeDatasetSource === source && this.claims.length > 0) {
      return;
    }

    this.isLoadingDataset = true;
    try {
      if (source === "synthetic") {
        this.activeDatasetSource = "synthetic";
        this.claims = this.syntheticClaims;
        if (this.claims.length > 0) {
          this.selectedClaimId = this.claims[0].id;
        }
      } else if (source === "bpjs-real") {
        if (!this.realBpjsClaims) {
          if (BPJS_REAL_CLAIMS.length > 0) {
            this.realBpjsClaims = BPJS_REAL_CLAIMS;
          } else {
            // Try fetching from local API endpoint if available
            try {
              const res = await fetch("/api/bpjs-sample");
              if (res.ok) {
                const json = await res.json();
                this.realBpjsClaims = (json as RawClaim[]).map(normalizeClaim);
              }
            } catch {
              // No-op
            }
          }
        }

        if (this.realBpjsClaims && this.realBpjsClaims.length > 0) {
          this.activeDatasetSource = "bpjs-real";
          this.claims = this.realBpjsClaims;
          this.selectedClaimId = this.claims[0].id;
        } else {
          console.warn("Dataset BPJS Real belum tersedia / kosong, tetap di sintetis");
        }
      }

      // Re-apply any stored decisions to newly active claims
      if (typeof window !== "undefined") {
        try {
          const savedDecisions = localStorage.getItem("aegis_decisions");
          if (savedDecisions) {
            const map = JSON.parse(savedDecisions) as Record<string, HitlAction>;
            this.applyDecisionsMap(map);
          }
        } catch (e) {
          console.error("Gagal apply decisions:", e);
        }
      }
    } finally {
      this.isLoadingDataset = false;
    }
  }

  selectClaim(id: string) {
    this.selectedClaimId = id;
  }

  setLayoutMode(mode: LayoutMode) {
    this.layoutMode = mode;
  }

  setDetailTab(tab: DetailTab) {
    this.activeDetailTab = tab;
  }

  setPanelWidth(width: number) {
    this.leftPanelWidth = Math.max(25, Math.min(60, width));
  }

  updateFilter<K extends keyof FilterOptions>(key: K, value: FilterOptions[K]) {
    this.filters[key] = value;
  }

  resetFilters() {
    this.filters = {
      search: "",
      risk: "all",
      status: "all",
      modus: "all",
      syndicate: "all",
      serviceType: "all",
      contradictionOnly: false,
      sortBy: "score-desc",
    };
  }

  async recordHitlDecision(action: HitlAction, note: string): Promise<AuditLogEntry | null> {
    const claim = this.selectedClaim;
    if (!claim) return null;

    const timestamp = new Date().toISOString();
    const prevHash = this.auditLogs.length > 0
      ? this.auditLogs[this.auditLogs.length - 1].hash
      : "0000000000000000000000000000000000000000000000000000000000000000";

    const payload = buildAuditPayload({
      prevHash,
      timestamp,
      claimId: claim.id,
      action,
      verifierId: this.verifierId,
      note,
      fraudScore: claim.fraudScore,
    });
    const hash = await sha256(payload);
    const signature = `ed25519_sig_${hash.slice(0, 16)}`;

    const entry: AuditLogEntry = {
      id: `AUD-${Date.now().toString(36).toUpperCase()}`,
      timestamp: new Date().toLocaleString("id-ID"),
      timestampIso: timestamp,
      claimId: claim.id,
      action,
      verifierId: this.verifierId,
      note,
      aiScore: claim.fraudScore,
      modus: claim.modus,
      syndicate: claim.syndicate,
      hash,
      prevHash,
      signature,
    };

    // Update claim locally
    this.claims = this.claims.map((c) =>
      c.id === claim.id ? { ...c, verifiedStatus: action } : c
    );

    // Update audit logs locally
    this.auditLogs = [...this.auditLogs, entry];

    // Save to localStorage
    if (typeof window !== "undefined") {
      try {
        const decisionsMap: Record<string, HitlAction> = {};
        for (const c of this.claims) {
          if (c.verifiedStatus) decisionsMap[c.id] = c.verifiedStatus;
        }
        localStorage.setItem("aegis_decisions", JSON.stringify(decisionsMap));
        localStorage.setItem("aegis_audit_logs", JSON.stringify(this.auditLogs));
      } catch (err) {
        console.error("Gagal menyimpan ke localStorage:", err);
      }
    }

    // Background sync to Supabase (fire and forget)
    saveAuditLogToSupabase(entry).catch((err) => console.warn("Supabase audit sync warning:", err));
    syncClaimDecisionToSupabase(claim.id, action, note).catch((err) => console.warn("Supabase claim sync warning:", err));

    return entry;
  }
  async verifyAuditTrail(): Promise<{ valid: boolean; brokenIndex?: number; reason?: string }> {
    return verifyAuditChain(this.auditLogs);
  }
}

export const dashboard = new DashboardStore();
