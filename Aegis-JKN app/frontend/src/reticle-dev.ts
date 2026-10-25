import { registerStore, registerCapabilities } from "@reticlehq/browser";
import { writable } from "svelte/store";
import { dashboard } from "$lib/stores/dashboard.svelte";
import { theme } from "$lib/stores/theme.svelte";
export const TESTIDS = [
  "landing-theme-toggle",
  "landing-cta-app",
  "landing-cta-hero",
  "landing-cta-arch",
  "landing-3d-canvas",
  "landing-mode-shield",
  "landing-mode-graph",
  "landing-mode-pulse",
  "landing-faq-toggle-0",
  "landing-cta-banner",
  "topbar-brand-home",
  "topbar-theme-toggle",
  "layout-mode-dual",
  "layout-mode-full-queue",
  "layout-mode-full-detail",
  "claim-search-input",
  "dataset-switch-synthetic",
  "dataset-switch-bpjs",
  "claim-row-item",
  "detail-tab-emr",
  "detail-tab-ai",
  "detail-tab-flow",
  "detail-tab-graphiti",
  "audit-trail-modal-button",
  "ai-report-generate-button",
  "hitl-action-approve",
  "hitl-action-escalate",
  "hitl-action-clarify",
  "audit-view-ledger",
  "audit-view-dossier",
  "audit-print-dossier",
  "audit-export-json",
  "audit-export-csv"
];

export const Sig = {
  VERIFICATION_TRIGGERED: "claim:verification_triggered",
  CLAIM_APPROVED: "claim:approved",
  CLAIM_ESCALATED: "claim:escalated",
  THEME_TOGGLED: "theme:toggled",
  LAYOUT_CHANGED: "layout:changed"
} as const;

export interface AppState {
  theme: "dark" | "light";
  selectedClaimId: string;
  layoutMode: string;
  activeDetailTab: string;
  status: string;
  claimsCount: number;
  activeDataset: string;
}

function getCurrentState(): AppState {
  return {
    theme: (theme?.current as "dark" | "light") || "dark",
    selectedClaimId: dashboard?.selectedClaimId || "KLM001",
    layoutMode: dashboard?.layoutMode || "dual",
    activeDetailTab: dashboard?.activeDetailTab || "emr",
    status: "ready",
    claimsCount: dashboard?.claims?.length || 300,
    activeDataset: dashboard?.activeDatasetSource || "synthetic",
  };
}

let currentState: AppState = getCurrentState();

const internalStore = writable<AppState>(currentState);
internalStore.subscribe((val) => {
  currentState = val;
});

// Subscribable store satisfying Reticle's StoreLike interface (subscribe + getState)
export const appStore = {
  subscribe: internalStore.subscribe,
  set: internalStore.set,
  update: internalStore.update,
  getState: () => {
    return getCurrentState();
  }
};

if (typeof window !== "undefined") {
  setInterval(() => {
    const next = getCurrentState();
    if (
      next.selectedClaimId !== currentState.selectedClaimId ||
      next.layoutMode !== currentState.layoutMode ||
      next.activeDetailTab !== currentState.activeDetailTab ||
      next.theme !== currentState.theme ||
      next.activeDataset !== currentState.activeDataset
    ) {
      currentState = next;
      internalStore.set(next);
    }
  }, 500);
}

if (import.meta.env.DEV) {
  registerStore("app", appStore);

  registerCapabilities({
    testids: TESTIDS,
    signals: Object.values(Sig),
    stores: ["app"]
  });
}
