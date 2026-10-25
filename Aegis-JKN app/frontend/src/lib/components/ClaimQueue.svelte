<script lang="ts">
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import type { Claim } from "$lib/types";
  import Icon from "./Icon.svelte";

  type DatasetSource = "synthetic" | "bpjs-real";

  interface DatasetCapableStore {
    activeDatasetSource?: DatasetSource;
    switchDatasetSource?: (source: DatasetSource) => Promise<void> | void;
  }

  function formatRupiah(val: number): string {
    return `Rp ${val.toLocaleString("id-ID")}`;
  }

  const syndicates = ["SYND-01", "SYND-02", "SYND-03", "SYND-04", "SYND-05"];

  const activeDatasetSource: DatasetSource = $derived(
    dashboard.activeDatasetSource ?? "synthetic"
  );

  const filterCounts = $derived({
    all: dashboard.claims.length,
    fraud: dashboard.claims.filter((c) => c.risk === "fraud").length,
    high: dashboard.claims.filter((c) => c.risk === "high").length,
    review: dashboard.claims.filter((c) => c.status === "review").length,
    auto_clear: dashboard.claims.filter((c) => c.status === "auto_clear").length,
    contradiction: dashboard.claims.filter((c) => c.hasContradiction).length,
  });

  function handleDatasetSwitch(source: DatasetSource) {
    const store = dashboard as unknown as DatasetCapableStore;
    if (typeof store.switchDatasetSource === "function") {
      store.switchDatasetSource(source);
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    const target = event.target as HTMLElement | null;
    if (
      target &&
      (target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.tagName === "SELECT" ||
        target.isContentEditable)
    ) {
      return;
    }

    if (event.key === "j" || event.key === "ArrowDown") {
      event.preventDefault();
      navigateQueue(1);
    } else if (event.key === "k" || event.key === "ArrowUp") {
      event.preventDefault();
      navigateQueue(-1);
    }
  }

  function navigateQueue(step: 1 | -1) {
    const list = dashboard.filteredClaims;
    if (!list || list.length === 0) return;

    const currentIndex = list.findIndex((c) => c.id === dashboard.selectedClaimId);
    let nextIndex = 0;

    if (currentIndex === -1) {
      nextIndex = step === 1 ? 0 : list.length - 1;
    } else {
      nextIndex = currentIndex + step;
      if (nextIndex < 0) nextIndex = 0;
      if (nextIndex >= list.length) nextIndex = list.length - 1;
    }

    const nextClaim = list[nextIndex];
    if (nextClaim) {
      dashboard.selectClaim(nextClaim.id);
      if (typeof document !== "undefined") {
        const el = document.getElementById(`claim-row-${nextClaim.id}`);
        if (el) {
          el.scrollIntoView({ block: "nearest", behavior: "smooth" });
        }
      }
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="flex h-full flex-col bg-card border-r border-slate-200/80 dark:border-[#a3b18a]/15 text-foreground overflow-hidden">
  <!-- Queue Header & Search -->
  <div class="p-3.5 border-b border-slate-200/80 dark:border-[#a3b18a]/15 space-y-2.5 bg-muted/20">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <Icon name="Activity" size={16} class="text-primary" />
        <h2 class="text-sm font-bold tracking-tight">Antrean Triase Klaim</h2>
      </div>
      <div class="flex items-center gap-2">
        <span class="hidden md:inline-flex items-center gap-0.5 text-[10px] text-muted-foreground font-mono" title="Navigasi cepat keyboard: j/k atau panah atas/bawah">
          <kbd class="px-1 py-0.2 rounded bg-muted border border-slate-200/60 dark:border-[#a3b18a]/20 text-[9px] shadow-2xs">j</kbd>/<kbd class="px-1 py-0.2 rounded bg-muted border border-slate-200/60 dark:border-[#a3b18a]/20 text-[9px] shadow-2xs">k</kbd>
        </span>
        <span class="rounded bg-primary/10 px-2 py-0.5 text-[11px] font-mono font-bold text-primary tabular-nums">
          {dashboard.filteredClaims.length} / {dashboard.claims.length}
        </span>
      </div>
    </div>

    <!-- Dataset Switcher Toggle -->
    <div
      class="grid grid-cols-2 p-0.5 rounded-lg bg-muted/60 border border-slate-200/60 dark:border-[#a3b18a]/20 text-[11px] font-medium"
      role="tablist"
      aria-label="Pilih Sumber Dataset"
    >
      <button
        type="button"
        role="tab"
        data-testid="dataset-switch-synthetic"
        aria-selected={activeDatasetSource === "synthetic"}
        onclick={() => handleDatasetSwitch("synthetic")}
        class="flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-md transition-all duration-150 min-h-[32px] {activeDatasetSource === 'synthetic' ? 'bg-background text-foreground shadow-2xs font-semibold' : 'text-muted-foreground hover:text-foreground'}"
      >
        <Icon name="Database" size={13} class={activeDatasetSource === 'synthetic' ? 'text-primary' : 'text-muted-foreground'} />
        <span class="truncate">Dataset Sintetis (300)</span>
      </button>

      <button
        type="button"
        role="tab"
        data-testid="dataset-switch-bpjs"
        aria-selected={activeDatasetSource === "bpjs-real"}
        onclick={() => handleDatasetSwitch("bpjs-real")}
        class="flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-md transition-all duration-150 min-h-[32px] {activeDatasetSource === 'bpjs-real' ? 'bg-background text-foreground shadow-2xs font-semibold' : 'text-muted-foreground hover:text-foreground'}"
      >
        <Icon name="FileText" size={13} class={activeDatasetSource === 'bpjs-real' ? 'text-primary' : 'text-muted-foreground'} />
        <span class="truncate">Data Riil BPJS FKRTL</span>
      </button>
    </div>

    <!-- Search Input -->
    <div class="relative">
      <Icon name="Search" size={14} class="absolute left-3 top-2.5 text-muted-foreground" />
      <input
        type="text"
        data-testid="claim-search-input"
        bind:value={dashboard.filters.search}
        placeholder="Cari KLM..., pasien, dokter, RS, ICD-10..."
        class="w-full rounded-lg border border-slate-200 dark:border-[#a3b18a]/20 bg-background pl-8 pr-3 py-1.5 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 shadow-2xs"
      />
      {#if dashboard.filters.search}
        <button
          type="button"
          onclick={() => (dashboard.filters.search = "")}
          class="absolute right-2.5 top-2 text-muted-foreground hover:text-foreground"
          aria-label="Bersihkan pencarian"
        >
          <Icon name="X" size={13} />
        </button>
      {/if}
    </div>

    <!-- Segmented Risk Filters -->
    <div class="flex flex-wrap gap-1 text-[11px]">
      <button
        type="button"
        onclick={() => { dashboard.updateFilter("risk", "all"); dashboard.updateFilter("status", "all"); }}
        class="inline-flex items-center gap-1 rounded-md px-2 py-1 font-semibold transition-all {dashboard.filters.risk === 'all' && dashboard.filters.status === 'all' ? 'bg-primary text-primary-foreground shadow-2xs' : 'bg-muted text-muted-foreground hover:text-foreground'}"
      >
        <span>Semua</span>
        <span class="ml-0.5 rounded-full px-1.5 py-0.2 text-[10px] font-mono tabular-nums {dashboard.filters.risk === 'all' && dashboard.filters.status === 'all' ? 'bg-white/20 text-white' : 'bg-background/80 text-muted-foreground'}">
          {filterCounts.all}
        </span>
      </button>

      <button
        type="button"
        onclick={() => { dashboard.updateFilter("risk", "fraud"); dashboard.updateFilter("status", "all"); }}
        class="inline-flex items-center gap-1 rounded-md px-2 py-1 font-semibold transition-all {dashboard.filters.risk === 'fraud' ? 'bg-rose-600 text-white shadow-2xs' : 'bg-rose-500/10 text-rose-800 dark:text-rose-300 hover:bg-rose-500/20'}"
      >
        <span>Fraud / Sindikat</span>
        <span class="ml-0.5 rounded-full px-1.5 py-0.2 text-[10px] font-mono tabular-nums {dashboard.filters.risk === 'fraud' ? 'bg-white/20 text-white' : 'bg-rose-500/20 text-rose-800 dark:text-rose-300'}">
          {filterCounts.fraud}
        </span>
      </button>

      <button
        type="button"
        onclick={() => { dashboard.updateFilter("risk", "high"); dashboard.updateFilter("status", "all"); }}
        class="inline-flex items-center gap-1 rounded-md px-2 py-1 font-semibold transition-all {dashboard.filters.risk === 'high' ? 'bg-amber-600 text-white shadow-2xs' : 'bg-amber-500/10 text-amber-800 dark:text-amber-300 hover:bg-amber-500/20'}"
      >
        <span>High Risk</span>
        <span class="ml-0.5 rounded-full px-1.5 py-0.2 text-[10px] font-mono tabular-nums {dashboard.filters.risk === 'high' ? 'bg-white/20 text-white' : 'bg-amber-500/20 text-amber-800 dark:text-amber-300'}">
          {filterCounts.high}
        </span>
      </button>

      <button
        type="button"
        onclick={() => { dashboard.updateFilter("status", "review"); dashboard.updateFilter("risk", "all"); }}
        class="inline-flex items-center gap-1 rounded-md px-2 py-1 font-semibold transition-all {dashboard.filters.status === 'review' ? 'bg-yellow-600 text-white shadow-2xs' : 'bg-yellow-500/10 text-yellow-800 dark:text-yellow-300 hover:bg-yellow-500/20'}"
      >
        <span>Review</span>
        <span class="ml-0.5 rounded-full px-1.5 py-0.2 text-[10px] font-mono tabular-nums {dashboard.filters.status === 'review' ? 'bg-white/20 text-white' : 'bg-yellow-500/20 text-yellow-800 dark:text-yellow-300'}">
          {filterCounts.review}
        </span>
      </button>

      <button
        type="button"
        onclick={() => { dashboard.updateFilter("status", "auto_clear"); dashboard.updateFilter("risk", "all"); }}
        class="inline-flex items-center gap-1 rounded-md px-2 py-1 font-semibold transition-all {dashboard.filters.status === 'auto_clear' ? 'bg-emerald-600 text-white shadow-2xs' : 'bg-emerald-500/10 text-emerald-800 dark:text-emerald-300 hover:bg-emerald-500/20'}"
      >
        <span>Auto-Clear</span>
        <span class="ml-0.5 rounded-full px-1.5 py-0.2 text-[10px] font-mono tabular-nums {dashboard.filters.status === 'auto_clear' ? 'bg-white/20 text-white' : 'bg-emerald-500/20 text-emerald-800 dark:text-emerald-300'}">
          {filterCounts.auto_clear}
        </span>
      </button>
    </div>

    <!-- Secondary Filters (Contradiction & Syndicate & Sort) -->
    <div class="flex items-center justify-between gap-2 pt-1 text-[11px]">
      <button
        type="button"
        onclick={() => dashboard.updateFilter("contradictionOnly", !dashboard.filters.contradictionOnly)}
        class="inline-flex items-center gap-1 rounded-md px-2 py-1 border transition-colors {dashboard.filters.contradictionOnly ? 'border-rose-500 bg-rose-500/15 text-rose-800 dark:text-rose-300 font-bold' : 'border-slate-200 dark:border-[#a3b18a]/20 bg-background text-muted-foreground hover:text-foreground'}"
      >
        <Icon name="AlertTriangle" size={12} />
        <span>Kontradiksi Saja</span>
        <span class="ml-0.5 rounded-full px-1.5 py-0.2 text-[10px] font-mono tabular-nums {dashboard.filters.contradictionOnly ? 'bg-rose-500/25 text-rose-900 dark:text-rose-200' : 'bg-muted text-muted-foreground'}">
          {filterCounts.contradiction}
        </span>
      </button>

      <select
        bind:value={dashboard.filters.syndicate}
        class="rounded-md border border-slate-200 dark:border-[#a3b18a]/20 bg-background px-2 py-1 text-[11px] text-foreground focus:outline-none focus:ring-1 focus:ring-primary/40"
      >
        <option value="all">Semua Sindikat</option>
        {#each syndicates as s}
          <option value={s}>{s}</option>
        {/each}
      </select>

      <select
        bind:value={dashboard.filters.sortBy}
        class="rounded-md border border-slate-200 dark:border-[#a3b18a]/20 bg-background px-2 py-1 text-[11px] text-foreground focus:outline-none focus:ring-1 focus:ring-primary/40"
      >
        <option value="score-desc">Skor Tertinggi</option>
        <option value="score-asc">Skor Terendah</option>
        <option value="cost-desc">Biaya Terbesar</option>
        <option value="date-desc">Terbaru</option>
      </select>
    </div>
  </div>

  <!-- Claim Rows List -->
  <div class="flex-1 overflow-y-auto divide-y divide-slate-200/60 dark:divide-[#a3b18a]/15 scrollbar-thin">
    {#each dashboard.filteredClaims as claim (claim.id)}
      {@const isSelected = dashboard.selectedClaimId === claim.id}
      <button
        type="button"
        id={`claim-row-${claim.id}`}
        data-testid="claim-row-item"
        onclick={() => dashboard.selectClaim(claim.id)}
        class="w-full text-left p-3 transition-all duration-150 relative {isSelected ? 'bg-primary/10 border-l-4 border-l-primary shadow-xs' : 'hover:bg-muted/40'}"
      >
        <!-- Top Row: Claim ID, Status, Fraud Score -->
        <div class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-1.5">
            <span class="font-mono font-bold text-xs {isSelected ? 'text-primary' : 'text-foreground'}">
              {claim.id}
            </span>
            <span class="text-[10px] text-muted-foreground font-mono">
              {claim.date}
            </span>
          </div>

          <!-- Fraud Score Badge -->
          <div class="flex items-center gap-1">
            {#if claim.verifiedStatus}
              <span class="rounded px-1.5 py-0.2 text-[9px] font-bold font-mono uppercase {claim.verifiedStatus === 'APPROVE' ? 'bg-emerald-500/20 text-emerald-800 dark:text-emerald-300' : claim.verifiedStatus === 'CLARIFY_RS' ? 'bg-yellow-500/20 text-yellow-800 dark:text-yellow-300' : 'bg-rose-500/20 text-rose-800 dark:text-rose-300'}">
                {claim.verifiedStatus === 'APPROVE' ? 'Setuju' : claim.verifiedStatus === 'CLARIFY_RS' ? 'Klarifikasi' : 'Tolak'}
              </span>
            {/if}
            <span class="rounded-full px-2 py-0.5 font-mono font-extrabold text-[10px] {claim.fraudScore >= 0.8 ? 'bg-rose-500/15 text-rose-800 dark:text-rose-400' : claim.fraudScore >= 0.6 ? 'bg-amber-500/15 text-amber-800 dark:text-amber-400' : 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-400'}">
              {(claim.fraudScore * 100).toFixed(0)}%
            </span>
          </div>
        </div>

        <!-- Middle Row: Patient & Doctor -->
        <div class="mt-1 flex items-baseline justify-between text-[11px]">
          <span class="font-medium text-foreground truncate max-w-[180px]">
            {claim.patient}
          </span>
          <span class="text-[10px] font-semibold text-muted-foreground">
            {claim.hospital}
          </span>
        </div>

        <!-- Diagnosis & Procedure -->
        <div class="mt-0.5 text-[11px] text-muted-foreground truncate">
          <span class="text-foreground font-medium">{claim.diagnosisIcd10.split(" - ")[0]}</span>:
          <span>{claim.procedureIcd9 ? claim.procedureIcd9.split(" - ")[0] : "Rawat Medis"}</span>
        </div>

        <!-- Bottom Row: Badges & Cost -->
        <div class="mt-2 flex items-center justify-between gap-1 text-[10px]">
          <div class="flex items-center gap-1 flex-wrap">
            {#if claim.hasContradiction}
              <span class="rounded bg-rose-500/15 text-rose-800 dark:text-rose-400 font-bold px-1.5 py-0.2 flex items-center gap-0.5">
                <Icon name="AlertTriangle" size={10} />
                <span>Kontra</span>
              </span>
            {/if}
            {#if claim.syndicate}
              <span class="rounded bg-primary/15 text-primary font-bold px-1.5 py-0.2">
                {claim.syndicate}
              </span>
            {/if}
            <span class="rounded bg-muted px-1.5 py-0.2 font-mono text-muted-foreground uppercase text-[9px]">
              {claim.serviceType === "rawat inap" ? "Inap" : "Jalan"}
            </span>
          </div>

          <span class="font-mono font-bold text-xs text-foreground">
            {formatRupiah(claim.costRp)}
          </span>
        </div>
      </button>
    {/each}

    {#if dashboard.filteredClaims.length === 0}
      <div class="p-8 text-center text-xs text-muted-foreground">
        <Icon name="Search" size={24} class="mx-auto mb-2 opacity-40" />
        Tidak ada berkas klaim yang cocok dengan filter.
      </div>
    {/if}
  </div>
</div>
