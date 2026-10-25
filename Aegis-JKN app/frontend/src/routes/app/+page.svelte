<script lang="ts">
  import { onMount } from "svelte";
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import Topbar from "$lib/components/Topbar.svelte";
  import ClaimQueue from "$lib/components/ClaimQueue.svelte";
  import EmrEvidencePanel from "$lib/components/EmrEvidencePanel.svelte";
  import MhgslAiPanel from "$lib/components/MhgslAiPanel.svelte";
  import RealtimePipelineFlow from "$lib/components/RealtimePipelineFlow.svelte";
  import GraphitiKnowledgeGraph from "$lib/components/GraphitiKnowledgeGraph.svelte";
  import HitlActionBar from "$lib/components/HitlActionBar.svelte";
  import AuditLogModal from "$lib/components/AuditLogModal.svelte";
  import Icon from "$lib/components/Icon.svelte";
  import type { DetailTab } from "$lib/types";

  let auditModalOpen = $state(false);
  let isDragging = $state(false);

  onMount(() => {
    dashboard.init();
  });

  function startResize(e: MouseEvent) {
    isDragging = true;
    const startX = e.clientX;
    const initialWidth = dashboard.leftPanelWidth;
    const totalWidth = window.innerWidth;

    function onMouseMove(moveEvent: MouseEvent) {
      const deltaX = moveEvent.clientX - startX;
      const deltaPercent = (deltaX / totalWidth) * 100;
      dashboard.setPanelWidth(initialWidth + deltaPercent);
    }

    function onMouseUp() {
      isDragging = false;
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    }

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
  }
</script>

<svelte:head>
  <title>Aegis-JKN · Meja Kerja Verifikator BPJS Kesehatan</title>
  <meta
    name="description"
    content="Clinical Decision Support System (CDSS) Verifikator Klaim JKN dengan MHGSL, Svelte Flow, dan Graphiti Knowledge Graph"
  />
</svelte:head>

<div class="h-screen w-screen flex flex-col bg-background text-foreground overflow-hidden select-text">
  <!-- Top Navigation Bar -->
  <Topbar />

  <!-- Main Workstation Layout -->
  <div class="flex-1 flex overflow-hidden relative">
    <!-- LEFT PANEL: Claim Triage Queue -->
    {#if dashboard.layoutMode === "dual" || dashboard.layoutMode === "full-queue"}
      <div
        class="h-full overflow-hidden flex flex-col"
        style="width: {dashboard.layoutMode === 'full-queue' ? '100%' : `${dashboard.leftPanelWidth}%`};"
      >
        <ClaimQueue />
      </div>
    {/if}

    <!-- RESIZABLE SPLIT DIVIDER (Only visible in dual mode) -->
    {#if dashboard.layoutMode === "dual"}
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
      <div
        role="separator"
        aria-orientation="vertical"
        aria-label="Pengubah ukuran panel"
        tabindex="-1"
        onmousedown={startResize}
        class="w-1 h-full cursor-col-resize hover:bg-[#588157]/40 active:bg-[#588157] transition-colors flex items-center justify-center bg-transparent shrink-0 z-20 {isDragging ? 'bg-[#588157]' : ''}"
        title="Geser untuk mengubah ukuran panel (Drag to resize)"
      >
        <div class="h-8 w-0.5 rounded-full bg-[#588157]/20"></div>
      </div>
    {/if}

    <!-- RIGHT PANEL: Detailed Evidence, AI Models, Svelte Flow & Graphiti -->
    {#if dashboard.layoutMode === "dual" || dashboard.layoutMode === "full-detail"}
      <div class="flex-1 h-full flex flex-col overflow-hidden bg-background">
        <!-- Tab Navigation Bar for Right Panel -->
        <div class="bg-card px-4 py-2 flex flex-wrap items-center justify-between gap-2 shrink-0 shadow-2xs">
          <div role="tablist" aria-label="Navigasi Panel Detail Klaim" class="flex items-center gap-1.5 overflow-x-auto">
            <button
              type="button"
              role="tab"
              data-testid="detail-tab-emr"
              aria-selected={dashboard.activeDetailTab === "emr"}
              onclick={() => dashboard.setDetailTab("emr")}
              class="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all min-h-[32px] {dashboard.activeDetailTab === 'emr' ? 'bg-primary text-primary-foreground shadow-2xs' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}"
              title="Tab 1: Bukti Rekam Medis (Tekan 1)"
            >
              <Icon name="FileText" size={14} />
              <span>Bukti Rekam Medis (EMR)</span>
              <kbd class="ml-1 rounded px-1.5 py-0.2 font-mono text-[10px] {dashboard.activeDetailTab === 'emr' ? 'bg-primary-foreground/20 text-primary-foreground' : 'bg-muted text-muted-foreground'}">1</kbd>
            </button>

            <button
              type="button"
              role="tab"
              data-testid="detail-tab-ai"
              aria-selected={dashboard.activeDetailTab === "ai"}
              onclick={() => dashboard.setDetailTab("ai")}
              class="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all min-h-[32px] {dashboard.activeDetailTab === 'ai' ? 'bg-primary text-primary-foreground shadow-2xs' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}"
              title="Tab 2: Pembuktian AI & SHAP (Tekan 2)"
            >
              <Icon name="Sparkles" size={14} />
              <span>Pembuktian AI & SHAP</span>
              <kbd class="ml-1 rounded px-1.5 py-0.2 font-mono text-[10px] {dashboard.activeDetailTab === 'ai' ? 'bg-primary-foreground/20 text-primary-foreground' : 'bg-muted text-muted-foreground'}">2</kbd>
            </button>

            <button
              type="button"
              role="tab"
              data-testid="detail-tab-flow"
              aria-selected={dashboard.activeDetailTab === "flow"}
              onclick={() => dashboard.setDetailTab("flow")}
              class="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all min-h-[32px] {dashboard.activeDetailTab === 'flow' ? 'bg-primary text-primary-foreground shadow-2xs' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}"
              title="Tab 3: Pipeline Realtime Svelte Flow (Tekan 3)"
            >
              <Icon name="GitBranch" size={14} />
              <span>Pipeline Realtime (Svelte Flow)</span>
              <kbd class="ml-1 rounded px-1.5 py-0.2 font-mono text-[10px] {dashboard.activeDetailTab === 'flow' ? 'bg-primary-foreground/20 text-primary-foreground' : 'bg-muted text-muted-foreground'}">3</kbd>
            </button>

            <button
              type="button"
              role="tab"
              data-testid="detail-tab-graphiti"
              aria-selected={dashboard.activeDetailTab === "graphiti"}
              onclick={() => dashboard.setDetailTab("graphiti")}
              class="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all min-h-[32px] {dashboard.activeDetailTab === 'graphiti' ? 'bg-primary text-primary-foreground shadow-2xs' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}"
              title="Tab 4: Knowledge Graph Graphiti (Tekan 4)"
            >
              <Icon name="Activity" size={14} />
              <span>Knowledge Graph (Graphiti)</span>
              <kbd class="ml-1 rounded px-1.5 py-0.2 font-mono text-[10px] {dashboard.activeDetailTab === 'graphiti' ? 'bg-primary-foreground/20 text-primary-foreground' : 'bg-muted text-muted-foreground'}">4</kbd>
            </button>
          </div>
          <!-- Open Audit Log Modal Button -->
          <button
            type="button"
            data-testid="audit-trail-modal-button"
            onclick={() => (auditModalOpen = true)}
            class="inline-flex items-center gap-1.5 rounded-xl bg-muted/60 hover:bg-muted px-3 py-1.5 text-xs font-semibold text-foreground transition-colors"
          >
            <Icon name="ClipboardList" size={13} class="text-primary" />
            <span>Audit Trail ({dashboard.auditLogs.length})</span>
          </button>
        </div>

        <!-- Detail Workspace Content (Active Tab) -->
        <div class="flex-1 overflow-hidden relative">
          {#if dashboard.activeDetailTab === "emr"}
            <EmrEvidencePanel />
          {:else if dashboard.activeDetailTab === "ai"}
            <MhgslAiPanel />
          {:else if dashboard.activeDetailTab === "flow"}
            <RealtimePipelineFlow />
          {:else if dashboard.activeDetailTab === "graphiti"}
            <GraphitiKnowledgeGraph />
          {/if}
        </div>

        <!-- Human-in-the-Loop Action Dock (Fixed at bottom of right panel) -->
        <HitlActionBar />
      </div>
    {/if}
  </div>
</div>

<!-- Modal: Immutable Audit Trail -->
<AuditLogModal bind:open={auditModalOpen} />
