<script lang="ts">
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import { theme } from "$lib/stores/theme.svelte";
  import {
    syncState,
    onSyncStateChange,
    checkSupabaseConnection,
    flushSyncQueue,
    type SupabaseSyncStatus
  } from "$lib/supabase";
  import type { LayoutMode } from "$lib/types";
  import Icon from "./Icon.svelte";

  // Reactive sync state synchronized via onSyncStateChange
  let sync = $state<SupabaseSyncStatus>({ ...syncState });
  let isCheckingSync = $state(false);
  let showSyncDetails = $state(false);

  // Theme toggle micro-interaction state
  let isThemeToggling = $state(false);
  let themeToast = $state<string | null>(null);
  let themeToastTimer: ReturnType<typeof setTimeout> | null = null;

  $effect(() => {
    const unsubscribe = onSyncStateChange((newStatus: SupabaseSyncStatus) => {
      sync = newStatus;
    });
    return () => {
      unsubscribe();
    };
  });

  // Global keyboard shortcuts listener for Alt+1, Alt+2, Alt+3
  $effect(() => {
    function handleKeyDown(e: KeyboardEvent): void {
      if (e.altKey && !e.ctrlKey && !e.metaKey && !e.shiftKey) {
        if (e.key === "1") {
          e.preventDefault();
          dashboard.setLayoutMode("dual");
        } else if (e.key === "2") {
          e.preventDefault();
          dashboard.setLayoutMode("full-queue");
        } else if (e.key === "3") {
          e.preventDefault();
          dashboard.setLayoutMode("full-detail");
        }
      }
    }

    if (typeof window !== "undefined") {
      window.addEventListener("keydown", handleKeyDown);
      return () => {
        window.removeEventListener("keydown", handleKeyDown);
      };
    }
  });

  async function handleTriggerSync(): Promise<void> {
    if (isCheckingSync) return;
    isCheckingSync = true;
    try {
      await checkSupabaseConnection();
      await flushSyncQueue();
    } catch (err) {
      console.warn("Gagal sinkronisasi manual Supabase:", err);
    } finally {
      setTimeout(() => {
        isCheckingSync = false;
      }, 300);
    }
  }

  function handleThemeToggle(): void {
    isThemeToggling = true;
    theme.toggle();
    const label = theme.current === "dark" ? "Mode Gelap aktif" : "Mode Terang aktif";
    themeToast = label;

    if (themeToastTimer) clearTimeout(themeToastTimer);
    themeToastTimer = setTimeout(() => {
      themeToast = null;
    }, 1400);

    setTimeout(() => {
      isThemeToggling = false;
    }, 250);
  }

  function formatRupiah(val: number): string {
    if (val >= 1_000_000_000) {
      return `Rp ${(val / 1_000_000_000).toFixed(2)} M`;
    }
    if (val >= 1_000_000) {
      return `Rp ${(val / 1_000_000).toFixed(1)} Jt`;
    }
    return `Rp ${val.toLocaleString("id-ID")}`;
  }
</script>

<header class="sticky top-0 z-40 border-b border-border/80 bg-background/95 backdrop-blur-md px-3 sm:px-4 py-2 shadow-xs transition-colors duration-200">
  <div class="flex flex-wrap items-center justify-between gap-2.5 sm:gap-3">
    <!-- Brand & System Identity -->
    <!-- Brand & System Identity with Link to Landing Page -->
    <div class="flex items-center gap-2.5 sm:gap-3 group transition-opacity hover:opacity-90 cursor-pointer">
      <a href="/" data-testid="topbar-brand-home" class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary/85 text-primary-foreground shadow-xs shadow-primary/25 ring-1 ring-primary/30 transition-transform duration-200 group-hover:scale-105">
        <Icon name="ShieldAlert" size={19} />
      </a>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-sm font-extrabold tracking-tight text-foreground">Aegis-JKN</span>
          <span class="inline-flex items-center gap-1 rounded-md bg-primary/10 border border-primary/20 px-1.5 py-0.5 text-[10px] font-bold text-primary font-mono leading-none">
            <span class="h-1.5 w-1.5 rounded-full bg-primary animate-pulse"></span>
            CDSS v2.1
          </span>
        </div>
        <div class="text-[11px] text-muted-foreground font-medium hidden sm:flex items-center gap-1.5">
          <span>Workstation</span>
          <span class="text-muted-foreground/60">•</span>
          <a href="/" class="text-[10px] text-primary/80 hover:text-primary font-semibold hover:underline">Beranda</a>
          <span class="text-muted-foreground/60">•</span>
          <a href="/it" class="text-[10px] text-[#588157] dark:text-[#a3b18a] font-bold hover:underline">Dashboard IT</a>
        </div>
      </div>

    <!-- Layout Mode Toggles with Informative Tooltips -->
    <nav
      class="flex items-center rounded-xl border border-border/80 bg-muted/50 p-1 text-xs shadow-2xs"
      aria-label="Pengatur Tata Letak Workstation"
    >
      <!-- Mode: Dual Panel -->
      <div class="relative group">
        <button
          type="button"
          data-testid="layout-mode-dual"
          onclick={() => dashboard.setLayoutMode("dual")}
          class="inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 min-h-[32px] text-xs font-semibold transition-all duration-150 active:scale-[0.98] {dashboard.layoutMode === 'dual'
            ? 'bg-card text-foreground shadow-xs border border-border/60'
            : 'text-muted-foreground hover:text-foreground hover:bg-card/40'}"
          aria-label="Aktifkan Mode Dual Panel"
          aria-pressed={dashboard.layoutMode === "dual"}
        >
          <svg class="w-3.5 h-3.5 shrink-0 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect width="18" height="18" x="3" y="3" rx="2" />
            <path d="M12 3v18" />
          </svg>
          <span>Dual Panel</span>
        </button>

        <!-- Tooltip: Dual Panel -->
        <div
          role="tooltip"
          class="pointer-events-none absolute left-1/2 top-full z-50 mt-2 -translate-x-1/2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top w-68 rounded-2xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] p-3 text-foreground shadow-2xl"
        >
          <div class="absolute -top-1.5 left-1/2 -translate-x-1/2 h-2.5 w-2.5 rotate-45 border-l border-t border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127]"></div>
          <div class="flex items-center justify-between border-b border-slate-200/70 dark:border-[#a3b18a]/20 pb-1 mb-1.5">
            <span class="text-xs font-bold text-foreground flex items-center gap-1.5">
              <span class="h-2 w-2 rounded-full bg-primary"></span>
              Dual Panel (Default)
            </span>
            <kbd class="rounded bg-muted px-1.5 py-0.5 text-[10px] font-mono font-semibold text-muted-foreground border border-border/60">Alt+1</kbd>
          </div>
          <p class="text-[11px] leading-relaxed text-muted-foreground">
            Tampilan terbelah seimbang: Antrean klaim di panel kiri dan detail rekam medis serta rekomendasi AI di panel kanan.
          </p>
          <div class="mt-1.5 pt-1 border-t border-border/40 text-[10px] text-primary font-medium">
            ✓ Optimal untuk alur verifikasi berkas harian
          </div>
        </div>
      </div>

      <!-- Mode: Full Antrean -->
      <div class="relative group">
        <button
          type="button"
          data-testid="layout-mode-full-queue"
          onclick={() => dashboard.setLayoutMode("full-queue")}
          class="inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 min-h-[32px] text-xs font-semibold transition-all duration-150 active:scale-[0.98] {dashboard.layoutMode === 'full-queue'
            ? 'bg-card text-foreground shadow-xs border border-border/60'
            : 'text-muted-foreground hover:text-foreground hover:bg-card/40'}"
          aria-label="Aktifkan Mode Full Antrean"
          aria-pressed={dashboard.layoutMode === "full-queue"}
        >
          <svg class="w-3.5 h-3.5 shrink-0 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect width="18" height="18" x="3" y="3" rx="2" />
            <path d="M3 9h18" />
            <path d="M3 15h18" />
          </svg>
          <span>Full Antrean</span>
        </button>

        <!-- Tooltip: Full Antrean -->
        <div
          role="tooltip"
          class="pointer-events-none absolute left-1/2 top-full z-50 mt-2 -translate-x-1/2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top w-68 rounded-2xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] p-3 text-foreground shadow-2xl"
        >
          <div class="absolute -top-1.5 left-1/2 -translate-x-1/2 h-2.5 w-2.5 rotate-45 border-l border-t border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127]"></div>
          <div class="flex items-center justify-between border-b border-slate-200/70 dark:border-[#a3b18a]/20 pb-1 mb-1.5">
            <span class="text-xs font-bold text-foreground flex items-center gap-1.5">
              <span class="h-2 w-2 rounded-full bg-amber-500"></span>
              Full Antrean Klaim
            </span>
            <kbd class="rounded bg-muted px-1.5 py-0.5 text-[10px] font-mono font-semibold text-muted-foreground border border-border/60">Alt+2</kbd>
          </div>
          <p class="text-[11px] leading-relaxed text-muted-foreground">
            Maksimalkan ruang kerja tabel antrean untuk triase cepat, pemfilteran massal, dan sortir risiko anomali tinggi.
          </p>
          <div class="mt-1.5 pt-1 border-t border-border/40 text-[10px] text-amber-600 dark:text-amber-400 font-medium">
            ✓ Optimal untuk penyaringan volume besar klaim
          </div>
        </div>
      </div>

      <!-- Mode: Full Detail & AI -->
      <div class="relative group">
        <button
          type="button"
          data-testid="layout-mode-full-detail"
          onclick={() => dashboard.setLayoutMode("full-detail")}
          class="inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 min-h-[32px] text-xs font-semibold transition-all duration-150 active:scale-[0.98] {dashboard.layoutMode === 'full-detail'
            ? 'bg-card text-foreground shadow-xs border border-border/60'
            : 'text-muted-foreground hover:text-foreground hover:bg-card/40'}"
          aria-label="Aktifkan Mode Full Detail dan AI"
          aria-pressed={dashboard.layoutMode === "full-detail"}
        >
          <svg class="w-3.5 h-3.5 shrink-0 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect width="18" height="18" x="3" y="3" rx="2" />
            <path d="M8 3v18" />
            <path d="m13 12 2 2 4-4" />
          </svg>
          <span>Full Detail & AI</span>
        </button>

        <!-- Tooltip: Full Detail -->
        <div
          role="tooltip"
          class="pointer-events-none absolute left-1/2 top-full z-50 mt-2 -translate-x-1/2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top w-72 rounded-2xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] p-3 text-foreground shadow-2xl"
        >
          <div class="absolute -top-1.5 left-1/2 -translate-x-1/2 h-2.5 w-2.5 rotate-45 border-l border-t border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127]"></div>
          <div class="flex items-center justify-between border-b border-slate-200/70 dark:border-[#a3b18a]/20 pb-1 mb-1.5">
            <span class="text-xs font-bold text-foreground flex items-center gap-1.5">
              <span class="h-2 w-2 rounded-full bg-indigo-500"></span>
              Full Detail & AI Forensik
            </span>
            <kbd class="rounded bg-muted px-1.5 py-0.5 text-[10px] font-mono font-semibold text-muted-foreground border border-border/60">Alt+3</kbd>
          </div>
          <p class="text-[11px] leading-relaxed text-muted-foreground">
            Fokus mendalam ke rekam medis lengkap, graf relasi MHGSL/Graphiti, pembuktian kontribusi SHAP, dan dossier audit.
          </p>
          <div class="mt-1.5 pt-1 border-t border-border/40 text-[10px] text-indigo-600 dark:text-indigo-400 font-medium">
            ✓ Optimal untuk investigasi sindikat fraud kompleks
          </div>
        </div>
      </div>
    </nav>

    <!-- Glanceable KPI Quick Chips with Informative Tooltips -->
    <div class="hidden lg:flex items-center gap-1.5 text-xs">
      <!-- Total Klaim -->
      <div class="relative group">
        <div
          class="flex items-center gap-1.5 rounded-lg border border-border/80 bg-card hover:bg-muted/40 px-2.5 py-1 min-h-[32px] shadow-2xs transition-all duration-150 cursor-default"
          role="status"
          aria-label="Total {dashboard.kpi.total} berkas klaim"
        >
          <span class="text-[10px] font-bold uppercase tracking-wider text-muted-foreground font-sans">Total</span>
          <span class="font-bold font-mono text-foreground tabular-nums text-xs">{dashboard.kpi.total}</span>
        </div>

        <div
          role="tooltip"
          class="pointer-events-none absolute left-1/2 top-full z-50 mt-1.5 -translate-x-1/2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top whitespace-nowrap rounded-xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] px-3 py-1.5 text-[11px] text-foreground shadow-xl"
        >
          Total {dashboard.kpi.total} klaim dalam batch workstation aktif
        </div>
      </div>

      <!-- Escalate / Fraud Priority -->
      <div class="relative group">
        <div
          class="flex items-center gap-1.5 rounded-lg border border-rose-500/30 bg-rose-500/10 hover:bg-rose-500/15 px-2.5 py-1 min-h-[32px] text-rose-700 dark:text-rose-300 transition-all duration-150 cursor-default"
          role="status"
          aria-label="{dashboard.kpi.escalateCount} klaim potensi fraud"
        >
          <span class="relative flex h-2 w-2">
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-rose-400 opacity-70"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-rose-500"></span>
          </span>
          <span class="text-[10px] font-bold uppercase tracking-wider font-sans">Fraud</span>
          <span class="font-bold font-mono tabular-nums text-xs">{dashboard.kpi.escalateCount}</span>
        </div>

        <div
          role="tooltip"
          class="pointer-events-none absolute left-1/2 top-full z-50 mt-1.5 -translate-x-1/2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top whitespace-nowrap rounded-xl border border-rose-500/30 bg-white dark:bg-[#203127] px-3 py-1.5 text-[11px] text-foreground shadow-xl"
        >
          <span class="font-semibold text-rose-600 dark:text-rose-400">{dashboard.kpi.escalateCount} Fraud</span>: Prioritas eskalasi P2PK / investigasi intensif
        </div>
      </div>

      <!-- Review / Clarification Needed -->
      <div class="relative group">
        <div
          class="flex items-center gap-1.5 rounded-lg border border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/15 px-2.5 py-1 min-h-[32px] text-amber-800 dark:text-amber-300 transition-all duration-150 cursor-default"
          role="status"
          aria-label="{dashboard.kpi.reviewCount} klaim butuh klarifikasi"
        >
          <span class="h-1.5 w-1.5 rounded-full bg-amber-500"></span>
          <span class="text-[10px] font-bold uppercase tracking-wider font-sans">Review</span>
          <span class="font-bold font-mono tabular-nums text-xs">{dashboard.kpi.reviewCount}</span>
        </div>

        <div
          role="tooltip"
          class="pointer-events-none absolute left-1/2 top-full z-50 mt-1.5 -translate-x-1/2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top whitespace-nowrap rounded-xl border border-amber-500/30 bg-white dark:bg-[#203127] px-3 py-1.5 text-[11px] text-foreground shadow-xl"
        >
          <span class="font-semibold text-amber-600 dark:text-amber-400">{dashboard.kpi.reviewCount} Klaim</span>: Butuh telaah EMR & klarifikasi ke RS
        </div>
      </div>

      <!-- Auto-Clear / Valid -->
      <div class="relative group">
        <div
          class="flex items-center gap-1.5 rounded-lg border border-emerald-500/30 bg-emerald-500/10 hover:bg-emerald-500/15 px-2.5 py-1 min-h-[32px] text-emerald-800 dark:text-emerald-300 transition-all duration-150 cursor-default"
          role="status"
          aria-label="{dashboard.kpi.autoClearCount} klaim auto-clear"
        >
          <span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
          <span class="text-[10px] font-bold uppercase tracking-wider font-sans">Valid</span>
          <span class="font-bold font-mono tabular-nums text-xs">{dashboard.kpi.autoClearCount}</span>
        </div>

        <div
          role="tooltip"
          class="pointer-events-none absolute left-1/2 top-full z-50 mt-1.5 -translate-x-1/2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top whitespace-nowrap rounded-xl border border-emerald-500/30 bg-white dark:bg-[#203127] px-3 py-1.5 text-[11px] text-foreground shadow-xl"
        >
          <span class="font-semibold text-emerald-600 dark:text-emerald-400">{dashboard.kpi.autoClearCount} Klaim</span>: Bersih, memenuhi syarat persetujuan otomatis
        </div>
      </div>

      <!-- Prevented Cost / Terselamatkan -->
      <div class="relative group">
        <div
          class="flex items-center gap-1.5 rounded-lg border border-primary/30 bg-primary/10 hover:bg-primary/15 px-2.5 py-1 min-h-[32px] text-primary transition-all duration-150 ring-1 ring-primary/20 cursor-default"
          role="status"
          aria-label="Estimasi biaya dicegah {formatRupiah(dashboard.kpi.preventedCostRp)}"
        >
          <span class="text-[10px] font-bold uppercase tracking-wider font-sans text-muted-foreground">Dicegah</span>
          <span class="font-bold font-mono tabular-nums text-xs">{formatRupiah(dashboard.kpi.preventedCostRp)}</span>
        </div>

        <div
          role="tooltip"
          class="pointer-events-none absolute right-0 top-full z-50 mt-1.5 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top-right whitespace-nowrap rounded-xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] px-3 py-1.5 text-[11px] text-foreground shadow-xl"
        >
          <span class="font-semibold text-primary">Biaya Terselamatkan</span>: Total penghematan dana jaminan sosial JKN
        </div>
      </div>
    </div>

    <!-- Status & Profile Controls -->
    <div class="flex items-center gap-2">
      <!-- Supabase Connection Badge with Smooth Animations & Interactive Dropdown -->
      <div class="relative group">
        <button
          type="button"
          onclick={() => {
            showSyncDetails = !showSyncDetails;
            if (showSyncDetails) void handleTriggerSync();
          }}
          class="inline-flex items-center gap-1.5 rounded-lg border border-border/80 bg-card hover:bg-muted/50 px-2.5 py-1 min-h-[32px] text-[11px] text-muted-foreground shadow-2xs transition-all duration-200 active:scale-95"
          aria-label="Status Supabase: {sync.connected ? 'Terhubung' : 'Offline'}. Klik untuk cek koneksi."
        >
          <!-- Dot Indicator with Smooth State Animation -->
          {#if sync.isSyncing || isCheckingSync}
            <span class="inline-flex items-center justify-center text-primary animate-spin duration-1000">
              <Icon name="RotateCcw" size={12} />
            </span>
          {:else if sync.connected}
            <span class="relative flex h-2 w-2">
              <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60 duration-1000"></span>
              <span class="relative inline-flex h-2 w-2 rounded-full bg-emerald-500 transition-colors duration-300"></span>
            </span>
          {:else}
            <span class="relative flex h-2 w-2">
              <span class="relative inline-flex h-2 w-2 rounded-full bg-rose-500 transition-colors duration-300"></span>
            </span>
          {/if}

          <span class="hidden sm:inline font-medium">Supabase:</span>
          <span class="font-mono font-semibold transition-colors duration-200 {sync.connected ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}">
            {sync.isSyncing || isCheckingSync ? 'Syncing...' : sync.connected ? 'Terhubung' : 'Offline'}
          </span>

          <!-- Pending Queue Badge if Offline Queue Has Items -->
          {#if sync.pendingCount > 0}
            <span class="rounded-full bg-amber-500/20 border border-amber-500/30 px-1.5 py-0.2 text-[10px] font-bold text-amber-700 dark:text-amber-400 font-mono transition-transform duration-200 animate-pulse">
              {sync.pendingCount}
            </span>
          {/if}
        </button>

        <!-- Supabase Status Popover Card -->
        <div
          role="tooltip"
          class="pointer-events-none absolute right-0 top-full z-50 mt-2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top-right w-76 rounded-2xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] p-3.5 text-foreground shadow-2xl"
        >
          <div class="absolute -top-1.5 right-6 h-2.5 w-2.5 rotate-45 border-l border-t border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127]"></div>
          <div class="flex items-center justify-between border-b border-slate-200/70 dark:border-[#a3b18a]/20 pb-1.5 mb-2">
            <div class="flex items-center gap-1.5">
              <Icon name="Database" size={14} class="text-primary" />
              <span class="text-xs font-bold text-foreground">Status Supabase</span>
            </div>
            <span class="inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] font-bold font-mono {sync.connected ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300' : 'bg-rose-500/15 text-rose-700 dark:text-rose-300'}">
              {sync.connected ? 'Online' : 'Offline'}
            </span>
          </div>

          <div class="space-y-1.5 text-[11px]">
            <div class="flex items-center justify-between">
              <span class="text-muted-foreground">Endpoint:</span>
              <span class="font-mono text-foreground font-semibold truncate max-w-[160px]" title={sync.endpoint}>
                {sync.endpoint.replace(/^https?:\/\//, '')}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-muted-foreground">Terakhir Sinkron:</span>
              <span class="font-mono text-foreground font-semibold">
                {sync.lastSyncTime || 'Belum ada'}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-muted-foreground">Antrean Offline:</span>
              <span class="font-mono font-semibold {sync.pendingCount > 0 ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'}">
                {sync.pendingCount} berkas
              </span>
            </div>
            {#if sync.error}
              <div class="rounded bg-rose-500/10 border border-rose-500/20 p-1 text-[10px] text-rose-700 dark:text-rose-300 leading-tight">
                {sync.error}
              </div>
            {/if}
          </div>

          <div class="mt-2.5 pt-2 border-t border-border/50 flex items-center justify-between gap-2">
            <span class="text-[10px] text-muted-foreground">Klik tombol untuk sinkron manual</span>
            <span class="text-[10px] font-semibold text-primary">Cek & Sync ⟳</span>
          </div>
        </div>
      </div>

      <!-- Verifier ID Badge with Tooltip -->
      <div class="relative group hidden md:block">
        <div
          class="flex items-center gap-1.5 rounded-lg border border-border/80 bg-muted/40 hover:bg-muted/70 px-2.5 py-1 min-h-[32px] text-xs transition-colors duration-150 cursor-default"
          role="status"
          aria-label="Verifikator ID: {dashboard.verifierId}"
        >
          <span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
          <Icon name="User" size={13} class="text-muted-foreground" />
          <span class="font-mono font-semibold text-foreground">{dashboard.verifierId}</span>
        </div>

        <div
          role="tooltip"
          class="pointer-events-none absolute right-0 top-full z-50 mt-1.5 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top-right whitespace-nowrap rounded-xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] px-3 py-1.5 text-[11px] text-foreground shadow-xl"
        >
          Verifikator BPJS Kesehatan • Hak Akses: Verifikasi & Rekomendasi HITL
        </div>
      </div>

      <!-- Theme Toggle with Visual Feedback & Animation -->
      <div class="relative group">
        <button
          type="button"
          data-testid="topbar-theme-toggle"
          onclick={handleThemeToggle}
          class="relative inline-flex h-8.5 w-8.5 min-w-[34px] min-h-[34px] items-center justify-center rounded-lg border border-border/80 bg-card hover:bg-muted text-foreground transition-all duration-200 active:scale-95 shadow-2xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 {isThemeToggling ? 'ring-2 ring-primary/40' : ''}"
          aria-label="Ganti tema gelap atau terang"
          title="Toggle Tema Tampilan (Terang / Gelap)"
        >
          <div class="transition-transform duration-300 ease-out {isThemeToggling ? 'rotate-180 scale-90' : 'rotate-0 scale-100'}">
            {#if theme.current === "dark"}
              <Icon name="Sun" size={16} class="text-amber-400 drop-shadow-[0_0_6px_rgba(251,191,36,0.5)]" />
            {:else}
              <Icon name="Moon" size={16} class="text-emerald-700" />
            {/if}
          </div>
        </button>

        <!-- Transient Toast Feedback when Theme Toggled -->
        {#if themeToast}
          <div
            role="alert"
            class="pointer-events-none absolute right-0 top-full z-50 mt-2 whitespace-nowrap rounded-lg border border-primary/30 bg-primary/10 px-2.5 py-1 text-[11px] font-semibold text-primary shadow-lg backdrop-blur-md transition-all duration-200 animate-in fade-in zoom-in-95"
          >
            {themeToast}
          </div>
        {:else}
          <!-- Regular Hover Tooltip -->
          <div
            role="tooltip"
            class="pointer-events-none absolute right-0 top-full z-50 mt-1.5 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 ease-out origin-top-right whitespace-nowrap rounded-lg border border-border/80 bg-popover/95 px-2.5 py-1 text-[11px] text-popover-foreground shadow-md backdrop-blur-md"
          >
            {theme.current === "dark" ? "Beralih ke Mode Terang" : "Beralih ke Mode Gelap"}
          </div>
        {/if}
      </div>
    </div>
  </div>
  </div>
</header>

